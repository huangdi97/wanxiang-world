"""G92D replay-safe logical compaction tests."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import SnapshotId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import CompactionPolicy, CompactionService


def _snapshot() -> SnapshotMetadata:
    return SnapshotMetadata(
        snapshot_id=SnapshotId("snap-g92d"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(5),
        event_seq=EventSeq(5),
        schema_version=SCHEMA,
        rule_version=RULES,
        created_world_time=WorldTime(5),
        content_ref="mem://snap-g92d",
    )


def test_compaction_keeps_refs_and_memory_summary_boundaries() -> None:
    manifest = CompactionService(
        CompactionPolicy(retain_recent_events=2, memory_summary_every_events=2)
    ).compact(
        build_fixture_events(),
        _snapshot(),
        replay_hash_before="golden",
        replay_hash_after="golden",
    )
    assert manifest.compacted is True
    assert manifest.source_event_count == 5
    assert [item.event_seq for item in manifest.archived_event_refs] == [1, 2, 3]
    assert manifest.retained_event_seqs == (4, 5)
    assert [
        (item.start_event_seq, item.end_event_seq) for item in manifest.memory_summary_refs
    ] == [
        (1, 2),
        (3, 3),
    ]
    assert manifest.archive_ref.endswith("through-3")


def test_compaction_rejects_non_golden_replay() -> None:
    with pytest.raises(ContractError):
        CompactionService().compact(
            build_fixture_events(),
            _snapshot(),
            replay_hash_before="before",
            replay_hash_after="after",
        )
