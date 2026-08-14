"""G19G: advanced digital human / XR presence research.

- Provider outage falls back to deterministic text without world corruption.
- All actions remain normal commands (utterance -> command payload).
- No real-person likeness without an approved fixture.
- Latency is measured; interruption returns to baseline; ordering preserved.
- Research flag off => no core regression.
"""

from __future__ import annotations

import pytest
from wanxiang_research.digital_human import (
    AvatarIdentity,
    DeterministicTextAvatar,
    LatencyProbe,
    PresenceGateway,
    RightsError,
    Utterance,
)
from wanxiang_research.flags import DEFAULT_FLAGS


class _FakeAvatarProvider:
    """Test provider: controllable latency, failures and interruption."""

    def __init__(self, fail: bool = False, latency_ms: float = 3.0) -> None:
        self._fail = fail
        self._latency_ms = latency_ms
        self._interrupted = 0
        self.name = "fake-avatar"

    def speak(self, avatar: AvatarIdentity, text: str) -> Utterance:
        if self._fail:
            raise RuntimeError("avatar provider unavailable")
        return Utterance(
            utterance_id=f"utt_{avatar.avatar_id}",
            avatar_id=avatar.avatar_id,
            text=text,
            provider=self.name,
            synthetic_label="synthetic:generated",
            latency_ms=self._latency_ms,
            sequence=0,
        )

    def interrupt(self, avatar: AvatarIdentity) -> bool:
        self._interrupted += 1
        return True

    def interrupt_count(self) -> int:
        return self._interrupted


def _stable_compile_ok() -> bool:
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    return StructuredCompiler().compile("stable_2", {"src": approved_source()}).ok


def test_provider_outage_falls_back_without_world_corruption() -> None:
    gateway = PresenceGateway(_FakeAvatarProvider(fail=True), DeterministicTextAvatar())
    avatar = AvatarIdentity(avatar_id="guide", synthetic=True, rights="synthetic-guide")
    utterance = gateway.speak(avatar, "hello")
    assert utterance.provider == "text-fallback"
    assert utterance.synthetic_label == "synthetic:generated"
    # Canonical world state is untouched: stable path unchanged after outage.
    assert _stable_compile_ok() is True


def test_actions_remain_normal_commands() -> None:
    gateway = PresenceGateway(_FakeAvatarProvider(), DeterministicTextAvatar())
    utterance = gateway.speak(AvatarIdentity("guide", synthetic=True), "hello")
    payload = utterance.as_command_payload()
    assert payload["action_type"] == "utterance"
    assert payload["synthetic_label"] == "synthetic:generated"
    assert set(payload) == {
        "action_type",
        "utterance_id",
        "avatar_id",
        "text",
        "provider",
        "synthetic_label",
    }


def test_no_real_person_likeness_without_approved_fixture() -> None:
    gateway = PresenceGateway(_FakeAvatarProvider(), DeterministicTextAvatar())
    real = AvatarIdentity(
        "host", synthetic=False, rights="approved-fixture", likeness_ref="real_person_a"
    )
    with pytest.raises(RightsError):
        gateway.speak(real, "hi")
    approved_gateway = PresenceGateway(
        _FakeAvatarProvider(),
        DeterministicTextAvatar(),
        approved_fixtures=("real_person_a",),
    )
    approved = AvatarIdentity(
        "host", synthetic=False, rights="approved-fixture", likeness_ref="real_person_a"
    )
    utterance = approved_gateway.speak(approved, "hi")
    assert utterance.text == "hi"


def test_latency_measured_and_ordering_preserved() -> None:
    gateway = PresenceGateway(_FakeAvatarProvider(latency_ms=3.0), DeterministicTextAvatar())
    avatar = AvatarIdentity("guide", synthetic=True)
    first = gateway.speak(avatar, "one")
    second = gateway.speak(avatar, "two")
    assert first.sequence < second.sequence
    assert gateway.latency_ms() == (3.0, 3.0)
    assert gateway.mean_latency_ms() == 3.0


def test_interrupt_returns_to_baseline() -> None:
    provider = _FakeAvatarProvider()
    gateway = PresenceGateway(provider, DeterministicTextAvatar())
    avatar = AvatarIdentity("guide", synthetic=True)
    assert gateway.interrupt(avatar) is True
    assert provider.interrupt_count() == 1
    utterance = gateway.speak(avatar, "after interrupt")
    assert utterance.interrupted is True
    assert utterance.provider == "fake-avatar"


def test_probe_measures_provider_latency() -> None:
    provider = _FakeAvatarProvider(latency_ms=0.0)
    clock_values = iter([1.0, 1.05, 2.0, 2.1])
    probe = LatencyProbe(provider, clock=lambda: next(clock_values))
    avatar = AvatarIdentity("guide", synthetic=True)
    first = probe.speak(avatar, "a")
    second = probe.speak(avatar, "b")
    assert first.latency_ms == pytest.approx(0.05)
    assert second.latency_ms == pytest.approx(0.1)


def test_flag_off_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("digital_human_xr") is False
    assert _stable_compile_ok() is True
