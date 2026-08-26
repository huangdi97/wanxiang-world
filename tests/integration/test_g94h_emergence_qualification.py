"""G94H: positive and false-positive worlds qualify only evidence-bound signals."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.institution_candidate import (
    create_institution_candidate,
    review_institution_candidate,
)
from wanxiang_substrate.evolution.norm_candidate import create_norm_candidate
from wanxiang_substrate.evolution.ontology_candidate import (
    create_ontology_candidate,
    review_ontology_candidate,
)
from wanxiang_substrate.evolution.ontology_law import OntologyLawEvolution
from wanxiang_substrate.evolution.pattern_detector import RepeatedPatternDetector
from wanxiang_substrate.evolution.pattern_detector_model import (
    PatternDetection,
    RepeatedPatternPolicy,
)
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.worldpack.assembler import literary_constitution


def _source(label: str) -> SourceRecord:
    content = (
        f"# G94H {label}\nCharacter: Alice\nCharacter: Bob\nCharacter: Carol\n"
        "The archive group repeats one shared watch practice across its windows.\n"
        "relationship: Alice -> Bob\nrule: repeated practice requires evidence\n"
    )
    return SourceRecord(
        source_id=f"g94h_{label.casefold()}_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://g94h_{label.casefold()}_source",
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
        provenance=f"synthetic:g94h:{label.casefold()}",
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


def _open_world(
    runtime: WorldRuntime,
    playable: PlayableService,
    *,
    label: str,
) -> tuple[WorldInstanceId, BranchId, dict[str, str]]:
    source = _source(label)
    package = (
        OneClickAuthoring().run(f"job_g94h_{label.casefold()}", (source,), profile="book").package
    )
    assert package.evidence_coverage > 0.0
    profile = playable.register_package(
        package,
        owner_id=f"g94h_{label.casefold()}_owner",
        visibility="private",
    )
    character = playable.entry.create_character(
        f"g94h_{label.casefold()}_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id=f"character_g94h_{label.casefold()}",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=f"g94h_{label.casefold()}_owner",
        mode="embodiment",
        session_id=f"session_g94h_{label.casefold()}",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    return instance, branch, _actor_ids(runtime.current_state(instance, branch))


def _qualified_detections(
    store: PatternObservationStore,
) -> tuple[PatternDetection, ...]:
    observations = tuple(
        sorted(
            store.query(kind="behavior", key="entity.update:status"),
            key=lambda item: item.observed_at,
        )
    )
    assert len(observations) >= 9
    detector = RepeatedPatternDetector(
        RepeatedPatternPolicy(
            minimum_occurrences=3,
            minimum_windows=2,
            minimum_support=0.75,
            maximum_counterexample_rate=0.25,
            minimum_confidence=0.8,
        )
    )
    detections: list[PatternDetection] = []
    for offset in (0, 3, 6):
        group = observations[offset : offset + 3]
        detection = next(
            item
            for item in detector.detect(
                store,
                window_start=group[0].observed_at,
                window_end=group[-1].observed_at + 1,
            )
            if item.key == "entity.update:status"
        )
        assert detection.qualified is True
        detections.append(detection)
    return tuple(detections)


@pytest.mark.integration
def test_positive_and_negative_worlds_replay_without_false_promotion(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    positive_instance, positive_branch, positive_actors = _open_world(
        runtime, playable, label="Positive"
    )
    positive_owner = "g94h_positive_owner"
    bob = EntityId(positive_actors["Bob"])
    for index in range(9):
        playable.action(
            positive_instance.value,
            viewer_id=positive_owner,
            action_type="set_status",
            payload={"entity_id": bob.value, "status": f"watch_{index}"},
        )
    positive_before = runtime.current_state(positive_instance, positive_branch)
    positive_events = runtime.events(positive_instance, positive_branch)
    positive_store = PatternObservationStore.rebuild(positive_events, window_size=1)
    detections = _qualified_detections(positive_store)
    norms = tuple(
        create_norm_candidate(
            detection,
            candidate_id=f"norm_g94h_{index}",
            scope="local",
            scope_ref=positive_instance.value,
            now_ticks=detection.window_end,
        )
        for index, detection in enumerate(detections, start=1)
    )
    institution = review_institution_candidate(
        create_institution_candidate(
            norms[0],
            candidate_id="institution_g94h_watch",
            role_refs=("role:watcher",),
            resource_refs=("resource:archive",),
            process_refs=("process:handover",),
        ),
        reviewer="reviewer",
        approved=True,
    )
    ontology = create_ontology_candidate(
        norms,
        candidate_id="ontology_g94h_watch",
        concept="shared:archive-watch",
        evidence_windows=tuple(
            (detection.window_start, detection.window_end) for detection in detections
        ),
        institution_candidates=(institution,),
    )
    reviewed = review_ontology_candidate(ontology, reviewer="policy", approved=True)
    constitution = literary_constitution()
    constitution_hash = constitution.compute_hash()
    assert OntologyLawEvolution.validate_ontology(reviewed, constitution) is True
    assert constitution.compute_hash() == constitution_hash
    assert (
        runtime.current_state(positive_instance, positive_branch).semantic_hash()
        == positive_before.semantic_hash()
    )
    assert runtime.events(positive_instance, positive_branch) == positive_events
    assert (
        runtime.restore_and_replay(positive_instance, positive_branch).state.semantic_hash()
        == positive_before.semantic_hash()
    )

    negative_instance, negative_branch, negative_actors = _open_world(
        runtime, playable, label="Negative"
    )
    negative_owner = "g94h_negative_owner"
    negative_bob = EntityId(negative_actors["Bob"])
    for index in range(3):
        playable.action(
            negative_instance.value,
            viewer_id=negative_owner,
            action_type="set_status",
            payload={"entity_id": negative_bob.value, "status": f"burst_{index}"},
        )
    negative_before = runtime.current_state(negative_instance, negative_branch)
    negative_events = runtime.events(negative_instance, negative_branch)
    negative_store = PatternObservationStore.rebuild(negative_events, window_size=100)
    burst = next(
        item
        for item in RepeatedPatternDetector(
            RepeatedPatternPolicy(minimum_occurrences=3, minimum_windows=2)
        ).detect(negative_store, window_start=0, window_end=100)
        if item.key == "entity.update:status"
    )
    assert burst.qualified is False
    assert burst.observed_window_count == 1
    with pytest.raises(ContractError, match="qualified"):
        create_norm_candidate(
            burst,
            candidate_id="norm_g94h_false_positive",
            scope="local",
            scope_ref=negative_instance.value,
            now_ticks=burst.window_end,
        )
    assert (
        runtime.current_state(negative_instance, negative_branch).semantic_hash()
        == negative_before.semantic_hash()
    )
    assert runtime.events(negative_instance, negative_branch) == negative_events
    assert (
        runtime.restore_and_replay(negative_instance, negative_branch).state.semantic_hash()
        == negative_before.semantic_hash()
    )
