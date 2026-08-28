"""Qualify the bounded original-prompt world product chain (G99A–G99E)."""

from __future__ import annotations

import hashlib
import json
from typing import Any, cast

from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.actor_continuity import (
    ContinuityQualificationSeed,
    SevenDayContinuityQualification,
)
from wanxiang_substrate.packages import (
    PackageManifest,
    SemanticVersion,
    export_install,
    install_export_hash,
)
from wanxiang_substrate.workshop import CreatorIntent, WorldRegistryCatalog
from wanxiang_substrate.world_lab import WorldRunArtifact

from m96_prompt_world_reporting import write_outputs
from reference_runtime import build_reference_runtime

PROMPT = (
    "南宋末年的江南水城，机械机关术已进入民用商业，水运繁荣但木材、铜料与粮食面临周期性压力；"
    "不同商帮、工匠行会与地方机构有各自目标、资源和秘密。"
)
SEED = 9601


def _commit_day(
    runtime: Any,
    instance: WorldInstanceId,
    branch: BranchId,
    actor_id: str,
    day: int,
    scope: str = "parent",
) -> str:
    state = runtime.current_state(instance, branch)
    result = runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(f"m96_{scope}_day_{day:02d}_{actor_id}"),
            instance_id=instance,
            branch_id=branch,
            expected_revision=BranchRevision(state.revision.value),
            action_type="set_status",
            payload={"entity_id": actor_id, "status": f"day-{day}"},
            actor_id=ActorId(actor_id),
            world_time=WorldTime(day),
        )
    )
    return result.event.event_id.value


def run() -> dict[str, Any]:
    runtime = build_reference_runtime()
    app = create_app(runtime)
    client: Any = TestClient(app)
    intent = CreatorIntent("m96_original_intent", "m96-author", PROMPT)
    created = client.post(
        "/workshop/from-prompt",
        json={
            "workshop_id": "m96_original_prompt_world",
            "owner_id": "m96-author",
            "intent": {
                "intent_id": intent.intent_id,
                "author_id": intent.author_id,
                "text": intent.text,
            },
            "visibility": "public",
            "display_name": "Jiangnan Mechanisms",
        },
    )
    if created.status_code != 201:
        raise RuntimeError(f"prompt creation failed: {created.status_code}: {created.text}")
    initial = cast(dict[str, Any], created.json())
    initial_prompt = cast(dict[str, Any], initial["prompt"])
    for action in ("review_e5", "accept_constraints", "preview"):
        reviewed = client.post(
            "/workshop/m96_original_prompt_world/review", json={"action": action}
        )
        if reviewed.status_code != 200:
            raise RuntimeError(f"review action failed: {action}: {reviewed.status_code}")
    final = cast(dict[str, Any], reviewed.json())
    build = app.state.workshop.get("m96_original_prompt_world")
    prompt_run = build.prompt_run
    if prompt_run is None:
        raise RuntimeError("prompt run missing after review")
    registry = WorldRegistryCatalog()
    for domain_id, version in build.package.domain_versions:
        registry.packages.register(
            PackageManifest(domain_id, "domain", SemanticVersion.parse(version), domain_id)
        )
    entry = registry.register(
        build.package.manifest,
        build.workshop.publishing,
        label="community",
    )
    opened = registry.open(entry.entry_id, viewer_id="m96-author")
    installed = registry.install(entry.entry_id, viewer_id="m96-author")
    install_export = export_install(installed.record)

    playable_profile = cast(dict[str, Any], final["playable_profile"])
    profile_id = str(playable_profile["profile_id"])
    character_id = "ent_prompt_actor_1"
    character = client.post(
        "/experience/characters",
        headers={"X-Wanxiang-User": "m96-author"},
        json={
            "display_name": "Focal Actor",
            "character_id": character_id,
            "compatible_profile_ids": [profile_id],
        },
    )
    if character.status_code != 201:
        raise RuntimeError(f"prompt character failed: {character.status_code}: {character.text}")
    entered = client.post(
        f"/experience/worlds/{profile_id}/enter",
        headers={"X-Wanxiang-User": "m96-author"},
        json={"mode": "embodiment", "session_id": "m96-session", "character_id": character_id},
    )
    if entered.status_code != 200:
        raise RuntimeError(f"prompt entry failed: {entered.status_code}: {entered.text}")
    instance_id = str(cast(dict[str, Any], entered.json()["instance"])["instance_id"])
    record = app.state.playable.store.get_instance(instance_id)
    instance = WorldInstanceId(instance_id)
    branch = BranchId(record.branch_id)
    action_response = client.post(
        f"/experience/instances/{instance_id}/action",
        headers={"X-Wanxiang-User": "m96-author"},
        json={"text": "set status to active"},
    )
    if action_response.status_code != 200:
        raise RuntimeError(
            f"prompt action failed: {action_response.status_code}: {action_response.text}"
        )
    action = cast(dict[str, Any], action_response.json())
    leave = client.post(
        f"/experience/instances/{instance_id}/leave", headers={"X-Wanxiang-User": "m96-author"}
    )
    continued = client.post(
        f"/experience/instances/{instance_id}/continue", headers={"X-Wanxiang-User": "m96-author"}
    )
    day_events: list[str] = []
    child_events: list[str] = []
    checkpoints: list[dict[str, Any]] = []
    child_branch_id = ""
    child_isolated = True
    parent_hash_at_fork = ""
    parent_events_at_fork: tuple[Any, ...] = ()
    for day in range(1, 8):
        day_events.append(_commit_day(runtime, instance, branch, character_id, day))
        snapshot = runtime.create_checkpoint(instance, branch)
        state = runtime.current_state(instance, branch)
        replayed = runtime.restore_and_replay(instance, branch)
        checkpoints.append(
            {
                "day": day,
                "snapshot_id": snapshot.snapshot_id.value,
                "revision": state.revision.value,
                "state_hash": state.semantic_hash(),
                "replay_hash": replayed.state.semantic_hash(),
                "replay_equal": replayed.state.semantic_hash() == state.semantic_hash(),
            }
        )
        if day == 4:
            parent_hash_at_fork = state.semantic_hash()
            parent_events_at_fork = runtime.events(instance, branch)
            child = runtime.create_branch(instance, branch)
            child_branch_id = child.branch_id.value
            child_event = _commit_day(
                runtime, instance, child.branch_id, character_id, 4, scope="child"
            )
            child_events.append(child_event)
            child_isolated = (
                runtime.current_state(instance, branch).semantic_hash() == parent_hash_at_fork
                and runtime.events(instance, branch) == parent_events_at_fork
                and runtime.restore_and_replay(instance, child.branch_id).state.semantic_hash()
                == runtime.current_state(instance, child.branch_id).semantic_hash()
                and bool(child_event)
            )
    final_state = runtime.current_state(instance, branch)
    continuity = SevenDayContinuityQualification(
        ContinuityQualificationSeed(
            build.package.package_id,
            (instance_id,),
            (EntityId(character_id), EntityId("ent_prompt_actor_2")),
            days=7,
            seed=SEED,
        )
    ).run()
    events = runtime.events(instance, branch)
    run_artifact = WorldRunArtifact(
        artifact_id="artifact:m96:original-prompt",
        world_package_ref=build.package.package_id,
        world_package_version=str(build.package.manifest.version),
        scenario_ref=profile_id,
        scenario_version=str(playable_profile["version"]),
        constitution_version="1",
        runtime_profile_ref="reference-runtime:m96-v1",
        provider_versions=(("prompt_genesis", prompt_run.provider_id), ("runtime", "reference-v1")),
        seed=SEED,
        commit_refs=tuple(event.event_id.value for event in events) + tuple(child_events),
        snapshot_refs=tuple(item["snapshot_id"] for item in checkpoints),
        branch_refs=(branch.value, child_branch_id),
        actor_trajectory_refs=(
            (character_id, final_state.semantic_hash()),
            ("ent_prompt_actor_2", final_state.semantic_hash()),
        ),
        validation_results=(
            ("prompt_claims", "E5"),
            ("review", "accepted"),
            ("registry", "published_and_installed"),
            ("replay", "equal"),
            ("branch", "isolated"),
        ),
        metrics=(
            ("bounded_days", 7.0),
            ("event_count", float(len(events))),
            ("checkpoint_count", float(len(checkpoints))),
            ("actor_count", 2.0),
            ("child_branch_event_count", float(len(child_events))),
        ),
        privacy_metadata=(("creation_mode", "prompt"), ("rights_scope", "creator_intent_only")),
        redacted_fields=("prompt_text", "source_payload", "private_source"),
    ).with_hash()
    checks = {
        "intent_hash_matches": initial_prompt.get("intent", {}).get("text_hash")
        == intent.text_hash,
        "genesis_provider_present": bool(prompt_run.provider_id),
        "all_generated_claims_e5": all(
            claim.completion_class == "E5" for claim in prompt_run.contract.claims
        ),
        "review_ready": prompt_run.contract.review_gate.ready_for_preview,
        "package_hash_valid": build.package.manifest.content_hash
        == build.package.manifest.compute_hash(),
        "publishable": build.publishing.publishable,
        "registry_opened": opened.entry.entry_id == entry.entry_id,
        "install_hash_valid": install_export_hash(install_export)
        == hashlib.sha256(
            json.dumps(install_export, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "play_commit_has_diff": bool(action["diff"]["changes"]),
        "leave_continue_same_state": leave.status_code == 200
        and continued.status_code == 200
        and continued.json().get("state_hash") == action["state_hash"],
        "seven_checkpoints": len(checkpoints) == 7,
        "seven_day_replay": all(item["replay_equal"] for item in checkpoints),
        "branch_isolated": child_isolated,
        "continuity_replay_equal": continuity.replay_equal,
        "continuity_leave_reenter_equal": continuity.leave_reenter_equal,
        "run_artifact_hash_valid": run_artifact.verify_hash(),
    }
    conclusion = "PASS" if all(checks.values()) else "FAIL"
    return write_outputs(
        checks=checks,
        conclusion=conclusion,
        intent=intent,
        prompt_run=prompt_run,
        build=build,
        entry=entry,
        opened=opened,
        install_export=install_export,
        profile_id=profile_id,
        instance_id=instance_id,
        branch=branch,
        action=action,
        leave=leave,
        continued=continued,
        events=events,
        day_events=day_events,
        checkpoints=checkpoints,
        child_branch_id=child_branch_id,
        continuity=continuity,
        run_artifact=run_artifact,
    )


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
