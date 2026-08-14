"""G13E: event/replay/branch/migration/version history forensics tests.

- Golden replay corpus produces stable semantic hashes.
- Unsupported event/rule versions fail explicitly (no silent adoption).
- Version-pinned instances reject rule drift.
- Branch ancestry isolation through the runtime is preserved.
- Migration on a pre-head DB preserves event/replay invariants (semantic hash).
"""

from __future__ import annotations

import json
import os
import pathlib

import pytest
from alembic import command
from alembic.config import Config
from tests.conftest import make_world_runtime
from tests.helpers.replay_fixture import BRANCH, INSTANCE, build_fixture_events
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import IncompatibleVersion
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.database import create_engine_for
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_runtime.replay import ReplayEngine

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOLDEN_FIXTURE = ROOT / "tests" / "fixtures" / "golden_replay_v1.json"


def _golden_events() -> tuple[CommittedEvent, ...]:
    from typing import Any, cast

    from wanxiang_domain.serialization_history import event_from_primitive

    data = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))
    raw = cast(list[dict[str, Any]], data["events"])
    return tuple(event_from_primitive(e) for e in raw)


def _as_event(
    event: CommittedEvent, schema: int | None = None, rule: int | None = None
) -> CommittedEvent:
    from dataclasses import replace

    return replace(
        event,
        schema_version=SchemaVersion(schema) if schema is not None else event.schema_version,
        rule_version=RuntimeVersion(rule) if rule is not None else event.rule_version,
    )


def test_golden_corpus_replays_to_fixture_hash() -> None:
    events = _golden_events()
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    expected = json.loads(GOLDEN_FIXTURE.read_text(encoding="utf-8"))["expected_semantic_hash"]
    assert final.semantic_hash() == expected


def test_unsupported_event_schema_version_fails_explicitly() -> None:
    events = _golden_events()
    corrupted = (_as_event(events[0], schema=99),) + events[1:]
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(corrupted)


def test_unsupported_rule_version_fails_explicitly() -> None:
    events = _golden_events()
    corrupted = (_as_event(events[0], rule=99),) + events[1:]
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(corrupted)


def test_replay_corrupt_sequence_still_fails() -> None:
    """The corruption guard remains after the branch-seq/revision fix."""
    events = _golden_events()
    from dataclasses import replace

    from wanxiang_domain.errors import CorruptEventStream

    swapped = replace(events[0], event_seq=events[0].event_seq.__class__(99))
    with pytest.raises(CorruptEventStream):
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay((swapped,) + events[1:])


def test_version_pinned_instance_rejects_rule_drift() -> None:
    """Old history must not silently adopt new runtime semantics."""
    events = _golden_events()
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RuntimeVersion(2), SchemaVersion(1)).replay(events)
    # And schema drift is rejected too.
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RuntimeVersion(1), SchemaVersion(2)).replay(events)


def test_branch_ancestry_isolation_via_runtime(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    created = runtime.create_world()
    instance_id = created.instance_id
    root_branch = created.root_branch_id

    def submit(action: str, payload: dict[str, FieldValue], branch: BranchId, revision: int) -> int:
        result = runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"cmd_{action}_{revision}"),
                instance_id=instance_id,
                branch_id=branch,
                expected_revision=BranchRevision(revision),
                action_type=action,
                payload=payload,
                world_time=WorldTime(revision + 1),
            )
        )
        return result.state.revision.value

    submit("create_entity", {"entity_id": "alice", "count": 10}, root_branch, 0)
    submit("create_entity", {"entity_id": "bob", "count": 0}, root_branch, 1)
    parent_hash = runtime.current_state(instance_id, root_branch).semantic_hash()

    child = runtime.create_branch(instance_id, root_branch)
    assert child.ancestry.parent_branch_id == root_branch
    submit("create_entity", {"entity_id": "carol", "count": 5}, child.branch_id, 2)

    # Parent history is untouched by the child commit.
    parent_state = runtime.current_state(instance_id, root_branch)
    assert parent_state.semantic_hash() == parent_hash
    parent_events = runtime.persistence.event_store.load(instance_id, root_branch)
    assert len(parent_events) == 2

    # Cold child replay (cache invalidated) and restore_and_replay both rebuild
    # the child state from events with the same semantic hash (G13E P0 fix).
    child_hash = runtime.current_state(instance_id, child.branch_id).semantic_hash()
    runtime.invalidate_state_cache()
    cold = runtime.current_state(instance_id, child.branch_id)
    assert cold.semantic_hash() == child_hash
    restored = runtime.restore_and_replay(instance_id, child.branch_id)
    assert restored.state.semantic_hash() == child_hash


def test_migration_preserves_replay_semantic_hash(persist_db_path: pathlib.Path) -> None:
    """Upgrade from 0001 (pre-head) to head preserves events and replay hash."""
    from sqlalchemy.orm import sessionmaker

    path = persist_db_path
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "0001_initial")
        factory = sessionmaker(
            bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
        )
        store = SqlAlchemyEventStore(factory)
        for event in build_fixture_events():
            store.append(event)
        before = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
            store.load(INSTANCE, BRANCH)
        )
        before_hash = before.semantic_hash()
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        os.environ.pop("WANXIANG_DATABASE_URL", None)

    factory2 = sessionmaker(
        bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
    )
    store2 = SqlAlchemyEventStore(factory2)
    after = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(store2.load(INSTANCE, BRANCH))
    assert after.semantic_hash() == before_hash
    assert after.revision.value == 5
    engine = factory2.kw["bind"]
    engine.dispose()
