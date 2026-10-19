"""Capped stronger-model fallback: texts Haiku could not label validly twice go to Sonnet, once.

Only records quarantined for *invalid output* (`invalid_record:...`, `missing_from_output`,
`invalid_json`, `max_tokens`) are eligible; refusals and empty texts are not. The number of texts
routed is capped at `max_frac` of the run's distinct texts (declared in the cost calculator as the
maximum fallback fraction) and the stage stops at the run cap like every other. Calls are logged
with role `enrich`, model `claude-sonnet-5-5` and the Sonnet `label_config`, which the completed
records carry too, so the grading export stays consistent.
"""
from __future__ import annotations

import json
import math
import sys

from .enricher import FALLBACK_MODEL, MAX_REVIEWS_PER_REQUEST, build_request, label_config, parse_response
from .llm import Caller
from .state import RunState, utc_now

ELIGIBLE_PREFIXES = ("invalid_record", "missing_from_output", "invalid_json", "max_tokens", "no_text_block")
DEFAULT_MAX_FRAC = 0.005
BATCH = 10   # small requests: a fallback text is by definition awkward


def eligible_heads(state: RunState) -> list[dict]:
    rows = [dict(r) for r in state.conn.execute(
        "SELECT r.review_id, r.reason, s.review_text FROM records r JOIN source s USING(review_id) "
        "WHERE r.status='quarantined' AND r.review_id = r.cache_source_id ORDER BY r.row_index")]
    return [r for r in rows if (r["reason"] or "").startswith(ELIGIBLE_PREFIXES)]


def run_fallback(state: RunState, caller: Caller, *, model: str = FALLBACK_MODEL, max_frac: float = DEFAULT_MAX_FRAC,
                 phase: str = "initial", log=None) -> dict:
    log = log or (lambda m: print(m, file=sys.stderr))
    cfg = label_config(model)
    n_distinct = state.conn.execute(
        "SELECT COUNT(*) FROM records WHERE review_id = cache_source_id AND reason IS NOT 'empty_review_text' "
        "AND reason IS NOT 'malformed_row'").fetchone()[0]
    cap = max(1, math.floor(max_frac * n_distinct))
    heads = eligible_heads(state)
    todo, skipped = heads[:cap], heads[cap:]
    out = {"model": model, "label_config": cfg, "max_frac": max_frac, "cap_texts": cap, "eligible": len(heads),
           "routed": len(todo), "skipped_over_cap": len(skipped), "completed": 0, "still_quarantined": 0, "calls": 0,
           "cost_usd": 0.0}
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        head_ids = [h["review_id"] for h in chunk]
        groups = []
        for h in chunk:
            ids = [r[0] for r in state.conn.execute(
                "SELECT review_id FROM records WHERE cache_source_id=? AND status='quarantined' ORDER BY row_index",
                (h["review_id"],))]
            groups.append({"review_ids": ids or [h["review_id"]], "review_text": h["review_text"]})
        texts = [g["review_text"] for g in groups]
        response, call_row, cost = caller.call(build_request(texts, model), stage="enrich", phase=phase,
                                               review_ids=head_ids, label_config=cfg)
        parsed = parse_response(response, texts)
        now = utc_now()
        # the texts were quarantined; put them back to pending inside the same transaction as the outcome
        with state.transaction() as c:
            for g in groups:
                c.execute(f"UPDATE records SET status='pending', updated_at=? WHERE review_id IN ({','.join('?' * len(g['review_ids']))})",
                          [now, *g["review_ids"]])
        results, quarantines = [], []
        for k, g in enumerate(groups):
            if k in parsed.labels:
                results.append({"review_ids": g["review_ids"], "label": parsed.labels[k], "label_config": cfg})
            else:
                quarantines.append({"review_ids": g["review_ids"], "reason": f"fallback_{parsed.invalid[k]} ({model})"})
        call_row["error"] = parsed.error or (f"{len(parsed.invalid)} invalid records" if parsed.invalid else None)
        call_row["status"] = "invalid" if (parsed.invalid and not parsed.labels) else "success"
        counts = state.commit_batch(results, quarantines, call_row)
        out["completed"] += counts["completed"]
        out["still_quarantined"] += counts["quarantined"]
        out["calls"] += 1
        out["cost_usd"] += cost
        log(f"fallback ({model}): {len(texts)} texts, {call_row['duration_s']}s, ${cost:.5f} | ok={len(parsed.labels)} "
            f"invalid={len(parsed.invalid)}")
    out["cost_usd"] = round(out["cost_usd"], 6)
    return out
