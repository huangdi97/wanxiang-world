"""Derived-state reader with a validated cache (application layer).

Reading canonical state is O(events) if replayed every time. This reader caches
the derived state per (instance, branch) and validates freshness against the
event-store head before reuse, so direct out-of-band writes are never masked.
"""

from __future__ import annotations

from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_application.ports import PersistenceBundle


class StateReader:
    def __init__(
        self,
        persistence: PersistenceBundle,
        rule_version: RuntimeVersion,
        schema_version: SchemaVersion,
    ) -> None:
        self._persistence = persistence
        self._rule_version = rule_version
        self._schema_version = schema_version
        self._cache: dict[tuple[str, str], InMemoryCanonicalState] = {}

    def state_at(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        upto_seq: EventSeq | None = None,
    ) -> InMemoryCanonicalState:
        cache_key = (instance_id.value, branch_id.value)
        cached = self._cache.get(cache_key)
        if upto_seq is None and cached is not None:
            branch_meta = self._persistence.branches.get(branch_id)
            base = (
                branch_meta.ancestry.fork_revision.value
                if branch_meta.ancestry.fork_revision is not None
                else 0
            )
            head = base + self._persistence.event_store.last_event_seq(instance_id, branch_id).value
            if cached.revision.value == head:
                return cached
            self._cache.pop(cache_key, None)
        branch = self._persistence.branches.get(branch_id)
        events = self._persistence.event_store.load(instance_id, branch_id)
        if upto_seq is not None:
            events = [e for e in events if e.event_seq.value <= upto_seq.value]
        engine = ReplayEngine(self._rule_version, self._schema_version)
        if branch.ancestry.parent_branch_id is not None:
            parent = self.state_at(
                instance_id,
                branch.ancestry.parent_branch_id,
                upto_seq=branch.ancestry.fork_event_seq,
            )
            state = engine.replay(events, baseline=parent, start_seq=1)
        elif not events:
            state = InMemoryCanonicalState(
                instance_id=instance_id,
                branch_id=branch_id,
                revision=BranchRevision(0),
                schema_version=self._schema_version,
                rule_version=self._rule_version,
            )
        else:
            state = engine.replay(events)
        state = state.with_branch(branch_id)
        if upto_seq is None:
            self._cache[cache_key] = state
        return state

    def update(
        self, instance_id: WorldInstanceId, branch_id: BranchId, state: InMemoryCanonicalState
    ) -> None:
        self._cache[(instance_id.value, branch_id.value)] = state

    def invalidate(self) -> None:
        self._cache.clear()
