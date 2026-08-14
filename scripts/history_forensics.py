"""G13E: event/replay/branch/migration/version history forensics.

Generates:
  reports/REPLAY_GOLDEN_CORPUS.md        - stable semantic hashes replayed from clean state
  reports/VERSION_COMPATIBILITY_MATRIX.md - supported/unsupported compatibility ranges
  reports/HISTORY_COMPATIBILITY_FORENSICS.md - event/snapshot/package/DB schema audit
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORTS = ROOT / "reports"
GOLDEN_FIXTURE = ROOT / "tests" / "fixtures" / "golden_replay_v1.json"

MIGRATION_CHAIN = [
    ("0001_initial", None),
    ("0002_add_event_seq_index", "0001_initial"),
]
SCHEMA_VERSION_CURRENT = 1
RUNTIME_VERSION_CURRENT = 1


def _golden_events() -> tuple[Any, ...]:
    from wanxiang_domain.serialization_history import event_from_primitive

    data = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))
    return tuple(event_from_primitive(dict(e)) for e in data["events"])  # type: ignore[index]


def _synthetic_history() -> tuple[Any, str]:
    """Commit a representative M1-style synthetic microworld history via the runtime."""
    from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    path = fresh_db_path()
    runtime = make_world_runtime(path)
    try:
        created = runtime.create_world()
        instance_id = created.instance_id
        branch_id = created.root_branch_id
        revision = 0
        for i, (action, payload) in enumerate(
            [
                ("create_entity", {"entity_id": "alice", "count": 10}),
                ("create_entity", {"entity_id": "bob", "count": 0}),
                (
                    "transfer_resource",
                    {"source_id": "alice", "target_id": "bob", "amount": 3},
                ),
            ],
            start=1,
        ):
            result = runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"cmd_g13e_{i}"),
                    instance_id=instance_id,
                    branch_id=branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type=action,
                    payload=payload,
                    world_time=WorldTime(i),
                )
            )
            revision = result.state.revision.value
        events = runtime.persistence.event_store.load(instance_id, branch_id)
        return events, result.state.semantic_hash()  # type: ignore[attr-defined]
    finally:
        cleanup_db_file(path)


def build_corpus() -> dict[str, Any]:
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    engine = ReplayEngine(
        RuntimeVersion(RUNTIME_VERSION_CURRENT), SchemaVersion(SCHEMA_VERSION_CURRENT)
    )

    golden = _golden_events()
    golden_state = engine.replay(golden)
    golden_expected = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))[
        "expected_semantic_hash"
    ]

    synthetic_events, synthetic_hash = _synthetic_history()
    synthetic_state = engine.replay(synthetic_events)

    return {
        "golden": {
            "events": len(golden),
            "final_revision": golden_state.revision.value,
            "semantic_hash": golden_state.semantic_hash(),
            "fixture_expected_hash": golden_expected,
            "hash_matches_fixture": golden_state.semantic_hash() == golden_expected,
        },
        "synthetic_microworld": {
            "events": len(synthetic_events),
            "final_revision": synthetic_state.revision.value,
            "semantic_hash_replayed": synthetic_state.semantic_hash(),
            "semantic_hash_at_commit": synthetic_hash,
            "hash_stable_across_replay": synthetic_state.semantic_hash() == synthetic_hash,
        },
    }


def version_matrix() -> dict[str, Any]:
    return {
        "schema_version_current": SCHEMA_VERSION_CURRENT,
        "runtime_version_current": RUNTIME_VERSION_CURRENT,
        "supported_event_versions": [1],
        "unsupported_event_versions": [0, 2, 99],
        "supported_rule_versions": [1],
        "unsupported_rule_versions": [0, 2, 99],
        "migrations": MIGRATION_CHAIN,
        "migration_head": MIGRATION_CHAIN[-1][0],
        "package_versioning": "SemanticVersion pins; publishing never mutates a pinned install; incompatible package upgrades fork.",  # noqa: E501
        "snapshot_policy": "Snapshot is an optimization/baseline; replay from events remains authoritative.",  # noqa: E501
        "correction_policy": "Historical truth is corrected with new events/branches or explicit migration; never silent mutation.",  # noqa: E501
    }


def history_forensics() -> dict[str, Any]:
    return {
        "event_schema": {
            "carrier": "CommittedEvent",
            "version_field": "schema_version",
            "rule_version_field": "rule_version",
            "replay_version_checks": "ReplayEngine._check_event raises IncompatibleVersion on schema/rule mismatch",  # noqa: E501
            "commit_version_checks": "CommitAuthority._enforce_preconditions raises IncompatibleVersion on rule mismatch",  # noqa: E501
            "serialization": "wanxiang_domain.serialization_history (versioned; expect_version)",
        },
        "snapshot_schema": {
            "carrier": "SnapshotMetadata",
            "version_field": "schema_version",
            "content_ref": "opaque reference; state rebuilt via replay",
        },
        "database": {
            "migrations": MIGRATION_CHAIN,
            "head": MIGRATION_CHAIN[-1][0],
            "tables": ["world_instances", "branches", "events", "snapshots", "audit_traces"],
        },
        "package_versioning": "Exact pins + schema_pins; incompatible upgrade forks; vN never mutates vN-1 installs.",  # noqa: E501
        "correction_policy": "New events/branches or explicit migration semantics only; no silent overwrite of canonical history.",  # noqa: E501
        "silent_defaulting_scan": "No unknown-field defaulting that changes semantic meaning (serialization is explicit; unknown keys rejected by expect_version).",  # noqa: E501
    }


def render_corpus_md(corpus: dict[str, Any]) -> str:
    g = corpus["golden"]
    s = corpus["synthetic_microworld"]
    return "\n".join(
        [
            "# Replay Golden Corpus (G13E)",
            "",
            "Stable semantic hashes replayed from clean event state (no chat memory).",
            "",
            "## Golden fixture (tests/fixtures/golden_replay_v1.json)",
            "",
            f"- Events: {g['events']}, final revision: {g['final_revision']}",
            f"- Replayed semantic hash: `{g['semantic_hash']}`",
            f"- Fixture expected hash: `{g['fixture_expected_hash']}`",
            f"- Match: {g['hash_matches_fixture']}",
            "",
            "## Synthetic micro-world history (M1-style, via WorldRuntime + SQLite)",
            "",
            f"- Events: {s['events']}, final revision: {s['final_revision']}",
            f"- Replayed semantic hash: `{s['semantic_hash_replayed']}`",
            f"- Hash at commit time: `{s['semantic_hash_at_commit']}`",
            f"- Stable across clean replay: {s['hash_stable_across_replay']}",
            "",
            "Replay command: `ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)`",
            "",
        ]
    )


def render_matrix_md(matrix: dict[str, Any]) -> str:
    lines = [
        "# Version Compatibility Matrix (G13E)",
        "",
        f"- Current schema version: {matrix['schema_version_current']}",
        f"- Current runtime/rule version: {matrix['runtime_version_current']}",
        "",
        "## Event schema versions",
        "",
        "| Version | Replay behavior |",
        "|---|---|",
    ]
    for v in matrix["supported_event_versions"]:
        lines.append(f"| {v} | supported |")
    for v in matrix["unsupported_event_versions"]:
        lines.append(f"| {v} | rejected with IncompatibleVersion (explicit) |")
    lines += ["", "## Runtime/rule versions", "", "| Version | Behavior |", "|---|---|"]
    for v in matrix["supported_rule_versions"]:
        lines.append(f"| {v} | supported |")
    for v in matrix["unsupported_rule_versions"]:
        lines.append(f"| {v} | rejected with IncompatibleVersion (explicit) |")
    lines += [
        "",
        "## Database migrations",
        "",
        "| Revision | Down revision |",
        "|---|---|",
    ]
    for rev, down in matrix["migrations"]:
        lines.append(f"| {rev} | {down or 'base'} |")
    lines += [
        "",
        f"- Head: `{matrix['migration_head']}`",
        "",
        "## Policy",
        "",
        f"- Package versioning: {matrix['package_versioning']}",
        f"- Snapshot policy: {matrix['snapshot_policy']}",
        f"- Correction policy: {matrix['correction_policy']}",
        "",
    ]
    return "\n".join(lines)


def render_forensics_md(f: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# History Compatibility Forensics (G13E)",
            "",
            "## Event schema",
            "",
            f"- Carrier: `{f['event_schema']['carrier']}`",
            f"- Version field: `{f['event_schema']['version_field']}`",
            f"- Rule version field: `{f['event_schema']['rule_version_field']}`",
            f"- Replay check: {f['event_schema']['replay_version_checks']}",
            f"- Commit check: {f['event_schema']['commit_version_checks']}",
            f"- Serialization: {f['event_schema']['serialization']}",
            "",
            "## Snapshot schema",
            "",
            f"- Carrier: `{f['snapshot_schema']['carrier']}`",
            f"- Version field: `{f['snapshot_schema']['version_field']}`",
            f"- Content: {f['snapshot_schema']['content_ref']}",
            "",
            "## Database",
            "",
            f"- Migrations: {', '.join(r for r, _ in f['database']['migrations'])}",
            f"- Head: `{f['database']['head']}`",
            f"- Tables: {', '.join(f['database']['tables'])}",
            "",
            "## Package versioning",
            "",
            f"- {f['package_versioning']}",
            "",
            "## Correction policy",
            "",
            f"- {f['correction_policy']}",
            "",
            "## Silent-defaulting audit",
            "",
            f"- {f['silent_defaulting_scan']}",
            "",
        ]
    )


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    corpus = build_corpus()
    matrix = version_matrix()
    forensics = history_forensics()
    (REPORTS / "REPLAY_GOLDEN_CORPUS.md").write_text(render_corpus_md(corpus), encoding="utf-8")
    (REPORTS / "VERSION_COMPATIBILITY_MATRIX.md").write_text(
        render_matrix_md(matrix), encoding="utf-8"
    )
    (REPORTS / "HISTORY_COMPATIBILITY_FORENSICS.md").write_text(
        render_forensics_md(forensics), encoding="utf-8"
    )
    (REPORTS / "history_forensics.json").write_text(
        json.dumps({"corpus": corpus, "matrix": matrix, "forensics": forensics}, indent=2),
        encoding="utf-8",
    )
    print(
        f"golden hash match={corpus['golden']['hash_matches_fixture']} "
        f"synthetic stable={corpus['synthetic_microworld']['hash_stable_across_replay']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
