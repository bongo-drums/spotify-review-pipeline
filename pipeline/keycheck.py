"""Free pre-flight check for the Anthropic key. Makes NO paid calls.

Usage:
    python -m pipeline.keycheck

1. Reports which expected variable names are present (names only; values are never printed).
2. If ANTHROPIC_API_KEY is set, sends one count_tokens request (free) carrying the real enricher
   system prompt and one tiny user message, and reports whether the key was accepted.

Exit codes: 0 key accepted, 2 key missing, 3 key rejected or request failed.
"""
from __future__ import annotations

import os
import sys

from . import config, enrich

EXPECTED_VARS = ("ANTHROPIC_API_KEY", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_DB_URL",
                 "VERCEL_TOKEN", "TYPESAFE_API_KEY")


def env_report() -> dict:
    """Presence of each expected variable, without values. Loads a local .env first if one exists."""
    try:
        from dotenv import load_dotenv
        load_dotenv(config.REPO_ROOT / ".env")
    except ImportError:
        pass
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    return {
        "present": {name: bool(os.environ.get(name, "").strip()) for name in EXPECTED_VARS},
        "dotenv_file_exists": (config.REPO_ROOT / ".env").exists(),
        "anthropic_key_chars": len(key),
        "anthropic_key_has_expected_prefix": key.startswith("sk-ant-"),
        "anthropic_base_url": os.environ.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com (default)",
    }


def count_tokens_probe(client) -> dict:
    """One free count_tokens call with the production system prompt. No tokens are billed."""
    resp = client.messages.count_tokens(
        model=enrich.MODEL,
        system=[{"type": "text", "text": enrich.system_prompt()}],
        messages=[{"role": "user", "content": enrich.build_user_message(
            [{"review_text": "Great app, it has all the songs I like.", "cache_source_id": "probe"}])}],
    )
    return {"model": enrich.MODEL, "system_prompt_tokens_plus_probe": resp.input_tokens}


def main(argv=None, *, client_factory=enrich.make_client, out=sys.stdout) -> int:
    report = env_report()
    for name, present in report["present"].items():
        print(f"{name:28s} {'set' if present else 'MISSING'}", file=out)
    print(f".env file present: {report['dotenv_file_exists']}", file=out)
    print(f"ANTHROPIC_BASE_URL: {report['anthropic_base_url']}", file=out)
    if not report["present"]["ANTHROPIC_API_KEY"]:
        print("\nANTHROPIC_API_KEY is not set in this session, so no model call was made.", file=out)
        print("Add it as an environment variable (or Network secret) on the cloud environment, save,", file=out)
        print("then start a NEW session: a running session does not pick up the change.", file=out)
        return 2
    print(f"ANTHROPIC_API_KEY: {report['anthropic_key_chars']} chars, "
          f"expected 'sk-ant-' prefix: {report['anthropic_key_has_expected_prefix']}", file=out)
    try:
        probe = count_tokens_probe(client_factory())
    except Exception as e:  # noqa: BLE001 - we want the provider's own message, not a traceback
        print(f"\nKey check FAILED: {type(e).__name__}: {e}", file=out)
        return 3
    print(f"\nKey accepted. count_tokens (free) on {probe['model']}: "
          f"{probe['system_prompt_tokens_plus_probe']} input tokens for the enricher prompt + 1 review.",
          file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
