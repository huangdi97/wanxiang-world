"""Runtime and candidate helpers for the bounded G101D emergence run."""

from __future__ import annotations

from typing import Any, cast

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.errors import ContractError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution import (
    EvolutionProvenance,
    OntologyLawEvolution,
    PatternObservationStore,
    RepeatedPatternDetector,
    RepeatedPatternPolicy,
    apply_organization_proposal,
    create_institution_candidate,
    create_norm_candidate,
    create_ontology_candidate,
    create_organization_proposal,
    empty_organization,
    evaluate_norm_candidate,
    review_institution_candidate,
    review_ontology_candidate,
    review_organization_proposal,
)
from wanxiang_substrate.evolution.pattern_detector_model import PatternDetection
from wanxiang_substrate.institution.model import Role
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.worldpack.assembler import literary_constitution

from m98_burn_in_support import SOURCE_HASH, SOURCE_REF, actor_ids, source


def open_world(
    runtime: WorldRuntime, playable: PlayableService, label: str
) -> tuple[WorldInstanceId, BranchId, dict[str, str], SourceRecord]:
    authored = OneClickAuthoring().run(f"job_g101d_{label}", (source(),), profile="book")
    owner = f"g101d_{label}_owner"
    profile = playable.register_package(authored.package, owner_id=owner, visibility="private")
    character = playable.entry.create_character(
        owner,
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id=f"ent_g101d_{label}_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=owner,
        mode="embodiment",
        session_id=f"session_g101d_{label}",
        character_id=character.character_id,
    )
    instance_data = cast(dict[str, object], entered["instance"])
    instance = WorldInstanceId(str(instance_data["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    names = actor_ids(runtime.current_state(instance, branch))
    if {"Alice", "Bob", "Carol"} - set(names):
        raise RuntimeError(f"{label} world did not produce the expected actor set")
    return instance, branch, names, source()


def status_events(
    runtime: WorldRuntime,
    playable: PlayableService,
    instance: WorldInstanceId,
    owner: str,
    *,
    count: int,
    prefix: str,
    target: str,
) -> tuple[CommittedEvent, ...]:
    for index in range(count):
        playable.action(
            instance.value,
            viewer_id=owner,
            action_type="set_status",
            payload={"entity_id": target, "status": f"{prefix}_{index}"},
        )
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    return tuple(runtime.events(instance, branch))


def detector() -> RepeatedPatternDetector:
    return RepeatedPatternDetector(
        RepeatedPatternPolicy(
            minimum_occurrences=3,
            minimum_windows=2,
            minimum_support=0.75,
            maximum_counterexample_rate=0.25,
            minimum_confidence=0.8,
        )
    )


def positive_detections(events: tuple[CommittedEvent, ...]) -> tuple[PatternDetection, ...]:
    store = PatternObservationStore.rebuild(events, window_size=1)
    observations = tuple(
        sorted(
            store.query(kind="behavior", key="entity.update:status"),
            key=lambda item: (item.observed_at, item.observation_id),
        )
    )
    if len(observations) < 9:
        raise RuntimeError(f"positive world has only {len(observations)} status observations")
    detections: list[PatternDetection] = []
    for offset in (0, 3, 6):
        group = observations[offset : offset + 3]
        detection = next(
            item
            for item in detector().detect(
                store,
                window_start=group[0].observed_at,
                window_end=group[-1].observed_at + 1,
            )
            if item.key == "entity.update:status"
        )
        if not detection.qualified:
            raise RuntimeError(f"positive detection {offset} did not qualify")
        detections.append(detection)
    return tuple(detections)


def null_control(events: tuple[CommittedEvent, ...]) -> dict[str, Any]:
    store = PatternObservationStore.rebuild(events, window_size=100)
    detection = next(
        item
        for item in detector().detect(store, window_start=0, window_end=100)
        if item.key == "entity.update:status"
    )
    rejected = False
    rejection = ""
    try:
        create_norm_candidate(
            detection,
            candidate_id="norm_g101d_false_positive",
            scope="local",
            scope_ref="control_g101d_no_pattern",
            now_ticks=detection.window_end,
        )
    except ContractError as exc:
        rejected = True
        rejection = str(exc)
    return {
        "window_size": store.window_size,
        "cache_hash": store.cache_hash(),
        "status_observation_count": len(store.query(kind="behavior", key="entity.update:status")),
        "detection": detection.to_dict(),
        "norm_candidate_rejected": rejected,
        "rejection_reason": rejection,
    }


def institution_dict(candidate: Any) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "rule": candidate.rule,
        "evidence_count": len(candidate.evidence),
        "stability_score": candidate.stability_score,
        "approved": candidate.approved,
        "reviewed_by": candidate.reviewed_by,
        "role_refs": list(candidate.role_refs),
        "resource_refs": list(candidate.resource_refs),
        "process_refs": list(candidate.process_refs),
    }


def organization_dict(proposal: Any, projected: Any) -> dict[str, object]:
    return {
        "proposal_id": proposal.proposal_id,
        "provider_ref": proposal.provider_ref,
        "approved": proposal.approved,
        "event_ref": proposal.event.event_ref,
        "before_status": proposal.before.status,
        "after_status": projected.status,
        "projected_membership_count": len(projected.memberships),
        "projection_only": True,
    }


def candidates(
    detections: tuple[PatternDetection, ...],
    actors: dict[str, str],
    source_record: SourceRecord,
) -> dict[str, Any]:
    norms = tuple(
        create_norm_candidate(
            detection,
            candidate_id=f"norm_g101d_watch_{index}",
            scope="local",
            scope_ref="world_g101d_positive",
            population_refs=tuple(sorted(actors.values())),
            now_ticks=detection.window_end,
        )
        for index, detection in enumerate(detections, start=1)
    )
    evaluations = tuple(evaluate_norm_candidate(norm) for norm in norms)
    provenance = EvolutionProvenance(
        origin_ref=f"pattern:{detections[0].detection_id}",
        source_refs=(source_record.content_ref,),
        event_refs=tuple(sorted({ref for item in detections for ref in item.event_refs})),
        producer="g101d_bounded_detector",
    )
    founder = EntityId(actors["Alice"])
    organization_before = empty_organization(EntityId("org_g101d_candidate"))
    founder_role = Role(
        EntityId("role_g101d_founder"),
        "founder",
        ("organization.manage_members",),
    )
    organization_proposal = create_organization_proposal(
        organization_before,
        proposal_id="organization_g101d_watch",
        founder_id=founder,
        founder_role=founder_role,
        membership_id=EntityId("membership_g101d_founder"),
        event_ref=detections[0].event_refs[0],
        at_ticks=detections[0].window_end,
        provenance=provenance,
    )
    reviewed_organization = review_organization_proposal(organization_proposal, reviewer="policy")
    projected_organization = apply_organization_proposal(organization_before, reviewed_organization)
    institution = review_institution_candidate(
        create_institution_candidate(
            norms[0],
            candidate_id="institution_g101d_watch",
            role_refs=("role:watcher",),
            resource_refs=("resource:archive",),
            process_refs=("process:handover",),
        ),
        reviewer="policy",
        approved=True,
    )
    ontology = create_ontology_candidate(
        norms,
        candidate_id="ontology_g101d_watch",
        concept="shared:archive-watch",
        evidence_windows=tuple(
            (detection.window_start, detection.window_end) for detection in detections
        ),
        institution_candidates=(institution,),
    )
    reviewed_ontology = review_ontology_candidate(ontology, reviewer="policy", approved=True)
    ontology_valid = OntologyLawEvolution.validate_ontology(
        reviewed_ontology, literary_constitution()
    )
    return {
        "pattern_detections": [item.to_dict() for item in detections],
        "norm_candidates": [item.to_dict() for item in norms],
        "norm_evaluations": [item.to_dict() for item in evaluations],
        "organization_candidate": organization_dict(reviewed_organization, projected_organization),
        "institution_candidate": institution_dict(institution),
        "ontology_candidate": reviewed_ontology.to_dict(),
        "ontology_validation": ontology_valid,
        "candidate_evidence_hash": semantic_sha256(
            {
                "detections": [item.to_dict() for item in detections],
                "norms": [item.to_dict() for item in norms],
                "institution": institution_dict(institution),
                "ontology": reviewed_ontology.to_dict(),
            }
        ),
        "source_hash": SOURCE_HASH,
        "source_ref": SOURCE_REF,
    }


__all__ = [
    "candidates",
    "detector",
    "institution_dict",
    "null_control",
    "open_world",
    "positive_detections",
    "status_events",
]
