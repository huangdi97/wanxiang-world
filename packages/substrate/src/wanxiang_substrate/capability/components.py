"""Capability & learning component schema (versioned) on the M1 component model."""

from __future__ import annotations

import json

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

CAPABILITY_SCHEMA_VERSION = SchemaVersion(1)

CAPABILITY_STATE_COMPONENT = "capability.state"
PRACTICE_RECORD_COMPONENT = "capability.practice_record"
ASSESSMENT_COMPONENT = "capability.assessment"


def capability_state_component(
    actor_id: EntityId,
    capability: str,
    level: int,
    mastery: float,
    confidence: float,
    evidence_refs: tuple[str, ...] = (),
    updated_revision: int = 1,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"cap_{actor_id.value}_{capability}"),
        component_type=CAPABILITY_STATE_COMPONENT,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        fields={
            "actor_id": actor_id.value,
            "capability": capability,
            "level": level,
            "mastery": mastery,
            "confidence": confidence,
            "evidence_refs": json.dumps(list(evidence_refs), sort_keys=True),
            "updated_revision": updated_revision,
        },
    )


def practice_record_component(
    record_id: EntityId,
    actor_id: EntityId,
    capability: str,
    practice_count: int,
    evidence_ref: str,
    seq: int,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"pr_{record_id.value}"),
        component_type=PRACTICE_RECORD_COMPONENT,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        fields={
            "record_id": record_id.value,
            "actor_id": actor_id.value,
            "capability": capability,
            "practice_count": practice_count,
            "evidence_ref": evidence_ref,
            "seq": seq,
        },
    )


def assessment_component(
    assessment_id: EntityId,
    actor_id: EntityId,
    capability: str,
    assessment_type: str,
    outcome: str,
    evidence_ref: str,
    seq: int,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"as_{assessment_id.value}"),
        component_type=ASSESSMENT_COMPONENT,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        fields={
            "assessment_id": assessment_id.value,
            "actor_id": actor_id.value,
            "capability": capability,
            "assessment_type": assessment_type,
            "outcome": outcome,
            "evidence_ref": evidence_ref,
            "seq": seq,
        },
    )
