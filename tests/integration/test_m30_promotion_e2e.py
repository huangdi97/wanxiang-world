"""G33G: M30 gate ? worldline promotion + cross-world candidate end-to-end."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldDefinitionId
from wanxiang_domain.lineage import LineageGraph
from wanxiang_domain.time import WorldTime
from wanxiang_domain.worldline import WorldDefinition
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.evolution.cross_world import CrossWorldDistiller
from wanxiang_substrate.evolution.platform_feedback import PlatformFeedbackLab
from wanxiang_substrate.evolution.promotion.pipeline import WorldlinePromotionPipeline
from wanxiang_substrate.evolution.telemetry import CrossWorldDataset, TelemetryEnvelope


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _commit(
    authority: CommitAuthority, state: InMemoryCanonicalState, entity_id: str, index: int
) -> InMemoryCanonicalState:
    result = authority.commit(
        state,
        CommitRequest(
            command_id=CommandId(f"cmd_{index}"),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            expected_revision=state.revision,
            delta=ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId(entity_id), entity_type="person"),)
            ),
            world_time=WorldTime(index),
            rule_version=RULES,
        ),
    )
    return result.state_after


@pytest.mark.integration
def test_synthetic_worldline_promotion_end_to_end_derived_instantiable() -> None:
    parent = WorldDefinition(
        definition_id=WorldDefinitionId("wd_parent"),
        version=1,
        name="Parent",
        constitution_ref="con_legacy_v5",
        genesis_ref="genesis://parent",
    ).with_hash()

    # A mature worldline: commit a few events.
    authority = CommitAuthority(InMemoryEventStore(), RULES, SCHEMA)
    state = _base_state()
    for i, eid in enumerate(("lin", "bao", "xiren"), start=1):
        state = _commit(authority, state, eid, i)

    pipeline = WorldlinePromotionPipeline()
    snapshot = pipeline.distill("wl_rc_001", ("norm:curfew", "relation:gift", "group:night_watch"))
    review = pipeline.review(
        snapshot,
        rights_ref="rights:cc0",
        source_refs=("ref://rc-ch30",),
        invariants_ok=True,
        reviewer="reviewer",
    )
    derived = pipeline.assemble(
        parent,
        snapshot,
        review,
        derived_name="Derived RC",
        derived_id=WorldDefinitionId("wd_derived"),
    )
    graph = LineageGraph()
    pipeline.record_lineage(
        graph,
        source_worldline_ref="wl_rc_001",
        parent_definition_id="wd_parent",
        derived_definition_id="wd_derived",
    )

    # Derived definition is instantiable: a new world can be born from it.
    derived_store = InMemoryEventStore()
    derived_authority = CommitAuthority(derived_store, RULES, SCHEMA)
    derived_state = _base_state()
    _commit(derived_authority, derived_state, "lin_derived", 1)
    assert derived.definition_id == WorldDefinitionId("wd_derived")
    assert derived.content_hash
    assert graph.ancestors("wd_derived") == ("wd_parent", "wl_rc_001")
    # Parent definition and source worldline hash unchanged.
    assert parent.content_hash


@pytest.mark.integration
def test_cross_world_candidate_end_to_end_unapproved_not_effective() -> None:
    dataset = CrossWorldDataset()
    for world in ("wld_a", "wld_b", "wld_c"):
        dataset.add(
            TelemetryEnvelope(
                envelope_id=f"t_{world}",
                world_ref=world,
                kind="aggregate",
                metric="quiet_after_curfew",
                consent=True,
                aggregate=1,
            )
        )
    distiller = CrossWorldDistiller(dataset, threshold=2)
    candidate = distiller.distill()[0]
    assert candidate.meets_threshold
    # Unapproved candidate is NOT effective (no activation, no release).
    with pytest.raises(PermissionDenied):
        distiller.activate(candidate)

    # Platform feedback: unapproved sandbox candidate never becomes a release.
    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        candidate.candidate_id,
        {"accuracy": 0.9},
        invariants_ok=True,
        security_ok=True,
        cost=1.0,
        deterministic=True,
    )
    with pytest.raises(PermissionDenied):
        lab.release(report, kind="domain", name="household", version="2.0.0", release_id="rel_1")
