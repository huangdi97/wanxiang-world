"""Server-side projection composition: perception, rights and mode filters.

Projections are DTOs composed server-side from canonical state; raw state is
never returned by default. Debug mode requires explicit privileged
authorization. Private beliefs/memories and sealed payloads never leak.
"""

from __future__ import annotations

from wanxiang_domain.entity import EntityState
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.projection.errors import UnauthorizedProjection
from wanxiang_substrate.projection.model import (
    ProjectionItem,
    ProjectionRequest,
    ProjectionSnapshot,
)

_SEALED = "sealed"
_BELIEF = "epistemic.belief"
_MEMORY = "epistemic.memory"
_PAYLOAD = "material.info_payload"
_PLACE = "spatial.place"


class ProjectionService:
    """Pure server-side projection composer (no mutation)."""

    def __init__(self, state: InMemoryCanonicalState, *, admin: bool = False) -> None:
        self._state = state
        self._admin = admin

    def compose(self, request: ProjectionRequest) -> ProjectionSnapshot:
        if request.mode == "debug" and not self._admin:
            raise UnauthorizedProjection(
                "debug projection requires explicit privileged authorization"
            )
        actor = EntityId(request.actor_id)
        items: list[ProjectionItem] = []
        for entity in self._state.entities():
            item = self._project_entity(entity, actor)
            if item is not None:
                items.append(item)
        items.sort(key=lambda i: i.entity_id)
        return ProjectionSnapshot(
            session_id=request.session_id,
            actor_id=request.actor_id,
            branch_id=request.branch_id,
            mode=request.mode,
            revision=self._state.revision.value,
            items=tuple(items),
        )

    def _project_entity(self, entity: EntityState, actor: EntityId) -> ProjectionItem | None:
        if self._is_sealed_payload(entity):
            return ProjectionItem(
                entity_id=entity.entity_id.value,
                entity_type=entity.entity_type,
                label="source_backed",
                redacted=True,
                redaction_reason="sealed_payload",
            )
        if entity.entity_type == _BELIEF:
            owner = self._belief_owner(entity)
            if owner is not None and owner != actor and not self._admin:
                return None  # private belief of another actor never leaks
            return self._item(entity, "model_inference")
        if entity.entity_type == _MEMORY:
            owner = self._belief_owner(entity)
            if owner is not None and owner != actor and not self._admin:
                return None  # private memory never leaks
            return self._item(entity, "reconstruction")
        if entity.entity_type == _PLACE:
            return self._project_place(entity, actor)
        return self._item(entity, "canon")

    def _project_place(self, entity: EntityState, actor: EntityId) -> ProjectionItem:
        privacy = entity_field(entity, "privacy")
        if privacy == "restricted" and not self._has_permission(actor, "enter"):
            return ProjectionItem(
                entity_id=entity.entity_id.value,
                entity_type=entity.entity_type,
                label="canon",
                redacted=True,
                redaction_reason="restricted_place",
            )
        return self._item(entity, "canon")

    @staticmethod
    def _item(entity: EntityState, label: str) -> ProjectionItem:
        fields: list[tuple[str, str]] = []
        for component in entity.components.values():
            for key, value in component.fields.items():
                if value is not None:
                    fields.append((f"{component.component_type}.{key}", str(value)))
        return ProjectionItem(
            entity_id=entity.entity_id.value,
            entity_type=entity.entity_type,
            label=label,
            fields=tuple(sorted(fields)),
        )

    def _has_permission(self, actor: EntityId, permission: str) -> bool:
        return (
            InstitutionQuery(self._state, now_ticks=_now(self._state))
            .check_permission(actor, permission)
            .allow
        )

    @staticmethod
    def _is_sealed_payload(entity: EntityState) -> bool:
        if entity.entity_type != _PAYLOAD:
            return False
        return entity_field(entity, "state") == _SEALED

    @staticmethod
    def _belief_owner(entity: EntityState) -> EntityId | None:
        raw = entity_field(entity, "actor_id")
        if raw:
            return EntityId(raw)
        return None


def entity_field(entity: EntityState, key: str) -> str:
    for component in entity.components.values():
        value = component.fields.get(key)
        if value is not None:
            return str(value)
    return ""


def _now(state: InMemoryCanonicalState) -> int:
    from wanxiang_substrate.temporal.query import TemporalQuery

    return TemporalQuery(state).now()
