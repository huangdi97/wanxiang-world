"""Application runtime: orchestrates the authoritative world vertical slice."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.audit import AuditRecord
from wanxiang_runtime.authority import (
    CommitAuthority,
    CommitRequest,
    authorize_structural_write,
)
from wanxiang_runtime.branch import fork_branch
from wanxiang_runtime.canonical_write import CanonicalWriteLease
from wanxiang_runtime.diff import StateDiff, diff_states
from wanxiang_runtime.invariants import InvariantCheck
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.snapshot import create_snapshot_metadata
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.replay_support import RestoreResult, replay_branch
from wanxiang_application.state_reader import StateReader
from wanxiang_application.world_lookup import find_root_branch

DEFAULT_SCHEMA_VERSION = SchemaVersion(1)
DEFAULT_WORLD_TIME = WorldTime(0)
Now = Callable[[], CommitTimestamp]


@dataclass(frozen=True, slots=True)
class CreateWorldResult:
    instance_id: WorldInstanceId
    root_branch_id: BranchId
    revision: BranchRevision


@dataclass(frozen=True, slots=True)
class SubmitCommandResult:
    event: CommittedEvent
    state: InMemoryCanonicalState
    audit: AuditRecord | None
    duplicate: bool = False


class WorldRuntime:
    """Authoritative application runtime (no HTTP/ORM/LLM dependencies)."""

    def __init__(
        self,
        persistence: PersistenceBundle,
        rule_version: RuntimeVersion,
        schema_version: SchemaVersion = DEFAULT_SCHEMA_VERSION,
        resolvers: ResolverRegistry | None = None,
        now: Now = CommitTimestamp.now,
        domain_invariants: tuple[InvariantCheck, ...] = (),
        world_invariants: tuple[InvariantCheck, ...] = (),
    ) -> None:
        self.persistence = persistence
        self._rule_version = rule_version
        self._schema_version = schema_version
        self._resolvers = resolvers or ResolverRegistry()
        self._now = now
        self._domain_invariants = domain_invariants
        self._world_invariants = world_invariants
        self._state_reader = StateReader(persistence, rule_version, schema_version)

    def _structural_lease(
        self, instance_id: WorldInstanceId, branch_id: BranchId, reference: str
    ) -> CanonicalWriteLease:
        # Structural canonical rows (instance/branch/snapshot/audit trace) are written
        # by this runtime, but the Commit Authority is the only minter; the runtime
        # asks the authority for a credential instead of minting one itself.
        return authorize_structural_write(
            instance_id=instance_id, branch_id=branch_id, audit_ref=f"world_runtime:{reference}"
        )

    # -- instance / branch lifecycle ------------------------------------

    def create_world(
        self,
        instance_id: WorldInstanceId | None = None,
        world_time: WorldTime = DEFAULT_WORLD_TIME,
    ) -> CreateWorldResult:
        instance_id = instance_id or WorldInstanceId.generate()
        root_branch = BranchId.generate()
        lease = self._structural_lease(instance_id, root_branch, "create_world")
        self.persistence.instances.create(
            instance_id,
            self._schema_version,
            self._rule_version,
            world_time,
            lease=lease,
        )
        self.persistence.branches.save(
            BranchMetadata(
                branch_id=root_branch,
                instance_id=instance_id,
                ancestry=BranchAncestry(),
                schema_version=self._schema_version,
                rule_version=self._rule_version,
            ),
            lease=lease,
        )
        return CreateWorldResult(
            instance_id=instance_id,
            root_branch_id=root_branch,
            revision=BranchRevision(0),
        )

    def find_existing_world(self, instance_id: WorldInstanceId) -> CreateWorldResult | None:
        root_branch_id = find_root_branch(self.persistence, instance_id)
        if root_branch_id is None:
            return None
        return CreateWorldResult(instance_id, root_branch_id, BranchRevision(0))

    def create_branch(
        self,
        instance_id: WorldInstanceId,
        parent_branch_id: BranchId,
        *,
        fork_revision: BranchRevision | None = None,
    ) -> BranchMetadata:
        parent = self.persistence.branches.get(parent_branch_id)
        parent_state = self._state_reader.state_at(instance_id, parent_branch_id)
        revision = fork_revision or parent_state.revision
        if revision.value > parent_state.revision.value:
            from wanxiang_domain.errors import ValidationRejected

            raise ValidationRejected("cannot fork beyond the parent head")
        fork_events = [
            e
            for e in self.persistence.event_store.load(instance_id, parent_branch_id)
            if e.revision.value <= revision.value
        ]
        fork_event_seq = EventSeq(len(fork_events))
        snapshot_ref = f"mem://{parent_branch_id.value}/fork/{revision.value}"
        child = fork_branch(
            parent,
            parent_state,
            fork_revision=revision,
            fork_event_seq=fork_event_seq,
            snapshot_ref=snapshot_ref,
        )
        branch_lease = self._structural_lease(instance_id, child.branch_id, "create_branch")
        self.persistence.branches.save(child, lease=branch_lease)
        # Persist a snapshot of the fork baseline so restore/replay is deterministic.
        fork_state = self._state_reader.state_at(
            instance_id, parent_branch_id, upto_seq=fork_event_seq
        )
        # The fork-baseline snapshot is keyed by the parent branch at the fork
        # revision (fork_state keeps the parent branch id), so it needs its own
        # lease scoped to that worldline.
        snapshot_lease = self._structural_lease(
            instance_id, fork_state.branch_id, "create_branch_snapshot"
        )
        self.persistence.snapshot_store.save(
            create_snapshot_metadata(fork_state, fork_event_seq, content_ref=snapshot_ref),
            fork_state,
            lease=snapshot_lease,
        )
        return child

    # -- command submission ---------------------------------------------

    def submit_command(self, command: CommandEnvelope) -> SubmitCommandResult:
        prior = self.persistence.event_store.command_result_event(command.command_id)
        if prior is not None:
            state = self._state_reader.state_at(command.instance_id, command.branch_id)
            return SubmitCommandResult(event=prior, state=state, audit=None, duplicate=True)

        branch = self.persistence.branches.get(command.branch_id)
        base = (
            branch.ancestry.fork_revision.value if branch.ancestry.fork_revision is not None else 0
        )
        state = self._state_reader.state_at(command.instance_id, command.branch_id)
        delta = self._resolvers.resolve(command, state)
        authority = CommitAuthority(
            self.persistence.event_store,
            self._rule_version,
            self._schema_version,
            branch_base_revision=BranchRevision(base),
            now=self._now,
            domain_invariants=self._domain_invariants,
            world_invariants=self._world_invariants,
        )
        result = authority.commit(
            state,
            CommitRequest(
                command_id=command.command_id,
                instance_id=command.instance_id,
                branch_id=command.branch_id,
                expected_revision=command.expected_revision,
                delta=delta,
                world_time=command.world_time or WorldTime(state.revision.value + 1),
                rule_version=self._rule_version,
                actor_id=command.actor_id,
                causation_id=command.causation_id,
                correlation_id=command.correlation_id,
            ),
        )
        if self.persistence.audit is not None:
            self.persistence.audit.record(
                result.audit,
                lease=self._structural_lease(
                    command.instance_id, command.branch_id, "submit_command_audit"
                ),
            )
        self._state_reader.update(command.instance_id, command.branch_id, result.state_after)
        return SubmitCommandResult(event=result.event, state=result.state_after, audit=result.audit)

    def action_types(self) -> tuple[str, ...]:
        """Registered deterministic action types (the legal action space)."""
        return self._resolvers.action_types()

    def invalidate_state_cache(self) -> None:
        """Drop cached derived state so the next read re-derives from events.

        The cache is a projection optimization; diagnostics that mutate the
        event store directly must invalidate it before querying.
        """
        self._state_reader.invalidate()

    # -- queries --------------------------------------------------------

    def current_state(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> InMemoryCanonicalState:
        return self._state_reader.state_at(instance_id, branch_id)

    def events(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> tuple[CommittedEvent, ...]:
        return self.persistence.event_store.load(instance_id, branch_id)

    def create_checkpoint(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> SnapshotMetadata:
        state = self._state_reader.state_at(instance_id, branch_id)
        seq = self.persistence.event_store.last_event_seq(instance_id, branch_id)
        metadata = create_snapshot_metadata(state, seq)
        self.persistence.snapshot_store.save(
            metadata, state, lease=self._structural_lease(instance_id, branch_id, "checkpoint")
        )
        return metadata

    def restore_and_replay(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> RestoreResult:
        return replay_branch(
            self.persistence,
            self._state_reader,
            self._rule_version,
            self._schema_version,
            instance_id,
            branch_id,
        )

    def diff(
        self,
        instance_id: WorldInstanceId,
        branch_a: BranchId,
        branch_b: BranchId,
    ) -> StateDiff:
        return diff_states(
            self._state_reader.state_at(instance_id, branch_a),
            self._state_reader.state_at(instance_id, branch_b),
        )

    def metrics(self, instance_id: WorldInstanceId) -> dict[str, int]:
        branches = self.persistence.branches.list(instance_id)
        event_count = 0
        for branch in branches:
            event_count += len(self.persistence.event_store.load(instance_id, branch.branch_id))
        snapshot_count = 0
        for branch in branches:
            snapshots = self.persistence.snapshot_store.latest(instance_id, branch.branch_id)
            if snapshots is not None:
                snapshot_count += 1
        return {
            "branches": len(branches),
            "events": event_count,
            "snapshots": snapshot_count,
        }

    # -- internals ------------------------------------------------------
