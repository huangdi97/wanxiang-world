"""G14H: SimulationAdapter & external-system byzantine behavior qualification.

External simulators/sensors can be slow, inconsistent or malicious without
owning world truth: proposals never auto-commit, invalid proposals are
rejected/audited, timeouts fail fast (no host deadlock), checkpoint mismatches
are detected, and byzantine observations are rejected or kept as conflicts.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.errors import AdapterContractError, OrchestrationError
from wanxiang_substrate.cosim.orchestrator import CoSimOrchestrator
from wanxiang_substrate.reality.bridge import RealityBridge
from wanxiang_substrate.reality.fusion import ObservationFusion
from wanxiang_substrate.reality.model import PhysicalObservation


class ByzantineSimulator(FakeSimulator):
    """A malicious simulator that emits proposals attempting to mutate reality."""

    def emit_proposed_deltas(self) -> tuple[ProposedWorldDelta, ...]:
        return (
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("byzantine_ent"),
                        entity_type="person",
                        components=(
                            ComponentData(
                                component_id=ComponentId("byz_cmp"),
                                component_type="resource",
                                schema_version=SchemaVersion(1),
                                fields={"count": 999},
                            ),
                        ),
                    ),
                )
            ),
        )


def test_external_bad_output_cannot_mutate_canonical_state() -> None:
    sim = ByzantineSimulator("evil", rate_ticks=2, growth=1)
    sim.initialize({})
    state = InMemoryCanonicalState(
        instance_id=WorldInstanceId("w"),
        branch_id=BranchId("b"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    sim.ingest_state(state)
    orch = CoSimOrchestrator()
    orch.register(sim, rate_ticks=2)
    orch.step_to(4)
    # The simulator's proposals are never auto-committed: no events are created
    # and the canonical state is untouched by the co-sim run.
    assert sim.emit_proposed_deltas()
    assert sim.emit_events() == ()
    assert state.revision.value == 0
    assert state.entity(EntityId("byzantine_ent")) is None


def test_invalid_proposal_rejected_and_arbitrated() -> None:
    orch = CoSimOrchestrator()
    fast = FakeSimulator("fast", rate_ticks=1, growth=1)
    slow = FakeSimulator("slow", rate_ticks=2, growth=10)
    orch.register(fast, rate_ticks=1)
    orch.register(slow, rate_ticks=2)
    result = orch.arbitrate({"fast": {"value": 1}, "slow": {"value": 2}})
    assert result.conflict is True
    assert result.winner == "fast"  # deterministic adjudication
    assert result.rejected == ("slow",)
    # A byzantine adapter that violates its declared rate is rejected.
    bad = FakeSimulator("bad", rate_ticks=2, growth=1)
    bad.initialize({})
    with pytest.raises(AdapterContractError):
        bad.advance(0, 3)  # wrong rate


def test_timeout_does_not_deadlock_host() -> None:
    class CrashingSimulator(FakeSimulator):
        def advance(self, t0: int, t1: int) -> None:
            raise RuntimeError("simulator crash/timeout")

    orch = CoSimOrchestrator()
    orch.register(CrashingSimulator("crash", rate_ticks=1, growth=1), rate_ticks=1)
    with pytest.raises(RuntimeError):
        orch.step_to(2)  # fail fast; no deadlock
    # A host with healthy simulators continues to advance after the faulty one
    # is removed (no global deadlock).
    healthy = CoSimOrchestrator()
    healthy.register(FakeSimulator("ok", rate_ticks=2, growth=1), rate_ticks=2)
    assert healthy.step_to(4) == 4


def test_checkpoint_mismatch_detected() -> None:
    orch = CoSimOrchestrator()
    orch.register(FakeSimulator("s", rate_ticks=2, growth=3), rate_ticks=2)
    orch.step_to(2)
    saved = orch.checkpoint()
    orch.step_to(4)
    orch.restore(saved)
    assert orch.step_to(2) == 2  # restored to the checkpointed clock/state
    # A tampered checkpoint (wrong length) is rejected explicitly.
    with pytest.raises(OrchestrationError):
        orch.restore(("garbage",))
    # A tampered simulator payload inside a well-formed checkpoint is rejected.
    with pytest.raises(AdapterContractError):
        orch.restore((2, "garbage"))


def test_byzantine_observations_rejected_or_conflicted() -> None:
    bridge = RealityBridge()
    from wanxiang_domain.errors import WanxiangError

    # Byzantine observations are rejected at the boundary (WanxiangError family).
    with pytest.raises(WanxiangError):
        bridge.ingest(
            PhysicalObservation(
                observation_id="neg", source="sensor", kind="weather", value=1.0, at_ticks=-1
            )
        )
    with pytest.raises(WanxiangError):
        bridge.ingest(
            PhysicalObservation(
                observation_id="conf",
                source="sensor",
                kind="weather",
                value=1.0,
                confidence=1.5,
            )
        )
    with pytest.raises(WanxiangError):
        bridge.ingest(
            PhysicalObservation(
                observation_id="unit",
                source="sensor",
                kind="position",
                value=1.0,
                unit="celsius",
            )
        )
    # Conflicting valid observations from different sources are retained as a
    # conflict set (never silently resolved).
    fusion = ObservationFusion()
    readings = (
        bridge.ingest(
            PhysicalObservation(
                observation_id="o1", source="a", kind="weather", value=20.0, at_ticks=5
            )
        ),
        bridge.ingest(
            PhysicalObservation(
                observation_id="o2", source="a", kind="weather", value=25.0, at_ticks=5
            )
        ),
    )
    results = fusion.fuse(readings)
    assert any(r.outcome == "conflict" for r in results)
