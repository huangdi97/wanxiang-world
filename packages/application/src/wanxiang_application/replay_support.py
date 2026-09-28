"""Restore canonical state by replaying a branch (snapshot baseline or events).

Extracted from the application runtime so the authoritative runtime file stays a
single, readable orchestration unit. Behaviour is unchanged: a root branch uses a
validated snapshot baseline when one exists and otherwise replays authoritative
events, while a child branch replays its own events over the parent state at the
fork point.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.snapshot_policy import snapshot_is_valid
from wanxiang_application.state_reader import StateReader


@dataclass(frozen=True, slots=True)
class RestoreResult:
    state: InMemoryCanonicalState
    used_snapshot: bool
    snapshot_rejected: bool = False


def replay_branch(
    persistence: PersistenceBundle,
    state_reader: StateReader,
    rule_version: RuntimeVersion,
    schema_version: SchemaVersion,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> RestoreResult:
    """Restore `(instance_id, branch_id)` from a snapshot baseline or events."""
    branch = persistence.branches.get(branch_id)
    events = persistence.event_store.load(instance_id, branch_id)
    if branch.ancestry.parent_branch_id is not None:
        # Child branch: replay its own events over the parent state at the fork
        # point (parent_branch_id is non-None here by construction).
        engine = ReplayEngine(rule_version, schema_version)
        parent = state_reader.state_at(
            instance_id,
            branch.ancestry.parent_branch_id,
            upto_seq=branch.ancestry.fork_event_seq,
        )
        return RestoreResult(
            state=engine.replay(events, baseline=parent, start_seq=1),
            used_snapshot=False,
        )
    latest = None
    try:
        latest = persistence.snapshot_store.latest(instance_id, branch_id)
    except WanxiangError:
        latest = None  # unreadable snapshot store: fall back to events
    usable = False
    if latest is not None:
        try:
            usable = snapshot_is_valid(
                latest, events, rule_version=rule_version, schema_version=schema_version
            )
        except WanxiangError:
            usable = False  # decode/validation failed: fall back to events
    if usable:
        assert latest is not None
        remaining = [e for e in events if e.event_seq.value > latest.metadata.event_seq.value]
        state = ReplayEngine(rule_version, schema_version).replay(remaining, baseline=latest.state)
        return RestoreResult(state=state, used_snapshot=True)
    # Corrupt/incompatible/unreadable snapshot: fall back to authoritative events
    # (observable via snapshot_rejected when a snapshot existed).
    engine = ReplayEngine(rule_version, schema_version)
    return RestoreResult(
        state=engine.replay(events),
        used_snapshot=False,
        snapshot_rejected=latest is not None,
    )
