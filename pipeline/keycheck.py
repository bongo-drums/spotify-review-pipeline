"""Pre-flight check before any paid run.

Usage:  python -m pipeline.keycheck [--no-smoke] [--ledger PATH]

Checks, in order, and prints one JSON report:
  1. credential  PIPELINE_ANTHROPIC_API_KEY (or ANTHROPIC_API_KEY) from the environment or .env.
                 The value is never printed; only its source, prefix and length.
  2. rates       cost/rates.csv loads and names the models the pipeline uses.
  3. ledger      the shared spend ledger opens; remaining budget under the cap.
  4. models      GET /v1/models/{id} for each priced model (free): the key works and the IDs exist.
  5. smoke       one enricher-shaped request with a single tiny review (thinking off, structured
                 output, cached system prompt): proves the exact request shape is accepted, and
                 records its real cost (well under a cent) in the ledger as run 'keycheck'.
Exit 0 only if every check passes.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

from dotenv import load_dotenv

from . import config, pricing
from .budget import SpendLedger
from .enricher import MODEL, build_request, estimate_prompt_tokens, label_config, parse_response

SMOKE_REVIEW = "Great app, it has all the songs I like."


def credential_status() -> dict:
    val, var = config.api_key()
    if val:
        return {"ok": True, "source": var, "prefix": val[:7] + "…", "length": len(val)}
    return {"ok": False, "source": None,
            "hint": "set PIPELINE_ANTHROPIC_API_KEY in the environment (or repo .env, which is git-ignored)"}


def check_models(client, models: list[str]) -> dict:
    import anthropic
    out = {"ok": True, "models": {}}
    for m in models:
        try:
            info = client.models.retrieve(m)
            out["models"][m] = {"ok": True, "display_name": getattr(info, "display_name", None),
                                "max_input_tokens": getattr(info, "max_input_tokens", None),
                                "max_tokens": getattr(info, "max_tokens", None)}
        except anthropic.AuthenticationError as e:
            out["models"][m] = {"ok": False, "error": f"AuthenticationError: {e.message}"}
            out["ok"] = False
            break
        except anthropic.APIStatusError as e:
            out["models"][m] = {"ok": False, "error": f"{type(e).__name__}: {e.message}"}
            out["ok"] = False
        except anthropic.APIConnectionError as e:
            out["models"][m] = {"ok": False, "error": f"APIConnectionError: {e}"}
            out["ok"] = False
            break
    return out


def smoke_test(client, ledger: SpendLedger, rates, model: str = MODEL) -> dict:
    import anthropic
    request = build_request([SMOKE_REVIEW], model)
    est_max = pricing.max_cost(model, "standard", estimate_prompt_tokens(request), request["max_tokens"], rates)
    res = ledger.reserve(est_max, call_id="keycheck-smoke")
    t0 = time.monotonic()
    try:
        response = client.messages.create(**request)
    except anthropic.APIError as e:
        ledger.release(res)
        return {"ok": False, "error": f"{type(e).__name__}: {getattr(e, 'message', e)}", "reserved_usd": round(est_max, 6)}
    duration = round(time.monotonic() - t0, 3)
    cost = pricing.cost_of(response.usage, model, "standard", rates)
    ledger.commit(res, cost, call_id="keycheck-smoke")
    parsed = parse_response(response, [SMOKE_REVIEW])
    u = response.usage
    return {
        "ok": not parsed.invalid, "model": response.model, "stop_reason": parsed.stop_reason,
        "duration_s": duration, "cost_usd": round(cost, 7), "reserved_usd": round(est_max, 6),
        "usage": {"input_tokens": u.input_tokens, "cache_creation_input_tokens": u.cache_creation_input_tokens,
                  "cache_read_input_tokens": u.cache_read_input_tokens, "output_tokens": u.output_tokens},
        "label": parsed.labels.get(0), "invalid": parsed.invalid or None, "request_id": getattr(response, "_request_id", None),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check API credential, rates, ledger and request shape before a paid run.")
    ap.add_argument("--no-smoke", action="store_true", help="skip the one tiny paid request")
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    ap.add_argument("--rates", default=os.fspath(config.RATES_CSV_PATH))
    args = ap.parse_args(argv)
    load_dotenv(config.REPO_ROOT / ".env")

    report: dict = {"credential": credential_status(), "label_config": label_config()}
    ok = report["credential"]["ok"]

    try:
        rates = pricing.load_rates(args.rates)
        models = sorted({m for (m, _, _) in rates})
        report["rates"] = {"ok": True, "path": args.rates, "models": models,
                           "haiku_standard_usd_per_mtok": {u: rates.get((MODEL, "standard", u)) for u in pricing.UNITS}}
    except (OSError, ValueError, KeyError) as e:
        report["rates"] = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        rates, models, ok = None, [], False

    ledger = SpendLedger(args.ledger, run_id="keycheck")
    report["ledger"] = {"ok": True, **ledger.summary()}

    if ok:
        import anthropic
        client = anthropic.Anthropic(api_key=config.api_key()[0], max_retries=1, timeout=60.0)
        report["models"] = check_models(client, models or [MODEL])
        ok = report["models"]["ok"]
        if ok and not args.no_smoke:
            report["smoke"] = smoke_test(client, ledger, rates)
            ok = report["smoke"]["ok"]
        elif args.no_smoke:
            report["smoke"] = {"skipped": True}
    else:
        report["models"] = {"skipped": "no credential"}
        report["smoke"] = {"skipped": "no credential"}
    report["ledger_after"] = ledger.summary()
    ledger.close()
    report["ok"] = ok
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not ok:
        print("keycheck FAILED: " + ("no API credential found" if not report["credential"]["ok"]
                                     else "see report above"), file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
