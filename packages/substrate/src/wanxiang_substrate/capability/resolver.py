"""Capability & learning resolvers through the M1 authority (G03G).

Every capability change is a CapabilityDelta computed from declared practice or
assessment evidence and applied through ProposedWorldDelta -> Commit Authority.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.capability.components import (
    assessment_component,
    capability_state_component,
    practice_record_component,
)
from wanxiang_substrate.capability.errors import (
    EvidenceRequired,
    UnsupportedAssessment,
)
from wanxiang_substrate.capability.model import (
    ASSESSMENT_OUTCOMES,
    SUPPORTED_ASSESSMENT_TYPES,
    AssessmentEvidence,
    CapabilityDelta,
    PracticeRecord,
    validate_capability_name,
)
from wanxiang_substrate.capability.policy import LearningPolicy
from wanxiang_substrate.capability.query import CapabilityQuery, capability_entity_id

ACTION_RECORD_PRACTICE = "capability.record_practice"
ACTION_RECORD_ASSESSMENT = "capability.record_assessment"
ACTION_APPLY_DELTA = "capability.apply_delta"


def register_capability_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_RECORD_PRACTICE, _record_practice)
    registry.register(ACTION_RECORD_ASSESSMENT, _record_assessment)
    registry.register(ACTION_APPLY_DELTA, _apply_delta)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _float(payload: Mapping[str, object], key: str, default: float = 0.0) -> float:
    value = payload.get(key, default)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be a number")
    return float(value)


def _evidence_refs(payload: Mapping[str, object], key: str) -> tuple[str, ...]:
    raw = payload.get(key, "[]")
    if not isinstance(raw, str):
        raise ValidationRejected(f"payload field {key!r} must be a JSON string array")
    try:
        decoded = json.loads(raw)
    except ValueError as exc:
        raise ValidationRejected(f"payload field {key!r} is not valid JSON") from exc
    if not isinstance(decoded, list):
        raise ValidationRejected(f"payload field {key!r} must encode a list")
    items = tuple(str(item) for item in cast(list[object], decoded) if isinstance(item, str))
    if not items:
        raise EvidenceRequired("capability change requires at least one evidence ref")
    return items


def _upsert_capability(
    state: InMemoryCanonicalState,
    new_state: object,
) -> tuple[EntityCreate, ...] | tuple[EntityUpdate, ...]:
    from wanxiang_substrate.capability.model import CapabilityState

    current_value = cast(CapabilityState, new_state)
    entity_id = capability_entity_id(current_value.actor_id, current_value.capability)
    component = capability_state_component(
        actor_id=current_value.actor_id,
        capability=current_value.capability,
        level=current_value.level,
        mastery=current_value.mastery,
        confidence=current_value.confidence,
        evidence_refs=current_value.evidence_refs,
        updated_revision=current_value.updated_revision,
    )
    if state.entity(entity_id) is None:
        return (
            EntityCreate(
                entity_id=entity_id,
                entity_type="capability.state",
                components=(component,),
            ),
        )
    return (EntityUpdate(entity_id=entity_id, components=(component,)),)


def _record_practice(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("record practice requires current state")
    payload = dict(command.payload)
    record_id = EntityId(_str(payload, "record_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    capability = _str(payload, "capability")
    validate_capability_name(capability)
    practice_count = _int(payload, "practice_count")
    if practice_count <= 0:
        raise ValidationRejected("practice_count must be positive")
    evidence_ref = _str(payload, "evidence_ref")
    record = PracticeRecord(record_id, actor_id, capability, practice_count, evidence_ref)
    delta = LearningPolicy.practice_delta(record)
    query = CapabilityQuery(state)
    current = query.capability(actor_id, capability)
    updated = LearningPolicy.apply(delta, current)
    seq = query.record_count(actor_id) + 1
    record_entity = EntityCreate(
        entity_id=EntityId(f"pr_{record_id.value}"),
        entity_type="capability.practice_record",
        components=(
            practice_record_component(
                record_id, actor_id, capability, practice_count, evidence_ref, seq
            ),
        ),
    )
    capability_op = _upsert_capability(state, updated)
    return ProposedWorldDelta(operations=(record_entity, *capability_op))


def _record_assessment(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("record assessment requires current state")
    payload = dict(command.payload)
    assessment_id = EntityId(_str(payload, "assessment_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    capability = _str(payload, "capability")
    validate_capability_name(capability)
    assessment_type = _str(payload, "assessment_type")
    if assessment_type not in SUPPORTED_ASSESSMENT_TYPES:
        raise UnsupportedAssessment(f"unsupported assessment type {assessment_type!r}")
    outcome = _str(payload, "outcome")
    if outcome not in ASSESSMENT_OUTCOMES:
        raise ValidationRejected(f"unsupported assessment outcome {outcome!r}")
    evidence_ref = _str(payload, "evidence_ref")
    evidence = AssessmentEvidence(
        assessment_id, actor_id, capability, assessment_type, outcome, evidence_ref
    )
    delta = LearningPolicy.assessment_delta(evidence)
    query = CapabilityQuery(state)
    current = query.capability(actor_id, capability)
    updated = LearningPolicy.apply(delta, current)
    seq = query.record_count(actor_id) + 1
    assessment_entity = EntityCreate(
        entity_id=EntityId(f"as_{assessment_id.value}"),
        entity_type="capability.assessment",
        components=(
            assessment_component(
                assessment_id, actor_id, capability, assessment_type, outcome, evidence_ref, seq
            ),
        ),
    )
    capability_op = _upsert_capability(state, updated)
    return ProposedWorldDelta(operations=(assessment_entity, *capability_op))


def _apply_delta(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("apply delta requires current state")
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    capability = _str(payload, "capability")
    validate_capability_name(capability)
    level_delta = _int(payload, "level_delta", 0)
    mastery_delta = _float(payload, "mastery_delta", 0.0)
    confidence_delta = _float(payload, "confidence_delta", 0.0)
    reason = _str(payload, "reason")
    evidence_refs = _evidence_refs(payload, "evidence_refs")
    delta = CapabilityDelta(
        actor_id=actor_id,
        capability=capability,
        level_delta=level_delta,
        mastery_delta=mastery_delta,
        confidence_delta=confidence_delta,
        reason=reason,
        evidence_refs=evidence_refs,
    )
    query = CapabilityQuery(state)
    current = query.capability(actor_id, capability)
    updated = LearningPolicy.apply(delta, current)
    return ProposedWorldDelta(operations=_upsert_capability(state, updated))
