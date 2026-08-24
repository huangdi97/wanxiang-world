"""Scenario mining and Genesis plans for three isolated starts (M65)."""

from __future__ import annotations

import hashlib
import json
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
class InitialSnapshot:
    """Immutable candidate snapshot description; it is not runtime state."""

    snapshot_hash: str
    draft_id: str
    revision: int
    entity_keys: tuple[str, ...]
    relation_count: int
    object_keys: tuple[str, ...]
    places: tuple[str, ...]
    events: tuple[tuple[str, str], ...]
    source_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ActivationSet:
    activation_id: str
    scenario_id: str
    entity_keys: tuple[str, ...]
    budget: int
    strategy: str = "affected_entities"


@dataclass(frozen=True, slots=True)
class CanonPolicy:
    mode: str
    evidence_policy: str
    completion_policy: str
    preserve_dissent: bool = True


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    profile_id: str
    clock: str
    scheduler: str
    activation: str
    budget: int


@dataclass(frozen=True, slots=True)
class GenesisPlan:
    genesis_id: str
    scenario: ScenarioSpec
    snapshot_hash: str
    activation_policy: str
    genesis_draft: GenesisDraft
    initial_snapshot: InitialSnapshot | None = None
    activation_set: ActivationSet | None = None
    canon_policy: CanonPolicy | None = None
    runtime_profile: RuntimeProfile | None = None


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
            scenario_id = f"{candidate.scenario_id}_{mode}"
            seed = self.reproducible_seed(draft, scenario_id)
            spec = ScenarioSpec(
                scenario_id=scenario_id,
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
            snapshot = self.initial_snapshot(draft, snapshot_hash)
            activation = ActivationSet(
                activation_id=f"activation_{index}",
                scenario_id=spec.scenario_id,
                entity_keys=tuple(sorted(spec.participants)),
                budget=max(1, min(100, len(spec.participants) or 1)),
            )
            plans.append(
                GenesisPlan(
                    genesis.genesis_id,
                    spec,
                    snapshot_hash,
                    "bounded_activation",
                    genesis,
                    initial_snapshot=snapshot,
                    activation_set=activation,
                    canon_policy=self.canon_policy(mode),
                    runtime_profile=RuntimeProfile(
                        profile_id=f"profile_{mode}",
                        clock="deterministic",
                        scheduler="bounded",
                        activation="affected_entities",
                        budget=100,
                    ),
                )
            )
        return tuple(plans)

    def reproducible_seed(self, draft: WorldDraft, scenario_id: str) -> int:
        material = {
            "draft_id": draft.draft_id,
            "revision": draft.revision,
            "scenario_id": scenario_id,
            "source_versions": draft.source_versions,
        }
        return int(
            hashlib.sha256(
                json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()[:8],
            16,
        )

    def initial_snapshot(self, draft: WorldDraft, snapshot_hash: str) -> InitialSnapshot:
        return InitialSnapshot(
            snapshot_hash=snapshot_hash,
            draft_id=draft.draft_id,
            revision=draft.revision,
            entity_keys=tuple(key for key, _name in draft.entities),
            relation_count=len(draft.relations),
            object_keys=draft.objects,
            places=draft.places,
            events=draft.events,
            source_refs=draft.source_refs,
        )

    def canon_policy(self, mode: str) -> CanonPolicy:
        policies = {
            "canonical_replay": CanonPolicy(mode, "direct_source_only", "keep_unknown"),
            "soft_canon": CanonPolicy(mode, "approved_candidate", "review_required"),
            "living_open": CanonPolicy(mode, "candidate_only", "user_choice_required"),
        }
        return policies.get(mode, CanonPolicy(mode, "candidate_only", "keep_unknown"))
