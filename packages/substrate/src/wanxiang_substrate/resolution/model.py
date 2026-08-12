"""Pure adjudication value objects (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId


@dataclass(frozen=True, slots=True)
class Adjudication:
    """Auditable resolution outcome: delta + explanation + provenance."""

    action_type: str
    version: int
    seed: int
    outcome: str
    delta: ProposedWorldDelta
    explanation: str
    observability: tuple[EntityId, ...] = ()
    provenance: tuple[str, ...] = ()
    uncertainty: float = 0.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.uncertainty <= 1.0):
            raise ContractError("uncertainty must be in [0, 1]")
        if not self.explanation:
            raise ContractError("adjudication explanation must be non-empty")


@dataclass(frozen=True, slots=True)
class ResolverVersionPin:
    """Pins the resolver version for an action in a run/world context."""

    action_type: str
    version: int

    def __post_init__(self) -> None:
        if self.version <= 0:
            raise ContractError("resolver version must be positive")
