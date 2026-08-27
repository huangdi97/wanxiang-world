"""Independent v5.5 Gate 32 source/canon immutability qualification."""

from __future__ import annotations

import json
import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.constitution import ConstitutionManifest
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
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

CONTENT = (
    "# Gate 32 Qualification\nCharacter: Alice\nCharacter: Bob\n"
    "Alice and Bob keep a shared archive watch.\n"
    "relationship: Alice -> Bob\nrule: reviewed evidence stays proposal-only\n"
)


def _source() -> SourceRecord:
    return SourceRecord(
        source_id="v55_gate32_source",
        kind="text",
        content_hash=payload_hash(CONTENT),
        content_ref="memory://v55_gate32_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=CONTENT,
        provenance="synthetic:v55_gate32",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type != "profile":
                continue
            name = component.fields.get("display_name")
            if isinstance(name, str):
                found[name] = entity.entity_id.value
    return found


def _detections(store: PatternObservationStore) -> tuple[PatternDetection, ...]:
    observations = tuple(
        sorted(
            store.query(kind="behavior", key="entity.update:status"),
            key=lambda item: item.observed_at,
        )
    )
    assert len(observations) == 9
    detector = RepeatedPatternDetector(
        RepeatedPatternPolicy(
            minimum_occurrences=3,
            minimum_windows=2,
            minimum_support=0.75,
            maximum_counterexample_rate=0.25,
            minimum_confidence=0.8,
        )
    )
    result: list[PatternDetection] = []
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
        result.append(detection)
    return tuple(result)


def _write_artifact(data: dict[str, object]) -> None:
    path = pathlib.Path("artifacts/v55/source_canon_immutability.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@pytest.mark.integration
def test_source_and_canon_remain_unchanged_through_derived_qualification(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    source_payload = source.payload
    source_hash = source.content_hash
    package = OneClickAuthoring().run("job_v55_gate32", (source,), profile="book").package
    package_id = package.package_id
    package_hash = package.manifest.content_hash
    assert package.evidence_coverage > 0.0
    assert package_hash == package.manifest.compute_hash()

    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="v55_gate32_owner", visibility="private")
    character = playable.entry.create_character(
        "v55_gate32_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_v55_gate32_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="v55_gate32_owner",
        mode="embodiment",
        session_id="session_v55_gate32_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    bob = EntityId(actors["Bob"])

    for index in range(9):
        playable.action(
            instance.value,
            viewer_id="v55_gate32_owner",
            action_type="set_status",
            payload={"entity_id": bob.value, "status": f"watch_{index}"},
        )

    before = runtime.current_state(instance, branch)
    before_events = runtime.events(instance, branch)
    before_event_ids = tuple(item.event_id.value for item in before_events)
    observations = PatternObservationStore.rebuild(before_events, window_size=1)
    detections = _detections(observations)
    norms = tuple(
        create_norm_candidate(
            detection,
            candidate_id=f"v55_gate32_norm_{index}",
            scope="local",
            scope_ref=instance.value,
            now_ticks=detection.window_end,
        )
        for index, detection in enumerate(detections, start=1)
    )
    institution = review_institution_candidate(
        create_institution_candidate(
            norms[0],
            candidate_id="v55_gate32_institution",
            role_refs=("role:watcher",),
            resource_refs=("resource:archive",),
            process_refs=("process:handover",),
        ),
        reviewer="reviewer",
        approved=True,
    )
    ontology = review_ontology_candidate(
        create_ontology_candidate(
            norms,
            candidate_id="v55_gate32_ontology",
            concept="shared:archive-watch",
            evidence_windows=tuple(
                (detection.window_start, detection.window_end) for detection in detections
            ),
            institution_candidates=(institution,),
        ),
        reviewer="policy",
        approved=True,
    )
    constitution: ConstitutionManifest = literary_constitution()
    constitution_hash = constitution.compute_hash()
    assert OntologyLawEvolution.validate_ontology(ontology, constitution) is True

    after_derivation = runtime.current_state(instance, branch)
    after_derivation_events = runtime.events(instance, branch)
    assert source.payload == source_payload
    assert source.content_hash == source_hash
    assert package.package_id == package_id
    assert package.manifest.content_hash == package_hash
    assert constitution.compute_hash() == constitution_hash
    assert after_derivation.semantic_hash() == before.semantic_hash()
    assert after_derivation_events == before_events
    assert tuple(item.event_id.value for item in after_derivation_events) == before_event_ids
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == before.semantic_hash()
    )

    child = runtime.create_branch(instance, branch).branch_id
    child_before = runtime.current_state(instance, child)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("v55_gate32_child_probe"),
            instance_id=instance,
            branch_id=child,
            expected_revision=child_before.revision,
            action_type="set_status",
            payload={"entity_id": bob.value, "status": "branch_only"},
            world_time=WorldTime(child_before.revision.value + 1),
        )
    )
    assert runtime.events(instance, branch) == before_events
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    child_state = runtime.current_state(instance, child)
    assert child_state.semantic_hash() != before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, child).state.semantic_hash()
        == child_state.semantic_hash()
    )

    _write_artifact(
        {
            "schema": "wanxiang.v5.5.source-canon-immutability.v1",
            "qualification": "G97 closure / Gate 32 independent qualification",
            "status": "ACCEPTED",
            "source": {
                "kind": "synthetic_private_qualification",
                "payload_embedded": False,
                "payload_unchanged": source.payload == source_payload,
                "content_hash_unchanged": source.content_hash == source_hash,
            },
            "product_chain": {
                "source_to_world_package": True,
                "world_package_id": package_id,
                "package_manifest_hash_stable": package.manifest.content_hash == package_hash,
                "preview_playable_sqlite_commit": True,
                "committed_event_count_before_derivation": len(before_events),
                "derived_candidate_count": len(norms) + 2,
            },
            "derived_evidence": {
                "pattern_detections": len(detections),
                "norm_candidates": len(norms),
                "institution_reviewed": institution.approved,
                "ontology_reviewed": ontology.approved,
                "constitution_hash_unchanged": constitution.compute_hash() == constitution_hash,
                "canonical_hash_unchanged_after_derivation": after_derivation.semantic_hash()
                == before.semantic_hash(),
                "event_history_unchanged_after_derivation": after_derivation_events
                == before_events,
                "replay_equal": runtime.restore_and_replay(instance, branch).state.semantic_hash()
                == before.semantic_hash(),
            },
            "branch_isolation": {
                "parent_history_unchanged": runtime.events(instance, branch) == before_events,
                "child_diverged": child_state.semantic_hash() != before.semantic_hash(),
                "child_replay_equal": runtime.restore_and_replay(
                    instance, child
                ).state.semantic_hash()
                == child_state.semantic_hash(),
            },
            "cross_goal_evidence": {
                "G93H": "reports/G93H_REPORT.md",
                "G94A_G94H": "reports/G94H_REPORT.md",
                "G97B": "reports/G97B_REPORT.md",
                "G97C": "reports/G97C_REPORT.md",
            },
            "boundary": {
                "commit_authority_only": True,
                "provider_or_candidate_canonical_write": False,
                "source_modified": False,
                "raw_source_recorded": False,
            },
        }
    )
