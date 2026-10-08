"""Run one M97 benchmark family through the real local product surfaces."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, cast

from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_substrate.actor_continuity import (
    ContinuityQualificationSeed,
    SevenDayContinuityQualification,
)
from wanxiang_substrate.quality.experience_collector import ExperienceTraceEvidence
from wanxiang_substrate.quality.experience_scenarios import ExperienceBenchmarkScenario
from wanxiang_substrate.sources.model import payload_hash
from wanxiang_substrate.workshop import CreatorIntent

from reference_runtime import build_reference_runtime

ROOT = Path(__file__).resolve().parent.parent
SOURCE_CONTENT = (
    "# M97 creator-owned source qualification\n"
    "Character: Alice\nCharacter: Bob\n"
    "Alice and Bob maintain a shared harbor ledger.\n"
    "relationship: Alice -> Bob\n"
    "rule: reviewed evidence remains proposal-only.\n"
)
PROMPT = (
    "南宋末年的江南水城，机械机关术已进入民用商业，水运繁荣但木材、铜料与粮食面临周期性压力；"
    "不同商帮、工匠行会与地方机构有各自目标、资源和秘密。"
)
SEEDS = (9701, 9702)
INPUT_HASHES = {
    "source_sha256": payload_hash(SOURCE_CONTENT),
    "prompt_sha256": CreatorIntent("m97_prompt_intent", "m97-creator", PROMPT).text_hash,
}


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _request(client: Any, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    response: Any = client.request(method, path, **kwargs)
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"{method} {path} returned HTTP {response.status_code}: {response.text}")
    value = response.json()
    if not isinstance(value, dict):
        raise RuntimeError(f"{method} {path} did not return an object")
    return cast(dict[str, Any], value)


def _create_world(client: Any, family: str, seed: int) -> tuple[str, str, Any]:
    owner = f"m97-{family}-owner"
    workshop_id = "m97_source_qualification" if family == "source" else "m96_original_prompt_world"
    if family == "source":
        created_response: Any = client.post(
            "/workshop/from-source",
            json={
                "workshop_id": workshop_id,
                "owner_id": owner,
                "profile": "book",
                "visibility": "private",
                "display_name": "M97 Source Qualification",
                "semantic_provider": "local",
                "sources": [
                    {
                        "source_id": f"m97_source_fixture_{seed}",
                        "kind": "text",
                        "content": SOURCE_CONTENT,
                        "stage": "E3",
                        "owner": "m97-creator",
                        "usage": "qualification",
                        "rights_approved": True,
                        "access": "private",
                        "provenance": "creator_owned_synthetic_m97",
                        "private_analysis_allowed": True,
                        "external_model_processing_allowed": False,
                        "package_inclusion_allowed": True,
                        "public_export_allowed": False,
                        "training_allowed": False,
                    }
                ],
            },
        )
    else:
        intent = CreatorIntent("m97_prompt_intent", "m97-creator", PROMPT)
        created_response = client.post(
            "/workshop/from-prompt",
            json={
                "workshop_id": workshop_id,
                "owner_id": owner,
                "intent": {
                    "intent_id": intent.intent_id,
                    "author_id": intent.author_id,
                    "text": intent.text,
                },
                "visibility": "private",
                "display_name": "M97 Prompt Qualification",
            },
        )
    if created_response.status_code != 201:
        raise RuntimeError(
            f"{family} workshop creation failed: {created_response.status_code}: "
            f"{created_response.text}"
        )
    created = cast(dict[str, Any], created_response.json())
    if family == "prompt":
        for action in ("review_e5", "accept_constraints", "preview"):
            reviewed: Any = client.post(f"/workshop/{workshop_id}/review", json={"action": action})
            if reviewed.status_code != 200:
                raise RuntimeError(f"prompt review {action} failed: {reviewed.status_code}")
        created = cast(dict[str, Any], reviewed.json())
    profile = cast(dict[str, Any], created.get("playable_profile") or {})
    profile_id = str(profile.get("profile_id", ""))
    if not profile_id:
        raise RuntimeError(f"{family} workshop did not expose a playable profile")
    build = client.app.state.workshop.get(workshop_id)
    return owner, profile_id, build


def _canonical_entity_ref(value: str) -> str:
    """Resolve a draft entity key to the runtime's canonical entity ref."""
    normalized = value.replace(":", "_")
    return normalized if normalized.startswith("ent_") else f"ent_{normalized}"


def run_family(scenario: ExperienceBenchmarkScenario, seed: int) -> ExperienceTraceEvidence:
    """Execute the scenario's actual API, runtime, and continuity trace."""
    runtime = build_reference_runtime()
    app = create_app(runtime)
    client: Any = TestClient(app)
    owner, profile_id, build = _create_world(client, scenario.family, seed)
    entity_ids = tuple(_canonical_entity_ref(str(item[0])) for item in build.package.draft.entities)
    if not entity_ids:
        raise RuntimeError(f"{scenario.family} package has no playable entity")
    actor_id = entity_ids[0]
    continuity_actor = entity_ids[1] if len(entity_ids) > 1 else f"ent_{scenario.family}_actor_2"
    character: Any = client.post(
        "/experience/characters",
        headers={"X-Wanxiang-User": owner},
        json={
            "display_name": f"M97 {scenario.family} actor",
            "character_id": actor_id,
            "compatible_profile_ids": [profile_id],
        },
    )
    if character.status_code != 201:
        raise RuntimeError(
            f"{scenario.family} character failed: {character.status_code}: {character.text}"
        )
    entered = _request(
        client,
        "POST",
        f"/experience/worlds/{profile_id}/enter",
        headers={"X-Wanxiang-User": owner},
        json={
            "mode": "embodiment",
            "session_id": f"m97-{scenario.family}-{seed}",
            "character_id": actor_id,
        },
    )
    instance_id = str(cast(dict[str, Any], entered["instance"])["instance_id"])
    actions: list[dict[str, Any]] = []
    for status in (
        f"{scenario.family}_active",
        f"{scenario.family}_progress",
        f"{scenario.family}_complete",
    ):
        actions.append(
            _request(
                client,
                "POST",
                f"/experience/instances/{instance_id}/action",
                headers={"X-Wanxiang-User": owner},
                json={
                    "action_type": "set_status",
                    "payload": {"entity_id": actor_id, "status": status},
                },
            )
        )
    rejected: Any = client.post(
        f"/experience/instances/{instance_id}/action",
        headers={"X-Wanxiang-User": owner},
        json={"action_type": "unknown_action", "payload": {}},
    )
    leave = _request(
        client,
        "POST",
        f"/experience/instances/{instance_id}/leave",
        headers={"X-Wanxiang-User": owner},
    )
    continued = _request(
        client,
        "POST",
        f"/experience/instances/{instance_id}/continue",
        headers={"X-Wanxiang-User": owner},
    )
    record = app.state.playable.store.get_instance(instance_id)
    instance = WorldInstanceId(instance_id)
    branch = BranchId(record.branch_id)
    state = runtime.current_state(instance, branch)
    replay = runtime.restore_and_replay(instance, branch)
    snapshot = runtime.create_checkpoint(instance, branch)
    evidence = [cast(dict[str, Any], item["evidence"]) for item in actions]
    event_refs = tuple(str(item["event_id"]) for item in actions)
    state_refs = (f"state:{scenario.family}:{seed}:entry:{entered['state_hash']}",) + tuple(
        f"state:{scenario.family}:{seed}:action:{index}:{item['state_hash']}"
        for index, item in enumerate(actions, start=1)
    )
    continuity = SevenDayContinuityQualification(
        ContinuityQualificationSeed(
            build.package.package_id,
            (instance_id,),
            (EntityId(actor_id), EntityId(continuity_actor)),
            days=7,
            seed=seed,
        )
    ).run()
    experience = build.workshop.experience
    goal_visible = bool(
        experience
        and "set_status" in experience.allowed_actions
        and "state_diff" in experience.ui_capabilities
    )
    revision_aligned = all(
        item["after_revision"] == item["before_revision"] + 1
        and item["state_diff_event_id"] == item["event_id"]
        for item in evidence
    )
    return ExperienceTraceEvidence(
        run_id=f"run:{scenario.scenario_id}:seed-{seed}",
        build_sha=_head(),
        seed=seed,
        trace_ref=f"trace:m97:{scenario.family}:{seed}",
        worldness_ref=f"worldness:m97:{scenario.family}:{build.package.package_id}",
        event_refs=event_refs,
        state_refs=state_refs,
        replay_refs=(
            f"replay:m97:{scenario.family}:{replay.state.semantic_hash()}",
            snapshot.snapshot_id.value,
        ),
        action_committed=all(bool(item["diff"]["changes"]) for item in actions),
        rejection_observed=rejected.status_code == 422,
        replay_equal=replay.state.semantic_hash() == state.semantic_hash(),
        character_identity_stable=(
            cast(dict[str, Any], continued["instance"]).get("instance_id") == instance_id
            and cast(dict[str, Any], continued["instance"]).get("actor_id", actor_id) == actor_id
        ),
        leave_continue_equal=(
            leave["status"] == "left" and continued["state_hash"] == actions[-1]["state_hash"]
        ),
        revision_aligned=revision_aligned,
        goal_visible=goal_visible,
        state_diff_count=sum(len(cast(list[Any], item["diff"]["changes"])) for item in actions),
        after_state_hashes=tuple(str(item["state_hash"]) for item in actions),
        memory_revision_count=continuity.memory_count,
        belief_revision_count=continuity.belief_revision_count,
        relationship_revision_count=continuity.relationship_revision_count,
    )


__all__ = ["INPUT_HASHES", "PROMPT", "SEEDS", "SOURCE_CONTENT", "run_family"]
