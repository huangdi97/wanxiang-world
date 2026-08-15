"""Narrative household domain resolvers (G35F).

Ritual (礼制), sick-visiting (探病, access-gated), letters (书信, sealed
payload) and message relay (传话) all resolve through the single Commit
Authority as ProposedWorldDeltas; no resolver writes state directly.
Reuses institution permissions for access control and material item/payload
components for letters. Generic; no Red Chamber proper nouns.
"""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.actions.registry import ActionRegistry
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.material.components import info_payload_component, item_component
from wanxiang_substrate.narrative.actions import (
    ACTION_PERFORM_RITUAL,
    ACTION_RELAY_MESSAGE,
    ACTION_SEND_LETTER,
    ACTION_VISIT_SICK,
    register_narrative_actions,
)
from wanxiang_substrate.narrative.components import (
    LETTER_COMPONENT,
    MESSAGE_COMPONENT,
    RITUAL_COMPONENT,
    VISIT_COMPONENT,
    letter_component,
    message_component,
    ritual_component,
    visit_component,
)


def register_narrative_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_PERFORM_RITUAL, _perform_ritual)
    registry.register(ACTION_VISIT_SICK, _visit_sick)
    registry.register(ACTION_SEND_LETTER, _send_letter)
    registry.register(ACTION_RELAY_MESSAGE, _relay_message)


def register_narrative_domain(resolvers: ResolverRegistry, actions: ActionRegistry) -> None:
    """Install the whole narrative Domain Pack (actions + resolvers)."""
    register_narrative_actions(actions)
    register_narrative_resolvers(resolvers)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _perform_ritual(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    ritual_id = EntityId(_str(payload, "ritual_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    ritual_name = _str(payload, "ritual_name")
    place_id = EntityId(_str(payload, "place_id"))
    ticks = _int(payload, "ticks")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=ritual_id,
                entity_type="narrative.ritual",
                components=(ritual_component(ritual_id, actor_id, ritual_name, place_id, ticks),),
            ),
        )
    )


def _visit_sick(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Visit a sick person; requires visit access to the place (访问权限)."""
    if state is None:
        raise ValidationRejected("visit requires current state")
    payload = dict(command.payload)
    visit_id = EntityId(_str(payload, "visit_id"))
    visitor = EntityId(_str(payload, "visitor_id"))
    patient = EntityId(_str(payload, "patient_id"))
    place = EntityId(_str(payload, "place_id"))
    ticks = _int(payload, "ticks")
    if state.entity(patient) is None:
        raise ValidationRejected(f"patient {patient.value} does not exist")
    if state.entity(place) is None:
        raise ValidationRejected(f"place {place.value} does not exist")
    decision = InstitutionQuery(state, now_ticks=ticks).check_permission(
        visitor, "narrative.visit", place.value
    )
    if not decision.allow:
        raise ValidationRejected(f"visitor {visitor.value} lacks visit access to {place.value}")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=visit_id,
                entity_type="narrative.visit",
                components=(visit_component(visit_id, visitor, patient, place, ticks),),
            ),
        )
    )


def _send_letter(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Send a letter: material item + sealed info payload + routing component."""
    payload = dict(command.payload)
    letter_id = EntityId(_str(payload, "letter_id"))
    sender = EntityId(_str(payload, "sender_id"))
    recipient = EntityId(_str(payload, "recipient_id"))
    payload_ref = _str(payload, "payload_ref")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=letter_id,
                entity_type="narrative.letter",
                components=(
                    letter_component(letter_id, sender, recipient),
                    item_component(letter_id, "narrative.letter"),
                    info_payload_component(letter_id, payload_ref),
                ),
            ),
        )
    )


def _relay_message(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Relay a spoken message to another actor (传话)."""
    payload = dict(command.payload)
    message_id = EntityId(_str(payload, "message_id"))
    from_actor = EntityId(_str(payload, "from_actor_id"))
    to_actor = EntityId(_str(payload, "to_actor_id"))
    content_ref = _str(payload, "content_ref")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=message_id,
                entity_type="narrative.message",
                components=(message_component(message_id, from_actor, to_actor, content_ref),),
            ),
        )
    )


__all__ = [
    "LETTER_COMPONENT",
    "MESSAGE_COMPONENT",
    "RITUAL_COMPONENT",
    "VISIT_COMPONENT",
    "register_narrative_actions",
    "register_narrative_domain",
    "register_narrative_resolvers",
]
