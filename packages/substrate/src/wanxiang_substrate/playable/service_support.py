"""Small pure helpers for the playable application facade."""

from __future__ import annotations

from wanxiang_substrate.playable.action_model import ActionAffordance
from wanxiang_substrate.playable.experience import ExperiencePackage
from wanxiang_substrate.playable.store import ExperienceInstanceRecord


def affordances(experience: ExperiencePackage) -> tuple[ActionAffordance, ...]:
    return tuple(
        ActionAffordance(
            action,
            required_fields=("entity_id", "status") if action == "set_status" else (),
            text_aliases=("set status", "status") if action == "set_status" else (),
        )
        for action in experience.allowed_actions
    )


def instance_dict(record: ExperienceInstanceRecord) -> dict[str, object]:
    return {
        "instance_id": record.instance_id,
        "profile_id": record.profile_id,
        "branch_id": record.branch_id,
        "mode": record.mode,
        "actor_id": record.actor_id,
        "last_revision": record.last_revision,
        "updated_seq": record.updated_seq,
    }
