"""Actor-private memory projection: never infer permission from an absent owner."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from wanxiang_domain.entity import EntityState

from wanxiang_substrate.playable.player_projection_support import (
    _entity_fields,
    _first_text,
    _private_owners,
)


def _memory_cards(entities: tuple[EntityState, ...], actor_id: str) -> list[str]:
    # An observer, or a session without an identified actor, has no private
    # memory scope. Do not infer permission from an absent owner field.
    if not actor_id:
        return []
    result: list[str] = []
    for entity in entities:
        kinds = {entity.entity_type.casefold()}
        kinds.update(
            component.component_type.casefold() for component in entity.components.values()
        )
        if not any("memory" in kind or "knowledge" in kind or "belief" in kind for kind in kinds):
            continue
        if _private_owners(entity) != {actor_id}:
            continue
        text = _first_text(_entity_fields(entity), ("content", "text", "summary", "description"))
        if text:
            result.append(text)
    return result
