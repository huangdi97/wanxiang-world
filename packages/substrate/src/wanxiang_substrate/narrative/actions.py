"""Narrative household domain action definitions (Domain Pack; G35F).

Missing actions (ritual/visit/letter/relay) are defined HERE in the domain
pack, never hard-coded into Core reference actions. Generic: no Red Chamber
proper nouns; any synthetic world can install this pack.
"""

from __future__ import annotations

from wanxiang_substrate.actions.model import ActionDefinition, ParameterSpec
from wanxiang_substrate.actions.registry import ActionRegistry

ACTION_PERFORM_RITUAL = "narrative.perform_ritual"
ACTION_VISIT_SICK = "narrative.visit_sick"
ACTION_SEND_LETTER = "narrative.send_letter"
ACTION_RELAY_MESSAGE = "narrative.relay_message"

NARRATIVE_ACTION_DEFINITIONS = (
    ActionDefinition(
        action_type=ACTION_PERFORM_RITUAL,
        version=1,
        parameters=(
            ParameterSpec("ritual_id", "str"),
            ParameterSpec("actor_id", "str"),
            ParameterSpec("ritual_name", "str"),
            ParameterSpec("place_id", "str"),
            ParameterSpec("ticks", "int", required=False),
        ),
        permission="narrative.ritual",
        requires_actor=True,
        description="Perform a household ritual at a place (etiquette/ritual domain).",
    ),
    ActionDefinition(
        action_type=ACTION_VISIT_SICK,
        version=1,
        parameters=(
            ParameterSpec("visit_id", "str"),
            ParameterSpec("visitor_id", "str"),
            ParameterSpec("patient_id", "str"),
            ParameterSpec("place_id", "str"),
            ParameterSpec("ticks", "int", required=False),
        ),
        permission="narrative.visit",
        requires_actor=True,
        description="Visit a sick person at their place (requires visit access).",
    ),
    ActionDefinition(
        action_type=ACTION_SEND_LETTER,
        version=1,
        parameters=(
            ParameterSpec("letter_id", "str"),
            ParameterSpec("sender_id", "str"),
            ParameterSpec("recipient_id", "str"),
            ParameterSpec("payload_ref", "str"),
        ),
        permission="narrative.letter",
        requires_actor=True,
        description="Send a letter with a sealed payload to a recipient.",
    ),
    ActionDefinition(
        action_type=ACTION_RELAY_MESSAGE,
        version=1,
        parameters=(
            ParameterSpec("message_id", "str"),
            ParameterSpec("from_actor_id", "str"),
            ParameterSpec("to_actor_id", "str"),
            ParameterSpec("content_ref", "str"),
        ),
        permission="narrative.relay",
        requires_actor=True,
        description="Relay a spoken message to another actor (message passing).",
    ),
)


def register_narrative_actions(registry: ActionRegistry) -> None:
    """Install the narrative domain pack action definitions."""
    for definition in NARRATIVE_ACTION_DEFINITIONS:
        registry.register(definition)
