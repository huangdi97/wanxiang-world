"""G94A: the observation cache is rebuilt from the real playable event stream."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# G94A Observation Town\nCharacter: Alice\nCharacter: Bob\n"
        "Alice keeps watch at the gate. Bob carries the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses record repeated duties\n"
    )
    return SourceRecord(
        source_id="g94a_observation_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g94a_observation_source",
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
        provenance="synthetic:g94a",
        access="private",
    )


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                name = component.fields.get("display_name")
                if isinstance(name, str):
                    found[name] = entity.entity_id.value
    return found


@pytest.mark.integration
def test_observation_store_rebuilds_from_playable_sqlite_history(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g94a_observation", (source,), profile="book")
    assert authored.package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    profile = playable.register_package(
        authored.package, owner_id="g94a_owner", visibility="private"
    )
    character = playable.entry.create_character(
        "g94a_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g94a_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g94a_owner",
        mode="embodiment",
        session_id="session_g94a_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    alice = EntityId(actors["Alice"])
    first = playable.action(
        instance.value,
        viewer_id="g94a_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "watching"},
    )
    second = playable.action(
        instance.value,
        viewer_id="g94a_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "watching"},
    )

    state_before = runtime.current_state(instance, branch)
    events_before = runtime.events(instance, branch)
    event_ids = tuple(event.event_id.value for event in events_before)
    cache = PatternObservationStore.rebuild(events_before, window_size=10)
    assert first.event_id in cache.event_refs()
    assert second.event_id in cache.event_refs()
    assert cache.query(kind="behavior")
    assert cache.statistics(window_start=0, window_end=100).unique_event_count > 0
    assert set(cache.event_refs()).issubset(set(event_ids))

    rebuilt = PatternObservationStore.rebuild(tuple(reversed(events_before)), window_size=10)
    assert rebuilt.cache_hash() == cache.cache_hash()
    assert rebuilt.to_dict() == cache.to_dict()
    assert tuple(event.event_id.value for event in runtime.events(instance, branch)) == event_ids
    assert runtime.current_state(instance, branch).revision == state_before.revision
    assert runtime.current_state(instance, branch).semantic_hash() == state_before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash()
        == state_before.semantic_hash()
    )
    assert source.payload == _source().payload
    assert source.content_hash == _source().content_hash
