"""Private memories require an explicit matching actor scope."""

# pyright: reportPrivateUsage=false

from wanxiang_domain.entity import ComponentData, EntityState
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_substrate.playable.player_projection_support import _memory_cards


def _memory(identity: str, owner_id: str | None, content: str) -> EntityState:
    fields: dict[str, str] = {"content": content}
    if owner_id is not None:
        fields["actor_id"] = owner_id
    component = ComponentData(
        component_id=ComponentId(f"component-{identity}"),
        component_type="memory",
        schema_version=SchemaVersion(1),
        fields=fields,
    )
    return EntityState(
        entity_id=EntityId(identity),
        entity_type="memory",
        components={component.component_id: component},
    )


def test_actor_only_sees_own_explicitly_owned_memories() -> None:
    memories = (
        _memory("memory-alice", "actor-alice", "alice-private-memory"),
        _memory("memory-bob", "actor-bob", "bob-private-memory"),
        _memory("memory-unowned", None, "unscoped-sensitive-memory"),
    )

    assert _memory_cards(memories, "actor-alice") == ["alice-private-memory"]
    assert _memory_cards(memories, "actor-bob") == ["bob-private-memory"]
    assert _memory_cards(memories, "") == []
    assert _memory_cards(memories, "actor-unknown") == []
