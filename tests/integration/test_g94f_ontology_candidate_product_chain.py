"""G94F: a real playable history supplies strict cross-window ontology evidence."""

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
from wanxiang_substrate.evolution.norm_candidate_model import NormOutcomeEvidence
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


def _source() -> SourceRecord:
    content = (
        "# G94F Shared Practice\nCharacter: Alice\nCharacter: Bob\nCharacter: Carol\n"
        "The three keep the archive watch and use one shared mark.\n"
        "relationship: Alice -> Bob\nrule: shared duties have consequences\n"
    )
    return SourceRecord(
        source_id="g94f_ontology_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g94f_ontology_source",
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
        provenance="synthetic:g94f",
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
def test_ontology_candidate_uses_real_cross_window_chain_without_constitution_mutation(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g94f_ontology", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g94f_owner", visibility="private")
    character = playable.entry.create_character(
        "g94f_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g94f_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g94f_owner",
        mode="embodiment",
        session_id="session_g94f_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    bob = EntityId(actors["Bob"])
    for index in range(9):
        playable.action(
            instance.value,
            viewer_id="g94f_owner",
            action_type="set_status",
            payload={"entity_id": bob.value, "status": f"watch_{index}"},
        )

    before = runtime.current_state(instance, branch)
    before_events = runtime.events(instance, branch)
    store = PatternObservationStore.rebuild(before_events, window_size=1)
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

    norms = tuple(
        create_norm_candidate(
            detection,
            candidate_id=f"norm_g94f_{index}",
            scope="local",
            scope_ref=instance.value,
            now_ticks=detection.window_end,
            outcome_evidence=(
                NormOutcomeEvidence(detection.event_refs[0], actors["Alice"], "reward"),
            ),
        )
        for index, detection in enumerate(detections, start=1)
    )
    institution = review_institution_candidate(
        create_institution_candidate(
            norms[0],
            candidate_id="institution_g94f_watch",
            role_refs=("role:watcher",),
            resource_refs=("resource:archive",),
            process_refs=("process:handover",),
        ),
        reviewer="reviewer",
        approved=True,
    )
    candidate = create_ontology_candidate(
        norms,
        candidate_id="ontology_g94f_watch",
        concept="shared:archive-watch",
        evidence_windows=tuple(
            (detection.window_start, detection.window_end) for detection in detections
        ),
        institution_candidates=(institution,),
    )
    assert candidate.approved is False
    reviewed = review_ontology_candidate(candidate, reviewer="policy", approved=True)
    constitution = literary_constitution()
    constitution_hash = constitution.compute_hash()
    assert OntologyLawEvolution.validate_ontology(reviewed, constitution) is True
    assert constitution.compute_hash() == constitution_hash
    assert package.manifest.content_hash == package.manifest.compute_hash()
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    assert runtime.events(instance, branch) == before_events
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == before.semantic_hash()
    )
