"""Initial invariant framework for the authoritative kernel.

Invariants are checked against the current state before a delta operation is
applied. The registry is a simple tuple of check functions; later Goals may add
checks without changing the authority path.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.errors import Conflict, ValidationRejected

if TYPE_CHECKING:
    from wanxiang_runtime.state import InMemoryCanonicalState


def check_no_duplicate_entity(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, EntityCreate) and state.entity(op.entity_id) is not None:
        raise Conflict(f"entity {op.entity_id.value} already exists")


def check_entity_exists_for_update(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, EntityUpdate) and state.entity(op.entity_id) is None:
        raise ValidationRejected(f"entity {op.entity_id.value} does not exist")


def check_entity_exists_for_delete(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, EntityDelete) and state.entity(op.entity_id) is None:
        raise ValidationRejected(f"entity {op.entity_id.value} does not exist")


def check_no_duplicate_relation(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, RelationCreate) and state.relation(op.relation_id) is not None:
        raise Conflict(f"relation {op.relation_id.value} already exists")


def check_relation_exists_for_delete(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, RelationDelete) and state.relation(op.relation_id) is None:
        raise ValidationRejected(f"relation {op.relation_id.value} does not exist")


def check_relation_references_exist(state: InMemoryCanonicalState, op: object) -> None:
    if isinstance(op, RelationCreate):
        if state.entity(op.source_id) is None:
            raise ValidationRejected(f"relation source entity {op.source_id.value} does not exist")
        if state.entity(op.target_id) is None:
            raise ValidationRejected(f"relation target entity {op.target_id.value} does not exist")


INVARIANTS: tuple[Callable[[InMemoryCanonicalState, object], None], ...] = (
    check_no_duplicate_entity,
    check_entity_exists_for_update,
    check_entity_exists_for_delete,
    check_no_duplicate_relation,
    check_relation_exists_for_delete,
    check_relation_references_exist,
)


def check_delta_invariants(state: InMemoryCanonicalState, delta: ProposedWorldDelta) -> None:
    """Run every registered invariant against each delta operation in order."""
    for op in delta.operations:
        for check in INVARIANTS:
            check(state, op)
