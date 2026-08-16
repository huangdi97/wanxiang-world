"""Genesis draft (G59G)."""

from __future__ import annotations

from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.draft.scenarios import ScenarioCandidate


@dataclass(frozen=True, slots=True)
class GenesisDraft:
    """Composed genesis plan: constitution/domain/world/scenario/seed/profile."""

    genesis_id: str
    constitution_ref: str
    domain_refs: tuple[str, ...]
    world_ref: str
    scenario_ref: str
    seed: str
    runtime_profile: dict[str, str] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        if not self.genesis_id or not self.world_ref or not self.scenario_ref:
            raise ContractError("genesis requires id, world ref and scenario ref")


class GenesisPlanBuilder:
    """Builds a GenesisDraft from a WorldDraft + chosen scenario."""

    def build(
        self,
        draft: WorldDraft,
        scenario: ScenarioCandidate,
        *,
        genesis_id: str = "genesis_1",
        seed: str = "wanxiang-reference-1",
    ) -> GenesisDraft:
        return GenesisDraft(
            genesis_id=genesis_id,
            constitution_ref=draft.constitution_ref,
            domain_refs=draft.selected_domains,
            world_ref=draft.draft_id,
            scenario_ref=scenario.scenario_id,
            seed=seed,
            runtime_profile={
                "clock": "tick",
                "scheduler": "deterministic",
                "agent": "reference",
                "budget": "bounded",
            },
        )
