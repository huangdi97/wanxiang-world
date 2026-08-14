"""ISA -> existing pipeline mapping (G30E).

A thin adapter that executes World Semantic ISA instructions through the
EXISTING machinery ? CommitAuthority (single mutation boundary), the branch
fork API, and kernel validation ? never a parallel command bus and never a
second event stream.

- DECLARE / ASSERT / RETRACT / PROPOSE  -> reduce to a delta, then CommitAuthority
- VALIDATE                              -> kernel invariant validation only
- COMMIT                                -> explicit commit through the boundary
- FORK                                  -> existing fork_branch (one history model)
- PROMOTE                               -> produces a PromotionUseCase ONLY; it
                                          never commits the parent worldline
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchMetadata
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.world_isa import WorldIsaOp, reduce_isa_to_delta

from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.invariants import check_delta_invariants
from wanxiang_runtime.state import InMemoryCanonicalState


@dataclass(frozen=True, slots=True)
class PromotionUseCase:
    """A promotion intent, not a commit: candidates never mutate the parent."""

    source_worldline_ref: str
    target_world_definition_ref: str
    candidate_ref: str
    policy: str = "candidate_only"


@dataclass(frozen=True, slots=True)
class IsaExecutionResult:
    op: WorldIsaOp
    delta: ProposedWorldDelta | None = None
    event: CommittedEvent | None = None
    state_after: InMemoryCanonicalState | None = None
    branch: BranchMetadata | None = None
    promotion: PromotionUseCase | None = None
    validated: bool | None = None


def execute_isa(
    op: WorldIsaOp,
    authority: CommitAuthority,
    state: InMemoryCanonicalState,
    *,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    world_time: WorldTime,
    command_id: CommandId | None = None,
    parent: BranchMetadata | None = None,
) -> IsaExecutionResult:
    """Execute one ISA instruction through the existing pipeline."""
    if op.op == "VALIDATE":
        delta = reduce_isa_to_delta(op)
        if delta is not None:
            check_delta_invariants(state, delta)
        return IsaExecutionResult(op=op, delta=delta, validated=True)

    if op.op == "FORK":
        from wanxiang_runtime.branch import fork_branch

        if parent is None:
            raise ValueError("FORK requires the parent branch metadata")
        fork_revision = state.revision
        fork_seq = fork_revision
        from wanxiang_domain.hierarchy import BranchRevision, EventSeq

        branch = fork_branch(
            parent,
            state,
            fork_revision=BranchRevision(fork_revision.value),
            fork_event_seq=EventSeq(fork_seq.value),
            snapshot_ref=str(op.payload.get("snapshot_ref", "mem://isa-fork")),
        )
        return IsaExecutionResult(op=op, branch=branch)

    if op.op == "PROMOTE":
        promotion = PromotionUseCase(
            source_worldline_ref=str(op.payload.get("source_worldline", "")),
            target_world_definition_ref=str(op.payload.get("target_world_definition", "")),
            candidate_ref=str(op.payload.get("candidate", "")),
            policy=str(op.payload.get("policy", "candidate_only")),
        )
        return IsaExecutionResult(op=op, promotion=promotion)

    # DECLARE / ASSERT / RETRACT / PROPOSE / COMMIT -> commit through the boundary.
    delta = reduce_isa_to_delta(op)
    if delta is None:
        raise ValueError(f"ISA op {op.op} is not a commit-bearing instruction")
    commit_id = command_id or CommandId(f"cmd_isa_{op.op.lower()}_{state.revision.value}")
    result = authority.commit(
        state,
        CommitRequest(
            command_id=commit_id,
            instance_id=instance_id,
            branch_id=branch_id,
            expected_revision=state.revision,
            delta=delta,
            world_time=world_time,
            rule_version=state.rule_version,
        ),
    )
    return IsaExecutionResult(
        op=op,
        delta=delta,
        event=result.event,
        state_after=result.state_after,
        validated=True,
    )
