"""Commit Authority: the only authoritative mutation pathway.

A Commit Authority accepts validated/resolved proposals, enforces commit
preconditions and core invariants, applies the delta deterministically, emits a
committed event through the append port, advances the branch revision and
produces an audit record. No transport, UI, model provider or plugin may mutate
canonical state outside this path.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import (
    Conflict,
    IncompatibleVersion,
    StaleRevision,
    ValidationRejected,
)
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    CommandId,
    CorrelationId,
    EventId,
    TraceId,
    WorldInstanceId,
)
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_domain.world_commit import (
    DELTA_SCHEMA_VERSION,
    WorldCommitKind,
    validate_world_commit_kind,
)

from wanxiang_runtime.audit import AuditRecord
from wanxiang_runtime.canonical_write import (
    CanonicalWriteLease,
    mint_canonical_write_lease,
)
from wanxiang_runtime.invariants import InvariantCheck, check_layered_delta_invariants
from wanxiang_runtime.ports import EventAppendPort
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta

DEFAULT_SCHEMA_VERSION = SchemaVersion(1)
DEFAULT_BRANCH_BASE_REVISION = BranchRevision(0)

Now = Callable[[], CommitTimestamp]


@dataclass(frozen=True, slots=True)
class CommitRequest:
    command_id: CommandId
    instance_id: WorldInstanceId
    branch_id: BranchId
    expected_revision: BranchRevision
    delta: ProposedWorldDelta
    world_time: WorldTime
    rule_version: RuntimeVersion
    actor_id: ActorId | None = None
    causation_id: CommandId | None = None
    correlation_id: CorrelationId | None = None
    kind: WorldCommitKind = "state"
    delta_schema_version: int = DELTA_SCHEMA_VERSION


@dataclass(frozen=True, slots=True)
class CommitResult:
    event: CommittedEvent
    state_after: InMemoryCanonicalState
    audit: AuditRecord


class CommitAuthority:
    """Executes the commit precondition -> apply -> append -> advance cycle."""

    def __init__(
        self,
        event_port: EventAppendPort,
        rule_version: RuntimeVersion,
        schema_version: SchemaVersion = DEFAULT_SCHEMA_VERSION,
        branch_base_revision: BranchRevision = DEFAULT_BRANCH_BASE_REVISION,
        now: Now = CommitTimestamp.now,
        domain_invariants: tuple[InvariantCheck, ...] = (),
        world_invariants: tuple[InvariantCheck, ...] = (),
    ) -> None:
        self._event_port = event_port
        self._rule_version = rule_version
        self._schema_version = schema_version
        self._branch_base_revision = branch_base_revision
        self._now = now
        self._domain_invariants = domain_invariants
        self._world_invariants = world_invariants

    def commit(self, state: InMemoryCanonicalState, request: CommitRequest) -> CommitResult:
        request_kind = validate_world_commit_kind(request.kind)
        self._enforce_preconditions(state, request)
        # Kernel -> Domain -> World invariant layers are monotonic: any layer may
        # deny, and no later layer can turn that denial into an allow.
        check_layered_delta_invariants(
            state,
            request.delta,
            domain=self._domain_invariants,
            world=self._world_invariants,
        )
        # apply_delta rechecks Kernel invariants and returns a pure new state.
        applied = apply_delta(state, request.delta)
        next_revision = BranchRevision(state.revision.value + 1)
        state_after = applied.with_revision(next_revision)
        event_id = EventId.generate()
        trace_id = TraceId.generate()
        event = CommittedEvent(
            event_id=event_id,
            instance_id=request.instance_id,
            branch_id=request.branch_id,
            event_seq=EventSeq(
                self._event_port.last_event_seq(request.instance_id, request.branch_id).value + 1
            ),
            revision=next_revision,
            schema_version=self._schema_version,
            command_id=request.command_id,
            delta=request.delta,
            world_time=request.world_time,
            rule_version=self._rule_version,
            actor_id=request.actor_id,
            causation_id=request.causation_id,
            correlation_id=request.correlation_id,
            trace_id=trace_id,
            commit_timestamp=self._now(),
        )
        # R7 Gate C: the authority mints exactly one lease for this worldline and
        # presents it to the append port. The audit ref ties the credential to the
        # authority rule version and the command that produced the event.
        lease = mint_canonical_write_lease(
            instance_id=request.instance_id,
            branch_id=request.branch_id,
            audit_ref=f"authority:{self._rule_version.value}#{request.command_id.value}",
        )
        # Atomic append: if this raises, no new state is exposed.
        self._event_port.append(event, lease=lease)
        audit = AuditRecord(
            trace_id=trace_id,
            command_id=request.command_id,
            event_id=event_id,
            instance_id=request.instance_id,
            branch_id=request.branch_id,
            revision=next_revision,
            rule_version=self._rule_version,
            world_time=request.world_time,
            actor_id=request.actor_id,
            correlation_id=request.correlation_id,
            commit_timestamp=event.commit_timestamp,
            kind=request_kind,
            delta_schema_version=request.delta_schema_version,
        )
        return CommitResult(event=event, state_after=state_after, audit=audit)

    def _enforce_preconditions(self, state: InMemoryCanonicalState, request: CommitRequest) -> None:
        if state.instance_id != request.instance_id or state.branch_id != request.branch_id:
            raise Conflict("commit request targets a different instance/branch than the state")
        current_revision = BranchRevision(
            self._branch_base_revision.value
            + self._event_port.last_event_seq(request.instance_id, request.branch_id).value
        )
        if request.expected_revision != current_revision:
            raise StaleRevision(
                "expected revision "
                f"{request.expected_revision.value}, current {current_revision.value}"
            )
        if state.revision != request.expected_revision:
            raise Conflict("state revision does not match the expected revision")
        if request.rule_version != self._rule_version:
            raise IncompatibleVersion(
                "commit rule version "
                f"{request.rule_version.value} != authority {self._rule_version.value}"
            )
        if request.delta.is_empty():
            raise ValidationRejected("cannot commit an empty ProposedWorldDelta")


def authorize_structural_write(
    *,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    audit_ref: str,
) -> CanonicalWriteLease:
    """Authority-side grant of a lease for a structural canonical row.

    Structural rows (world instance, branch, snapshot, audit trace) are written by
    the application runtime rather than by a single `commit`, but only the Commit
    Authority may turn "write this row" into a credential. This module is therefore
    the sole production caller of `mint_canonical_write_lease`; a caller must ask
    the authority for a lease and may never mint one itself.

    Args:
        instance_id: The world instance the granted lease authorizes.
        branch_id: The worldline the granted lease authorizes.
        audit_ref: Deterministic provenance string recorded with the credential.
    """
    return mint_canonical_write_lease(
        instance_id=instance_id, branch_id=branch_id, audit_ref=audit_ref
    )
