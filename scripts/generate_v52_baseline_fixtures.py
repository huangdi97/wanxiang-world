"""Generate the v5.2 compatibility golden baseline (G29A).

Freezes one old Event stream, Snapshot, Branch, WorldPack manifest set, and
API contract as reproducible fixtures under tests/fixtures/v5_2_baseline/,
plus a manifest.json with per-file sha256 and a combined semantic hash.

Run from repository root:

    uv run python scripts/generate_v52_baseline_fixtures.py

The fixtures are the golden values for v5.2 backward-compatibility regressions:
later goals may extend the API but must keep these loadable and hash-stable.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "tests" / "fixtures" / "v5_2_baseline"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from dataclasses import replace  # noqa: E402

from tests.helpers.replay_fixture import (  # noqa: E402
    BRANCH,
    INSTANCE,
    RULES,
    SCHEMA,
    build_fixture_events,
)
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta  # noqa: E402
from wanxiang_domain.hierarchy import (  # noqa: E402
    BranchAncestry,
    BranchMetadata,
    BranchRevision,
    EventSeq,
)
from wanxiang_domain.ids import (  # noqa: E402
    BranchId,
    CommandId,
    EntityId,
    EventId,
    SnapshotId,
    TraceId,
)
from wanxiang_domain.serialization_history import (  # noqa: E402
    ancestry_to_primitive,
    event_to_primitive,
    snapshot_to_primitive,
)
from wanxiang_domain.time import CommitTimestamp, WorldTime  # noqa: E402
from wanxiang_runtime.authority import CommitAuthority, CommitRequest  # noqa: E402
from wanxiang_runtime.branch import fork_branch  # noqa: E402
from wanxiang_runtime.ports import InMemoryEventStore  # noqa: E402
from wanxiang_runtime.replay import ReplayEngine  # noqa: E402
from wanxiang_runtime.snapshot import create_snapshot_metadata  # noqa: E402
from wanxiang_runtime.state import InMemoryCanonicalState, state_to_primitive  # noqa: E402


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(name: str, payload: dict[str, object]) -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    (TARGET / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {TARGET / name}")


def git_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def git_branch() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def build_events_fixture() -> dict[str, object]:
    events = build_fixture_events()
    final_state = ReplayEngine(RULES, SCHEMA).replay(events)
    return {
        "schema_version": SCHEMA.value,
        "instance_id": INSTANCE.value,
        "branch_id": BRANCH.value,
        "rule_version": RULES.value,
        "final_revision": final_state.revision.value,
        "expected_semantic_hash": final_state.semantic_hash(),
        "events": [event_to_primitive(e) for e in events],
    }


def build_snapshot_fixture() -> dict[str, object]:
    events = build_fixture_events()
    final_state = ReplayEngine(RULES, SCHEMA).replay(events)
    metadata = create_snapshot_metadata(
        final_state,
        EventSeq(5),
        snapshot_id=SnapshotId("snap_golden_v52"),
        content_ref="fixture://v5_2_baseline/snapshot.json",
    )
    return {
        "schema_version": SCHEMA.value,
        "metadata": snapshot_to_primitive(metadata),
        "state": state_to_primitive(final_state),
        "expected_semantic_hash": final_state.semantic_hash(),
    }


def build_branch_fixture() -> dict[str, object]:
    parent_events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    parent_state = engine.replay(parent_events)
    parent_hash = parent_state.semantic_hash()

    parent_meta = BranchMetadata(
        branch_id=BRANCH,
        instance_id=INSTANCE,
        ancestry=BranchAncestry(),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    child_id = BranchId("br_golden_child")
    child_meta = fork_branch(
        parent_meta,
        parent_state,
        fork_revision=BranchRevision(5),
        fork_event_seq=EventSeq(5),
        snapshot_ref="fixture://v5_2_baseline/snapshot.json",
        branch_id=child_id,
    )

    store = InMemoryEventStore()
    fixed_ts = CommitTimestamp.from_isoformat("2026-08-14T00:00:00+00:00")
    authority = CommitAuthority(
        store,
        RULES,
        SCHEMA,
        branch_base_revision=BranchRevision(5),
        now=lambda: fixed_ts,
    )
    child_state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=child_id,
        revision=BranchRevision(5),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    for entity in parent_state.entities():
        child_state = child_state.apply(
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=entity.entity_id,
                        entity_type=entity.entity_type,
                        components=tuple(entity.components.values()),
                    ),
                )
            )
        )
    child_state = child_state.with_revision(BranchRevision(5))
    child_req = CommitRequest(
        command_id=CommandId("cmd_child"),
        instance_id=INSTANCE,
        branch_id=child_id,
        expected_revision=BranchRevision(5),
        delta=ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("carol"), entity_type="person"),)
        ),
        world_time=WorldTime(6),
        rule_version=RULES,
    )
    authority.commit(child_state.with_branch(child_id), child_req)
    child_events = store.load(INSTANCE, child_id)
    # Normalize random commit metadata so the fixture is reproducible.
    child_events = tuple(
        replace(
            e,
            event_id=EventId(f"evt_child_{index}"),
            trace_id=TraceId(f"trc_child_{index}"),
            commit_timestamp=fixed_ts,
        )
        for index, e in enumerate(child_events, start=1)
    )
    child_hash = (
        ReplayEngine(RULES, SCHEMA).replay(child_events, parent_state, start_seq=1).semantic_hash()
    )

    return {
        "schema_version": SCHEMA.value,
        "parent_branch_id": BRANCH.value,
        "parent_expected_semantic_hash": parent_hash,
        "parent_events": [event_to_primitive(e) for e in parent_events],
        "child_branch_id": child_id.value,
        "child_ancestry": ancestry_to_primitive(child_meta.ancestry),
        "child_expected_semantic_hash": child_hash,
        "child_events": [event_to_primitive(e) for e in child_events],
    }


def build_worldpack_fixture() -> dict[str, object]:
    import reference_worlds.synthetic_full.synthetic_full as sf  # noqa: PLC0415

    source = ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"
    manifests = sf.build_manifests()
    return {
        "source": "reference_worlds/synthetic_full/synthetic_full.py",
        "source_sha256": sha256_bytes(source.read_bytes()),
        "manifests": [m.canonical() for m in manifests],
        "expected_hashes": {m.package_id: m.compute_hash() for m in manifests},
    }


def build_api_fixture() -> dict[str, object]:
    from wanxiang_api.app import create_app  # noqa: PLC0415

    from export_openapi import build_contract  # noqa: PLC0415

    return build_contract(create_app())


def main() -> int:
    payloads: dict[str, dict[str, object]] = {
        "events.json": build_events_fixture(),
        "snapshot.json": build_snapshot_fixture(),
        "branch.json": build_branch_fixture(),
        "worldpack.json": build_worldpack_fixture(),
        "api.json": build_api_fixture(),
    }
    for name, payload in payloads.items():
        write_json(name, payload)

    hashes: dict[str, str] = {}
    for name in sorted(payloads):
        hashes[name] = sha256_bytes((TARGET / name).read_bytes())
    combined = sha256_bytes(
        "\n".join(f"{name}:{hashes[name]}" for name in sorted(hashes)).encode("utf-8")
    )
    manifest: dict[str, object] = {
        "kind": "V5_2_BASELINE_MANIFEST",
        "git_head": git_head(),
        "git_branch": git_branch(),
        "python_version": sys.version.split()[0],
        "files": hashes,
        "combined_semantic_hash": combined,
    }
    write_json("manifest.json", manifest)
    print(f"combined_semantic_hash={combined}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
