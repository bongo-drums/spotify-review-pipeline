"""verify / group / rank / recommend / export / run, end to end against a fake client, then the course checker."""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from pipeline import grouping, memo, ranking, verifier
from pipeline import run as runner
from pipeline.enricher import SYSTEM_PROMPT as ENRICH_PROMPT
from pipeline.export import export_grading
from pipeline.state import RunState
from tests.conftest import HEADER
from tests.test_pilot import FakeMessages, _rule

ROOT = Path(__file__).resolve().parent.parent
_REVIEW = re.compile(r"^#(\d+)\n(.*)$", re.M)


class FakeAllStages(FakeMessages):
    """Routes by system prompt: enricher (inherited), verifier, group namer, memo writer."""

    def create(self, **kw):
        system = kw["system"][0]["text"]
        if system == ENRICH_PROMPT:
            return super().create(**kw)
        self.calls.append(kw)
        user = kw["messages"][0]["content"]
        usage = SimpleNamespace(input_tokens=300, cache_creation_input_tokens=0, cache_read_input_tokens=900, output_tokens=120)
        if system == verifier.SYSTEM_PROMPT:
            recs = []
            for m in _REVIEW.finditer(user):
                k, body = int(m.group(1)), m.group(2)
                r = _rule(body)
                num = re.search(r"#(\d+)", body)
                if num and int(num.group(1)) % 2:     # the verifier disagrees on severity for odd-numbered texts
                    r = {**r, "v": r["v"] % 5 + 1}
                recs.append({"i": k, "t": r["t"], "n": r["n"], "v": r["v"], "r": False})
            text = json.dumps({"reviews": recs})
        elif system == grouping.SYSTEM_PROMPT:
            ids = re.findall(r"^issue (\S+) ", user, re.M)
            text = json.dumps({"issues": [{"id": i, "name": f"Name for {i}", "summary": "Customers report this."} for i in ids]})
        elif system == memo.SYSTEM_PROMPT:
            claims = re.findall(r"^(C\d+) \| (\S+) \| (\w+) \| ", user, re.M)
            top = re.findall(r"^rank 1 \| (\S+) \|", user, re.M)[0]
            ev = re.findall(rf"^{re.escape(top)} \| (\S+) \| ", user, re.M)
            top_claims = [c for c in claims if c[1] == top]
            bad = "REJECTED" in user
            text = json.dumps({
                "headline": "Fix playback and ads first",
                "situation": [f"Complaints concentrate in a few issues; the top issue has {{{top_claims[0][0]}}} complaints."
                              + ("" if bad else " It was mentioned 42 times.")],   # digits -> rejected once
                "top_issues": [{"issue_id": top, "why_it_matters": f"Severity sum {{{top_claims[1][0]}}}.",
                                "claim_ids": [top_claims[0][0], top_claims[1][0]], "evidence_review_ids": ev[:1]}],
                "recommendation": {"focus_area": "usability", "argument": f"Priority {{{top_claims[3][0]}}} leads.",
                                   "claim_ids": [top_claims[3][0]]},
                "alternatives": [{"focus_area": "playback", "case_for": "Crashes block use.", "why_not_now": "Fewer reports."}],
                "limitations": ["Self-selected public reviews."]})
        else:
            raise AssertionError("unknown system prompt")
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason="end_turn", stop_details=None,
                               usage=usage, model=kw["model"], _request_id="req_fake")


def _client():
    return SimpleNamespace(messages=FakeAllStages())


@pytest.fixture
def reviews_csv(tmp_path):
    phrases = ["Ads every song", "Love this app", "Great music. Love it!", "Cannot login anymore", "Uninstalling now",
               "Worst update ever", "Meh"]
    rows = []
    for i in range(120):
        text = "" if i == 7 else ("Love this app" if i in (40, 41, 42) else f"{phrases[i % len(phrases)]} #{i}")
        rows.append([f"id-{i:03d}", text, str(1 + i % 5), "0", "9.0.1", f"2025-{1 + i % 12:02d}-{1 + i % 27:02d} 10:00:00"])
    path = tmp_path / "reviews.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    return path


def test_ranking_matches_checker_arithmetic():
    members = [{"issue_id": "b.x", "review_id": "1", "severity": 3}, {"issue_id": "a.y", "review_id": "2", "severity": 2},
               {"issue_id": "b.x", "review_id": "3", "severity": 4}, {"issue_id": "c.z", "review_id": "4", "severity": 7}]
    rows = ranking.rank(members)
    assert [r["issue_id"] for r in rows] == ["b.x", "c.z", "a.y"]           # 7 ties: issue_id ascending
    assert rows[0] == {"rank": "1", "issue_id": "b.x", "complaint_count": "2", "severity_sum": "7",
                       "mean_severity": "3.500000", "priority_score": "7"}
    assert ranking.mean_string(2, 3) == "0.666667" and ranking.mean_string(5, 8) == "0.625000"
    claims = ranking.build_claims(rows, top_k=1)
    assert [c["claim_id"] for c in claims] == ["C1", "C2", "C3", "C4"] and claims[2]["value"] == "3.500000"


def test_verifier_sample_and_planted_errors():
    assert verifier.sample_rule(1000, 0.01, 10) == 10 and verifier.sample_rule(5000, 0.01, 10) == 50
    assert verifier.sample_rule(3, 0.01, 10) == 3
    lab = {"topic": "playback", "intent": "complaint", "severity": 3}
    for k in range(6):
        bad, which = verifier.corrupt(lab, k)
        assert bad[which] != lab[which] and all(bad[f] == lab[f] for f in lab if f != which)
    verified = [{"review_id": f"r{i}", "enricher": lab, "verifier": dict(lab)} for i in range(8)]
    pe = verifier.planted_error_check(verified, "s")
    assert pe["planted"] == 5 and pe["detected"] == 5 and pe["detection_rate"] == 1.0


def test_run_end_to_end_resume_export_and_checker(reviews_csv, tmp_path):
    out, ledger, grading = tmp_path / "run1", tmp_path / "ledger.sqlite", tmp_path / "grading"
    client = _client()
    # 1) interrupted-style run: stop after 60 texts with saved progress -> checkpoint_before
    first = runner.run(reviews_csv, out, max_usd=1.0, limit=60, ledger_path=ledger, client=client)
    assert first["status"] == "stopped_at_limit" and first["checkpoint_before"]["completed_count"] >= 60
    assert (out / "checkpoints" / "checkpoint_before.json").exists()
    n_calls = len(client.messages.calls)
    # 2) resume: remaining texts in phase=resume, then verify/group/rank/recommend, then export
    second = runner.run(reviews_csv, out, max_usd=1.0, ledger_path=ledger, client=client, export=grading)
    assert second["status"] == "ok" and second["resumed"] and second["phase"] == "resume"
    assert second["checkpoint_after"]["completed_count"] == 119 and second["counts_after"]["pending"] == 0
    d = second["downstream"]
    assert d["verify"]["verified"] == 10 and d["verify"]["sample"] == 10          # min_n on 116 heads
    assert d["verify"]["planted_errors"]["detection_rate"] == 1.0
    assert d["group"]["issues"] >= 3 and d["group"]["naming"]["calls"] == 1
    assert d["recommend"]["status"] == "validated" and d["recommend"]["calls"] == 2  # digits rejected once, then ok
    assert second["cost_by_stage"].keys() == {"enrich", "verify", "group", "memo"}
    art = out / "artifacts"
    for name in ("membership.csv", "ranking.csv", "claims.csv", "aggregates.json", "issues.json", "verification.json",
                 "verification.md", "memo.json", "memo.md"):
        assert (art / name).exists(), name
    md = (art / "memo.md").read_text()
    body = md.split("## Situation")[1].split("## Claims appendix")[0].replace("id-042", "")
    assert "(C1)" in md and "42" not in body          # the typed digit was rejected; numbers come from claims.csv
    ver = json.loads((art / "verification.json").read_text())
    assert ver["agreement"]["topic"] == 1.0 and ver["agreement"]["severity"] < 1.0 and ver["disagreements"]
    # cache: rerunning downstream makes zero model calls
    before = len(client.messages.calls)
    third = runner.run(reviews_csv, out, max_usd=1.0, ledger_path=ledger, client=client, stages=("verify", "group", "rank", "recommend"))
    assert third["downstream"]["model_calls"] == 0 and len(client.messages.calls) == before
    # offline ranking regeneration is byte-identical
    rk = (art / "ranking.csv").read_bytes()
    assert ranking.main(["--run", str(out)]) == 0 and (art / "ranking.csv").read_bytes() == rk

    # 3) grading export passes the course checker's mechanical audit
    files = {p.name for p in grading.iterdir()}
    assert {"run.json", "ingestion.json", "records.jsonl", "membership.csv", "ranking.csv", "claims.csv", "calls.jsonl",
            "checkpoint_before.json", "checkpoint_after.json"} <= files
    calls = [json.loads(l) for l in (grading / "calls.jsonl").read_text().splitlines()]
    assert {c["role"] for c in calls} == {"enrich", "verify", "group", "memo"}
    assert {c["phase"] for c in calls if c["role"] == "enrich"} == {"initial", "resume"}
    checker = ROOT / "docs" / "course" / "check_submission.py"
    ref = tmp_path / "ref.json"
    subprocess.run([sys.executable, str(checker), "reference", "--full", str(reviews_csv), "--analysis", str(reviews_csv),
                    "--out", str(ref)], check=True, capture_output=True)
    res = tmp_path / "check.json"
    subprocess.run([sys.executable, str(checker), "check", "--reference", str(ref), "--submission", str(grading), "--out", str(res)],
                   check=True, capture_output=True)
    audit = json.loads(res.read_text())
    assert audit["status"] == "pass", audit["issue_counts"]
    assert audit["coverage"]["valid_completed"] == 119 and audit["coverage"]["quarantined"] == 1
    assert audit["coverage"]["valid_cache_reuses"] == 2 and audit["working_coverage_point_candidate"] == 1.0
    assert audit["calculated_ranking"][0]["issue_id"] == list(csv.DictReader(open(grading / "ranking.csv")))[0]["issue_id"]


def test_fallback_routes_twice_invalid_texts_to_sonnet(tmp_path):
    """A text Haiku cannot label validly twice goes to Sonnet once (capped); the fake Sonnet fails it too, so it
    stays quarantined with a fallback reason, and the call log shows the Sonnet enrich call."""
    rows = [[f"id-{i:03d}", "INVALID label please" if i == 3 else f"Love this app #{i}", "5", "0", "9.0.1", "2025-01-01 10:00:00"]
            for i in range(40)]
    path = tmp_path / "r.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    out, ledger, client = tmp_path / "fb", tmp_path / "l.sqlite", _client()
    rep = runner.run(path, out, max_usd=1.0, ledger_path=ledger, client=client, stages=("enrich", "fallback"), fallback_frac=0.1)
    fb = rep["downstream"]["fallback"]
    assert fb["eligible"] == 1 and fb["routed"] == 1 and fb["cap_texts"] == 4 and fb["calls"] == 1
    assert fb["completed"] == 0 and fb["still_quarantined"] == 1
    with RunState(out / "state.sqlite") as st:
        row = st.conn.execute("SELECT status, reason, attempts FROM records WHERE review_id='id-003'").fetchone()
        assert row[0] == "quarantined" and row[1].startswith("fallback_invalid_record") and row[2] == 3
        models = [r[0] for r in st.conn.execute("SELECT model FROM calls WHERE stage='enrich' ORDER BY started_at")]
        assert models == ["claude-haiku-5-5", "claude-haiku-5-5", "claude-sonnet-5-5"]
        cfg = st.conn.execute("SELECT label_config FROM calls WHERE model='claude-sonnet-5-5'").fetchone()[0]
        assert cfg.startswith("labels-v1|claude-sonnet-5-5|")
    assert rep["stage_calls"]["fallback"]["calls"] == 1 and rep["stage_calls"]["enrich"]["calls"] == 2
    assert client.messages.calls[-1]["thinking"] == {"type": "between_tools"}


def test_publish_rest_and_file_backed_records(reviews_csv, tmp_path, monkeypatch):
    """REST loader: checks the schema exists, deletes the run's rows, inserts every table in batches; records can
    come from labels.csv + the source CSV when the run DB is absent (fresh clone)."""
    from pipeline import publish
    out, ledger = tmp_path / "pub", tmp_path / "l.sqlite"
    rep = runner.run(reviews_csv, out, max_usd=1.0, ledger_path=ledger, client=_client())
    assert rep["status"] == "ok"
    calls = []

    def fake_request(method, url, key, body=None, prefer=None):
        calls.append((method, url.split("/rest/v1/")[1], len(body) if isinstance(body, list) else None))
        return {"GET": 200, "DELETE": 204}.get(method, 201), "[]"
    res = publish.load_rest(out, "https://x.supabase.co", "k", batch=50, request=fake_request)
    assert res["counts"]["records"] == 120 and res["counts"]["runs"] == 1 and res["counts"]["issues"] >= 3
    assert calls[0] == ("GET", "runs?select=run_id&limit=1", None)
    assert [c for c in calls if c[0] == "DELETE"][0][1] == "memo?run_id=eq.pub"
    assert sum(c[2] or 0 for c in calls if c[0] == "POST" and c[1] == "records") == 120
    # same rows without the run DB (labels.csv + source csv)
    from_db = list(publish.iter_records(out))
    (out / "state.sqlite").unlink()
    from_files = list(publish.iter_records(out, source_csv=reviews_csv))
    assert len(from_files) == 120 and from_files[0] == from_db[0] and from_files[7]["status"] == "quarantined"
    assert {r["review_id"]: r for r in from_files} == {r["review_id"]: r for r in from_db}
    snap = publish.write_json_snapshot(out, tmp_path / "snap", max_records=None)
    assert snap["records_written"] == 120
