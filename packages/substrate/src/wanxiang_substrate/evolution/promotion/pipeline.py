"""Worldline -> Derived World promotion pipeline (G33B).

A mature worldline can be safely frozen/distilled into a NEW World Definition
(derived world) without mutating the parent definition or source worldline:

  long-horizon distill -> Source/Rights/Invariant review -> freeze Genesis
  snapshot -> Package Assembler compiles a new WorldDefinition (new id) ->
  approval -> lineage edge recorded.

The derived definition is re-instantiable and the parent is never touched.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.ids import WorldDefinitionId
from wanxiang_domain.lineage import LineageEdge, LineageGraph
from wanxiang_domain.worldline import WorldDefinition


@dataclass(frozen=True, slots=True)
class GenesisSnapshot:
    """A frozen genesis snapshot of the distilled content."""

    genesis_ref: str
    distilled_facts: tuple[str, ...]
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.genesis_ref:
            raise ValueError("genesis snapshot requires a ref")

    def with_hash(self) -> GenesisSnapshot:
        payload = json.dumps(
            {"genesis_ref": self.genesis_ref, "facts": sorted(self.distilled_facts)},
            sort_keys=True,
        )
        return GenesisSnapshot(
            genesis_ref=self.genesis_ref,
            distilled_facts=self.distilled_facts,
            content_hash=hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        )


@dataclass(frozen=True, slots=True)
class PromotionReview:
    """Source/Rights/Invariant review of a promotion candidate."""

    rights_ref: str
    source_refs: tuple[str, ...]
    invariants_ok: bool
    approved_by: str | None = None

    @property
    def approved(self) -> bool:
        return self.invariants_ok and self.approved_by is not None


class WorldlinePromotionPipeline:
    """distill -> review -> freeze -> assemble -> record lineage."""

    def distill(self, worldline_ref: str, facts: tuple[str, ...]) -> GenesisSnapshot:
        """Long-horizon distill: freeze a bounded distilled summary."""
        if not facts:
            raise ValueError("cannot distill an empty worldline")
        return GenesisSnapshot(
            genesis_ref=f"genesis://{worldline_ref}",
            distilled_facts=facts,
        ).with_hash()

    def review(
        self,
        snapshot: GenesisSnapshot,
        *,
        rights_ref: str,
        source_refs: tuple[str, ...],
        invariants_ok: bool,
        reviewer: str,
    ) -> PromotionReview:
        """Source/Rights/Invariant review with an approval hook."""
        if reviewer not in ("reviewer", "policy"):
            raise PermissionDenied(
                f"reviewer {reviewer!r} is not authorized; expected reviewer/policy"
            )
        if not snapshot.content_hash:
            raise PermissionDenied("genesis snapshot must be frozen before review")
        return PromotionReview(
            rights_ref=rights_ref,
            source_refs=source_refs,
            invariants_ok=invariants_ok,
            approved_by=reviewer if invariants_ok else None,
        )

    def assemble(
        self,
        parent: WorldDefinition,
        snapshot: GenesisSnapshot,
        review: PromotionReview,
        *,
        derived_name: str,
        derived_id: WorldDefinitionId,
    ) -> WorldDefinition:
        """Package Assembler compiles a new World Definition (new id)."""
        if not review.approved:
            raise PermissionDenied("promotion candidate is not approved; no new definition created")
        return WorldDefinition(
            definition_id=derived_id,
            version=1,
            name=derived_name,
            constitution_ref=parent.constitution_ref,
            genesis_ref=snapshot.genesis_ref,
            package_ref=f"pack://{derived_id.value}@1.0.0",
        ).with_hash()

    def record_lineage(
        self,
        graph: LineageGraph,
        *,
        source_worldline_ref: str,
        parent_definition_id: str,
        derived_definition_id: str,
    ) -> LineageEdge:
        """Record the promotion lineage edge (parent never modified)."""
        for node_id, kind in (
            (source_worldline_ref, "worldline"),
            (parent_definition_id, "definition"),
            (derived_definition_id, "derived_world"),
        ):
            if graph.get_node(node_id) is None:
                from wanxiang_domain.lineage import LineageNode

                graph.add_node(LineageNode(node_id=node_id, kind=kind))  # type: ignore[arg-type]
        # The worldline derives from the parent definition (fork), and the
        # derived world is promoted from the worldline (promotion).
        graph.add_edge(
            LineageEdge(
                parent_node_id=parent_definition_id,
                child_node_id=source_worldline_ref,
                edge_kind="fork",
                origin_ref=f"worldline://{source_worldline_ref}",
            )
        )
        edge = LineageEdge(
            parent_node_id=source_worldline_ref,
            child_node_id=derived_definition_id,
            edge_kind="promotion",
            origin_ref=f"promotion://{derived_definition_id}",
        )
        graph.add_edge(edge)
        return edge
