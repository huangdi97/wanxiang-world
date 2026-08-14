"""Replay engine: rebuild canonical state from committed events.

Replay uses the same trusted delta-application semantics as Commit Authority
(`InMemoryCanonicalState.apply`); it never invents a second mutation model.
Corrupt/incompatible history fails explicitly.
"""

from __future__ import annotations

from collections.abc import Sequence

from wanxiang_domain.errors import CorruptEventStream, IncompatibleVersion
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

from wanxiang_runtime.state import InMemoryCanonicalState


class ReplayEngine:
    """Deterministic replay of an ordered committed-event stream."""

    def __init__(
        self,
        rule_version: RuntimeVersion,
        schema_version: SchemaVersion,
    ) -> None:
        self._rule_version = rule_version
        self._schema_version = schema_version

    def replay(
        self,
        events: Sequence[CommittedEvent],
        baseline: InMemoryCanonicalState | None = None,
        *,
        start_seq: int | None = None,
    ) -> InMemoryCanonicalState:
        if not events:
            if baseline is None:
                raise CorruptEventStream("replay requires events or a baseline")
            return baseline
        instance_id = events[0].instance_id
        branch_id = events[0].branch_id
        state = baseline or InMemoryCanonicalState(
            instance_id=instance_id,
            branch_id=branch_id,
            revision=BranchRevision(0),
            schema_version=self._schema_version,
            rule_version=self._rule_version,
        )
        # Branch-local stream sequence and revision are independent counters:
        # - a fresh/root stream starts at seq 1;
        # - a child branch restarts its own local seq at 1 while revision
        #   continues from the fork baseline (callers pass start_seq=1);
        # - replaying events after a snapshot baseline continues the same
        #   branch's local seq (default: baseline.revision + 1, which equals
        #   the next seq for root branches where seq == revision).
        expected_seq = start_seq if start_seq is not None else state.revision.value + 1
        expected_revision = state.revision.value + 1
        for event in events:
            self._check_event(event, instance_id, branch_id, expected_seq, expected_revision)
            state = state.apply(event.delta).with_revision(event.revision)
            expected_seq += 1
            expected_revision += 1
        return state

    def _check_event(
        self,
        event: CommittedEvent,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        expected_seq: int,
        expected_revision: int,
    ) -> None:
        if event.instance_id != instance_id or event.branch_id != branch_id:
            raise CorruptEventStream("event instance/branch does not match the stream")
        if event.event_seq.value != expected_seq:
            raise CorruptEventStream(
                f"expected event seq {expected_seq}, got {event.event_seq.value}"
            )
        if event.revision.value != expected_revision:
            raise CorruptEventStream(
                f"event revision {event.revision.value} does not match expected {expected_revision}"
            )
        if event.schema_version != self._schema_version:
            raise IncompatibleVersion(
                "event schema version "
                f"{event.schema_version.value} != replay {self._schema_version.value}"
            )
        if event.rule_version != self._rule_version:
            raise IncompatibleVersion(
                "event rule version "
                f"{event.rule_version.value} != replay {self._rule_version.value}"
            )
