"""API DTO schemas (transport shape only; no canonical rules here)."""

from __future__ import annotations

from pydantic import BaseModel, Field

FieldValue = int | str | float | bool | None


class CreateWorldRequest(BaseModel):
    instance_id: str | None = None


class WorldCreated(BaseModel):
    instance_id: str
    root_branch_id: str
    revision: int


class WorldInfo(BaseModel):
    instance_id: str
    schema_version: int
    rule_version: int
    created_world_time: int


class SubmitActionRequest(BaseModel):
    branch_id: str
    expected_revision: int = Field(ge=0)
    action_type: str
    payload: dict[str, FieldValue] = {}
    command_id: str | None = None
    world_time: int | None = Field(default=None, ge=0)


class EventSummary(BaseModel):
    event_id: str
    event_seq: int
    revision: int
    command_id: str
    action_ops: int


class ActionResponse(BaseModel):
    duplicate: bool
    event: EventSummary | None
    revision: int
    state_hash: str
    state: dict[str, object]


class StateResponse(BaseModel):
    revision: int
    state_hash: str
    state: dict[str, object]


class EventsResponse(BaseModel):
    events: list[dict[str, object]]


class CheckpointResponse(BaseModel):
    snapshot_id: str
    revision: int
    event_seq: int


class ReplayResponse(BaseModel):
    used_snapshot: bool
    revision: int
    state_hash: str
    state: dict[str, object]


class CreateBranchRequest(BaseModel):
    parent_branch_id: str
    fork_revision: int | None = Field(default=None, ge=0)


class BranchResponse(BaseModel):
    branch_id: str
    instance_id: str
    parent_branch_id: str | None
    fork_revision: int | None
    fork_event_seq: int | None


class CompareRequest(BaseModel):
    branch_a: str
    branch_b: str


class DiffResponse(BaseModel):
    added_entities: list[str]
    removed_entities: list[str]
    updated_entities: list[str]
    added_relations: list[str]
    removed_relations: list[str]
