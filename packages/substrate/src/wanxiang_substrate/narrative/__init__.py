"""Narrative household/historical-China domain pack (G35F).

Generic domain (ritual/visit/letter/message + access/duty) reusable by any
synthetic world; explicitly NOT a RedChamberCore and free of Red Chamber
proper nouns. All writes flow through the single Commit Authority.
"""

from wanxiang_substrate.narrative.actions import (
    ACTION_PERFORM_RITUAL,
    ACTION_RELAY_MESSAGE,
    ACTION_SEND_LETTER,
    ACTION_VISIT_SICK,
    NARRATIVE_ACTION_DEFINITIONS,
    register_narrative_actions,
)
from wanxiang_substrate.narrative.components import (
    LETTER_COMPONENT,
    MESSAGE_COMPONENT,
    NARRATIVE_SCHEMA_VERSION,
    RITUAL_COMPONENT,
    VISIT_COMPONENT,
    letter_component,
    message_component,
    ritual_component,
    visit_component,
)
from wanxiang_substrate.narrative.query import NarrativeQuery
from wanxiang_substrate.narrative.resolver import (
    register_narrative_domain,
    register_narrative_resolvers,
)

__all__ = [
    "ACTION_PERFORM_RITUAL",
    "ACTION_RELAY_MESSAGE",
    "ACTION_SEND_LETTER",
    "ACTION_VISIT_SICK",
    "LETTER_COMPONENT",
    "MESSAGE_COMPONENT",
    "NARRATIVE_ACTION_DEFINITIONS",
    "NARRATIVE_SCHEMA_VERSION",
    "NarrativeQuery",
    "RITUAL_COMPONENT",
    "VISIT_COMPONENT",
    "letter_component",
    "message_component",
    "register_narrative_actions",
    "register_narrative_domain",
    "register_narrative_resolvers",
    "ritual_component",
    "visit_component",
]
