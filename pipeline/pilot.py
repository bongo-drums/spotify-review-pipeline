"""Cold/warm classification pilot on a small review file (standard tier).

Usage:
    python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
        --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25

Phases:
  cold  classify every pending text in <= 50-review requests. The first request writes the
        system-prompt cache; later ones read it. Labels are committed to the run DB.
  warm  re-send the exact same requests immediately afterwards (cache reads only) to measure
        warm wall-clock and label stability. Nothing is committed; labels are only compared.

Every request reserves its worst-case cost in the shared ledger (the $20 cap) and the run
stops cleanly at --max-usd. Resumable: re-running with the same --out continues.
Add --dry-run to build the requests and print the worst-case cost without calling the API.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from . import config, pricing
from .budget import BudgetExceeded, SpendLedger
from .enricher import (MAX_ATTEMPTS, MAX_REVIEWS_PER_REQUEST, MODEL, PROMPT_SHA256, build_request,
                       estimate_prompt_tokens, label_config, parse_response)
from .hashing import file_sha256
from .ingest import ingest
from .state import RunState, utc_now

STAGE = "classify"
LABEL_FIELDS = ("topic", "subtopic", "intent", "severity", "sentiment", "needs_review")
BACKOFF_S = (2.0, 4.0, 8.0)   # bounded backoff after the SDK's own retries are exhausted


class RunCapExceeded(RuntimeError):
    """The per-run --max-usd would be exceeded by the next request."""


def _write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def check_manifest(manifest_path, input_path) -> dict:
    """Record the dataset manifest and, if it lists the input file's sha256, verify it.

    The course manifest's exact layout is not fixed here, so any dict carrying a `sha256`
    (or `sha256sum`) next to a name/path/file that matches the input's basename is used.
    """
    result = {"manifest_path": str(manifest_path) if manifest_path else None, "found_entry": False,
              "sha256_matches": None, "input_sha256": file_sha256(input_path)}
    if not manifest_path:
        return result
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        result["error"] = f"{type(e).__name__}: {e}"
        return result
    result["manifest_sha256"] = file_sha256(manifest_path)
    base = Path(input_path).name
    expected = None

    def walk(node, key=None):
        nonlocal expected
        if expected is not None:
            return
        if isinstance(node, dict):
            names = [str(node.get(k, "")) for k in ("name", "path", "file", "filename")] + [str(key or "")]
            sha = node.get("sha256") or node.get("sha256sum")
            if sha and any(Path(n).name == base for n in names if n):
                expected = str(sha).lower()
                return
            for k, v in node.items():
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                walk(v, key)
        elif isinstance(node, str) and key and Path(str(key)).name == base and len(node) == 64:
            expected = node.lower()

    walk(manifest)
    if expected is not None:
        result["found_entry"] = True
        result["manifest_sha256_for_input"] = expected
        result["sha256_matches"] = expected == result["input_sha256"]
    return result


class Pilot:
    def __init__(self, out_dir, *, model=MODEL, tier="standard", batch_size=MAX_REVIEWS_PER_REQUEST,
                 max_usd=0.25, ledger_path=None, client=None, limit=None, rates=None, dry_run=False):
        if not 1 <= batch_size <= MAX_REVIEWS_PER_REQUEST:
            raise ValueError(f"batch size must be 1..{MAX_REVIEWS_PER_REQUEST}")
        self.out_dir = Path(out_dir)
        self.run_id = self.out_dir.name
        self.model, self.tier, self.batch_size = model, tier, batch_size
        self.max_usd, self.limit, self.dry_run = float(max_usd), limit, dry_run
        self.rates = rates if rates is not None else pricing.load_rates()
        self.cfg = label_config(model)
        self.state = RunState(self.out_dir / "state.sqlite")
        self.ledger = SpendLedger(ledger_path, run_id=self.run_id)
        self._client = client
        self.system_tokens: int | None = None
        self.run_spent = float(self.state.conn.execute(
            "SELECT COALESCE(SUM(cost_usd_estimate),0) FROM calls WHERE run_id=?", (self.run_id,)).fetchone()[0])
        self.warm_labels: dict[str, dict] = {}
        self.events: list[str] = []

    # ---- infrastructure ------------------------------------------------

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(max_retries=2, timeout=120.0)
        return self._client

    def close(self):
        self.state.close()
        self.ledger.close()

    def log(self, msg: str) -> None:
        self.events.append(f"{utc_now()} {msg}")
        print(msg, file=sys.stderr)

    def measure_system_prompt(self) -> int | None:
        """Exact system-prompt size via the free count_tokens endpoint (None if unavailable)."""
        req = build_request(["x"], self.model)
        try:
            n = self.client.messages.count_tokens(model=self.model, system=req["system"], messages=req["messages"])
            self.system_tokens = int(n.input_tokens)
        except Exception as e:  # noqa: BLE001 - diagnostics only; the pilot does not depend on it
            self.log(f"count_tokens unavailable ({type(e).__name__}); using a character estimate")
        return self.system_tokens

    def _check_run_cap(self, est_max: float) -> None:
        if self.run_spent + est_max > self.max_usd + 1e-9:
            raise RunCapExceeded(
                f"next request could cost ${est_max:.4f}; run has spent ${self.run_spent:.4f} of --max-usd {self.max_usd:.2f}")

    def _call_with_backoff(self, request: dict, call_id: str, phase: str, ids: list[str]):
        import anthropic
        last = None
        for attempt, delay in enumerate((*BACKOFF_S, None), start=1):
            t0 = time.monotonic()
            started = utc_now()
            try:
                return self.client.messages.create(**request)
            except (anthropic.RateLimitError, anthropic.APIConnectionError) as e:
                last, retryable = e, True
            except anthropic.APIStatusError as e:
                last, retryable = e, e.status_code >= 500
            self.state.record_call({
                "call_id": f"{call_id}-fail{attempt}", "run_id": self.run_id, "stage": STAGE, "phase": phase,
                "model": self.model, "label_config": self.cfg, "request_review_ids": ids, "attempt": attempt,
                "status": "failed", "error": f"{type(last).__name__}: {str(last)[:300]}",
                "service_tier": self.tier, "started_at": started, "ended_at": utc_now(),
                "duration_s": round(time.monotonic() - t0, 3),
            })
            if not retryable or delay is None:
                raise last
            self.log(f"{type(last).__name__} on attempt {attempt}; retrying in {delay:.0f}s")
            time.sleep(delay)
        raise last  # pragma: no cover

    # ---- one request -----------------------------------------------------

    def _send(self, groups: list[dict], phase: str) -> dict:
        """Reserve, call, price, validate and (cold only) commit one request. Returns parsed info."""
        import uuid
        texts = [g["review_text"] for g in groups]
        ids = [g["cache_source_id"] for g in groups]
        request = build_request(texts, self.model)
        est_prompt = estimate_prompt_tokens(request, self.system_tokens)
        est_max = pricing.max_cost(self.model, self.tier, est_prompt, request["max_tokens"], self.rates)
        call_id = uuid.uuid4().hex
        if self.dry_run:
            return {"call_id": call_id, "n": len(texts), "est_prompt_tokens": est_prompt,
                    "max_tokens": request["max_tokens"], "est_max_usd": est_max}
        self._check_run_cap(est_max)
        reservation = self.ledger.reserve(est_max, call_id=call_id)
        t0, started = time.monotonic(), utc_now()
        try:
            response = self._call_with_backoff(request, call_id, phase, ids)
        except BaseException:
            self.ledger.release(reservation)
            raise
        duration = time.monotonic() - t0
        usage = response.usage
        cost = pricing.cost_of(usage, self.model, self.tier, self.rates)
        self.ledger.commit(reservation, cost, call_id)
        self.run_spent += cost
        parsed = parse_response(response, texts)
        call_row = {
            "call_id": call_id, "run_id": self.run_id, "stage": STAGE, "phase": phase, "model": self.model,
            "label_config": self.cfg, "request_review_ids": ids, "attempt": 1,
            "status": "invalid" if (parsed.invalid and not parsed.labels) else "success",
            "error": parsed.error or (f"{len(parsed.invalid)} invalid records" if parsed.invalid else None),
            "input_tokens": getattr(usage, "input_tokens", 0) or 0,
            "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
            "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
            "output_tokens": getattr(usage, "output_tokens", 0) or 0,
            "service_tier": self.tier, "started_at": started, "ended_at": utc_now(),
            "duration_s": round(duration, 3), "cost_usd_estimate": cost,
        }
        if phase == "cold":
            heads = [g["review_ids"][0] for g in groups]
            attempts = {r[0]: r[1] for r in self.state.conn.execute(
                f"SELECT review_id, attempts FROM records WHERE review_id IN ({','.join('?' * len(heads))})", heads)}
            results, retries, quarantines = [], [], []
            for k, g in enumerate(groups):
                if k in parsed.labels:
                    results.append({"review_ids": g["review_ids"], "label": parsed.labels[k], "label_config": self.cfg})
                    continue
                reason = parsed.invalid[k]
                done = attempts.get(g["review_ids"][0], 0) + 1
                if reason.startswith("refusal") or done >= MAX_ATTEMPTS:
                    quarantines.append({"review_ids": g["review_ids"], "reason": f"{reason} (attempt {done})"})
                else:
                    retries.append({"review_ids": g["review_ids"], "reason": reason})
            counts = self.state.commit_batch(results, quarantines, call_row, retries)
        else:
            self.state.record_call(call_row)
            counts = {"completed": 0, "quarantined": 0, "retried": 0}
            for k, lab in parsed.labels.items():
                self.warm_labels[groups[k]["cache_source_id"]] = lab
        self.log(f"{phase}: {len(texts)} texts, {duration:.1f}s, in={call_row['input_tokens']} "
                 f"cache_w={call_row['cache_creation_input_tokens']} cache_r={call_row['cache_read_input_tokens']} "
                 f"out={call_row['output_tokens']} ${cost:.5f} | ok={len(parsed.labels)} invalid={len(parsed.invalid)} "
                 f"stop={parsed.stop_reason}")
        return {"call_id": call_id, "cost": cost, "duration": duration, "parsed": parsed, "counts": counts}

    # ---- phases ------------------------------------------------------------

    def run_cold(self) -> dict:
        t0, calls, sent, dry = time.monotonic(), 0, 0, []
        while True:
            want = self.batch_size if self.limit is None else min(self.batch_size, self.limit - sent)
            if want <= 0:
                break
            groups = self.state.pending_text_groups(want)
            if not groups:
                break
            info = self._send(groups, "cold")
            calls += 1
            sent += len(groups)
            if self.dry_run:
                dry.append(info)
                # park the groups so the loop advances; run_pilot() restores them to pending at the end
                self.state.commit_batch([], quarantines=[{"review_ids": g["review_ids"], "reason": "dry_run"} for g in groups])
        return {"calls": calls, "texts_sent": sent, "wall_s": round(time.monotonic() - t0, 3), "dry_run": dry}

    def run_warm(self) -> dict:
        """Replay every successful cold request verbatim; compare labels; commit nothing."""
        t0, calls, sent = time.monotonic(), 0, 0
        rows = self.state.conn.execute(
            "SELECT request_review_ids FROM calls WHERE run_id=? AND phase='cold' AND status IN ('success','invalid') "
            "ORDER BY started_at", (self.run_id,)).fetchall()
        for (ids_json,) in rows:
            ids = json.loads(ids_json)
            groups = []
            for rid in ids:
                text = self.state.conn.execute("SELECT review_text FROM source WHERE review_id=?", (rid,)).fetchone()[0]
                groups.append({"cache_source_id": rid, "review_text": text, "review_ids": [rid]})
            self._send(groups, "warm")
            calls += 1
            sent += len(groups)
        return {"calls": calls, "texts_sent": sent, "wall_s": round(time.monotonic() - t0, 3)}

    # ---- reporting ---------------------------------------------------------

    def _phase_stats(self, phase: str) -> dict:
        rows = [dict(r) for r in self.state.conn.execute(
            "SELECT * FROM calls WHERE run_id=? AND phase=? ORDER BY started_at", (self.run_id, phase))]
        ok = [r for r in rows if r["status"] in ("success", "invalid")]
        durs = [r["duration_s"] for r in ok if r["duration_s"] is not None]
        usage = {k: sum(r[k] or 0 for r in ok) for k in
                 ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")}
        texts = sum(len(json.loads(r["request_review_ids"] or "[]")) for r in ok)
        stats = {
            "calls": len(ok), "failed_calls": len(rows) - len(ok), "texts": texts,
            "wall_s_sum_of_calls": round(sum(durs), 3),
            "call_duration_s": {"mean": round(statistics.mean(durs), 3), "p50": round(statistics.median(durs), 3),
                                "max": round(max(durs), 3)} if durs else None,
            "usage": usage, "cost_usd": round(sum(r["cost_usd_estimate"] or 0 for r in ok), 6),
            "calls_detail": [{k: r[k] for k in ("call_id", "status", "error", "input_tokens",
                                                "cache_creation_input_tokens", "cache_read_input_tokens",
                                                "output_tokens", "duration_s", "cost_usd_estimate")} for r in rows],
        }
        if texts:
            stats["per_text"] = {
                "input_tokens": round(usage["input_tokens"] / texts, 2),
                "cache_read_tokens": round(usage["cache_read_input_tokens"] / texts, 2),
                "cache_write_tokens": round(usage["cache_creation_input_tokens"] / texts, 2),
                "output_tokens": round(usage["output_tokens"] / texts, 2),
                "cost_usd": round(stats["cost_usd"] / texts, 7),
                "seconds": round(sum(durs) / texts, 4) if durs else None,
            }
        return stats

    def _label_stats(self) -> dict:
        rows = self.state.conn.execute(
            "SELECT review_id, cache_source_id, label, reason, status FROM records").fetchall()
        dist = {f: Counter() for f in LABEL_FIELDS}
        n_labeled = 0
        for r in rows:
            if r["label"]:
                n_labeled += 1
                lab = json.loads(r["label"])
                for f in LABEL_FIELDS:
                    dist[f][str(lab.get(f))] += 1
        agreement = None
        if self.warm_labels:
            same_field = Counter()
            compared, identical = 0, 0
            for r in rows:
                if r["review_id"] in self.warm_labels and r["label"]:
                    cold, warm = json.loads(r["label"]), self.warm_labels[r["review_id"]]
                    compared += 1
                    identical += all(cold[f] == warm[f] for f in LABEL_FIELDS)
                    for f in LABEL_FIELDS:
                        same_field[f] += cold[f] == warm[f]
            agreement = {"texts_compared": compared,
                         "identical_on_all_fields": round(identical / compared, 4) if compared else None,
                         "by_field": {f: round(same_field[f] / compared, 4) for f in LABEL_FIELDS} if compared else {}}
        return {
            "labeled_rows": n_labeled,
            "distribution": {f: dict(sorted(c.items())) for f, c in dist.items()},
            "quarantine_reasons": dict(Counter(r["reason"] for r in rows if r["status"] == "quarantined")),
            "cold_warm_agreement": agreement,
        }

    def export_labels_csv(self, path: Path) -> int:
        cols = ["review_id", "cache_source_id", "status", "topic", "subtopic", "intent", "severity", "sentiment",
                "needs_review", "entities", "evidence_sentence", "evidence", "reason", "attempts"]
        n = 0
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for r in self.state.conn.execute(
                    "SELECT review_id, cache_source_id, status, label, reason, attempts FROM records ORDER BY row_index"):
                lab = json.loads(r["label"]) if r["label"] else {}
                w.writerow([r["review_id"], r["cache_source_id"], r["status"], lab.get("topic"), lab.get("subtopic"),
                            lab.get("intent"), lab.get("severity"), lab.get("sentiment"), lab.get("needs_review"),
                            json.dumps(lab.get("entities", []), ensure_ascii=False) if lab else "",
                            lab.get("evidence_sentence"), lab.get("evidence"), r["reason"], r["attempts"]])
                n += 1
        return n


def run_pilot(input_path, out_dir, manifest_path=None, *, max_usd=0.25, model=MODEL, tier="standard",
              batch_size=MAX_REVIEWS_PER_REQUEST, phases=("cold", "warm"), ledger_path=None, client=None,
              limit=None, rates=None, dry_run=False) -> dict:
    input_path, out_dir = Path(input_path), Path(out_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"input not found: {input_path}")
    out_dir.mkdir(parents=True, exist_ok=True)
    resumed = (out_dir / "state.sqlite").exists()
    if not resumed:
        ingest(input_path, out_dir)
    manifest_check = check_manifest(manifest_path, input_path)

    pilot = Pilot(out_dir, model=model, tier=tier, batch_size=batch_size, max_usd=max_usd,
                  ledger_path=ledger_path, client=client, limit=limit, rates=rates, dry_run=dry_run)
    report = {
        "run_id": pilot.run_id, "created_at": utc_now(), "status": "ok", "resumed": resumed, "dry_run": dry_run,
        "model": model, "tier": tier, "label_config": pilot.cfg, "prompt_sha256": PROMPT_SHA256,
        "batch_size": batch_size, "max_usd": max_usd, "phases_requested": list(phases),
        "input": {"path": str(input_path), "sha256": manifest_check["input_sha256"],
                  "rows": pilot.state.record_count(), **pilot.state.status_counts()},
        "manifest_check": manifest_check,
    }
    try:
        if resumed:
            released = pilot.ledger.release_orphans(pilot.run_id)
            if released:
                pilot.log(f"released {released} orphaned reservation(s) from a previous process")
        if not dry_run:
            pilot.measure_system_prompt()
        report["system_prompt_tokens"] = pilot.system_tokens
        heads = pilot.state.conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(LENGTH(s.review_text)),0) FROM records r JOIN source s USING(review_id) "
            "WHERE r.review_id = r.cache_source_id AND r.status != 'quarantined'").fetchone()
        report["input"]["distinct_texts"] = heads[0]
        report["input"]["distinct_text_chars"] = heads[1]
        report["input"]["avg_chars_per_distinct_text"] = round(heads[1] / heads[0], 2) if heads[0] else None
        if "cold" in phases:
            report["cold_loop"] = pilot.run_cold()
        if "warm" in phases and not dry_run:
            if pilot.state.conn.execute("SELECT 1 FROM calls WHERE run_id=? AND phase='warm' LIMIT 1",
                                        (pilot.run_id,)).fetchone():
                pilot.log("warm phase already recorded for this run; skipping")
            else:
                report["warm_loop"] = pilot.run_warm()
    except RunCapExceeded as e:
        report["status"], report["stopped_because"] = "stopped_run_cap", str(e)
        pilot.log(f"STOP: {e}")
    except BudgetExceeded as e:
        report["status"], report["stopped_because"] = "stopped_global_cap", str(e)
        pilot.log(f"STOP: {e}")
    finally:
        if dry_run:
            dry = report.get("cold_loop", {}).get("dry_run", [])
            report["dry_run_estimate"] = {
                "requests": len(dry), "texts": sum(d["n"] for d in dry),
                "worst_case_usd_one_pass": round(sum(d["est_max_usd"] for d in dry), 6),
                "worst_case_usd_cold_plus_warm": round(2 * sum(d["est_max_usd"] for d in dry), 6),
                "est_prompt_tokens_total": sum(d["est_prompt_tokens"] for d in dry),
            }
            report.pop("cold_loop", None)
            # restore the parked groups so a real run starts clean
            pilot.state.conn.execute(
                "UPDATE records SET status='pending', attempts=0, reason=NULL WHERE reason='dry_run'")
        else:
            report["phases"] = {p: pilot._phase_stats(p) for p in ("cold", "warm")}
            report["labels"] = pilot._label_stats()
            report["labels_csv_rows"] = pilot.export_labels_csv(out_dir / "labels.csv")
            report["checkpoint"] = pilot.state.export_checkpoint(out_dir / "checkpoint.json", run_id=pilot.run_id)
        report["run_spent_usd"] = round(pilot.run_spent, 6)
        report["ledger"] = pilot.ledger.summary()
        report["final_counts"] = pilot.state.status_counts()
        report["events"] = pilot.events
        report["finished_at"] = utc_now()
        _write_json(out_dir / "pilot_report.json", report)
        pilot.close()
    return report


def _summary(report: dict) -> dict:
    out = {"status": report["status"], "run_id": report["run_id"], "model": report["model"],
           "input_rows": report["input"]["rows"], "distinct_texts": report["input"].get("distinct_texts"),
           "final_counts": report.get("final_counts"), "run_spent_usd": report.get("run_spent_usd"),
           "ledger_remaining_usd": report.get("ledger", {}).get("remaining_usd"),
           "out": str(Path(report["input"]["path"]).parent)}
    if report.get("stopped_because"):
        out["stopped_because"] = report["stopped_because"]
    if report.get("dry_run"):
        out["dry_run_estimate"] = report.get("dry_run_estimate")
    for p in ("cold", "warm"):
        st = report.get("phases", {}).get(p)
        if st and st["calls"]:
            out[p] = {"calls": st["calls"], "wall_s": st["wall_s_sum_of_calls"], "usage": st["usage"],
                      "cost_usd": st["cost_usd"], "per_text": st.get("per_text")}
    if report.get("labels", {}).get("cold_warm_agreement"):
        out["cold_warm_agreement"] = report["labels"]["cold_warm_agreement"]
    return out


def main(argv=None) -> int:
    load_dotenv(config.REPO_ROOT / ".env")
    ap = argparse.ArgumentParser(description="Run the cold/warm classification pilot.")
    ap.add_argument("--input", required=True, help="small review CSV (e.g. cost_100.csv)")
    ap.add_argument("--manifest", help="dataset manifest.json (sha256 of the input is verified if listed)")
    ap.add_argument("--out", required=True, help="run directory (its name is the run_id)")
    ap.add_argument("--max-usd", type=float, default=0.25, help="hard cap for this run (default 0.25)")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--tier", default="standard", choices=("standard",), help="pilots run on the standard tier")
    ap.add_argument("--batch-size", type=int, default=MAX_REVIEWS_PER_REQUEST)
    ap.add_argument("--phases", default="cold,warm", help="comma list from: cold,warm")
    ap.add_argument("--limit", type=int, help="classify at most this many distinct texts")
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    ap.add_argument("--dry-run", action="store_true", help="build requests and price the worst case; no API calls")
    args = ap.parse_args(argv)
    phases = tuple(p.strip() for p in args.phases.split(",") if p.strip())
    bad = [p for p in phases if p not in ("cold", "warm")]
    if bad:
        print(f"pilot failed: unknown phase(s) {bad}", file=sys.stderr)
        return 1
    try:
        report = run_pilot(args.input, args.out, args.manifest, max_usd=args.max_usd, model=args.model,
                           tier=args.tier, batch_size=args.batch_size, phases=phases, ledger_path=args.ledger,
                           limit=args.limit, dry_run=args.dry_run)
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        print(f"pilot failed: {e}", file=sys.stderr)
        return 1
    print(json.dumps(_summary(report), indent=2))
    return 0 if report["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
