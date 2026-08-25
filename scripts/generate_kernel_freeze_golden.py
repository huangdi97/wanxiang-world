"""G54B: Kernel freeze goldens generator (M51).

Freezes deterministic semantic goldens for the frozen Kernel surface used by
the Source->LivingWorld program: Commit event hashes, Replay final state hash,
Branch fork isolation, Worldline (WorldDefinition) hash, Package manifest
hash, and the Kernel v1 ABI golden hash. Regeneration must be byte-stable.

No domain content, no LLM/provider coupling. Pure and deterministic.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any, cast

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from tests.helpers.replay_fixture import (  # noqa: E402
    BRANCH,
    INSTANCE,
    RULES,
    SCHEMA,
    build_fixture_events,
)
from wanxiang_domain.event import CommittedEvent  # noqa: E402
from wanxiang_domain.hierarchy import EventSeq  # noqa: E402
from wanxiang_domain.ids import BranchId, WorldDefinitionId  # noqa: E402
from wanxiang_domain.serialization_history import event_to_primitive  # noqa: E402
from wanxiang_domain.worldline import WorldDefinition  # noqa: E402
from wanxiang_runtime.replay import ReplayEngine  # noqa: E402
from wanxiang_substrate.kernel.abi import abi_golden  # noqa: E402
from wanxiang_substrate.packages.model import (  # noqa: E402
    PackageKind,
    PackageManifest,
    SemanticVersion,
)

GOLDEN_PATH = ROOT / "reports" / "kernel_freeze_golden.json"


def _sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def event_hash(event: Any) -> str:
    canonical = json.dumps(event_to_primitive(event), sort_keys=True, separators=(",", ":"))
    return _sha256(canonical)


def reference_manifest() -> PackageManifest:
    return PackageManifest(
        package_id="world_ref",
        kind=cast(PackageKind, "world"),
        version=SemanticVersion(1, 0, 0),
        name="Reference World",
        dependencies=(),
        content_hash="",
    ).with_hash()


def build_golden() -> dict[str, Any]:
    events = build_fixture_events()
    replay = ReplayEngine(RULES, SCHEMA).replay(events)
    # Branch fork isolation: fork at revision 2, replay child events 3-5.
    child = BranchId("br_golden_child")
    # Child branch carries its own branch-local event seq (1..n) while
    # revision continues from the fork baseline (3..5).
    child_events = tuple(
        CommittedEvent(
            event_id=e.event_id,
            instance_id=e.instance_id,
            branch_id=child,
            event_seq=EventSeq(index),
            revision=e.revision,
            schema_version=e.schema_version,
            command_id=e.command_id,
            delta=e.delta,
            world_time=e.world_time,
            rule_version=e.rule_version,
        )
        for index, e in enumerate((x for x in events if x.revision.value > 2), start=1)
    )
    child_replay = ReplayEngine(RULES, SCHEMA).replay(
        child_events,
        start_seq=1,
        baseline=ReplayEngine(RULES, SCHEMA).replay(events[:2]),
    )
    definition = WorldDefinition(
        definition_id=WorldDefinitionId("wdef_kernel_freeze"),
        version=1,
        name="Kernel Freeze Reference",
        constitution_ref="constitution:v1",
        genesis_ref="genesis:ref",
        package_ref="world_ref",
        schema_version=1,
    ).with_hash()
    manifest = reference_manifest()
    abi = abi_golden()
    payload: dict[str, Any] = {
        "kernel_freeze_version": 1,
        "instance_id": INSTANCE.value,
        "root_branch_id": BRANCH.value,
        "event_hashes": [event_hash(e) for e in events],
        "replay_final_state_hash": replay.semantic_hash(),
        "branch_fork": {
            "child_branch_id": child.value,
            "fork_revision": 2,
            "child_replay_state_hash": child_replay.semantic_hash(),
            "parent_state_hash_unchanged": ReplayEngine(RULES, SCHEMA)
            .replay(events[:2])
            .semantic_hash(),
        },
        "worldline": {
            "definition_id": definition.definition_id.value,
            "content_hash": definition.content_hash,
        },
        "package": {
            "package_id": manifest.package_id,
            "version": str(manifest.version),
            "content_hash": manifest.content_hash,
        },
        "abi_golden_hash": abi["golden_hash"],
        "combined": {},
    }
    combined = {
        "kernel_freeze_version": payload["kernel_freeze_version"],
        "event_hashes": payload["event_hashes"],
        "replay_final_state_hash": payload["replay_final_state_hash"],
        "branch_fork": payload["branch_fork"],
        "worldline": payload["worldline"],
        "package": payload["package"],
        "abi_golden_hash": payload["abi_golden_hash"],
    }
    payload["combined"] = _sha256(json.dumps(combined, sort_keys=True, separators=(",", ":")))
    return payload


def main() -> int:
    golden = build_golden()
    with GOLDEN_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(golden, indent=2, sort_keys=True) + "\n")
    print(f"wrote {GOLDEN_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
