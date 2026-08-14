"""G18D: strategy / experiment workbench completion.

- Same experiment config/seed reproduces a deterministic result.
- Results link to package/runtime versions and branch ancestry.
- Invalid simulator proposals are visible as rejected, not hidden.
"""

from __future__ import annotations

import pytest
from wanxiang_api.strategy_workbench_service import ExperimentDefinition, StrategyWorkbenchService


def _definition(
    experiment_id: str = "exp_1", seed: int = 7, horizon: int = 8
) -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id,
        seed,
        simulators={"fast": {"rate_ticks": 2, "growth": 1}, "slow": {"rate_ticks": 4, "growth": 3}},
        horizon=horizon,
    )


def test_same_config_seed_reproduces_deterministic_result() -> None:
    service = StrategyWorkbenchService()
    a = service.run(_definition("exp_det", seed=42))
    b = service.run(_definition("exp_det", seed=42))
    assert a["result_hash"] == b["result_hash"]
    assert a["config_hash"] == b["config_hash"]
    # A different seed is captured in the config provenance (result reruns are
    # reproducible and traceable to the exact experiment definition).
    c = service.run(_definition("exp_det", seed=43))
    assert a["config_hash"] != c["config_hash"]


def test_result_links_to_versions_and_branch_ancestry() -> None:
    service = StrategyWorkbenchService()
    result = service.run(_definition("exp_prov"), ancestry=("root_branch", "child_branch"))
    assert result["runtime_version"] == 1
    assert result["schema_version"] == 1
    assert result["branch_ancestry"] == ("root_branch", "child_branch")
    assert result["counterfactual"] is True  # never historical fact


def test_invalid_simulator_proposal_visible_as_rejected() -> None:
    service = StrategyWorkbenchService()
    result = service.arbitrate({"sim_a": {"x": 1}, "sim_b": {"x": 2}})
    assert result["conflict"] is True
    assert result["winner"] == "sim_a"
    assert "sim_b" in result["rejected"]
    # A wrong-rate simulator (invalid proposal) is an explicit contract error,
    # never silently hidden.
    from wanxiang_substrate.cosim.adapter import FakeSimulator
    from wanxiang_substrate.cosim.errors import AdapterContractError

    bad = FakeSimulator("bad", rate_ticks=2, growth=1)
    bad.initialize({})
    with pytest.raises(AdapterContractError):
        bad.advance(0, 3)
