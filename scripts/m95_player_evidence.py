"""Run the real SQLite-backed M95 Player route and emit sanitized evidence."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any, cast

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from wanxiang_api.app import build_runtime, create_app
from wanxiang_domain.ids import BranchId, WorldInstanceId

from m95_player_server import JOB_ID, SOURCE_ID, source_record

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {"x-wanxiang-user": "studio"}


def _prepare_sqlite_parent(database_url: str) -> None:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return
    raw_path = database_url[len(prefix) :]
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)


def _upgrade(database_url: str) -> None:
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old


def _source_payload() -> dict[str, object]:
    record = source_record()
    rights = record.rights
    if rights is None:
        raise RuntimeError("the creator-owned fixture must carry explicit rights")
    return {
        "source_id": record.source_id,
        "kind": record.kind,
        "content": record.payload,
        "stage": record.stage,
        "rights_approved": rights.approved,
        "access": record.access,
        "private_analysis_allowed": rights.private_analysis_allowed,
        "package_inclusion_allowed": rights.package_inclusion_allowed,
        "public_export_allowed": rights.public_export_allowed,
        "training_allowed": rights.training_allowed,
        "owner": rights.owner,
        "usage": rights.usage,
        "provenance": record.provenance,
    }


def _json(response: Any) -> dict[str, Any]:
    if response.status_code >= 300:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    return cast(dict[str, Any], response.json())


def _event_refs(runtime: Any, instance_id: str, branch_id: str) -> list[str]:
    events = runtime.events(WorldInstanceId(instance_id), BranchId(branch_id))
    return [str(getattr(event.event_id, "value", event.event_id)) for event in events]


def run(database_url: str, output: Path) -> dict[str, object]:
    _prepare_sqlite_parent(database_url)
    _upgrade(database_url)
    runtime = build_runtime(database_url)
    app = create_app(runtime)
    source = source_record()
    with TestClient(app) as raw_client:
        client: Any = raw_client
        one_click = _json(
            client.post(
                "/studio/one-click",
                headers=HEADERS,
                json={"job_id": JOB_ID, "profile": "book", "sources": [_source_payload()]},
            )
        )
        profile = _json(
            client.post(
                f"/studio/jobs/{JOB_ID}/playable-profile",
                headers=HEADERS,
                json={
                    "owner_id": "studio",
                    "visibility": "public",
                    "display_name": "江南机关城",
                    "description": "一座沿水道展开的机关城，机关与人情都从清晨开始。",
                    "scenario_name": "潮汐门初启",
                    "opening_hint": "先听一听城门内外的水声，再决定往哪里走。",
                },
            )
        )
        profile_data = cast(dict[str, Any], profile["profile"])
        profile_id = str(profile_data["profile_id"])
        _json(
            client.post(
                "/experience/player/characters",
                headers=HEADERS,
                json={
                    "display_name": "沈砚",
                    "character_id": "ent_alice",
                    "compatible_profile_ids": [profile_id],
                    "identity": "守夜人",
                    "intro": "熟悉城门与水道的守夜人。",
                    "stance": "谨慎观察",
                    "starting_location": "沉水巷",
                    "knowledge_boundary": "只知道自己亲眼见过的事。",
                },
            )
        )
        entered = _json(
            client.post(
                f"/experience/player/worlds/{profile_id}/enter",
                headers=HEADERS,
                json={
                    "mode": "embodiment",
                    "session_id": "m95_evidence_session",
                    "character_id": "ent_alice",
                },
            )
        )
        instance_id = str(entered["instance_id"])
        record = app.state.playable.store.get_instance(instance_id)
        world_id = WorldInstanceId(instance_id)
        branch_id = BranchId(record.branch_id)
        before = runtime.current_state(world_id, branch_id)
        acted = _json(
            client.post(
                f"/experience/player/instances/{instance_id}/action",
                headers=HEADERS,
                json={"text": "让自己保持清醒"},
            )
        )
        after = runtime.current_state(world_id, branch_id)
        view = cast(dict[str, Any], acted["view"])
        recent_changes = cast(list[object], view["recent_changes"])
        if acted.get("status") != "committed" or acted.get("changed") is not True:
            raise RuntimeError(f"player action did not commit: {acted}")
        if not any("清醒" in str(change) for change in recent_changes):
            raise RuntimeError(f"player projection omitted the committed change: {view}")
        left = _json(
            client.post(f"/experience/player/instances/{instance_id}/leave", headers=HEADERS)
        )
        continued = _json(
            client.post(f"/experience/player/instances/{instance_id}/continue", headers=HEADERS)
        )
        replayed = runtime.restore_and_replay(world_id, branch_id).state
        event_refs = _event_refs(runtime, instance_id, record.branch_id)
        if replayed.semantic_hash() != after.semantic_hash():
            raise RuntimeError("replay hash differs from the post-action canonical state")
        result: dict[str, object] = {
            "milestone": "M95",
            "goal": "G98A-G98E experience remediation",
            "status": "M95_REMEDIATION_REQUIRED",
            "automated_readiness": "PASS",
            "human_acceptance": "USER_INPUT_REQUIRED",
            "gate_80": "LOCKED",
            "input": {
                "source_id": SOURCE_ID,
                "sha256": source.content_hash,
                "provenance": source.provenance,
                "rights_boundary": (
                    "creator-owned synthetic fixture; no private source bytes emitted"
                ),
            },
            "version": {
                "git_head": subprocess.run(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
                ).stdout.strip(),
                "schema_version": 1,
                "rule_version": 1,
                "migration_head": "0004_add_world_metadata",
                "seed": "deterministic fixture IDs; runtime IDs recorded below",
            },
            "refs": {
                "job_id": JOB_ID,
                "package_id": one_click["package_id"],
                "profile_id": profile_id,
                "world_instance_id": instance_id,
                "branch_id": record.branch_id,
                "actor_id": "ent_alice",
                "event_ids": event_refs,
            },
            "trace": {
                "before_revision": before.revision.value,
                "after_revision": after.revision.value,
                "after_state_hash": after.semantic_hash(),
                "replay_state_hash": replayed.semantic_hash(),
                "action_status": acted["status"],
                "action_changed": acted["changed"],
                "leave_status": left["status"],
                "continued_instance_id": continued["instance_id"],
                "continued_same_instance": continued["instance_id"] == instance_id,
            },
            "boundaries": {
                "implemented": (
                    "Chinese Player projection/UI, server-backed continuity and action path"
                ),
                "validated": (
                    "API route chain, SQLite persistence, Commit Authority, replay and "
                    "browser journey"
                ),
                "experimental": (
                    "Prompt Genesis and bounded long-horizon/World Lab/emergence remain "
                    "bounded/experimental"
                ),
                "not_proven": (
                    "human comprehension, immersion, agency rating and real-player acceptance"
                ),
                "external_blocked": (
                    "live PostgreSQL and heavy physical/visual E2E have no real environment"
                ),
            },
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.database_url, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
