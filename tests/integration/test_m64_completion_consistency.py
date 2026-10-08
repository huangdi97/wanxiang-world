"""M64 missingness, completion levels, constraints, and uncertainty tests."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.completion_engine import (
    CompletionEngine,
    ConstraintSet,
    MissingnessNode,
)


@pytest.mark.integration
def test_missingness_graph_and_completion_levels_remain_honest() -> None:
    nodes = (
        MissingnessNode("location", "actor initial location", True, (), "spatial", (), "E3"),
        MissingnessNode("schedule", "schedule coverage", True, (), "schedule", ("location",), "E4"),
        MissingnessNode(
            "ownership",
            "object ownership",
            True,
            ("source_a#1", "source_b#1"),
            "ownership",
            (),
            "E2",
        ),
        MissingnessNode("fiction", "user authored detail", False, (), "experience", (), "E5"),
    )
    result = CompletionEngine().solve(nodes)
    assert result.graph.edges == (("schedule", "location"),)
    classes = {candidate.completion_class for candidate in result.candidates}
    assert classes == {"E1", "E3", "E4", "E5"}
    assert all(candidate.can_enter_canon is False for candidate in result.candidates)
    assert result.uncertainty > 0.0
    assert any(issue.category == "spatial" for issue in result.consistency.issues)
    with pytest.raises(ValueError, match="cannot be silently upgraded"):
        CompletionEngine().reject_e0_upgrade("E3", "E0")


@pytest.mark.integration
def test_consistency_solver_covers_temporal_identity_topology_and_rights() -> None:
    constraints = ConstraintSet(
        temporal=(("late", "1990"), ("early", "1985")),
        identity_keys=("alice", "alice"),
        topology_nodes=("a", "b", "c"),
        topology_edges=(("a", "b"),),
        ownership=(("seal", "alice"), ("seal", "bob")),
        knowledge_edges=(("secret", "alice"),),
        observed_entities=("bob",),
        roles=(("", "keeper"),),
        scenario_required=("initial_time", "activation"),
        scenario_present=("activation",),
        package_dependencies=("family==1",),
        package_lock=("family==2",),
        rights_ok=False,
    )
    report = CompletionEngine().solve((), constraints=constraints).consistency
    categories = {issue.category for issue in report.issues}
    assert categories == {
        "temporal",
        "identity",
        "topology",
        "ownership",
        "knowledge",
        "organization",
        "scenario",
        "package",
        "rights",
    }
    assert report.ok is False


@pytest.mark.unit
def test_completion_reference_is_deterministic() -> None:
    node = MissingnessNode("n", "initial time", True, (), "temporal", (), "E2")
    first = CompletionEngine().solve((node,))
    second = CompletionEngine().solve((node,))
    assert first == second
    assert first.candidates[0].origin_label == "domain_rule"
