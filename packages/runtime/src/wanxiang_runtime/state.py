"""In-memory canonical world state and pure delta application.

`InMemoryCanonicalState` is immutable: mutation happens only by deriving a new
state via `apply_delta`, which validates invariants first. There is no public
mutator, so no caller can bypass Commit Authority semantics at the state level.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
)
from wanxiang_domain.entity import EntityState, RelationState
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, EntityId, RelationId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

from wanxiang_runtime.invariants import check_delta_invariants


@dataclass(frozen=True, slots=True)
class InMemoryCanonicalState:
    """Authoritative read model derived from committed events (immutable)."""

    instance_id: WorldInstanceId
    branch_id: BranchId
    revision: BranchRevision
    schema_version: SchemaVersion
    rule_version: RuntimeVersion
    _entities: dict[EntityId, EntityState] = field(default_factory=dict[EntityId, EntityState])
    _relations: dict[RelationId, RelationState] = field(
        default_factory=dict[RelationId, RelationState]
    )

    def entity(self, entity_id: EntityId) -> EntityState | None:
        return self._entities.get(entity_id)

    def entities(self) -> tuple[EntityState, ...]:
        return tuple(sorted(self._entities.values(), key=lambda e: e.entity_id.value))

    def relation(self, relation_id: RelationId) -> RelationState | None:
        return self._relations.get(relation_id)

    def relations(self) -> tuple[RelationState, ...]:
        return tuple(sorted(self._relations.values(), key=lambda r: r.relation_id.value))

    def with_revision(self, revision: BranchRevision) -> InMemoryCanonicalState:
        """Derive a copy of this state at a different branch revision."""
        return InMemoryCanonicalState(
            instance_id=self.instance_id,
            branch_id=self.branch_id,
            revision=revision,
            schema_version=self.schema_version,
            rule_version=self.rule_version,
            _entities=dict(self._entities),
            _relations=dict(self._relations),
        )

    def semantic_hash(self) -> str:
        """Deterministic canonical hash of entities, relations and revision."""
        payload = {
            "revision": self.revision.value,
            "entities": [
                {
                    "id": e.entity_id.value,
                    "type": e.entity_type,
                    "components": [
                        {
                            "id": c.component_id.value,
                            "type": c.component_type,
                            "version": c.schema_version.value,
                            "fields": dict(c.fields),
                        }
                        for c in sorted(e.components.values(), key=lambda c: c.component_id.value)
                    ],
                }
                for e in self.entities()
            ],
            "relations": [
                {
                    "id": r.relation_id.value,
                    "type": r.relation_type,
                    "source": r.source_id.value,
                    "target": r.target_id.value,
                    "attributes": dict(r.attributes),
                }
                for r in self.relations()
            ],
        }
        return semantic_sha256(payload)

    def apply(self, delta: ProposedWorldDelta) -> InMemoryCanonicalState:
        """Validate invariants and derive a new state applying ``delta`` (pure).

        Any invariant violation raises before a new state is returned; the input
        state is never modified. Revision is unchanged here; Commit Authority
        advances the revision when it commits.
        """
        check_delta_invariants(self, delta)
        entities = dict(self._entities)
        relations = dict(self._relations)
        for op in delta.operations:
            if isinstance(op, EntityCreate):
                entities[op.entity_id] = EntityState(
                    entity_id=op.entity_id,
                    entity_type=op.entity_type,
                    components={c.component_id: c for c in op.components},
                )
            elif isinstance(op, EntityUpdate):
                current = entities[op.entity_id]
                merged = dict(current.components)
                for component in op.components:
                    merged[component.component_id] = component
                entities[op.entity_id] = EntityState(
                    entity_id=current.entity_id,
                    entity_type=current.entity_type,
                    components=merged,
                )
            elif isinstance(op, EntityDelete):
                del entities[op.entity_id]
            elif isinstance(op, RelationCreate):
                relations[op.relation_id] = RelationState(
                    relation_id=op.relation_id,
                    relation_type=op.relation_type,
                    source_id=op.source_id,
                    target_id=op.target_id,
                    attributes=op.attributes,
                )
            else:
                del relations[op.relation_id]
        return InMemoryCanonicalState(
            instance_id=self.instance_id,
            branch_id=self.branch_id,
            revision=self.revision,
            schema_version=self.schema_version,
            rule_version=self.rule_version,
            _entities=entities,
            _relations=relations,
        )


def apply_delta(state: InMemoryCanonicalState, delta: ProposedWorldDelta) -> InMemoryCanonicalState:
    """Pure module-level alias for :meth:`InMemoryCanonicalState.apply`."""
    return state.apply(delta)
