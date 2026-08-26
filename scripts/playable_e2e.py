"""CLI qualification over the same PlayableService used by API and Studio."""

from __future__ import annotations

import argparse
import json
from typing import cast

from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.store import ExperienceInstanceRecord
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

from reference_runtime import build_reference_runtime

_DEFAULT_CONTENT = (
    "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)


def run(content: str) -> dict[str, object]:
    source = SourceRecord(
        source_id="cli_playable_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://cli_playable_source",
        stage="E3",
        rights=RightsEnvelope(owner="cli", usage="qualification", approved=True),
        payload=content,
        provenance="cli:g88h",
        access="private",
    )
    authored = OneClickAuthoring().run("job_cli_playable", (source,), profile="book")
    runtime = build_reference_runtime()
    service = PlayableService(runtime)
    profile = service.register_package(authored.package, owner_id="cli", visibility="public")
    character = service.entry.create_character(
        "cli",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    entered = service.enter(
        profile.profile_id,
        viewer_id="cli",
        mode="embodiment",
        session_id="session_cli_playable",
        character_id=character.character_id,
    )
    instance = cast(dict[str, object], entered["instance"])
    instance_id = str(instance["instance_id"])
    action = service.action(instance_id, viewer_id="cli", text="set status to awake")
    record: ExperienceInstanceRecord = service.store.get_instance(instance_id)
    replay = runtime.restore_and_replay(WorldInstanceId(instance_id), BranchId(record.branch_id))
    replay_equal = replay.state.semantic_hash() == action.state_hash
    service.leave(instance_id, viewer_id="cli")
    continued = service.continue_instance(instance_id, viewer_id="cli")
    return {
        "source_profile": authored.source_profile,
        "package_id": profile.world_package_ref,
        "profile_id": profile.profile_id,
        "instance_id": instance_id,
        "entered_entities": len(
            cast(list[object], cast(dict[str, object], entered["state"])["entities"])
        ),
        "proposal_status": action.proposal.status,
        "committed_event_id": action.event_id,
        "state_diff_changes": len(action.diff.changes),
        "replay_equal": replay_equal,
        "continued_instance_id": cast(dict[str, object], continued["instance"])["instance_id"],
        "same_instance_after_continue": (
            cast(dict[str, object], continued["instance"])["instance_id"] == instance_id
        ),
        "source_path_or_digest_emitted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", default=_DEFAULT_CONTENT)
    args = parser.parse_args()
    print(json.dumps(run(args.content), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
