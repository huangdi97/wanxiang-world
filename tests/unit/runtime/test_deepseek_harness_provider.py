"""Official DeepSeek Harness SDK adapter tests without fake live evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from wanxiang_runtime.deepseek_harness_provider import (
    OfficialDeepSeekHarnessProvider,
    OfficialDshSettings,
)
from wanxiang_runtime.r7_agent_harness_contract import (
    HarnessConsequence,
    HarnessProtocolError,
    HarnessUnavailable,
    WorldObservation,
)


@dataclass(frozen=True)
class _Result:
    final_response: str


class _FakeHarness:
    def __init__(self, answers: list[str]) -> None:
        self.answers = answers
        self.calls: list[tuple[str, str]] = []
        self.closed = False

    def run(self, prompt: str, *, session_id: str) -> _Result:
        self.calls.append((prompt, session_id))
        if not self.answers:
            raise RuntimeError("no answer")
        return _Result(self.answers.pop(0))

    def close(self) -> None:
        self.closed = True


def _settings(tmp_path: Path) -> OfficialDshSettings:
    return OfficialDshSettings(
        dsh_home=tmp_path / "dsh-home",
        cwd=tmp_path,
        provider="deepseek-official",
        model="deepseek-v4-flash",
        reasoning_effort="max",
        max_tokens=4096,
        request_timeout_seconds=10.0,
    )


def test_official_adapter_identifies_only_an_injected_official_sdk(tmp_path: Path) -> None:
    fake = _FakeHarness([])
    captured: dict[str, object] = {}

    def factory(**kwargs: object) -> _FakeHarness:
        captured.update(kwargs)
        return fake

    provider = OfficialDeepSeekHarnessProvider(
        _settings(tmp_path),
        harness_factory=factory,
        sdk_version="0.2-test",
    )
    try:
        info = provider.info()
        assert info.official_dsh is True
        assert info.kind == "official-deepseek-harness-sdk"
        assert info.harness_version == "0.2-test"
        assert captured["provider"] == "deepseek-official"
        assert captured["model"] == "deepseek-v4-flash"
        assert "api_key" not in captured
    finally:
        provider.close()
    assert fake.closed is True


def test_official_adapter_parses_proposal_and_uses_worldline_session(tmp_path: Path) -> None:
    fake = _FakeHarness(
        [
            (
                '{"status":"proposed","proposal":{"proposalId":"p1",'
                '"action":"set_status","rationaleRef":"dsh#turn-1",'
                '"payloadDigest":"abc"},"reason":"bounded proposal"}'
            )
        ]
    )
    provider = OfficialDeepSeekHarnessProvider(
        _settings(tmp_path), harness_factory=lambda **_: fake, sdk_version="test"
    )
    try:
        decision = provider.decide(
            WorldObservation(
                worldline_id="wl_official",
                revision=4,
                state_hash="state-4",
                allowed_history=("evt-4",),
                allowed_context={"pendingAction": "set_status"},
            )
        )
    finally:
        provider.close()

    assert decision.status == "proposed"
    assert decision.proposal is not None
    assert decision.proposal.action == "set_status"
    assert fake.calls[0][1] == "wanxiang-wl_official"
    assert "no commit authority" in fake.calls[0][0]


def test_official_adapter_requires_exact_json_not_wrapped_text(tmp_path: Path) -> None:
    fake = _FakeHarness(["Here is the requested JSON: {}"])
    provider = OfficialDeepSeekHarnessProvider(
        _settings(tmp_path), harness_factory=lambda **_: fake, sdk_version="test"
    )
    try:
        with pytest.raises(HarnessProtocolError, match="exact JSON"):
            provider.decide(WorldObservation("wl_bad", 0, "state-0"))
    finally:
        provider.close()


def test_official_adapter_reports_consequence_to_same_worldline_session(tmp_path: Path) -> None:
    fake = _FakeHarness(['{"acknowledged":true}'])
    provider = OfficialDeepSeekHarnessProvider(
        _settings(tmp_path), harness_factory=lambda **_: fake, sdk_version="test"
    )
    try:
        assert provider.deliver_consequence(
            HarnessConsequence(
                worldline_id="wl_official",
                proposal_id="p1",
                status="rejected",
                revision=None,
                state_hash=None,
                reason="policy denied",
            )
        )
    finally:
        provider.close()
    assert fake.calls[0][1] == "wanxiang-wl_official"
    assert '"status": "rejected"' in fake.calls[0][0]


def test_official_adapter_refuses_missing_sdk_when_no_factory(tmp_path: Path) -> None:
    provider = OfficialDeepSeekHarnessProvider(_settings(tmp_path))
    try:
        try:
            import deepseek_harness  # type: ignore[import-not-found]  # noqa: F401
        except ModuleNotFoundError:
            with pytest.raises(HarnessUnavailable, match="not installed"):
                provider.info()
        else:
            pytest.skip("official SDK is installed on this host; absence path not applicable")
    finally:
        provider.close()


def test_settings_reject_invalid_limits(tmp_path: Path) -> None:
    with pytest.raises(HarnessUnavailable, match="max_tokens"):
        OfficialDshSettings(
            dsh_home=tmp_path,
            cwd=tmp_path,
            provider="deepseek-official",
            model="deepseek-v4-flash",
            max_tokens=0,
        )
