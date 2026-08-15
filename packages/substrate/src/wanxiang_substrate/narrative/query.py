"""Narrative household domain queries (G35F).

Read-only projections over canonical state: rituals, visits, letters and
messages, plus delegated access/duty checks through the institution query.
"""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.model import PermissionDecision
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.narrative.components import (
    LETTER_COMPONENT,
    MESSAGE_COMPONENT,
    RITUAL_COMPONENT,
    VISIT_COMPONENT,
)


class NarrativeQuery:
    """Read-only narrative domain projection (never mutates state)."""

    def __init__(self, state: InMemoryCanonicalState, now_ticks: int = 0) -> None:
        self._state = state
        self._now = now_ticks

    def rituals_by(self, actor_id: EntityId) -> tuple[str, ...]:
        """Ritual names performed by an actor (礼制)."""
        return tuple(
            _field(component.fields, "ritual_name")
            for entity in self._state.entities()
            for component in entity.components.values()
            if component.component_type == RITUAL_COMPONENT
            and _field(component.fields, "actor_id") == actor_id.value
        )

    def visits_for(self, patient_id: EntityId) -> tuple[str, ...]:
        """Visitors who visited a patient (探病)."""
        return tuple(
            _field(component.fields, "visitor_id")
            for entity in self._state.entities()
            for component in entity.components.values()
            if component.component_type == VISIT_COMPONENT
            and _field(component.fields, "patient_id") == patient_id.value
        )

    def letters_for(self, recipient_id: EntityId) -> tuple[str, ...]:
        """Letter senders whose letters are addressed to an actor (书信)."""
        return tuple(
            _field(component.fields, "sender_id")
            for entity in self._state.entities()
            for component in entity.components.values()
            if component.component_type == LETTER_COMPONENT
            and _field(component.fields, "recipient_id") == recipient_id.value
        )

    def messages_for(self, actor_id: EntityId) -> tuple[str, ...]:
        """Content refs of messages relayed to an actor (传话)."""
        return tuple(
            _field(component.fields, "content_ref")
            for entity in self._state.entities()
            for component in entity.components.values()
            if component.component_type == MESSAGE_COMPONENT
            and _field(component.fields, "to_actor_id") == actor_id.value
        )

    def access_allowed(
        self, actor_id: EntityId, permission: str, target: str = ""
    ) -> PermissionDecision:
        """Access control (访问权限) delegated to the institution query."""
        return InstitutionQuery(self._state, now_ticks=self._now).check_permission(
            actor_id, permission, target
        )

    def pending_duties(self, actor_id: EntityId) -> tuple[str, ...]:
        """Due, unfulfilled duties (职责) delegated to the institution query."""
        return tuple(
            duty.duty_type
            for duty in InstitutionQuery(self._state, now_ticks=self._now).due_duties(actor_id)
        )


def _field(fields: Mapping[str, object], key: str) -> str:
    value = fields.get(key)
    return value if isinstance(value, str) else ""
