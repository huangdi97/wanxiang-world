"""G35F: narrative household/historical-China domain pack (generic; synthetic).

The pack is installable by ANY synthetic world and contains NO Red Chamber
proper nouns / no RedChamberCore. Real《红楼梦》 text remains EXTERNAL_BLOCKED.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData, FieldValue
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, CommandId, ComponentId, EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.institution.components import permission_component
from wanxiang_substrate.material.components import INFO_PAYLOAD_COMPONENT
from wanxiang_substrate.narrative import (
    ACTION_PERFORM_RITUAL,
    ACTION_RELAY_MESSAGE,
    ACTION_SEND_LETTER,
    ACTION_VISIT_SICK,
    NarrativeQuery,
    register_narrative_domain,
)

FORBIDDEN_RED_CHAMBER_NAMES = (
    "林黛玉",
    "贾宝玉",
    "潇湘馆",
    "怡红院",
    "红楼梦",
    "贾府",
    "太虚幻境",
    "荣国府",
)


def _component(entity: str, kind: str) -> ComponentData:
    safe = f"{kind.replace('.', '_')}_{entity}"
    return ComponentData(
        component_id=ComponentId(safe),
        component_type=kind,
        schema_version=SCHEMA,
        fields={"entity_id": entity},
    )


def _base_state(*, visit_access: bool = False) -> InMemoryCanonicalState:
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    specs = (
        ("visitor", "actor"),
        ("patient", "actor"),
        ("recipient", "actor"),
        ("sickroom", "place"),
        ("hall", "place"),
    )
    for entity, kind in specs:
        delta = ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId(entity),
                    entity_type=kind,
                    components=(_component(entity, f"{kind}.base"),),
                ),
            )
        )
        state = state.apply(delta)
    if visit_access:
        perm = permission_component(
            permission_id=EntityId("perm_visit_1"),
            actor_id=EntityId("visitor"),
            permission="narrative.visit",
            target="sickroom",
            granter_id=EntityId("household"),
            start_ticks=0,
        )
        state = state.apply(
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("perm_visit_1"),
                        entity_type="institution.permission",
                        components=(perm,),
                    ),
                )
            )
        )
    return state


def _command(
    action_type: str,
    payload: Mapping[str, FieldValue],
    actor: str = "visitor",
) -> CommandEnvelope:
    safe = action_type.replace(".", "_")
    return CommandEnvelope(
        command_id=CommandId(f"cmd_{safe}"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(0),
        action_type=action_type,
        payload=payload,
        actor_id=ActorId(actor),
    )


def _installed_domain() -> tuple[ResolverRegistry, ActionRegistry]:
    resolvers = ResolverRegistry()
    actions = ActionRegistry()
    register_reference_actions(actions)
    register_narrative_domain(resolvers, actions)
    return resolvers, actions


@pytest.mark.unit
def test_domain_pack_installs_actions_without_touching_core() -> None:
    resolvers, actions = _installed_domain()
    assert actions.get(ACTION_PERFORM_RITUAL) is not None
    assert actions.get(ACTION_VISIT_SICK) is not None
    assert actions.get(ACTION_SEND_LETTER) is not None
    assert actions.get(ACTION_RELAY_MESSAGE) is not None
    for action in (
        ACTION_PERFORM_RITUAL,
        ACTION_VISIT_SICK,
        ACTION_SEND_LETTER,
        ACTION_RELAY_MESSAGE,
    ):
        assert action in resolvers.action_types()
    # Core reference actions were NOT extended: narrative actions live in the pack.
    core = ActionRegistry()
    register_reference_actions(core)
    assert core.get(ACTION_PERFORM_RITUAL) is None


@pytest.mark.unit
def test_perform_ritual_resolves_through_authority() -> None:
    resolvers, _ = _installed_domain()
    state = _base_state()
    delta = resolvers.resolve(
        _command(
            ACTION_PERFORM_RITUAL,
            {
                "ritual_id": "ritual_1",
                "actor_id": "visitor",
                "ritual_name": "morning_greeting",
                "place_id": "hall",
                "ticks": 3,
            },
        ),
        state,
    )
    next_state = state.apply(delta)
    assert next_state.entity(EntityId("ritual_1")) is not None
    assert NarrativeQuery(next_state).rituals_by(EntityId("visitor")) == ("morning_greeting",)


@pytest.mark.unit
def test_visit_sick_requires_access_permission() -> None:
    resolvers, _ = _installed_domain()
    state = _base_state(visit_access=False)
    command = _command(
        ACTION_VISIT_SICK,
        {
            "visit_id": "visit_1",
            "visitor_id": "visitor",
            "patient_id": "patient",
            "place_id": "sickroom",
            "ticks": 5,
        },
    )
    with pytest.raises(ValidationRejected):
        resolvers.resolve(command, state)
    # With granted access the visit resolves.
    state = _base_state(visit_access=True)
    delta = resolvers.resolve(command, state)
    next_state = state.apply(delta)
    assert next_state.entity(EntityId("visit_1")) is not None
    assert NarrativeQuery(next_state).visits_for(EntityId("patient")) == ("visitor",)
    assert (
        NarrativeQuery(next_state)
        .access_allowed(EntityId("visitor"), "narrative.visit", "sickroom")
        .allow
        is True
    )


@pytest.mark.unit
def test_send_letter_creates_sealed_payload() -> None:
    resolvers, _ = _installed_domain()
    state = _base_state()
    delta = resolvers.resolve(
        _command(
            ACTION_SEND_LETTER,
            {
                "letter_id": "letter_1",
                "sender_id": "visitor",
                "recipient_id": "recipient",
                "payload_ref": "letters/poem_01",
            },
        ),
        state,
    )
    next_state = state.apply(delta)
    letter = next_state.entity(EntityId("letter_1"))
    assert letter is not None
    kinds = {c.component_type for c in letter.components.values()}
    assert "narrative.letter" in kinds
    assert INFO_PAYLOAD_COMPONENT in kinds
    assert NarrativeQuery(next_state).letters_for(EntityId("recipient")) == ("visitor",)


@pytest.mark.unit
def test_relay_message_reaches_recipient() -> None:
    resolvers, _ = _installed_domain()
    state = _base_state()
    delta = resolvers.resolve(
        _command(
            ACTION_RELAY_MESSAGE,
            {
                "message_id": "message_1",
                "from_actor_id": "visitor",
                "to_actor_id": "recipient",
                "content_ref": "msg:请过府一叙",
            },
        ),
        state,
    )
    next_state = state.apply(delta)
    assert next_state.entity(EntityId("message_1")) is not None
    assert NarrativeQuery(next_state).messages_for(EntityId("recipient")) == ("msg:请过府一叙",)


@pytest.mark.unit
def test_narrative_domain_has_no_red_chamber_proper_nouns() -> None:
    package = (
        Path(__file__).resolve().parents[2] / "packages/substrate/src/wanxiang_substrate/narrative"
    )
    text = "".join(p.read_text(encoding="utf-8") for p in package.rglob("*.py"))
    forbidden = [name for name in FORBIDDEN_RED_CHAMBER_NAMES if name in text]
    assert forbidden == [], f"narrative domain must not contain Red Chamber names: {forbidden}"
