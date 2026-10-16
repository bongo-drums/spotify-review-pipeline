"""One paid model call, done safely: reserve -> call (bounded backoff) -> price -> commit -> log.

Used by the verify, group and memo stages (the enricher pilot has the same logic inline in
pilot.py). Every call is written to the run DB's `calls` table with the contract role name in
`stage`, so the grading export and the cost evidence see every attempt, failed ones included.
"""
from __future__ import annotations

import sys
import time
import uuid
from pathlib import Path

from . import config, pricing
from .budget import SpendLedger
from .enricher import estimate_prompt_tokens
from .state import RunState, utc_now

BACKOFF_S = (2.0, 4.0, 8.0)


def thinking_off(model: str) -> dict:
    """The request value that turns reasoning off for `model`.

    claude-haiku-5-5 accepts {"type": "disabled"}. claude-sonnet-5-5 rejects it (400) and wants
    {"type": "between_tools"}: the model does not think before responding; only short notes between
    tool calls would come back as thinking blocks, and this pipeline uses no tools.
    """
    return {"type": "between_tools"} if model.startswith("claude-sonnet-5") else {"type": "disabled"}


class RunCapExceeded(RuntimeError):
    """The per-run --max-usd would be exceeded by the next request."""


def make_client():
    import anthropic
    key, _ = config.api_key()
    if not key:
        raise RuntimeError("no API key: set PIPELINE_ANTHROPIC_API_KEY (see python -m pipeline.keycheck)")
    return anthropic.Anthropic(api_key=key, max_retries=2, timeout=180.0)


class Caller:
    """Shares one run DB, one ledger and one per-run cap across stages."""

    def __init__(self, state: RunState, ledger: SpendLedger, run_id: str, *, client=None, rates=None,
                 tier: str = "standard", max_usd: float | None = None, log=None):
        self.state, self.ledger, self.run_id = state, ledger, run_id
        self._client, self.tier = client, tier
        self.rates = rates if rates is not None else pricing.load_rates()
        self.max_usd = max_usd
        self._log = log or (lambda m: print(m, file=sys.stderr))

    @property
    def client(self):
        if self._client is None:
            self._client = make_client()
        return self._client

    def run_spent(self) -> float:
        return float(self.state.conn.execute(
            "SELECT COALESCE(SUM(cost_usd_estimate),0) FROM calls WHERE run_id=?", (self.run_id,)).fetchone()[0])

    def call(self, request: dict, *, stage: str, phase: str, review_ids: list[str], label_config: str | None = None,
             system_tokens: int | None = None, extra_call_fields: dict | None = None):
        """Send one Messages request. Returns (response, call_row, cost_usd).

        The call row is NOT yet written: the caller commits it together with the results it derives
        (one transaction), via RunState.commit_batch / record_call. Failed attempts ARE written here.
        """
        import anthropic
        model = request["model"]
        est_prompt = estimate_prompt_tokens(request, system_tokens)
        est_max = pricing.max_cost(model, self.tier, est_prompt, request["max_tokens"], self.rates)
        if self.max_usd is not None and self.run_spent() + est_max > self.max_usd + 1e-9:
            raise RunCapExceeded(f"next {stage} request could cost ${est_max:.4f}; run has spent "
                                 f"${self.run_spent():.4f} of --max-usd {self.max_usd:.2f}")
        call_id = uuid.uuid4().hex
        reservation = self.ledger.reserve(est_max, call_id=call_id)
        base = {"run_id": self.run_id, "stage": stage, "phase": phase, "model": model, "label_config": label_config,
                "request_review_ids": review_ids, "service_tier": self.tier, **(extra_call_fields or {})}
        last = None
        try:
            for attempt, delay in enumerate((*BACKOFF_S, None), start=1):
                t0, started = time.monotonic(), utc_now()
                try:
                    response = self.client.messages.create(**request)
                    break
                except (anthropic.RateLimitError, anthropic.APIConnectionError) as e:
                    last, retryable = e, True
                except anthropic.APIStatusError as e:
                    last, retryable = e, e.status_code >= 500
                self.state.record_call({**base, "call_id": f"{call_id}-fail{attempt}", "attempt": attempt,
                                        "status": "failed", "error": f"{type(last).__name__}: {str(last)[:300]}",
                                        "started_at": started, "ended_at": utc_now(),
                                        "duration_s": round(time.monotonic() - t0, 3)})
                if not retryable or delay is None:
                    raise last
                self._log(f"{stage}: {type(last).__name__} on attempt {attempt}; retrying in {delay:.0f}s")
                time.sleep(delay)
        except BaseException:
            self.ledger.release(reservation)
            raise
        duration = time.monotonic() - t0
        usage = response.usage
        cost = pricing.cost_of(usage, model, self.tier, self.rates)
        self.ledger.commit(reservation, cost, call_id)
        row = {**base, "call_id": call_id, "attempt": 1, "status": "success", "error": None,
               "input_tokens": getattr(usage, "input_tokens", 0) or 0,
               "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
               "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
               "output_tokens": getattr(usage, "output_tokens", 0) or 0,
               "started_at": started, "ended_at": utc_now(), "duration_s": round(duration, 3),
               "cost_usd_estimate": cost}
        return response, row, cost


def text_block_from_response(response) -> str | None:
    return next((b.text for b in getattr(response, "content", []) if getattr(b, "type", None) == "text"), None)


def stage_calls(state: RunState, run_id: str, stage: str) -> list[dict]:
    return [dict(r) for r in state.conn.execute(
        "SELECT * FROM calls WHERE run_id=? AND stage=? ORDER BY started_at", (run_id, stage))]


def stage_summary(state: RunState, run_id: str, stage: str) -> dict:
    rows = stage_calls(state, run_id, stage)
    ok = [r for r in rows if r["status"] in ("success", "invalid")]
    usage = {k: sum(r[k] or 0 for r in ok) for k in pricing.USAGE_UNITS}
    import json as _json
    texts = sum(len(_json.loads(r["request_review_ids"] or "[]")) for r in ok)
    return {"calls": len(ok), "failed_calls": len(rows) - len(ok), "usage": usage, "texts": texts,
            "cost_usd": round(sum(r["cost_usd_estimate"] or 0 for r in ok), 6),
            "wall_s_sum_of_calls": round(sum(r["duration_s"] or 0 for r in ok), 3),
            "models": sorted({r["model"] for r in ok})}


def artifact_path(run_dir, name: str) -> Path:
    return Path(run_dir) / "artifacts" / name
