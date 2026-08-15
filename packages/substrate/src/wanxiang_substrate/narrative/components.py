"""Narrative household/historical-China domain components (G35F).

Generic domain (ritual/visit/letter/message) reusable by ANY synthetic world;
contains NO Red Chamber proper nouns and is not a RedChamberCore. Versioned
components on the M1 component model; routing reuse material item/payload
components for letters.
"""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

NARRATIVE_SCHEMA_VERSION = SchemaVersion(1)

RITUAL_COMPONENT = "narrative.ritual"
VISIT_COMPONENT = "narrative.visit"
LETTER_COMPONENT = "narrative.letter"
MESSAGE_COMPONENT = "narrative.message"


def ritual_component(
    ritual_id: EntityId,
    actor_id: EntityId,
    ritual_name: str,
    place_id: EntityId,
    ticks: int,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"ritual_{ritual_id.value}"),
        component_type=RITUAL_COMPONENT,
        schema_version=NARRATIVE_SCHEMA_VERSION,
        fields={
            "ritual_id": ritual_id.value,
            "actor_id": actor_id.value,
            "ritual_name": ritual_name,
            "place_id": place_id.value,
            "ticks": ticks,
        },
    )


def visit_component(
    visit_id: EntityId,
    visitor_id: EntityId,
    patient_id: EntityId,
    place_id: EntityId,
    ticks: int,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"visit_{visit_id.value}"),
        component_type=VISIT_COMPONENT,
        schema_version=NARRATIVE_SCHEMA_VERSION,
        fields={
            "visit_id": visit_id.value,
            "visitor_id": visitor_id.value,
            "patient_id": patient_id.value,
            "place_id": place_id.value,
            "ticks": ticks,
            "state": "done",
        },
    )


def letter_component(
    letter_id: EntityId,
    sender_id: EntityId,
    recipient_id: EntityId,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"letter_{letter_id.value}"),
        component_type=LETTER_COMPONENT,
        schema_version=NARRATIVE_SCHEMA_VERSION,
        fields={
            "letter_id": letter_id.value,
            "sender_id": sender_id.value,
            "recipient_id": recipient_id.value,
            "state": "sealed",
        },
    )


def message_component(
    message_id: EntityId,
    from_actor_id: EntityId,
    to_actor_id: EntityId,
    content_ref: str,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"message_{message_id.value}"),
        component_type=MESSAGE_COMPONENT,
        schema_version=NARRATIVE_SCHEMA_VERSION,
        fields={
            "message_id": message_id.value,
            "from_actor_id": from_actor_id.value,
            "to_actor_id": to_actor_id.value,
            "content_ref": content_ref,
            "state": "delivered",
        },
    )
