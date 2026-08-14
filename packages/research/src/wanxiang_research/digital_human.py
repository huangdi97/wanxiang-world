"""Advanced digital human / XR presence research (G19G, experimental).

Embodiment/presence goes through a Port/Adapter: utterances are produced as
normal command payloads and never mutate canonical state directly. Providers
are labeled synthetic and carry identity/voice rights; a deterministic text
fallback is the baseline when a provider is unavailable. No real-person
likeness is used without an approved fixture.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol


class RightsError(Exception):
    """Raised when an unapproved real-person likeness/voice is requested."""


@dataclass(frozen=True, slots=True)
class AvatarIdentity:
    avatar_id: str
    synthetic: bool = True
    rights: str = ""
    likeness_ref: str = ""  # empty means pure synthetic; otherwise approved fixture


@dataclass(frozen=True, slots=True)
class Utterance:
    utterance_id: str
    avatar_id: str
    text: str
    provider: str
    synthetic_label: str
    latency_ms: float
    sequence: int
    interrupted: bool = False

    def as_command_payload(self) -> dict[str, object]:
        # All actions remain normal commands; the gateway never writes world state.
        return {
            "action_type": "utterance",
            "utterance_id": self.utterance_id,
            "avatar_id": self.avatar_id,
            "text": self.text,
            "provider": self.provider,
            "synthetic_label": self.synthetic_label,
        }


class AvatarProvider(Protocol):
    name: str

    def speak(self, avatar: AvatarIdentity, text: str) -> Utterance: ...

    def interrupt(self, avatar: AvatarIdentity) -> bool: ...


class DeterministicTextAvatar:
    """Deterministic text baseline (no paid API; latency is measured)."""

    def __init__(self, base_latency_ms: float = 0.0) -> None:
        self._base_latency_ms = base_latency_ms
        self.name = "text-fallback"

    def speak(self, avatar: AvatarIdentity, text: str) -> Utterance:
        return Utterance(
            utterance_id=f"utt_{avatar.avatar_id}_{len(text)}",
            avatar_id=avatar.avatar_id,
            text=text,
            provider=self.name,
            synthetic_label="synthetic:generated",
            latency_ms=self._base_latency_ms,
            sequence=0,
        )

    def interrupt(self, avatar: AvatarIdentity) -> bool:
        return False


class PresenceGateway:
    """Routes presence actions through provider + fallback; rights checked first."""

    def __init__(
        self,
        provider: AvatarProvider,
        fallback: AvatarProvider,
        approved_fixtures: Sequence[str] = (),
    ) -> None:
        self._provider = provider
        self._fallback = fallback
        self._approved = frozenset(approved_fixtures)
        self._sequence = 0
        self._latencies: list[float] = []
        self._interrupted: set[str] = set()

    def _next_sequence(self) -> int:
        self._sequence += 1
        return self._sequence

    def _check_rights(self, avatar: AvatarIdentity) -> None:
        if avatar.synthetic:
            return
        if avatar.likeness_ref not in self._approved:
            raise RightsError(f"likeness {avatar.likeness_ref!r} is not an approved fixture")

    def speak(self, avatar: AvatarIdentity, text: str) -> Utterance:
        self._check_rights(avatar)
        try:
            utterance = self._provider.speak(avatar, text)
        except Exception:
            # Provider outage: deterministic text fallback; canonical world untouched.
            utterance = self._fallback.speak(avatar, text)
        self._latencies.append(utterance.latency_ms)
        return Utterance(
            utterance_id=utterance.utterance_id,
            avatar_id=utterance.avatar_id,
            text=utterance.text,
            provider=utterance.provider,
            synthetic_label=utterance.synthetic_label,
            latency_ms=utterance.latency_ms,
            sequence=self._next_sequence(),
            interrupted=avatar.avatar_id in self._interrupted,
        )

    def interrupt(self, avatar: AvatarIdentity) -> bool:
        # Interruption clears the active provider stream and returns to baseline.
        self._interrupted.add(avatar.avatar_id)
        return self._provider.interrupt(avatar)

    def latency_ms(self) -> tuple[float, ...]:
        return tuple(self._latencies)

    def mean_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)


class LatencyProbe:
    """Observability probe wrapping a provider's speak with measured latency."""

    def __init__(self, provider: AvatarProvider, clock: Callable[[], float] | None = None) -> None:
        self._provider = provider
        self._clock = clock if clock is not None else lambda: 0.0

    @property
    def name(self) -> str:
        return self._provider.name

    def speak(self, avatar: AvatarIdentity, text: str) -> Utterance:
        start = self._clock()
        utterance = self._provider.speak(avatar, text)
        elapsed = self._clock() - start
        return Utterance(
            utterance_id=utterance.utterance_id,
            avatar_id=utterance.avatar_id,
            text=utterance.text,
            provider=utterance.provider,
            synthetic_label=utterance.synthetic_label,
            latency_ms=elapsed,
            sequence=utterance.sequence,
            interrupted=utterance.interrupted,
        )

    def interrupt(self, avatar: AvatarIdentity) -> bool:
        return self._provider.interrupt(avatar)
