"""Permission-filtered StateDiff derived from committed canonical state."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Protocol

from wanxiang_domain.entity import EntityState, RelationState
from wanxiang_runtime.state import InMemoryCanonicalState

DiffCategory = Literal[
    "actor",
    "location",
    "relation",
    "item",
    "task",
    "knowledge",
    "organization",
    "state",
]
ChangeKind = Literal["added", "removed", "updated"]


@dataclass(frozen=True, slots=True)
class DiffChange:
    category: DiffCategory
    subject_id: str
    kind: ChangeKind
    before: Mapping[str, object]
    after: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "before", MappingProxyType(dict(self.before)))
        object.__setattr__(self, "after", MappingProxyType(dict(self.after)))

    def to_dict(self) -> dict[str, object]:
        return {
            "category": self.category,
            "subject_id": self.subject_id,
            "kind": self.kind,
            "before": dict(self.before),
            "after": dict(self.after),
        }


@dataclass(frozen=True, slots=True)
class CommittedStateDiff:
    """Facts computed from state/event results, not from narrative output."""

    revision_before: int
    revision_after: int
    changes: tuple[DiffChange, ...]
    event_id: str = ""
    no_change: bool = False

    def __post_init__(self) -> None:
        if self.revision_after < self.revision_before:
            raise ValueError("StateDiff revisions must be monotonic")
        if self.no_change != (not self.changes):
            raise ValueError("no_change must match the change list")

    @classmethod
    def from_states(
        cls,
        before: InMemoryCanonicalState,
        after: InMemoryCanonicalState,
        *,
        event_id: str = "",
        viewer_actor_id: str | None = None,
        admin: bool = False,
        allowed_categories: Sequence[str] | None = None,
    ) -> CommittedStateDiff:
        allowed = set(allowed_categories or DiffCategory.__args__)
        changes: list[DiffChange] = []
        before_entities = {item.entity_id.value: item for item in before.entities()}
        after_entities = {item.entity_id.value: item for item in after.entities()}
        for entity_id in sorted(set(before_entities) | set(after_entities)):
            old = before_entities.get(entity_id)
            new = after_entities.get(entity_id)
            source = new or old
            assert source is not None
            category = _category(source)
            if category not in allowed or not _visible(source, category, viewer_actor_id, admin):
                continue
            old_fields = _entity_fields(old) if old is not None else {}
            new_fields = _entity_fields(new) if new is not None else {}
            if old is None:
                kind: ChangeKind = "added"
            elif new is None:
                kind = "removed"
            elif old_fields != new_fields or old.entity_type != new.entity_type:
                kind = "updated"
            else:
                continue
            changes.append(DiffChange(category, entity_id, kind, old_fields, new_fields))
        before_relations = {item.relation_id.value: item for item in before.relations()}
        after_relations = {item.relation_id.value: item for item in after.relations()}
        for relation_id in sorted(set(before_relations) | set(after_relations)):
            old_relation = before_relations.get(relation_id)
            new_relation = after_relations.get(relation_id)
            if old_relation == new_relation:
                continue
            old_fields = _relation_fields(old_relation) if old_relation else {}
            new_fields = _relation_fields(new_relation) if new_relation else {}
            if old_relation is None:
                kind: ChangeKind = "added"
            elif new_relation is None:
                kind = "removed"
            else:
                kind = "updated"
            changes.append(DiffChange("relation", relation_id, kind, old_fields, new_fields))
        changes.sort(key=lambda item: (item.category, item.subject_id, item.kind))
        return cls(
            before.revision.value,
            after.revision.value,
            tuple(changes),
            event_id=event_id,
            no_change=not changes,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "revision_before": self.revision_before,
            "revision_after": self.revision_after,
            "no_change": self.no_change,
            "changes": [change.to_dict() for change in self.changes],
        }


class NarrativeRenderer(Protocol):
    def render(self, diff: CommittedStateDiff) -> str: ...


def render_narrative(diff: CommittedStateDiff, renderer: NarrativeRenderer) -> str:
    """Render a separate projection; the renderer cannot change the StateDiff."""

    return renderer.render(diff)


def _category(entity: EntityState | None) -> DiffCategory:
    if entity is None:
        return "state"
    names = {entity.entity_type.casefold()}
    names.update(component.component_type.casefold() for component in entity.components.values())
    if names & {"actor", "person", "character", "agent"}:
        return "actor"
    if names & {"place", "location", "spatial.place"}:
        return "location"
    if names & {"item", "object", "material", "custody"}:
        return "item"
    if names & {"task", "opportunity", "challenge"}:
        return "task"
    if any("belief" in name or "memory" in name or "knowledge" in name for name in names):
        return "knowledge"
    if names & {"organization", "institution", "role"}:
        return "organization"
    return "state"


def _entity_fields(entity: EntityState | None) -> dict[str, object]:
    if entity is None:
        return {}
    fields: dict[str, object] = {"entity_type": entity.entity_type}
    for component in sorted(entity.components.values(), key=lambda item: item.component_id.value):
        for key, value in sorted(component.fields.items()):
            fields[f"{component.component_type}.{key}"] = value
    return fields


def _relation_fields(relation: RelationState | None) -> dict[str, object]:
    if relation is None:
        return {}
    return {
        "relation_type": relation.relation_type,
        "source_id": relation.source_id.value,
        "target_id": relation.target_id.value,
        **dict(relation.attributes),
    }


def _visible(
    entity: EntityState,
    category: DiffCategory,
    viewer_actor_id: str | None,
    admin: bool,
) -> bool:
    if category != "knowledge" or admin:
        return True
    fields = _entity_fields(entity)
    owner = fields.get("epistemic.belief.actor_id") or fields.get("epistemic.memory.actor_id")
    if owner is None:
        return False
    return viewer_actor_id is not None and str(owner) == viewer_actor_id
