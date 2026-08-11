"""Thin transport routes: map HTTP <-> application use cases. No canonical rules."""

from __future__ import annotations

from fastapi import APIRouter, Request
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.errors import NotFound
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.state import state_to_primitive

from wanxiang_api.schemas import (
    ActionResponse,
    BranchResponse,
    CheckpointResponse,
    CompareRequest,
    CreateBranchRequest,
    CreateWorldRequest,
    DiffResponse,
    EventsResponse,
    EventSummary,
    ReplayResponse,
    StateResponse,
    SubmitActionRequest,
    WorldCreated,
    WorldInfo,
)

router = APIRouter()


def _runtime(request: Request) -> WorldRuntime:
    return request.app.state.runtime


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/worlds", response_model=WorldCreated, status_code=201)
def create_world(payload: CreateWorldRequest, request: Request) -> WorldCreated:
    instance_id = WorldInstanceId(payload.instance_id) if payload.instance_id else None
    result = _runtime(request).create_world(instance_id=instance_id)
    return WorldCreated(
        instance_id=result.instance_id.value,
        root_branch_id=result.root_branch_id.value,
        revision=result.revision.value,
    )


@router.get("/worlds/{instance_id}", response_model=WorldInfo)
def get_world(instance_id: str, request: Request) -> WorldInfo:
    store = _runtime(request).persistence.instances
    schema, rule, created = store.get(WorldInstanceId(instance_id))
    return WorldInfo(
        instance_id=instance_id,
        schema_version=schema.value,
        rule_version=rule.value,
        created_world_time=created.ticks,
    )


@router.get("/worlds/{instance_id}/state", response_model=StateResponse)
def get_state(instance_id: str, request: Request, branch_id: str | None = None) -> StateResponse:
    runtime = _runtime(request)
    branch = _resolve_branch(runtime, instance_id, branch_id)
    state = runtime.current_state(WorldInstanceId(instance_id), branch)
    return StateResponse(
        revision=state.revision.value,
        state_hash=state.semantic_hash(),
        state=state_to_primitive(state),
    )


@router.get("/worlds/{instance_id}/events", response_model=EventsResponse)
def get_events(instance_id: str, request: Request, branch_id: str | None = None) -> EventsResponse:
    runtime = _runtime(request)
    branch = _resolve_branch(runtime, instance_id, branch_id)
    events = runtime.events(WorldInstanceId(instance_id), branch)
    from wanxiang_domain.serialization_history import event_to_primitive

    return EventsResponse(events=[event_to_primitive(event) for event in events])


@router.post("/worlds/{instance_id}/actions", response_model=ActionResponse)
def submit_action(
    instance_id: str, payload: SubmitActionRequest, request: Request
) -> ActionResponse:
    runtime = _runtime(request)
    from wanxiang_domain.command import CommandEnvelope

    command = CommandEnvelope(
        command_id=CommandId(payload.command_id) if payload.command_id else CommandId.generate(),
        instance_id=WorldInstanceId(instance_id),
        branch_id=BranchId(payload.branch_id),
        expected_revision=BranchRevision(payload.expected_revision),
        action_type=payload.action_type,
        payload=dict(payload.payload),
        world_time=WorldTime(payload.world_time) if payload.world_time is not None else None,
    )
    result = runtime.submit_command(command)
    event_summary = EventSummary(
        event_id=result.event.event_id.value,
        event_seq=result.event.event_seq.value,
        revision=result.event.revision.value,
        command_id=result.event.command_id.value,
        action_ops=len(result.event.delta.operations),
    )
    return ActionResponse(
        duplicate=result.duplicate,
        event=event_summary,
        revision=result.state.revision.value,
        state_hash=result.state.semantic_hash(),
        state=state_to_primitive(result.state),
    )


@router.post("/worlds/{instance_id}/checkpoint", response_model=CheckpointResponse)
def checkpoint(
    instance_id: str, request: Request, branch_id: str | None = None
) -> CheckpointResponse:
    runtime = _runtime(request)
    branch = _resolve_branch(runtime, instance_id, branch_id)
    metadata = runtime.create_checkpoint(WorldInstanceId(instance_id), branch)
    return CheckpointResponse(
        snapshot_id=metadata.snapshot_id.value,
        revision=metadata.revision.value,
        event_seq=metadata.event_seq.value,
    )


@router.post("/worlds/{instance_id}/replay", response_model=ReplayResponse)
def replay(instance_id: str, request: Request, branch_id: str | None = None) -> ReplayResponse:
    runtime = _runtime(request)
    branch = _resolve_branch(runtime, instance_id, branch_id)
    result = runtime.restore_and_replay(WorldInstanceId(instance_id), branch)
    return ReplayResponse(
        used_snapshot=result.used_snapshot,
        revision=result.state.revision.value,
        state_hash=result.state.semantic_hash(),
        state=state_to_primitive(result.state),
    )


@router.post("/worlds/{instance_id}/branches", response_model=BranchResponse, status_code=201)
def create_branch(
    instance_id: str, payload: CreateBranchRequest, request: Request
) -> BranchResponse:
    runtime = _runtime(request)
    branch = runtime.create_branch(
        WorldInstanceId(instance_id),
        BranchId(payload.parent_branch_id),
        fork_revision=(
            BranchRevision(payload.fork_revision) if payload.fork_revision is not None else None
        ),
    )
    return BranchResponse(
        branch_id=branch.branch_id.value,
        instance_id=branch.instance_id.value,
        parent_branch_id=(
            branch.ancestry.parent_branch_id.value if branch.ancestry.parent_branch_id else None
        ),
        fork_revision=(
            branch.ancestry.fork_revision.value if branch.ancestry.fork_revision else None
        ),
        fork_event_seq=(
            branch.ancestry.fork_event_seq.value if branch.ancestry.fork_event_seq else None
        ),
    )


@router.post("/worlds/{instance_id}/branches/compare", response_model=DiffResponse)
def compare(instance_id: str, payload: CompareRequest, request: Request) -> DiffResponse:
    diff = _runtime(request).diff(
        WorldInstanceId(instance_id),
        BranchId(payload.branch_a),
        BranchId(payload.branch_b),
    )
    return DiffResponse(
        added_entities=[e.value for e in diff.added_entities],
        removed_entities=[e.value for e in diff.removed_entities],
        updated_entities=[e.value for e in diff.updated_entities],
        added_relations=[r.value for r in diff.added_relations],
        removed_relations=[r.value for r in diff.removed_relations],
    )


def _resolve_branch(runtime: WorldRuntime, instance_id: str, branch_id: str | None) -> BranchId:
    if branch_id is not None:
        return BranchId(branch_id)
    branches = runtime.persistence.branches.list(WorldInstanceId(instance_id))
    if not branches:
        raise NotFound(f"no branches for instance {instance_id}")
    return branches[0].branch_id
