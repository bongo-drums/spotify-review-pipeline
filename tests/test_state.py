import json

import pytest

from pipeline.state import RunState

CFG = "labels-v1|claude-haiku-5-5"


def _state(ingested):
    _, out = ingested
    return RunState(out / "state.sqlite")


def test_pending_text_groups(ingested):
    with _state(ingested) as st:
        groups = st.pending_text_groups(10)
        assert [g["cache_source_id"] for g in groups] == ["r1", "r2", "r6"]
        assert groups[0]["review_ids"] == ["r1", "r5", "r7"]
        assert groups[1]["review_ids"] == ["r2", "r8"]
        assert "\n" in groups[1]["review_text"]
        assert len(st.pending_text_groups(2)) == 2


def test_commit_batch_and_cache_hits(ingested, tmp_path):
    with _state(ingested) as st:
        out = st.commit_batch(
            results=[{"review_ids": ["r1"], "label": {"topic": "praise"}, "label_config": CFG}],
            quarantines=[{"review_ids": ["r6"], "reason": "invalid_output_twice"}],
            call_row={"run_id": "t", "stage": "classify", "phase": "initial", "model": "claude-haiku-5-5",
                      "request_review_ids": ["r1", "r6"], "attempt": 1, "status": "success",
                      "input_tokens": 100, "output_tokens": 20},
        )
        assert out["completed"] == 1 and out["quarantined"] == 1 and out["call_id"]
        # r5 and r7 share r1's text: the cache completes them without another call
        assert st.apply_cache_hits(CFG) == 2
        rows = {r["review_id"]: dict(r) for r in st.conn.execute("SELECT * FROM records")}
        assert rows["r5"]["status"] == "completed" and rows["r5"]["reason"] == "label_cache"
        assert json.loads(rows["r7"]["label"]) == {"topic": "praise"}
        assert rows["r6"]["status"] == "quarantined" and rows["r6"]["attempts"] == 1
        assert st.status_counts() == {"pending": 2, "completed": 3, "quarantined": 3}
        assert [g["cache_source_id"] for g in st.pending_text_groups(10)] == ["r2"]

        # re-applying the same batch does not double count
        again = st.commit_batch(results=[{"review_ids": ["r1"], "label": {"topic": "x"}, "label_config": CFG}])
        assert again["completed"] == 0

        snap = st.export_checkpoint(tmp_path / "ckpt.json", run_id="t")
        assert snap["counts"]["completed"] == 3 and snap["completed_ids_count"] == 3
        assert json.loads((tmp_path / "ckpt.json").read_text())["completed_ids_sha256"] == snap["completed_ids_sha256"]


def test_commit_batch_is_atomic(ingested):
    """An exception midway through a batch must leave no trace (no call row, no label, no cache)."""
    with _state(ingested) as st:
        before = st.status_counts()
        with pytest.raises(TypeError):
            st.commit_batch(
                results=[
                    {"review_ids": ["r1", "r5", "r7"], "label": {"topic": "praise"}, "label_config": CFG},
                    {"review_ids": ["r6"], "label": {"bad": object()}, "label_config": CFG},  # not JSON-serializable
                ],
                quarantines=[{"review_ids": ["r2"], "reason": "x"}],
                call_row={"run_id": "t", "stage": "classify", "status": "success"},
            )
        assert st.status_counts() == before
        assert st.conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0] == 0
        assert st.conn.execute("SELECT COUNT(*) FROM label_cache").fetchone()[0] == 0
        assert st.conn.execute("SELECT attempts FROM records WHERE review_id='r1'").fetchone()[0] == 0


def test_commit_batch_rejects_mixed_texts(ingested):
    with _state(ingested) as st:
        with pytest.raises(ValueError):
            st.commit_batch(results=[{"review_ids": ["r1", "r2"], "label": {}, "label_config": CFG}])
        assert st.status_counts()["completed"] == 0


def test_retries_keep_pending(ingested):
    with _state(ingested) as st:
        st.commit_batch(results=[], retries=[{"review_ids": ["r6"], "reason": "invalid_json"}])
        row = st.conn.execute("SELECT status, attempts, reason FROM records WHERE review_id='r6'").fetchone()
        assert tuple(row) == ("pending", 1, "invalid_json")
