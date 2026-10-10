"""Actor-scoped possessions, assigned goals and unlocated people stay truthful."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData, EntityState
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_projection_support import (
    _actor_owned_entities,
    _person_card,
)


def _entity(identity: str, kind: str, owner: str | None = None) -> EntityState:
    fields: dict[str, str] = {"name": identity}
    if owner is not None:
        fields["owner_id"] = owner
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
