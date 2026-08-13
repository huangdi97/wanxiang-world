"""G11A-G11D: SimulationAdapter contract, orchestrator, campaign domain."""

from __future__ import annotations

import pytest
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.campaign import CampaignDomain, Order, Region, Unit
from wanxiang_substrate.cosim.errors import AdapterContractError, OrchestrationError
from wanxiang_substrate.cosim.orchestrator import CoSimOrchestrator


@pytest.mark.unit
def test_adapter_contract_lifecycle_and_checkpoint() -> None:
    sim = FakeSimulator("supply", rate_ticks=2, growth=3)
    sim.initialize({})
    sim.ingest_state(
        InMemoryCanonicalState(
            instance_id=WorldInstanceId("w"),
            branch_id=BranchId("b"),
            revision=BranchRevision(0),
            schema_version=SchemaVersion(1),
            rule_version=RuntimeVersion(1),
        )
    )
    sim.advance(0, 2)
    assert sim.checkpoint().value == 3
    sim.advance(2, 4)
    assert sim.checkpoint().value == 6
    saved = sim.checkpoint()
    sim.advance(4, 6)
    sim.restore(saved)
    assert sim.checkpoint().value == 6
    assert sim.describe_assumptions() == ("flat terrain", "no weather")
    assert "deterministic" in sim.describe_validity_envelope()
    with pytest.raises(AdapterContractError):
        sim.advance(0, 3)  # wrong rate


@pytest.mark.unit
def test_adapter_never_commits() -> None:
    sim = FakeSimulator("supply", rate_ticks=1)
    sim.initialize({})
    sim.advance(0, 5)
    assert sim.emit_events() == ()
    assert sim.emit_proposed_deltas() == ()


@pytest.mark.unit
def test_multi_rate_orchestrator_deterministic_and_restartable() -> None:
    orch = CoSimOrchestrator()
    fast = FakeSimulator("fast", rate_ticks=1, growth=1)
    slow = FakeSimulator("slow", rate_ticks=2, growth=10)
    orch.register(fast, rate_ticks=1)
    orch.register(slow, rate_ticks=2)
    # Advance through several synchronization barriers.
    for _ in range(4):
        orch.advance_one_barrier()
    fast_state = fast.checkpoint().value
    slow_state = slow.checkpoint().value
    assert fast_state == 4
    assert slow_state == 20
    # Restartable: checkpoint and restore reproduce the same state.
    saved = orch.checkpoint()
    orch.step_to(10)
    orch.restore(saved)
    assert fast.checkpoint().value == fast_state
    assert slow.checkpoint().value == slow_state


@pytest.mark.unit
def test_conflicting_proposals_adjudicated_explicitly() -> None:
    orch = CoSimOrchestrator()
    result = orch.arbitrate({"b_sim": {"x": 1}, "a_sim": {"x": 2}})
    assert result.conflict is True
    assert result.winner == "a_sim"
    assert result.rejected == ("b_sim",)
    single = orch.arbitrate({"a_sim": {"x": 1}})
    assert single.conflict is False
    assert single.winner == "a_sim"


@pytest.mark.unit
def test_campaign_logistics_movement_and_fog_of_war() -> None:
    campaign = CampaignDomain()
    campaign.add_region(Region("north", routes=("south",), capacity=100))
    campaign.add_region(Region("south", routes=("north",), capacity=100))
    campaign.add_region(Region("east", routes=(), capacity=100))
    campaign.add_unit(Unit("u1", "blue", "north", strength=10, supply=5))
    campaign.add_unit(Unit("u2", "red", "east", strength=8, supply=2))
    # Blue does not know the red-held east region yet (fog-of-war).
    assert campaign.knows("blue", "east") is False
    campaign.issue_order(Order("o1", "u1", "south", issued_at=0, delay_ticks=2))
    campaign.advance_to(1)
    assert campaign.location("u1") == "north"  # not yet arrived
    campaign.advance_to(2)
    assert campaign.location("u1") == "south"
    # Movement to an unreachable region fails silently (no route).
    campaign.issue_order(Order("o2", "u1", "east", issued_at=2, delay_ticks=1))
    campaign.advance_to(3)
    assert campaign.location("u1") == "south"
    # Supply flow.
    campaign.deliver_supply("u1", 10)
    assert campaign.supply_level("u1") == 15
    with pytest.raises(OrchestrationError):
        campaign.issue_order(Order("o3", "ghost", "south", issued_at=0, delay_ticks=1))
