"""Minimal canonical state/event diff for M1 diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.ids import EntityId, RelationId

from wanxiang_runtime.state import InMemoryCanonicalState


@dataclass(frozen=True, slots=True)
class StateDiff:
    added_entities: tuple[EntityId, ...] = ()
    removed_entities: tuple[EntityId, ...] = ()
    updated_entities: tuple[EntityId, ...] = ()
    added_relations: tuple[RelationId, ...] = ()
    removed_relations: tuple[RelationId, ...] = ()

    def is_empty(self) -> bool:
        return not (
            self.added_entities
            or self.removed_entities
            or self.updated_entities
            or self.added_relations
            or self.removed_relations
        )


def diff_states(before: InMemoryCanonicalState, after: InMemoryCanonicalState) -> StateDiff:
    before_entities = {e.entity_id: e for e in before.entities()}
    after_entities = {e.entity_id: e for e in after.entities()}
    before_relations = {r.relation_id: r for r in before.relations()}
    after_relations = {r.relation_id: r for r in after.relations()}

    added_entities = tuple(eid for eid in after_entities if eid not in before_entities)
    removed_entities = tuple(eid for eid in before_entities if eid not in after_entities)
    updated_entities = tuple(
        eid
        for eid in set(before_entities) & set(after_entities)
        if before_entities[eid] != after_entities[eid]
    )
    added_relations = tuple(rid for rid in after_relations if rid not in before_relations)
    removed_relations = tuple(rid for rid in before_relations if rid not in after_relations)
    return StateDiff(
        added_entities=added_entities,
        removed_entities=removed_entities,
        updated_entities=updated_entities,
        added_relations=added_relations,
        removed_relations=removed_relations,
    )
