"""Canonical player action use case extracted from the facade."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wanxiang_domain.errors import ContractError, NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.actions import IntentCompiler
from wanxiang_substrate.playable.entry import active_lease
from wanxiang_substrate.playable.evidence import PlayerActionEvidence
from wanxiang_substrate.playable.service_model import (
    EventLike,
    PlayableActionResult,
    SubmittedResult,
)
from wanxiang_substrate.playable.service_session import owned_instance
from wanxiang_substrate.playable.service_support import affordances
from wanxiang_substrate.playable.state_diff import CommittedStateDiff
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def perform_action(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
    text: str = "",
    action_type: str = "",
    payload: dict[str, object] | None = None,
) -> PlayableActionResult:
    record = owned_instance(service, instance_id, viewer_id)
    if record.mode != "embodiment" or not record.session_id or not record.actor_id:
        raise ContractError("only an embodied actor may submit a world action")
    if active_lease(service.entry, record.session_id) is None:
        raise ContractError("embodiment lease is not active")
    experience = service._experiences.get(record.profile_id)
    if experience is None:
        raise NotFound(f"experience {record.profile_id!r} not found")

    compiler = IntentCompiler(affordances(experience))
    common = {
        "session_id": record.session_id,
        "instance_id": record.instance_id,
        "branch_id": record.branch_id,
        "actor_id": record.actor_id,
    }
    result = (
        compiler.compile_structured(**common, action_type=action_type, payload=payload or {})
        if action_type
        else compiler.compile_text(**common, text=text)
    )
    if not result.proposal.accepted:
        raise ContractError(result.proposal.rejection_reason or result.proposal.clarification)

    before = service.runtime.current_state(
        WorldInstanceId(record.instance_id), BranchId(record.branch_id)
    )
    command = result.proposal.to_command(before.revision.value)
    submitted = cast(SubmittedResult, service.runtime.submit_command(command))
    event = cast(EventLike, submitted.event)
    event_id = str(getattr(event.event_id, "value", event.event_id))
    diff = CommittedStateDiff.from_states(
        before,
        submitted.state,
        event_id=event_id,
        viewer_actor_id=record.actor_id,
        allowed_categories=experience.state_diff_fields,
    )
    evidence = PlayerActionEvidence.from_committed(
        result.proposal,
        command_id=command.command_id.value,
        event_id=event_id,
        before_revision=before.revision.value,
        after_revision=submitted.state.revision.value,
        before_state_hash=before.semantic_hash(),
        after_state_hash=submitted.state.semantic_hash(),
        diff=diff,
    )
    service.store.save_instance(
        ExperienceInstanceRecord(
            record.instance_id,
            record.profile_id,
            record.owner_id,
            record.branch_id,
            mode=record.mode,
            actor_id=record.actor_id,
            session_id=record.session_id,
            lease_id=record.lease_id,
            last_revision=submitted.state.revision.value,
            updated_seq=record.updated_seq + 1,
        )
    )
    return PlayableActionResult(
        result.proposal,
        event_id,
        submitted.state.revision.value,
        submitted.state.semantic_hash(),
        diff,
        evidence,
    )
