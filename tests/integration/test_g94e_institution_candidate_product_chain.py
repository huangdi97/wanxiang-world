"""G94E: an institution candidate is structured from real norm evidence."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.institution_candidate import (
    create_institution_candidate,
    review_institution_candidate,
)
from wanxiang_substrate.evolution.norm_candidate import create_norm_candidate
from wanxiang_substrate.evolution.pattern_detector import RepeatedPatternDetector
from wanxiang_substrate.evolution.pattern_detector_model import RepeatedPatternPolicy
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# G94E Institution Town\nCharacter: Alice\nCharacter: Bob\n"
        "Alice keeps watch at the gate. Bob carries the letter.\n"
        "relationship: Alice -> Bob\nrule: stable roles and processes need review\n"
    )
    return SourceRecord(
        source_id="g94e_institution_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g94e_institution_source",
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
        provenance="synthetic:g94e",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                value = component.fields.get("display_name")
                if isinstance(value, str):
                    found[value] = entity.entity_id.value
    return found


@pytest.mark.integration
def test_institution_candidate_review_does_not_auto_commit(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g94e_institution", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g94e_owner", visibility="private")
    character = playable.entry.create_character(
        "g94e_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g94e_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g94e_owner",
        mode="embodiment",
        session_id="session_g94e_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    bob = EntityId(actors["Bob"])
    for _ in range(3):
        playable.action(
            instance.value,
            viewer_id="g94e_owner",
            action_type="set_status",
            payload={"entity_id": bob.value, "status": "on_duty"},
        )
    before = runtime.current_state(instance, branch)
    events = runtime.events(instance, branch)
    observation_store = PatternObservationStore.rebuild(events, window_size=1)
    first_tick = events[-3].world_time.ticks
    last_tick = events[-1].world_time.ticks
    detection = next(
        item
        for item in RepeatedPatternDetector(
            RepeatedPatternPolicy(
                minimum_occurrences=3,
                minimum_windows=2,
                minimum_support=0.75,
                maximum_counterexample_rate=0.25,
                minimum_confidence=0.8,
            )
        ).detect(observation_store, window_start=first_tick, window_end=last_tick + 1)
        if item.key == "entity.update:status"
    )
    norm = create_norm_candidate(
        detection,
        candidate_id="norm_g94e_duty",
        scope="local",
        scope_ref=instance.value,
        now_ticks=detection.window_end,
    )
    institution = create_institution_candidate(
        norm,
        candidate_id="institution_g94e_duty",
        role_refs=("role:watcher",),
        resource_refs=("resource:ledger",),
        process_refs=("process:gate-duty",),
    )
    reviewed = review_institution_candidate(institution, reviewer="policy", approved=True)
    assert reviewed.approved is True
    assert reviewed.reviewed_by == "policy"
    assert runtime.current_state(instance, branch).revision == before.revision
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == before.semantic_hash()
    )
