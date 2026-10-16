"""Stage 2 (Classify): the Haiku enricher.

Usage (paid; needs ANTHROPIC_API_KEY in the environment or a local .env):
    python -m pipeline.enrich --run runs/<run_id> [--max-usd 0.25] [--max-requests N] [--phase resume]

Design (see docs/PLAN.md):
- claude-haiku-5-5, thinking disabled, effort low, JSON-schema structured output.
- At most 50 distinct texts per request (contract cap). Exact-duplicate texts are sent
  once and the validated label is written to every review_id that shares the text.
- Compact output: single-letter keys, and the evidence quote is a sentence *index*
  that code expands to `text[start:end]`, so it is always an exact source substring.
- Every returned ID is validated. A review with invalid or missing output is retried
  once in a small request, then quarantined with the reason.
- Before each request the worst-case cost is reserved in the shared spend ledger;
  the actual cost (from the response's usage) is committed after it returns.
- Each request's outcome is committed to the run DB in one transaction, so Ctrl-C
  or a crash never loses or double-counts a batch, and a resume sends only pending texts.

The golden human labels (evals/golden/) are never read by this module.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from . import config, pricing
from .budget import BudgetExceeded, SpendLedger
from .hashing import canonical
from .sentences import sentence_spans
from .state import RunState, utc_now

MODEL = "claude-haiku-5-5"
PROMPT_VERSION = "enrich-v1"
SCHEMA_VERSION = "schema-v1"
EFFORT = "low"
THINKING = {"type": "disabled"}
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "enrich_v1.md"

MAX_BATCH = 50             # contract: at most 50 reviews per enrichment request
RETRY_BATCH = 5            # retried reviews go in small requests so one bad review can't sink 50
MAX_ATTEMPTS = 2           # first try + one retry, then quarantine
OUTPUT_TOKENS_PER_REVIEW = 90
OUTPUT_TOKENS_OVERHEAD = 200
TRANSPORT_RETRIES = 4      # bounded backoff for 429 / 5xx / connection errors
BACKOFF_BASE_S = 2.0
BACKOFF_MAX_S = 60.0
REQUEST_TIMEOUT_S = 120.0
RAW_TEXT_LOG_LIMIT = 20_000

TOPICS = ("access", "usability", "playback", "downloads", "catalog", "billing", "support", "other")
INTENTS = ("cancellation", "complaint", "request", "praise", "unclear")
SUBTOPICS = {
    "access": ("login_failure", "account_locked_hacked", "signup"),
    "usability": ("ads_interruptions", "ui_redesign", "controls_navigation", "queue_playlist_mgmt",
                  "notifications_widgets"),
    "playback": ("crash_wont_open", "stops_skips_glitches", "connectivity", "audio_quality",
                 "background_play", "battery_resource"),
    "downloads": ("offline_needs_internet", "downloads_disappear", "download_fails"),
    "catalog": ("missing_content", "search", "recommendations", "lyrics", "podcasts"),
    "billing": ("price", "premium_only_controls", "charges_refunds", "subscription_activation"),
    "support": ("no_response", "unhelpful_response", "positive_support"),
    "other": ("general_negative", "general_positive", "unrelated"),
}
ALL_SUBTOPICS = tuple(s for subs in SUBTOPICS.values() for s in subs)
MAX_ENTITIES = 3
MAX_ENTITY_CHARS = 60


# ---- prompt, schema and label_config --------------------------------------

def system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def output_schema() -> dict:
    item = {
        "type": "object",
        "properties": {
            "i": {"type": "integer"},
            "t": {"type": "string", "enum": list(TOPICS)},
            "n": {"type": "string", "enum": list(INTENTS)},
            "v": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
            "m": {"type": "number"},
            "q": {"type": "integer"},
            "u": {"type": "string", "enum": list(ALL_SUBTOPICS)},
            "e": {"type": "array", "items": {"type": "string"}},
            "f": {"type": "boolean"},
        },
        "required": ["i", "t", "n", "v", "m", "q", "u", "e", "f"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {"r": {"type": "array", "items": item}},
        "required": ["r"],
        "additionalProperties": False,
    }


def settings() -> dict:
    """Every setting that changes labels. Its digest is part of label_config."""
    return {"model": MODEL, "prompt_version": PROMPT_VERSION, "schema_version": SCHEMA_VERSION,
            "effort": EFFORT, "thinking": THINKING, "system_prompt": system_prompt(),
            "schema": output_schema(), "sentence_splitter": "sentences.py v1"}


def label_config() -> str:
    """model+prompt+schema version string required by the grading contract, plus a content digest
    so any edit to the prompt, schema or settings invalidates the result cache."""
    digest = hashlib.sha256(canonical(settings()).encode("utf-8")).hexdigest()[:12]
    return f"{MODEL}+{PROMPT_VERSION}+{SCHEMA_VERSION}+effort-{EFFORT}+thinking-off+{digest}"


def build_user_message(groups: list[dict]) -> str:
    """One JSON line per distinct text: {"i": n, "s": [sentences]} with n = 1..len(groups).
    JSON string escaping keeps review text from breaking out of its line."""
    lines = []
    for n, g in enumerate(groups, 1):
        text = g["review_text"]
        sents = [text[a:b] for a, b in sentence_spans(text)]
        lines.append(json.dumps({"i": n, "s": sents}, ensure_ascii=False))
    return "\n".join(lines)


def max_output_tokens(n_reviews: int) -> int:
    return OUTPUT_TOKENS_OVERHEAD + OUTPUT_TOKENS_PER_REVIEW * n_reviews


def request_params(groups: list[dict]) -> dict:
    if not 0 < len(groups) <= MAX_BATCH:
        raise ValueError(f"a request must carry 1..{MAX_BATCH} reviews, got {len(groups)}")
    return {
        "model": MODEL,
        "max_tokens": max_output_tokens(len(groups)),
        "system": [{"type": "text", "text": system_prompt(), "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": build_user_message(groups)}],
        "thinking": THINKING,
        "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": output_schema()}},
    }


def prompt_token_upper_bound(params: dict) -> int:
    """Conservative token bound for the budget reservation: UTF-8 bytes of everything sent.
    (Tokens never exceed bytes for this tokenizer's byte-level fallback; the real count is far lower.)"""
    return len(canonical({k: params[k] for k in ("system", "messages", "output_config")}).encode("utf-8"))


# ---- response validation ---------------------------------------------------

def _bad_item(item, n_groups: int, spans_by_pos: dict) -> str | None:
    if not isinstance(item, dict):
        return "item_not_object"
    if set(item) != {"i", "t", "n", "v", "m", "q", "u", "e", "f"}:
        return "item_keys"
    i = item["i"]
    if isinstance(i, bool) or not isinstance(i, int) or not 1 <= i <= n_groups:
        return "bad_id"
    if item["t"] not in TOPICS:
        return "bad_topic"
    if item["n"] not in INTENTS:
        return "bad_intent"
    v = item["v"]
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5:
        return "bad_severity"
    m = item["m"]
    if isinstance(m, bool) or not isinstance(m, (int, float)) or not -1.0 <= m <= 1.0:
        return "bad_sentiment"
    q = item["q"]
    if isinstance(q, bool) or not isinstance(q, int) or not 0 <= q < len(spans_by_pos[i]):
        return "bad_evidence_index"
    if item["u"] not in SUBTOPICS[item["t"]]:
        return "subtopic_not_in_topic"
    e = item["e"]
    if (not isinstance(e, list) or len(e) > MAX_ENTITIES
            or not all(isinstance(x, str) and 0 < len(x.strip()) <= MAX_ENTITY_CHARS for x in e)):
        return "bad_entities"
    if not isinstance(item["f"], bool):
        return "bad_needs_review"
    return None


def to_label(item: dict, text: str, spans: list[tuple[int, int]]) -> dict:
    a, b = spans[item["q"]]
    return {
        "topic": item["t"],
        "intent": item["n"],
        "severity": item["v"],
        "sentiment": round(float(item["m"]), 2),
        "subtopic": item["u"],
        "entities": [x.strip() for x in item["e"]],
        "evidence_quote": text[a:b],
        "evidence_sentence": item["q"],
        "needs_review": item["f"],
    }


@dataclass
class Parsed:
    labels: dict = field(default_factory=dict)    # position -> label
    problems: dict = field(default_factory=dict)  # position -> reason
    batch_error: str | None = None


def parse_response(text: str | None, groups: list[dict], stop_reason: str | None = None) -> Parsed:
    """Validate a response against the request: every position 1..N exactly once, every field legal."""
    out = Parsed()
    n = len(groups)
    if stop_reason == "refusal":
        out.batch_error = "refusal"
    elif stop_reason == "max_tokens":
        out.batch_error = "max_tokens"
    if out.batch_error is None:
        try:
            data = json.loads(text or "")
        except (json.JSONDecodeError, TypeError):
            out.batch_error = "invalid_json"
        else:
            if not isinstance(data, dict) or set(data) != {"r"} or not isinstance(data["r"], list):
                out.batch_error = "bad_envelope"
    if out.batch_error:
        out.problems = {pos: out.batch_error for pos in range(1, n + 1)}
        return out

    spans = {pos: sentence_spans(g["review_text"]) for pos, g in enumerate(groups, 1)}
    seen: dict[int, dict] = {}
    for item in data["r"]:
        reason = _bad_item(item, n, spans)
        i = item.get("i") if isinstance(item, dict) else None
        valid_pos = isinstance(i, int) and not isinstance(i, bool) and 1 <= i <= n
        if valid_pos and i in seen or valid_pos and i in out.problems:
            out.problems[i] = "duplicate_id"
            seen.pop(i, None)
            continue
        if reason:
            if valid_pos:
                out.problems[i] = reason
            continue  # an item with an unknown id cannot be attributed; its review shows up as missing
        seen[i] = item
    for pos in range(1, n + 1):
        if pos in seen:
            out.labels[pos] = to_label(seen[pos], groups[pos - 1]["review_text"], spans[pos])
        elif pos not in out.problems:
            out.problems[pos] = "missing_from_output"
    return out


# ---- the run loop ----------------------------------------------------------

class EnrichAborted(RuntimeError):
    """The run stopped without finishing (budget, auth/config error, or persistent outage)."""


def _usage_dict(usage) -> dict:
    keys = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
    d = {k: int(getattr(usage, k, 0) or 0) for k in keys}
    tier = getattr(usage, "service_tier", None)
    if tier:
        d["service_tier"] = tier
    return d


def _response_text(resp) -> str | None:
    parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    return "".join(parts) if parts else None


def make_client():
    """Anthropic client from ANTHROPIC_API_KEY only (env or a local, gitignored .env).
    SDK retries are off: this module does its own bounded, logged, budget-aware retries."""
    try:
        from dotenv import load_dotenv
        load_dotenv(config.REPO_ROOT / ".env")
    except ImportError:
        pass
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise EnrichAborted("ANTHROPIC_API_KEY is not set (put it in .env, never in code or logs)")
    import anthropic
    return anthropic.Anthropic(api_key=key, max_retries=0, timeout=REQUEST_TIMEOUT_S)


class Enricher:
    def __init__(self, state: RunState, ledger: SpendLedger, client, run_id: str, *,
                 phase: str = "initial", tier: str = "standard", max_batch: int = MAX_BATCH,
                 run_cap_usd: float | None = None, log_path=None, rates=None,
                 sleep=time.sleep, clock=time.monotonic):
        if phase not in ("initial", "resume"):
            raise ValueError("phase must be 'initial' or 'resume'")
        if not 0 < max_batch <= MAX_BATCH:
            raise ValueError(f"max_batch must be 1..{MAX_BATCH}")
        self.state, self.ledger, self.client = state, ledger, client
        self.run_id, self.phase, self.tier, self.max_batch = run_id, phase, tier, max_batch
        self.run_cap_usd = run_cap_usd
        self.rates = rates if rates is not None else pricing.load_rates()
        self.log_path = Path(log_path) if log_path else None
        self.sleep, self.clock = sleep, clock
        self.cfg = label_config()
        self.stats = {"requests": 0, "attempts": 0, "failed_attempts": 0, "completed": 0,
                      "cache_completed": 0, "quarantined": 0, "retried": 0, "cost_usd": 0.0,
                      "usage": dict.fromkeys(pricing.USAGE_UNITS, 0)}

    # -- logging --

    def _log(self, entry: dict) -> None:
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _call_row(self, *, call_id, request_id, groups, attempt, status, error, usage, started, ended,
                  duration, cost, stop_reason) -> dict:
        return {
            "call_id": call_id, "request_id": request_id, "run_id": self.run_id, "stage": "enrich",
            "phase": self.phase, "model": MODEL, "label_config": self.cfg,
            "request_review_ids": [g["cache_source_id"] for g in groups], "attempt": attempt,
            "status": status, "error": error,
            "input_tokens": usage.get("input_tokens") if usage else None,
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens") if usage else None,
            "cache_read_input_tokens": usage.get("cache_read_input_tokens") if usage else None,
            "output_tokens": usage.get("output_tokens") if usage else None,
            "service_tier": self.tier, "started_at": started, "ended_at": ended,
            "duration_s": duration, "cost_usd_estimate": cost, "stop_reason": stop_reason,
        }

    # -- budget --

    def _reserve(self, amount: float, call_id: str):
        if self.run_cap_usd is not None:
            spent, outstanding = self.ledger.run_totals(self.run_id)
            if spent + outstanding + amount > self.run_cap_usd + 1e-9:
                raise BudgetExceeded(
                    f"run {self.run_id}: reserve ${amount:.4f} would exceed the run cap ${self.run_cap_usd:.2f} "
                    f"(committed ${spent:.4f}, outstanding ${outstanding:.4f})")
        return self.ledger.reserve(amount, call_id=call_id)

    # -- one request, with bounded transport retries --

    def _send(self, groups: list[dict], attempt: int):
        """Send one request (retrying transport failures). Returns (response, call_meta).
        Raises EnrichAborted on budget refusal, non-retryable errors or a persistent outage."""
        import anthropic

        params = request_params(groups)
        worst = pricing.max_cost(MODEL, self.tier, prompt_token_upper_bound(params), params["max_tokens"],
                                 rates=self.rates)
        for transport_try in range(1, TRANSPORT_RETRIES + 1):
            call_id = uuid.uuid4().hex
            try:
                res = self._reserve(worst, call_id)
            except BudgetExceeded as e:
                raise EnrichAborted(f"budget: {e}") from e
            started, t0 = utc_now(), self.clock()
            self.stats["attempts"] += 1
            error, unknown_charge = None, False
            try:
                raw = self.client.messages.with_raw_response.create(**params)
                resp = raw.parse()
                request_id = raw.headers.get("request-id") or getattr(resp, "_request_id", None)
            except (anthropic.RateLimitError, anthropic.InternalServerError) as e:
                error, retryable = f"{type(e).__name__}: status {e.status_code}", True
                request_id = e.response.headers.get("request-id") if e.response is not None else None
            except anthropic.APIStatusError as e:  # 400/401/403/404/413...: not retryable, not billed
                error, retryable = f"{type(e).__name__}: status {e.status_code}: {e.message}"[:500], False
                request_id = e.response.headers.get("request-id") if e.response is not None else None
            except anthropic.APIConnectionError as e:  # includes timeouts: the outcome is unknown
                error, retryable, unknown_charge, request_id = f"{type(e).__name__}", True, True, None
            except BaseException as e:  # Ctrl-C (or a bug) mid-request: charge unknown, book the worst case
                self.ledger.commit(res, worst)
                ended = utc_now()
                row = self._call_row(call_id=call_id, request_id=None, groups=groups, attempt=attempt,
                                     status="failed", error=f"{type(e).__name__}_in_flight_unknown_charge",
                                     usage=None, started=started, ended=ended,
                                     duration=round(self.clock() - t0, 3), cost=worst, stop_reason=None)
                self.state.record_call(row)
                self._log({**row, "outcome": "failed", "unknown_charge_booked_usd": worst})
                raise
            else:
                return resp, {"call_id": call_id, "request_id": request_id, "reservation": res,
                              "started": started, "t0": t0, "attempt": attempt, "worst": worst}

            # failed attempt: book the cost truthfully, log it, maybe back off and retry
            duration = round(self.clock() - t0, 3)
            if unknown_charge:
                self.ledger.commit(res, worst)  # conservative until reconciled with the console
                cost = worst
                error += " (unknown charge: worst case booked)"
            else:
                self.ledger.release(res)
                cost = 0.0
            self.stats["failed_attempts"] += 1
            self.stats["cost_usd"] += cost
            row = self._call_row(call_id=call_id, request_id=request_id, groups=groups, attempt=attempt,
                                 status="failed", error=error, usage=None, started=started, ended=utc_now(),
                                 duration=duration, cost=cost, stop_reason=None)
            self.state.record_call(row)
            self._log({**row, "outcome": "failed", "transport_try": transport_try})
            if not retryable:
                raise EnrichAborted(f"non-retryable API error: {error}")
            if transport_try < TRANSPORT_RETRIES:
                delay = min(BACKOFF_BASE_S * 2 ** (transport_try - 1), BACKOFF_MAX_S)
                self.sleep(delay + random.uniform(0, delay / 2))
        raise EnrichAborted(f"API still failing after {TRANSPORT_RETRIES} tries; work stays pending for resume")

    def _process(self, groups: list[dict]) -> None:
        attempt = max(g["attempts"] for g in groups) + 1
        resp, meta = self._send(groups, attempt)
        usage = _usage_dict(resp.usage)
        cost = pricing.cost_of(usage, MODEL, self.tier, rates=self.rates)
        self.ledger.commit(meta["reservation"], cost, call_id=meta["call_id"])
        duration = round(self.clock() - meta["t0"], 3)
        text = _response_text(resp)
        parsed = parse_response(text, groups, resp.stop_reason)

        results, quarantines, retries = [], [], []
        for pos, g in enumerate(groups, 1):
            if pos in parsed.labels:
                results.append({"review_ids": g["review_ids"], "label": parsed.labels[pos],
                                "label_config": self.cfg})
            elif g["attempts"] + 1 >= MAX_ATTEMPTS:
                quarantines.append({"review_ids": g["review_ids"],
                                    "reason": f"invalid_output_after_retry:{parsed.problems[pos]}"})
            else:
                retries.append({"review_ids": g["review_ids"], "reason": f"retry:{parsed.problems[pos]}"})
        status = "invalid" if parsed.batch_error else "success"
        row = self._call_row(call_id=meta["call_id"], request_id=meta["request_id"], groups=groups,
                             attempt=attempt, status=status, error=parsed.batch_error, usage=usage,
                             started=meta["started"], ended=utc_now(), duration=duration, cost=cost,
                             stop_reason=resp.stop_reason)
        counts = self.state.commit_batch(results, quarantines, call_row=row, retries=retries)
        self._log({**row, "outcome": "failed" if parsed.batch_error else "succeeded", "usage_raw": usage,
                   "item_problems": {str(k): v for k, v in parsed.problems.items()},
                   "response_text": (text or "")[:RAW_TEXT_LOG_LIMIT]})
        self.stats["requests"] += 1
        self.stats["cost_usd"] += cost
        for k in pricing.USAGE_UNITS:
            self.stats["usage"][k] += usage.get(k, 0)
        for k in ("completed", "quarantined", "retried"):
            self.stats[k] += counts[k]

    def next_batch(self) -> list[dict]:
        """Retries first, in small requests; otherwise up to max_batch fresh texts in source order."""
        groups = self.state.pending_text_groups(self.max_batch)
        retry = [g for g in groups if g["attempts"] > 0]
        return retry[:RETRY_BATCH] if retry else groups

    def run(self, max_requests: int | None = None) -> dict:
        """Enrich until nothing is pending (or max_requests successful requests). Returns stats."""
        t0 = self.clock()
        self.stats["cache_completed"] += self.state.apply_cache_hits(self.cfg)
        stopped = None
        while True:
            if max_requests is not None and self.stats["requests"] >= max_requests:
                stopped = "max_requests"
                break
            batch = self.next_batch()
            if not batch:
                break
            self._process(batch)
            # the batch may have completed texts that other pending rows share (none within a run,
            # but a result cache imported for a warm run can); keep the cache step cheap and exact
            self.stats["cache_completed"] += self.state.apply_cache_hits(self.cfg)
        self.stats["stopped"] = stopped
        self.stats["wall_s"] = round(self.clock() - t0, 3)
        self.stats["label_config"] = self.cfg
        self.stats["status_counts"] = self.state.status_counts()
        return self.stats


# ---- result-cache import (warm runs) ---------------------------------------

def import_label_cache(state: RunState, source_db, label_config_value: str) -> int:
    """Copy validated labels for one label_config from another run DB's result cache."""
    state.conn.execute("ATTACH DATABASE ? AS src", (str(source_db),))  # not allowed inside a transaction
    try:
        with state.transaction() as c:
            return c.execute(
                "INSERT OR IGNORE INTO label_cache(text_sha256,label_config,label,source_review_id,created_at) "
                "SELECT text_sha256,label_config,label,source_review_id,created_at FROM src.label_cache "
                "WHERE label_config=?", (label_config_value,)).rowcount
    finally:
        state.conn.execute("DETACH DATABASE src")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the Haiku enricher on a run DB's pending reviews (PAID).")
    ap.add_argument("--run", required=True, help="run directory containing state.sqlite (from pipeline.ingest)")
    ap.add_argument("--run-id", help="ledger/call-log run id (default: the run directory name)")
    ap.add_argument("--phase", choices=("initial", "resume"), default="initial")
    ap.add_argument("--max-usd", type=float, help="sub-cap for this run id, inside the global $20 ledger cap")
    ap.add_argument("--max-requests", type=int, help="stop after N successful requests (interruption demo)")
    ap.add_argument("--batch-size", type=int, default=MAX_BATCH)
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    args = ap.parse_args(argv)

    run_dir = Path(args.run)
    run_id = args.run_id or run_dir.name
    state = RunState(run_dir / "state.sqlite")
    ledger = SpendLedger(args.ledger, run_id=run_id)
    if args.phase == "resume":
        released = ledger.release_orphans(run_id)
        if released:
            print(f"released {released} orphaned reservation(s) from a crashed process", file=sys.stderr)
    try:
        enricher = Enricher(state, ledger, make_client(), run_id, phase=args.phase,
                            max_batch=args.batch_size, run_cap_usd=args.max_usd,
                            log_path=run_dir / "enrich_calls.jsonl")
        stats = enricher.run(max_requests=args.max_requests)
    except EnrichAborted as e:
        print(f"enrich stopped: {e}", file=sys.stderr)
        print(json.dumps(state.status_counts()), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        snap = state.export_checkpoint(run_dir / "checkpoint_interrupted.json", run_id=run_id)
        print(f"\ninterrupted; saved progress {snap['counts']} -> {run_dir / 'checkpoint_interrupted.json'}",
              file=sys.stderr)
        return 130
    finally:
        print(json.dumps({"ledger": ledger.summary()}), file=sys.stderr)
    state.export_checkpoint(run_dir / "checkpoint_latest.json", run_id=run_id)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
