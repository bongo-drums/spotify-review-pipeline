import json
from types import SimpleNamespace

import pytest

from pipeline import enricher as en


def _resp(payload, stop_reason="end_turn"):
    text = payload if isinstance(payload, str) else json.dumps(payload)
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop_reason,
                           stop_details=None, usage=None)


def test_split_sentences_spans_are_exact_substrings():
    text = "  Ads every song.  Really?\r\nUninstalling!   "
    spans = en.split_sentences(text)
    assert [text[a:b] for a, b in spans] == ["Ads every song.", "Really?", "Uninstalling!"]
    assert en.split_sentences("") == [] and en.split_sentences("   \n ") == []
    assert en.split_sentences("no punctuation at all") == [(0, 21)]
    long = " ".join(f"s{i}." for i in range(20))
    spans = en.split_sentences(long)
    assert len(spans) == en.MAX_SENTENCES and long[spans[-1][0]:spans[-1][1]].startswith("s11.") and spans[-1][1] == len(long)


def test_format_and_request_shape():
    msg = en.build_user_message(["One. Two", "Line one\nline two"])
    assert msg == "#0\n[0] One. [1] Two\n#1\n[0] Line one [1] line two"
    req = en.build_request(["x"] * 3)
    assert req["model"] == en.MODEL and req["max_tokens"] == en.OUTPUT_TOKENS_BASE + 3 * en.OUTPUT_TOKENS_PER_REVIEW
    assert req["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert req["thinking"] == {"type": "disabled"}
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert req["output_config"]["format"]["schema"] == en.OUTPUT_SCHEMA
    assert en.label_config().startswith("labels-v1|claude-haiku-5-5|") and en.label_config() == en.label_config()
    with pytest.raises(ValueError):
        en.build_user_message([])
    with pytest.raises(ValueError):
        en.build_user_message(["x"] * (en.MAX_REVIEWS_PER_REQUEST + 1))
    assert en.estimate_prompt_tokens(req) > en.estimate_prompt_tokens(req, system_tokens=10) > 0


def test_parse_response_valid_invalid_missing():
    texts = ["Ads every song. Really annoying!", "Great app, love it", "Won't open at all. Tried twice.", "meh"]
    good = {"i": 0, "t": "usability", "s": "ads_interruptions", "n": "complaint", "v": 3, "m": 1,
            "e": ["ads", " Spotify ", "", "a", "b", "c", "d"], "q": 1, "r": False}
    bad_pair = {"i": 1, "t": "other", "s": "ads_interruptions", "n": "praise", "v": 1, "m": 4, "e": [], "q": 0, "r": False}
    bad_q = {"i": 2, "t": "playback", "s": "crash_wont_open", "n": "complaint", "v": 4, "m": 0, "e": [], "q": 5, "r": False}
    dup = dict(good, i=0, v=5)  # duplicate index is ignored
    bad_m = dict(good, i=3, m=7)
    parsed = en.parse_response(_resp({"reviews": [good, bad_pair, bad_q, dup, {"i": 9, **good}, bad_m]}), texts)
    assert set(parsed.labels) == {0} and set(parsed.invalid) == {1, 2, 3}
    lab = parsed.labels[0]
    assert lab["evidence_quote"] == "Really annoying!" and lab["evidence_sentence"] == 1 and lab["severity"] == 3
    assert lab["sentiment"] == -0.5 and lab["sentiment_level"] == 1
    assert "sentiment level" in parsed.invalid[3]
    assert lab["entities"] == ["ads", "Spotify", "a", "b", "c"]
    assert parsed.invalid[1].startswith("invalid_record:subtopic")
    assert "out of range" in parsed.invalid[2]
    assert en.parse_response(_resp({"reviews": [good]}), texts).invalid[3] == "missing_from_output"
    assert parsed.error is None


def test_parse_response_request_level_failures():
    texts = ["a", "b"]
    p = en.parse_response(_resp("not json"), texts)
    assert p.invalid == {0: p.error, 1: p.error} and p.error.startswith("invalid_json")
    p = en.parse_response(_resp({"reviews": []}, stop_reason="max_tokens"), texts)
    assert p.error == "max_tokens" and set(p.invalid) == {0, 1}
    r = _resp({"reviews": []}, stop_reason="refusal")
    r.stop_details = SimpleNamespace(category="cyber")
    p = en.parse_response(r, texts)
    assert p.error == "refusal:cyber" and p.invalid == {0: "refusal:cyber", 1: "refusal:cyber"}
    assert en.parse_response(SimpleNamespace(content=[], stop_reason="end_turn"), texts).error == "no_text_block"


def test_out_of_range_evidence_index_on_single_sentence_text_uses_whole_text():
    from types import SimpleNamespace
    from pipeline.enricher import parse_response
    import json
    text = "worst update ever🤬removed everything🤬bring it back"      # one span for the splitter
    rec = {"i": 0, "t": "other", "s": "general_negative", "n": "complaint", "v": 2, "m": 0, "e": [], "q": 2, "r": False}
    resp = SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps({"reviews": [rec]}))], stop_reason="end_turn")
    out = parse_response(resp, [text])
    assert out.labels[0]["evidence_quote"] == text and out.labels[0]["evidence_sentence"] == 0 and not out.invalid
    two = "First one. Second one."
    out2 = parse_response(SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps({"reviews": [{**rec, "q": 5}]}))],
                                          stop_reason="end_turn"), [two])
    assert 0 in out2.invalid and "out of range" in out2.invalid[0]
