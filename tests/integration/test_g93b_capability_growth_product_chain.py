"""G93B: capability growth proposal submitted through the real product chain."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.capability import CapabilityQuery, register_capability_resolvers
from wanxiang_substrate.capability.model import AssessmentEvidence, PracticeRecord
from wanxiang_substrate.evolution.capability_growth import (
    CapabilityCandidate,
    create_capability_candidate,
    promote_capability_candidate,
    validate_capability_candidate,
)
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Capability Chain\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "rule: a watchkeeper must observe the gate\n"
    )
    return SourceRecord(
        source_id="g93b_capability_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93b_capability_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g93b",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)
    register_capability_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type != "profile":
                continue
            display_name = component.fields.get("display_name")
            if isinstance(display_name, str):
                found[display_name] = entity.entity_id.value
    return found


def _candidate(actor_id: EntityId, source: SourceRecord) -> CapabilityCandidate:
    provenance = EvolutionProvenance(
        origin_ref="run:g93b",
        source_refs=(source.content_ref,),
        event_refs=("event:g93b:action",),
        producer="runtime_projection",
    )
    practices = tuple(
        PracticeRecord(
            record_id=EntityId(f"practice_g93b_{index}"),
            actor_id=actor_id,
            capability="watchkeeping",
            practice_count=1,
            evidence_ref=f"practice:g93b:{index}",
        )
        for index in range(1, 4)
    )
    assessment = AssessmentEvidence(
        assessment_id=EntityId("assessment_g93b_pass"),
        actor_id=actor_id,
        capability="watchkeeping",
        assessment_type="practical",
        outcome="pass",
        evidence_ref="assessment:g93b:pass",
    )
    return create_capability_candidate(
        candidate_id="candidate_g93b_watchkeeping",
        actor_id=actor_id,
        capability="watchkeeping",
        domain_ref="domain:gate",
        domain_capabilities=("watchkeeping",),
        current_capabilities=(),
        practice_records=practices,
        assessments=(assessment,),
        provenance=provenance,
    )


@pytest.mark.integration
def test_capability_growth_qualifies_and_commits_only_via_existing_runtime(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93b_capability", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(
        package,
        owner_id="g93b_owner",
        visibility="private",
        allowed_actions=("set_status", "capability.apply_delta"),
    )
    character = playable.entry.create_character(
        "g93b_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93b_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93b_owner",
        mode="embodiment",
        session_id="session_g93b_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    record = playable.store.get_instance(instance.value)
    branch = BranchId(record.branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    actor = EntityId(actors["Alice"])
    action = playable.action(
        instance.value,
        viewer_id="g93b_owner",
        action_type="set_status",
        payload={"entity_id": actor.value, "status": "active"},
    )
    candidate = _candidate(actor, source)
    validation = validate_capability_candidate(candidate)
    assert validation.valid is True
    promotion = promote_capability_candidate(candidate, validation)
    before_proposal = runtime.current_state(instance, branch)
    assert CapabilityQuery(before_proposal).capability(actor, "watchkeeping") is None
    committed = playable.action(
        instance.value,
        viewer_id="g93b_owner",
        action_type="capability.apply_delta",
        payload=promotion.action_payload(),
    )
    assert committed.event_id != action.event_id
    skill = CapabilityQuery(runtime.current_state(instance, branch)).capability(
        actor, "watchkeeping"
    )
    assert skill is not None
    assert skill.level == 1
    assert set(promotion.runtime_delta.evidence_refs).issubset(skill.evidence_refs)
    assert runtime.restore_and_replay(instance, branch).state.semantic_hash() == (
        runtime.current_state(instance, branch).semantic_hash()
    )
