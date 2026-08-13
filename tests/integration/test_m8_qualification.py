"""M8 qualification: mechanistic external models participate without owning
canonical state.

Synthetic campaign with two fake simulators at different rates, organization
orders, logistics/resource flow, movement constraints and fog-of-war; then
batch experiments across seeds/variants with distributions and ValidityEnvelope.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.campaign import CampaignDomain, Order, Region, Unit
from wanxiang_substrate.cosim.orchestrator import CoSimOrchestrator
from wanxiang_substrate.reality.experiment import ExperimentRuntime, ExperimentSpec
from wanxiang_substrate.recovery.budget import ResourceBudget


def _run_value(seed: int, param: str, value: object) -> float:
    return seed * float(value if isinstance(value, (int, float)) else 0.0)


@pytest.mark.integration
def test_m8_campaign_cosim_and_batch_experiment() -> None:
    # 1) Two deterministic fake simulators at different rates.
    orch = CoSimOrchestrator()
    supply = FakeSimulator("supply", rate_ticks=2, growth=2)
    weather = FakeSimulator("weather", rate_ticks=5, growth=1)
    orch.register(supply, rate_ticks=2)
    orch.register(weather, rate_ticks=5)
    for _ in range(10):
        orch.advance_one_barrier()
    assert supply.checkpoint().value == 20  # 10 steps at rate 2 over 20 ticks
    assert weather.checkpoint().value == 4  # 4 steps at rate 5 over 20 ticks

    # 2) Adapters only emit events/proposed deltas; never commit.
    assert supply.emit_events() == ()
    assert supply.emit_proposed_deltas() == ()

    # 3) Conflicting simulator proposals are adjudicated explicitly.
    result = orch.arbitrate({"weather": {"x": 1}, "supply": {"x": 2}})
    assert result.conflict is True
    assert result.winner == "supply"

    # 4) Campaign: organization orders, logistics, movement, fog-of-war.
    campaign = CampaignDomain()
    campaign.add_region(Region("north", routes=("south",), capacity=100))
    campaign.add_region(Region("south", routes=("north",), capacity=100))
    campaign.add_region(Region("east", routes=(), capacity=100))
    campaign.add_unit(Unit("u_blue", "blue", "north", strength=10, supply=5))
    campaign.add_unit(Unit("u_red", "red", "east", strength=8, supply=2))
    assert campaign.knows("blue", "east") is False  # fog-of-war
    campaign.issue_order(Order("o_move", "u_blue", "south", issued_at=0, delay_ticks=3))
    campaign.advance_to(3)
    assert campaign.location("u_blue") == "south"
    campaign.deliver_supply("u_blue", 10)
    assert campaign.supply_level("u_blue") == 15
    campaign.issue_order(Order("o_blocked", "u_blue", "east", issued_at=3, delay_ticks=1))
    campaign.advance_to(4)
    assert campaign.location("u_blue") == "south"  # no route; deviation

    # 5) Batch experiments across seeds/variants: distributions + envelope.
    spec = ExperimentSpec(
        experiment_id="exp_campaign",
        baseline_ref="snap://campaign_v1",
        parameter_variants=(("supply", 2), ("supply", 4)),
        seeds=(1, 2, 3),
    )
    runner = ExperimentRuntime(budget=ResourceBudget(max_commands=100), rule_version=4)
    results = runner.run(spec, mutate=_run_value)
    assert len(results) == 6
    assert {m.rule_version for m in results} == {4}
    again = runner.run(spec, mutate=_run_value)
    assert [m.value for m in results] == [m.value for m in again]
    finding = runner.finding(
        spec,
        "more supply wins",
        supported=True,
        assumptions=("no weather", "flat terrain"),
    )
    assert "reproduce" in finding.validity_envelope
    assert finding.assumptions == ("no weather", "flat terrain")
    assert len(runner.distribution(spec, "supply")) == 6
