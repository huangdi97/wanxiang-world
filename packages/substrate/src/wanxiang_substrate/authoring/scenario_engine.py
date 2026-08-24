"""Scenario mining and Genesis plans for three isolated starts (M65)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.draft.genesis import GenesisDraft, GenesisPlanBuilder
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.draft.scenarios import ScenarioCandidate, ScenarioMiner


@dataclass(frozen=True, slots=True)
class ScenarioSpec:
    scenario_id: str
    initial_time: str
    participants: tuple[str, ...]
    canon_mode: str
    runtime_profile: tuple[tuple[str, str], ...]
    seed: int


@dataclass(frozen=True, slots=True)
class GenesisPlan:
    genesis_id: str
    scenario: ScenarioSpec
    snapshot_hash: str
    activation_policy: str
    genesis_draft: GenesisDraft


class ScenarioEngine:
    """Builds deterministic scenario candidates without runtime writes."""

    def mine(self, draft: WorldDraft) -> tuple[ScenarioCandidate, ...]:
        found = ScenarioMiner().mine(draft)
        if found:
            return found
        return (
            ScenarioCandidate(
                scenario_id="scenario_default",
                initial_time="unknown",
                participants=tuple(key for key, _name in draft.entities),
                source_refs=draft.source_refs,
                description="reference start with explicit unknown time",
            ),
        )

    def build_three(self, draft: WorldDraft) -> tuple[GenesisPlan, ...]:
        candidates = self.mine(draft)
        plans: list[GenesisPlan] = []
        modes = ("canonical_replay", "soft_canon", "living_open")
        for index, mode in enumerate(modes, start=1):
            candidate = candidates[(index - 1) % len(candidates)]
            seed = int(hashlib.sha256(f"{draft.draft_id}:{mode}".encode()).hexdigest()[:8], 16)
            spec = ScenarioSpec(
                scenario_id=f"{candidate.scenario_id}_{mode}",
                initial_time=candidate.initial_time,
                participants=candidate.participants,
                canon_mode=mode,
                runtime_profile=(
                    ("clock", "deterministic"),
                    ("scheduler", "bounded"),
                    ("activation", "affected_entities"),
                ),
                seed=seed,
            )
            genesis = GenesisPlanBuilder().build(
                draft,
                candidate,
                genesis_id=f"genesis_{index}",
                seed=f"{seed:08x}",
            )
            snapshot_hash = hashlib.sha256(
                f"{draft.draft_id}:{draft.revision}:{spec.scenario_id}:{seed}".encode()
            ).hexdigest()
            plans.append(
                GenesisPlan(genesis.genesis_id, spec, snapshot_hash, "bounded_activation", genesis)
            )
        return tuple(plans)
