"""RC-001 long-horizon evolution + promotion candidate (G37C).

Controlled time-acceleration, stable-structure distillation, promotion-candidate
generation and Derived World Definition creation ONLY when the policy gate is
reached. Reuses G33B WorldlinePromotionPipeline + G33A validate_promotion.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.ids import WorldDefinitionId
from wanxiang_domain.lineage import LineageGraph
from wanxiang_domain.worldline import WorldDefinition

from wanxiang_substrate.evolution.promotion.ladder import (
    PromotionEvidence,
    validate_promotion,
)
from wanxiang_substrate.evolution.promotion.pipeline import (
    GenesisSnapshot,
    WorldlinePromotionPipeline,
)


def accelerate(horizon_ticks: int, *, ticks_per_step: int = 10) -> int:
    """Controlled time-acceleration: number of bounded steps to the horizon."""
    if horizon_ticks < 0 or ticks_per_step <= 0:
        raise ValueError("horizon_ticks >= 0 and ticks_per_step > 0")
    return (horizon_ticks + ticks_per_step - 1) // ticks_per_step


def distill_stable(
    pipeline: WorldlinePromotionPipeline, worldline_ref: str, facts: tuple[str, ...]
) -> GenesisSnapshot:
    """Distill stable relationship/habit/institution/world structure."""
    return pipeline.distill(worldline_ref, facts)


@dataclass(frozen=True, slots=True)
class LongHorizonPromotion:
    """Result of a long-horizon promotion attempt."""

    worldline_ref: str
    snapshot: GenesisSnapshot
    evidence: PromotionEvidence
    gate_reached: bool
    derived: WorldDefinition | None = None
    lineage_edge_recorded: bool = False


def promote_long_horizon(
    pipeline: WorldlinePromotionPipeline,
    *,
    worldline_ref: str,
    facts: tuple[str, ...],
    stability: float,
    evidence_count: int,
    cross_scenario: bool,
    approved: bool,
    gate_stability: float,
    graph: LineageGraph | None = None,
    derived_id: WorldDefinitionId | None = None,
    parent_definition_id: str = "wd_rc001",
) -> LongHorizonPromotion:
    """Promote a distilled worldline ONLY when the policy gate is reached."""
    snapshot = distill_stable(pipeline, worldline_ref, facts)
    evidence = PromotionEvidence(
        current_level="L2",
        target_level="L3",
        evidence_count=evidence_count,
        stability=stability,
        cross_scenario=cross_scenario,
        approved=approved,
    )
    validate_promotion(evidence)  # one-step, no skipping; raises if insufficient
    gate_reached = stability >= gate_stability
    derived: WorldDefinition | None = None
    edge_recorded = False
    if gate_reached:
        review = pipeline.review(
            snapshot,
            rights_ref="worldpack:literary-historical",
            source_refs=("loc://rc001",),
            invariants_ok=True,
            reviewer="policy",
        )
        derived = pipeline.assemble(
            pipeline_placeholder_parent(),
            snapshot,
            review,
            derived_name=f"Derived RC-001 @ {worldline_ref}",
            derived_id=derived_id or WorldDefinitionId(f"wd_derived_{worldline_ref}"),
        )
        if graph is not None:
            pipeline.record_lineage(
                graph,
                source_worldline_ref=worldline_ref,
                parent_definition_id=parent_definition_id,
                derived_definition_id=derived.definition_id.value,
            )
            edge_recorded = True
    return LongHorizonPromotion(
        worldline_ref=worldline_ref,
        snapshot=snapshot,
        evidence=evidence,
        gate_reached=gate_reached,
        derived=derived,
        lineage_edge_recorded=edge_recorded,
    )


def pipeline_placeholder_parent():
    """Minimal parent WorldDefinition for assemble (synthetic mechanism)."""
    from wanxiang_domain.ids import WorldDefinitionId

    return WorldDefinition(
        definition_id=WorldDefinitionId("wd_rc001"),
        version=1,
        name="RC-001 Synthetic",
        constitution_ref="con_literary_historical",
        genesis_ref="gen_rc001",
    ).with_hash()
