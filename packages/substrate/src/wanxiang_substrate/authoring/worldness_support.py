"""Shared immutable evidence types for M66 validation and simulation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from wanxiang_substrate.authoring.worldness_policy import (
    WorldnessGates,
    WorldnessIntegrity,
)

WORLDNESS_DIMENSIONS = (
    "persistence",
    "causality",
    "epistemic",
    "spatial",
    "consequence",
    "autonomy",
    "branch_isolation",
    "replayability",
    "provenance",
    "uncertainty",
)


@dataclass(frozen=True, slots=True)
class WorldnessInput:
    entity_count: int
    relation_count: int
    event_count: int
    source_count: int
    uncertainty: float
    replay_equal: bool
    branch_isolated: bool
    draft_id: str = ""
    draft_revision: int = 0
    source_refs: tuple[str, ...] = ()
    domain_refs: tuple[str, ...] = ()
    completion_refs: tuple[str, ...] = ()
    package_id: str = ""
    provider_ids: tuple[str, ...] = ()
    seed: int = 0
    place_count: int = 0
    object_count: int = 0
    object_required: bool = False
    # Legacy callers predate explicit package evidence; real package runs pass
    # their measured coverage at construction time.
    evidence_coverage: float = 1.0
    action_committed: bool = False
    action_evidence_refs: tuple[str, ...] = ()
    integrity: WorldnessIntegrity = WorldnessIntegrity()


@dataclass(frozen=True, slots=True)
class WorldnessDimensionEvidence:
    """Measured dimension result with source evidence and repair guidance."""

    name: str
    measurement: str
    score: float
    evidence: tuple[str, ...]
    failure: str = ""
    remediation: str = ""


@dataclass(frozen=True, slots=True)
class WorldnessScore:
    dimensions: tuple[tuple[str, float], ...]
    overall: float
    passed: bool
    evidence: tuple[WorldnessDimensionEvidence, ...] = ()
    gates: WorldnessGates = WorldnessGates(False, False, False)
    violations: tuple[str, ...] = ()

    def value(self, name: str) -> float:
        return dict(self.dimensions).get(name, 0.0)


@dataclass(frozen=True, slots=True)
class SimulationStep:
    day: int
    tick: int
    active_entities: int
    event_count: int
    state_hash: str


@dataclass(frozen=True, slots=True)
class SimulationTrace:
    branch_id: str
    seed: int
    horizon_days: int
    accelerated: bool
    steps: tuple[SimulationStep, ...]
    final_hash: str
    replay_hash: str


class BoundedSimulation:
    """Deterministic reference simulation; it never writes canonical state."""

    def run(
        self,
        value: WorldnessInput,
        *,
        branch_id: str = "preview",
        horizon_days: int = 7,
        accelerated: bool = True,
    ) -> SimulationTrace:
        if not branch_id or not 1 <= horizon_days <= 365:
            raise ValueError("branch_id is required and horizon_days must be 1..365")
        steps: list[SimulationStep] = []
        for day in range(1, horizon_days + 1):
            tick = day if accelerated else day * 24
            active = min(value.entity_count, max(1, day % (value.entity_count + 1)))
            events = min(value.event_count, day)
            material = {
                "branch": branch_id,
                "seed": value.seed,
                "day": day,
                "tick": tick,
                "active": active,
                "events": events,
                "draft": value.draft_id,
                "revision": value.draft_revision,
            }
            state_hash = hashlib.sha256(
                json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            steps.append(SimulationStep(day, tick, active, events, state_hash))
        final_hash = steps[-1].state_hash
        replay_hash = hashlib.sha256(
            "|".join(step.state_hash for step in steps).encode()
        ).hexdigest()
        return SimulationTrace(
            branch_id,
            value.seed,
            horizon_days,
            accelerated,
            tuple(steps),
            final_hash,
            replay_hash,
        )


@dataclass(frozen=True, slots=True)
class FailureLocation:
    dimension: str
    layer: str
    target: str
    reason: str
    source_refs: tuple[str, ...]


class FailureLocalizer:
    """Maps observable score failures to Forge inputs and missingness layers."""

    _TARGETS = {
        "persistence": ("draft", "entities"),
        "causality": ("completion", "events"),
        "epistemic": ("missingness", "uncertainty"),
        "spatial": ("domain", "relations"),
        "consequence": ("completion", "events"),
        "autonomy": ("domain", "entities"),
        "branch_isolation": ("package", "preview branch"),
        "replayability": ("package", "replay"),
        "provenance": ("draft", "source refs"),
        "uncertainty": ("missingness", "uncertainty"),
    }

    def locate(
        self, score: WorldnessScore, value: WorldnessInput, *, threshold: float = 0.6
    ) -> tuple[FailureLocation, ...]:
        refs = value.source_refs
        locations: list[FailureLocation] = []
        for dimension, amount in score.dimensions:
            if amount < threshold:
                layer, target = self._TARGETS[dimension]
                locations.append(
                    FailureLocation(
                        dimension,
                        layer,
                        target,
                        f"score {amount:.3f} is below threshold {threshold:.3f}",
                        refs,
                    )
                )
        return tuple(locations)


@dataclass(frozen=True, slots=True)
class BranchIsolationProof:
    source_fingerprint: str
    branch_ids: tuple[str, ...]
    branch_fingerprints: tuple[tuple[str, str], ...]
    isolated: bool


@dataclass(frozen=True, slots=True)
class DeterminismEnvelope:
    seed: int
    provider_ids: tuple[str, ...]
    nondeterminism: tuple[str, ...]
    trace_hash: str
    replay_equal: bool
    valid: bool


def prove_branch_isolation(value: WorldnessInput, *branch_ids: str) -> BranchIsolationProof:
    """Prove branch observations are namespaced while the source stays fixed."""
    ids = tuple(branch_ids) or ("preview", "repair")
    if any(not item for item in ids) or len(set(ids)) != len(ids):
        raise ValueError("branch ids must be non-empty and unique")
    source_fingerprint = hashlib.sha256(
        json.dumps(asdict(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    branch_fingerprints = tuple(
        (branch, hashlib.sha256(f"{source_fingerprint}:{branch}".encode()).hexdigest())
        for branch in ids
    )
    return BranchIsolationProof(
        source_fingerprint,
        ids,
        branch_fingerprints,
        len({fingerprint for _branch, fingerprint in branch_fingerprints}) == len(ids),
    )


def determinism_envelope(
    value: WorldnessInput,
    first: SimulationTrace,
    second: SimulationTrace,
    *,
    provider_ids: tuple[str, ...] = (),
    nondeterminism: tuple[str, ...] = (),
) -> DeterminismEnvelope:
    """Record replay equality and provider/nondeterminism inputs explicitly."""
    same = first.replay_hash == second.replay_hash and first.steps == second.steps
    return DeterminismEnvelope(
        value.seed,
        tuple(sorted(provider_ids or value.provider_ids)),
        tuple(nondeterminism),
        first.replay_hash,
        same,
        same and not nondeterminism,
    )
