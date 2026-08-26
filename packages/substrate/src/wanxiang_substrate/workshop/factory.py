"""Workshop-specific prompt and hybrid draft assembly over the v5.4 compiler."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.pipeline_support import default_domain_registry
from wanxiang_substrate.compile import CompilerBoundary, CompilerInput, PackageAssembler
from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.domains.resolver import DomainDependencyResolver
from wanxiang_substrate.draft.coverage import CoverageAssessor
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.workshop.genesis_contract import PromptGenesisContract
from wanxiang_substrate.workshop.hybrid_genesis import HybridGenesisResult


def prompt_world_draft(
    contract: PromptGenesisContract,
    *,
    draft_id: str,
    provider_id: str,
) -> WorldDraft:
    """Materialize an E5 prompt candidate into the existing editable WorldDraft."""
    actor_values = tuple(
        item.value for item in contract.constraints if item.kind == "actor" and item.value.strip()
    )
    place_values = tuple(
        item.value for item in contract.constraints if item.kind in {"place", "setting"}
    )
    rule_values = tuple(item.value for item in contract.constraints if item.kind == "rule")
    actor_names = actor_values or ("Focal Actor",)
    if len(actor_names) == 1:
        actor_names = (*actor_names, "Local Witness")
    entities = tuple(
        (f"prompt:actor:{index}", value) for index, value in enumerate(actor_names, start=1)
    )
    places = tuple(dict.fromkeys(place_values or ("Prompt Space",)))
    primary_actor = entities[0][0]
    secondary_actor = entities[1][0]
    registry = default_domain_registry()
    selected = ("family", "narrative", "spatial")
    resolution = DomainDependencyResolver().resolve(registry, selected)
    if not resolution.ok:
        raise ContractError("prompt domain composition is not resolvable")
    draft = WorldDraft(
        draft_id=draft_id,
        revision=1,
        status="READY_TO_COMPILE",
        source_refs=(f"prompt:{contract.intent.intent_id}",),
        source_versions=((f"prompt:{contract.intent.intent_id}", "1"),),
        constitution_ref="constitution:v1",
        selected_domains=resolution.order,
        dependency_lock=resolution.order,
        entities=entities,
        relations=((primary_actor, secondary_actor, "prompt-association"),),
        places=places,
        events=(("prompt_genesis", "unknown"),),
        rules=rule_values,
        scenario_candidates=(f"scenario:{contract.intent.intent_id}",),
        genesis_candidates=contract.generated_fact_ids,
        compiler_metadata={
            "pipeline": "workshop-prompt",
            "creation_mode": "prompt",
            "evidence_class": "E5",
            "intent_id": contract.intent.intent_id,
            "provider_id": provider_id,
        },
    )
    return _with_coverage(draft, registry)


def hybrid_world_draft(
    source_draft: WorldDraft,
    hybrid: HybridGenesisResult,
    *,
    draft_id: str,
) -> WorldDraft:
    """Pin hybrid provenance onto the source draft without replacing source fields."""
    if hybrid.conflicts:
        conflicts = tuple(sorted({f"hybrid:{item.key}" for item in hybrid.conflicts}))
    else:
        conflicts = ()
    metadata = dict(source_draft.compiler_metadata)
    metadata.update(
        {
            "creation_mode": "hybrid",
            "hybrid_fingerprint": hybrid.fingerprint,
            "hybrid_precedence": hybrid.policy.precedence,
            "prompt_evidence_class": "E5",
        }
    )
    return replace(
        source_draft,
        draft_id=draft_id,
        revision=source_draft.revision + 1,
        status="READY_TO_COMPILE" if not conflicts else "COMPLETION_REQUIRED",
        unresolved_conflicts=tuple(sorted(set(source_draft.unresolved_conflicts + conflicts))),
        genesis_candidates=tuple(
            sorted(
                set(
                    source_draft.genesis_candidates + tuple(item.claim_id for item in hybrid.claims)
                )
            )
        ),
        compiler_metadata=metadata,
    )


def compile_preview_draft(draft: WorldDraft):
    """Compile a workshop draft through the existing compiler/package boundary."""
    registry = default_domain_registry()
    domain_versions = tuple(
        (domain_id, registry.require(domain_id).version) for domain_id in draft.selected_domains
    )
    outcome = CompilerBoundary().check(
        CompilerInput(
            draft=draft,
            draft_revision=draft.revision,
            source_versions=draft.source_versions,
            domain_versions=domain_versions,
        )
    )
    if not outcome.ok:
        raise ContractError("workshop draft is not compilable: " + "; ".join(outcome.reasons))
    coverage = CoverageAssessor().assess(draft, registry)
    return PackageAssembler().assemble(
        draft,
        compile_outcome=outcome,
        domain_versions=domain_versions,
        evidence_coverage=coverage.coverage,
        for_preview=True,
    )


def _with_coverage(draft: WorldDraft, registry: DomainRegistry) -> WorldDraft:
    coverage = CoverageAssessor().assess(draft, registry)
    completion = CoverageAssessor().completion_items(draft, registry)
    if coverage.coverage <= 0.0 or completion:
        raise ContractError(
            "prompt draft has incomplete measured coverage: "
            + ",".join(completion or coverage.unknown)
        )
    return replace(
        draft,
        coverage=coverage.coverage,
        quality=max(0.0, coverage.coverage - 0.1),
        completion_items=completion,
    )


__all__ = ["compile_preview_draft", "hybrid_world_draft", "prompt_world_draft"]
