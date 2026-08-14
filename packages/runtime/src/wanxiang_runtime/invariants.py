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
from wanxiang_domain.errors import Conflict, ConstitutionViolation, ValidationRejected

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


# Platform-protected identities: world deltas may never create/update/delete
# these or relate to them (single commit boundary, Reality Root, no
# self-amendment, world policy cannot elevate itself to platform authority).
PLATFORM_PROTECTED_ENTITY_PREFIX = "sys_"
PLATFORM_PROTECTED_ENTITY_IDS: frozenset[str] = frozenset(
    {
        "sys_reality_root",
        "sys_commit_boundary",
        "sys_commit_authority",
        "sys_constitution",
    }
)


def _is_protected(entity_id: object) -> bool:
    if isinstance(entity_id, str):
        return (
            entity_id.startswith(PLATFORM_PROTECTED_ENTITY_PREFIX)
            or entity_id in PLATFORM_PROTECTED_ENTITY_IDS
        )
    value = getattr(entity_id, "value", None)
    if isinstance(value, str):
        return (
            value.startswith(PLATFORM_PROTECTED_ENTITY_PREFIX)
            or value in PLATFORM_PROTECTED_ENTITY_IDS
        )
    return False


def check_no_mutation_of_protected_entities(state: InMemoryCanonicalState, op: object) -> None:
    """Kernel+constitution gate: world deltas cannot touch platform identities."""
    if isinstance(op, (EntityCreate, EntityUpdate, EntityDelete)):
        target = getattr(op, "entity_id", None)
        if target is not None and _is_protected(target):
            raise ConstitutionViolation(f"world delta must not mutate platform entity {target}")


def check_no_relation_to_protected_entities(state: InMemoryCanonicalState, op: object) -> None:
    """World deltas cannot relate platform identities to world content."""
    if isinstance(op, (RelationCreate, RelationDelete)):
        source = getattr(op, "source_id", None)
        target = getattr(op, "target_id", None)
        if source is not None and _is_protected(source):
            raise ConstitutionViolation(f"world delta must not relate platform entity {source}")
        if target is not None and _is_protected(target):
            raise ConstitutionViolation(f"world delta must not relate platform entity {target}")


INVARIANTS: tuple[Callable[[InMemoryCanonicalState, object], None], ...] = (
    check_no_duplicate_entity,
    check_entity_exists_for_update,
    check_entity_exists_for_delete,
    check_no_duplicate_relation,
    check_relation_exists_for_delete,
    check_relation_references_exist,
    check_no_mutation_of_protected_entities,
    check_no_relation_to_protected_entities,
)


def check_delta_invariants(state: InMemoryCanonicalState, delta: ProposedWorldDelta) -> None:
    """Run every registered invariant against each delta operation in order."""
    for op in delta.operations:
        for check in INVARIANTS:
            check(state, op)
