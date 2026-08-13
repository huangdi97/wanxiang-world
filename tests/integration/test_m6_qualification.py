"""M6 qualification: reality-coupled context and controlled experiments.

Deterministic fake physical observations (duplicates + conflicts) -> Reality
Bridge -> Fusion -> Opportunity/Challenge -> Director proposal through normal
validation/commit -> multi-seed experiment from a fixed baseline.
"""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.reality.bridge import FakeSensorAdapter, RealityBridge
from wanxiang_substrate.reality.challenge import ChallengeCompiler
from wanxiang_substrate.reality.director import WorldDirector
from wanxiang_substrate.reality.experiment import (
    ExperimentRuntime,
    ExperimentSpec,
)
from wanxiang_substrate.reality.fusion import FusionPolicy, ObservationFusion
from wanxiang_substrate.reality.model import NormalizedReading
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_m6")
TOWN = EntityId("town")


def make_m6_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("m6.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),
        )
    )


def _run_value(seed: int, param: str, value: object) -> float:
    return seed * float(value if isinstance(value, (int, float)) else 0.0)


@pytest.fixture
def m6_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_m6_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_m6_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="m6.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_m6_reality_fusion_challenge_director_experiment(
    m6_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = m6_world

    # 1) Fake physical observations with duplicates + conflicts into the bridge.
    bridge = RealityBridge()
    bridge.register_adapter(
        "supply",
        FakeSensorAdapter("supply_sensor", "count", (5, 5, 5), unit="count", confidence=0.9),
    )
    bridge.register_adapter(
        "temp",
        FakeSensorAdapter("temp_sensor", "weather", (20, 24), unit="celsius", confidence=0.8),
    )
    readings = bridge.poll(at_ticks=1)
    # Observations are data on the bus, never canonical truth.
    assert all(isinstance(r, NormalizedReading) for r in readings)
    assert bridge.readings()

    # 2) Fuse: duplicates -> consistent proposal; conflicts -> conflict set.
    fusion = ObservationFusion(FusionPolicy(confidence_threshold=0.7, conflict_window_ticks=5))
    conflict_inputs = (
        NormalizedReading("c1", "temp_sensor", "weather", 20, "celsius", 1, 0.9),
        NormalizedReading("c2", "temp_sensor", "weather", 24, "celsius", 3, 0.8),
    )
    fused = fusion.fuse(readings + conflict_inputs)
    outcomes = {f.outcome for f in fused}
    assert "proposal" in outcomes
    assert "conflict" in outcomes
    conflict = next(f for f in fused if f.outcome == "conflict")
    assert conflict.value is None  # never averaged blindly
    assert conflict.sources

    # 3) Generate an opportunity/challenge from world conditions.
    compiler = ChallengeCompiler()
    opportunities = compiler.detect({"supply_low": True, "idle": False}, at_ticks=5)
    assert len(opportunities) == 1
    spec = compiler.compile(
        opportunities[0],
        action_type="material.transfer",
        prerequisites=("has_item",),
        safety=("no_harm",),
        rights=("authorized",),
        evidence=("outcome_recorded",),
        end_conditions=("outcome_verified",),
    )
    assert "authorized" in spec.rights_requirements
    assert "outcome_verified" in spec.end_conditions

    # 4) Director proposes an external event under constraints; the proposal
    #    traverses normal validation/commit (becomes a committed event).
    director = WorldDirector(version=2)
    proposal = director.propose_focus("supply_run", at_ticks=6, action_type="create_entity")
    revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(f"cmd_dir_{proposal.proposal_id}"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(revision),
            action_type=proposal.action_type,
            payload={"entity_id": "supply_1", "entity_type": "material.item"},
            world_time=WorldTime(revision + 1),
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(EntityId("supply_1")) is not None
    # Directors never commit directly (no commit method on directors).
    assert not hasattr(director, "commit")

    # 5) Multi-seed experiment from a fixed baseline; results deterministic.
    baseline_hash = state.semantic_hash()
    experiment = ExperimentSpec(
        experiment_id="exp_supply",
        baseline_ref=baseline_hash,
        parameter_variants=(("speed", 2), ("speed", 4)),
        seeds=(1, 2, 3),
    )
    runner = ExperimentRuntime(rule_version=3)
    results = runner.run(experiment, mutate=_run_value)
    assert len(results) == 6
    assert {m.rule_version for m in results} == {3}
    assert {m.seed for m in results} == {1, 2, 3}
    again = runner.run(experiment, mutate=_run_value)
    assert [m.value for m in results] == [m.value for m in again]
    # The baseline (world state) is never mutated by experiment runs.
    assert runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash() == baseline_hash
    finding = runner.finding(
        experiment,
        "faster supply runs win",
        supported=True,
        assumptions=("flat terrain", "no weather"),
    )
    assert finding.validity_envelope
    assert "reproduce" in finding.validity_envelope
    envelope = runner.envelope(experiment)
    assert envelope.seeds == (1, 2, 3)
    assert envelope.rule_versions == (3,)
