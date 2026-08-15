"""G33B: Worldline -> Derived World promotion pipeline."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.ids import WorldDefinitionId
from wanxiang_domain.lineage import LineageGraph, LineageNode
from wanxiang_domain.worldline import WorldDefinition
from wanxiang_substrate.evolution.promotion.pipeline import (
    WorldlinePromotionPipeline,
)

PARENT = WorldDefinition(
    definition_id=WorldDefinitionId("wd_rc_parent"),
    version=1,
    name="Red Chamber Parent",
    constitution_ref="con_legacy_v5",
    genesis_ref="genesis://rc-parent",
    package_ref="pack://rc-parent@1.0.0",
).with_hash()


@pytest.mark.unit
def test_promotion_does_not_mutate_parent_definition_or_worldline() -> None:
    pipeline = WorldlinePromotionPipeline()
    parent_before = PARENT.content_hash
    snapshot = pipeline.distill("wl_rc_001", ("norm:curfew", "group:night_watch", "relation:gift"))
    review = pipeline.review(
        snapshot,
        rights_ref="rights:cc0",
        source_refs=("ref://rc-ch30",),
        invariants_ok=True,
        reviewer="reviewer",
    )
    derived = pipeline.assemble(
        PARENT,
        snapshot,
        review,
        derived_name="Red Chamber Derived",
        derived_id=WorldDefinitionId("wd_rc_derived"),
    )
    # Parent untouched; derived definition is a NEW id with its own hash.
    assert PARENT.content_hash == parent_before
    assert derived.definition_id == WorldDefinitionId("wd_rc_derived")
    assert derived.content_hash != PARENT.content_hash
    assert snapshot.content_hash  # genesis snapshot frozen


@pytest.mark.unit
def test_unapproved_promotion_is_rejected() -> None:
    pipeline = WorldlinePromotionPipeline()
    snapshot = pipeline.distill("wl_rc_001", ("fact_a",))
    review = pipeline.review(
        snapshot,
        rights_ref="rights:cc0",
        source_refs=(),
        invariants_ok=False,  # invariant review failed -> not approved
        reviewer="reviewer",
    )
    assert review.approved is False
    with pytest.raises(PermissionDenied):
        pipeline.assemble(
            PARENT,
            snapshot,
            review,
            derived_name="Should Not Exist",
            derived_id=WorldDefinitionId("wd_never"),
        )


@pytest.mark.unit
def test_derived_world_is_reinstantiable() -> None:
    pipeline = WorldlinePromotionPipeline()
    snapshot = pipeline.distill("wl_rc_001", ("norm:curfew",))
    review = pipeline.review(
        snapshot,
        rights_ref="rights:cc0",
        source_refs=("ref://rc",),
        invariants_ok=True,
        reviewer="policy",
    )
    derived = pipeline.assemble(
        PARENT,
        snapshot,
        review,
        derived_name="Red Chamber Derived",
        derived_id=WorldDefinitionId("wd_rc_derived"),
    )
    # The derived World Definition is a complete, versioned birth definition:
    # it carries constitution + genesis refs and can instantiate a new world.
    assert derived.constitution_ref == PARENT.constitution_ref
    assert derived.genesis_ref == snapshot.genesis_ref
    assert derived.version == 1
    prim = derived.to_primitive()
    assert prim["definition_id"] == "wd_rc_derived"
    assert prim["genesis_ref"] == "genesis://wl_rc_001"


@pytest.mark.unit
def test_lineage_edge_recorded_without_touching_parent() -> None:
    pipeline = WorldlinePromotionPipeline()
    graph = LineageGraph()
    graph.add_node(LineageNode(node_id="wd_rc_parent", kind="definition"))
    edge = pipeline.record_lineage(
        graph,
        source_worldline_ref="wl_rc_001",
        parent_definition_id="wd_rc_parent",
        derived_definition_id="wd_rc_derived",
    )
    assert edge.edge_kind == "promotion"
    assert edge.child_node_id == "wd_rc_derived"
    assert graph.ancestors("wd_rc_derived") == ("wd_rc_parent", "wl_rc_001")
    # Parent definition node is unchanged (no history copy).
    assert graph.get_node("wd_rc_parent").definition_ref == ""  # type: ignore[union-attr]
