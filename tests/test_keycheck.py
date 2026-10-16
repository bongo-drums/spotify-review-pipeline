"""keycheck never makes paid calls; these tests use a fake client and never touch the network."""
import io

import pytest

from pipeline import keycheck


class _Resp:
    input_tokens = 1234


class _FakeMessages:
    def __init__(self):
        self.calls = []

    def count_tokens(self, **kw):
        self.calls.append(kw)
        return _Resp()


class _FakeClient:
    def __init__(self):
        self.messages = _FakeMessages()


def test_missing_key_exits_2_without_calling(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(keycheck, "env_report", lambda: {
        "present": dict.fromkeys(keycheck.EXPECTED_VARS, False), "dotenv_file_exists": False,
        "anthropic_key_chars": 0, "anthropic_key_has_expected_prefix": False, "anthropic_base_url": "x"})
    client = _FakeClient()
    out = io.StringIO()
    assert keycheck.main([], client_factory=lambda: client, out=out) == 2
    assert client.messages.calls == []
    assert "MISSING" in out.getvalue()
    assert "NEW session" in out.getvalue()


def test_present_key_makes_one_free_count_tokens_call(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-not-a-real-key")
    client = _FakeClient()
    out = io.StringIO()
    assert keycheck.main([], client_factory=lambda: client, out=out) == 0
    assert len(client.messages.calls) == 1
    call = client.messages.calls[0]
    assert call["model"] == "claude-haiku-5-5"
    assert "max_tokens" not in call  # count_tokens, not messages.create
    assert "1234 input tokens" in out.getvalue()
    assert "sk-ant-test" not in out.getvalue()  # the value is never printed


def test_rejected_key_exits_3(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-bad")

    class Boom(_FakeClient):
        def __init__(self):
            super().__init__()
            self.messages.count_tokens = self._raise

        def _raise(self, **kw):
            raise RuntimeError("authentication_error: invalid x-api-key")

    out = io.StringIO()
    assert keycheck.main([], client_factory=Boom, out=out) == 3
    assert "invalid x-api-key" in out.getvalue()


def test_env_report_never_contains_values(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret-value")
    r = keycheck.env_report()
    assert r["present"]["ANTHROPIC_API_KEY"] is True
    assert r["anthropic_key_has_expected_prefix"] is True
    assert "secret" not in str(r)
