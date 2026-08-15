"""Perception / belief / memory + message propagation (G36E).

PerceptionEnvelope wraps an observation; perceive() forms an actor memory.
propagate_message() moves a message through a chain with deterministic rumour
distortion and confidence decay (misunderstanding). FutureCanon is never
propagated: propagation candidates come only from the runtime view (G35E).
Pure; no write path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.epistemic.model import MemoryRecord
from wanxiang_substrate.sources.canon import CanonClaim, CompiledCanon

Channel = Literal["visual", "acoustic", "textual"]
VALID_CHANNELS = ("visual", "acoustic", "textual")


@dataclass(frozen=True, slots=True)
class PerceptionEnvelope:
    """An observation an actor could perceive (never canonical truth)."""

    envelope_id: str
    observer_id: EntityId
    content_ref: str
    channel: Channel
    confidence: float
    at_ticks: int
    source_event_ref: str = ""
    visibility: Literal["public", "group", "private"] = "public"

    def __post_init__(self) -> None:
        if not self.envelope_id or not self.content_ref:
            raise ContractError("perception envelope requires id and content ref")
        if self.channel not in VALID_CHANNELS:
            raise ContractError(f"invalid channel {self.channel!r}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")


def perceive(
    envelope: PerceptionEnvelope,
    *,
    memory_id: EntityId,
) -> MemoryRecord:
    """Perception forms an observation memory for the observer."""
    return MemoryRecord(
        memory_id=memory_id,
        actor_id=envelope.observer_id,
        kind="observation",
        content_ref=envelope.content_ref,
        at_ticks=envelope.at_ticks,
        salience=envelope.confidence,
        source_obs_ref=envelope.source_event_ref or None,
    )


def rumour_distortion(content: str, hop: int, seed: int) -> str:
    """Deterministic rumour distortion: every 3rd hop appends a marker."""
    if (seed + hop) % 3 == 0:
        return f"{content} (rumoured)"
    return content


@dataclass(frozen=True, slots=True)
class PropagatedMessage:
    """A message after passing through a propagation chain."""

    message_id: str
    origin: str
    hops: tuple[str, ...]
    final_content: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.message_id or not self.origin:
            raise ContractError("propagated message requires id and origin")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")


def propagate_message(
    *,
    message_id: str,
    origin: str,
    chain: tuple[str, ...],
    content: str,
    seed: int,
    decay: float = 0.9,
) -> PropagatedMessage:
    """Propagate a message through a chain with rumour + misunderstanding.

    Each hop applies deterministic distortion (rumour) and multiplies
    confidence by decay (misunderstanding). Deterministic per inputs.
    """
    if not (0.0 < decay <= 1.0):
        raise ContractError("decay must be within (0,1]")
    final_content = content
    confidence = 1.0
    for hop, _actor in enumerate(chain):
        final_content = rumour_distortion(final_content, hop, seed)
        confidence = round(confidence * decay, 4)
    return PropagatedMessage(
        message_id=message_id,
        origin=origin,
        hops=chain,
        final_content=final_content,
        confidence=confidence,
    )


def propagatable_claims(canon: CompiledCanon) -> tuple[CanonClaim, ...]:
    """Claims eligible for propagation: runtime view only (never FutureCanon)."""
    return canon.runtime_view
