"""Actor-scoped possessions, assigned goals and unlocated people stay truthful."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from types import SimpleNamespace

from wanxiang_domain.entity import ComponentData, EntityState
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_memory import _memory_cards
from wanxiang_substrate.playable.player_projection_support import (
    _actor_owned_entities,
    _event_card,
    _known_people_cards,
    _opportunity_cards,
    _person_card,
    _same_location,
)


def _entity(
    identity: str,
    kind: str,
    owner: str | None = None,
    location: str | None = None,
) -> EntityState:
    fields: dict[str, str] = {"name": identity}
    if owner is not None:
        fields["owner_id"] = owner
    if location is not None:
        fields["location"] = location
    component = ComponentData(
        component_id=ComponentId(f"component-{identity}"),
        component_type=kind,
        schema_version=SchemaVersion(1),
        fields=fields,
    )
    return EntityState(
        entity_id=EntityId(identity),
        entity_type=kind,
        components={component.component_id: component},
    )


def _entity_with_fields(identity: str, kind: str, fields: dict[str, str]) -> EntityState:
    component = ComponentData(
        component_id=ComponentId(f"component-{identity}"),
        component_type=kind,
        schema_version=SchemaVersion(1),
        fields=fields,
    )
    return EntityState(
        entity_id=EntityId(identity),
        entity_type=kind,
        components={component.component_id: component},
    )


def test_conflicting_owner_fields_never_widen_actor_scope() -> None:
    copy = _copy_for("zh-CN")
    conflicting = _entity_with_fields(
        "conflict-task",
        "task",
        {"name": "conflict", "owner_id": "actor-bob", "actor_id": "actor-alice"},
    )

    assert _opportunity_cards((conflicting,), copy, "actor-alice") == []
    assert _opportunity_cards((conflicting,), copy, "") == []

    item = _entity_with_fields(
        "conflict-item",
        "item",
        {"name": "relic", "holder_id": "actor-alice", "owner_id": "actor-bob"},
    )
    assert _actor_owned_entities((item,), {"item"}, copy, "actor-alice") == []

    event = _entity_with_fields(
        "conflict-event",
        "event",
        {"name": "secret", "actor_id": "actor-bob", "owner_id": "actor-alice"},
    )
    assert _event_card((event,), {}, copy, "actor-alice") is None

    memory = _entity_with_fields(
        "conflict-memory",
        "memory",
        {"content": "secret", "actor_id": "actor-bob", "owner_id": "actor-alice"},
    )
    assert _memory_cards((memory,), "actor-alice") == []


def test_unowned_and_other_actor_objects_are_not_player_possessions() -> None:
    items = (
        _entity("public-statue", "object"),
        _entity("alice-lantern", "item", "actor-alice"),
        _entity("bob-book", "object", "actor-bob"),
        _entity("alice-task", "task", "actor-alice"),
        _entity("unassigned-goal", "opportunity"),
    )
    copy = _copy_for("zh-CN")

    assert _actor_owned_entities(items, {"item", "object", "material"}, copy, "actor-alice") == [
        "alice-lantern"
    ]
    assert _actor_owned_entities(items, {"task", "opportunity"}, copy, "actor-alice") == [
        "alice-task"
    ]
    assert _actor_owned_entities(items, {"item", "object", "material"}, copy, "") == []
    assert _actor_owned_entities(items, {"item", "object", "material"}, copy, "actor-bob") == [
        "bob-book"
    ]


def test_person_cards_preserve_unknown_location() -> None:
    copy = _copy_for("zh-CN")
    person = _person_card(_entity("remote-person", "person"), copy)
    assert person["location"] is None


def test_birth_place_is_not_current_presence() -> None:
    copy = _copy_for("zh-CN")
    born = _entity_with_fields(
        "born",
        "person",
        {"name": "Born", "place_of_birth": "Garden"},
    )

    assert _person_card(born, copy)["location"] is None
    assert _known_people_cards((born,), (), "", "Garden", copy) == []


def test_known_people_are_actor_scoped_and_remote_live_state_is_redacted() -> None:
    copy = _copy_for("zh-CN")
    alice = _entity("actor-alice", "person", location="Garden")
    bob = _entity("bob", "person", location="Garden")
    carol = _entity("carol", "person", location="Harbor")
    dave = _entity("dave", "person", location="Tower")
    relation = SimpleNamespace(
        source_id=EntityId("actor-alice"),
        target_id=EntityId("carol"),
        relation_type="friend",
    )

    cards = _known_people_cards(
        (alice, bob, carol, dave),
        (relation,),
        "actor-alice",
        "Garden",
        copy,
    )
    by_name = {str(card["name"]): card for card in cards}

    assert set(by_name) == {"bob", "carol"}
    assert by_name["bob"]["location"] == "Garden"
    assert by_name["carol"]["location"] is None
    assert by_name["carol"]["status"] is None
    assert "dave" not in by_name


def test_tasks_and_opportunities_are_not_reported_as_current_events() -> None:
    copy = _copy_for("zh-CN")
    entities = (
        _entity("alice-quest", "task", "actor-alice"),
        _entity("open-call", "opportunity"),
        _entity("world-event", "event"),
    )

    card = _event_card(entities, {}, copy, "actor-alice")

    assert card == {"name": "world-event", "description": None, "status": None}
    assert _event_card(entities[:2], {}, copy, "actor-alice") is None


def test_owner_scoped_opportunities_and_current_event_stay_private() -> None:
    copy = _copy_for("zh-CN")
    entities = (
        _entity("bob-secret", "task", "actor-bob"),
        _entity("alice-quest", "task", "actor-alice"),
        _entity("open-call", "opportunity"),
        _entity("bob-event", "event", "actor-bob"),
    )

    alice = _opportunity_cards(entities, copy, "actor-alice")
    assert [str(row["name"]) for row in alice] == ["alice-quest", "open-call"]

    observer = _opportunity_cards(entities, copy, "")
    assert [str(row["name"]) for row in observer] == ["open-call"]

    assert _event_card(
        (_entity("bob-event", "event", "actor-bob"), _entity("world-event", "event")),
        {},
        copy,
        "actor-alice",
    ) == {"name": "world-event", "description": None, "status": None}
    assert (
        _event_card((_entity("bob-event", "event", "actor-bob"),), {}, copy, "actor-alice") is None
    )
    assert _event_card((_entity("bob-event", "event", "actor-bob"),), {}, copy, "") is None


def test_present_people_use_source_equivalent_location_identity() -> None:
    copy = _copy_for("zh-CN")
    decomposed = "Cafe\u0301"
    composed = "Café"
    spaced = "  café  "

    assert _same_location(decomposed, composed)
    assert _same_location(spaced, composed)

    bob = _entity("bob", "person", location=decomposed)
    cards = _known_people_cards((bob,), (), "", spaced, copy)
    assert [str(card["name"]) for card in cards] == ["bob"]
    assert cards[0]["location"] == decomposed


def test_location_identity_does_not_fuzzy_merge_distinct_places() -> None:
    assert not _same_location("Garden", "Garden Annex")
    assert not _same_location(None, "Garden")
