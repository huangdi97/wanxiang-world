"""Versioned action registry with reference actions."""

from __future__ import annotations

from wanxiang_substrate.actions.model import ActionDefinition, ParameterSpec


class ActionRegistry:
    """Maps (action_type, version) -> ActionDefinition."""

    def __init__(self) -> None:
        self._definitions: dict[tuple[str, int], ActionDefinition] = {}

    def register(self, definition: ActionDefinition) -> None:
        self._definitions[(definition.action_type, definition.version)] = definition

    def get(self, action_type: str, version: int = 1) -> ActionDefinition | None:
        return self._definitions.get((action_type, version))

    def all(self) -> tuple[ActionDefinition, ...]:
        return tuple(sorted(self._definitions.values(), key=lambda d: (d.action_type, d.version)))


def register_reference_actions(registry: ActionRegistry) -> None:
    """Register the G03D reference action definitions (move, read, rest, ...)."""
    registry.register(
        ActionDefinition(
            action_type="spatial.move",
            version=1,
            parameters=(
                ParameterSpec("entity_id", "str"),
                ParameterSpec("target_place_id", "str"),
            ),
            requires_actor=True,
            description="Move an entity to a target place (authority: spatial).",
        )
    )
    registry.register(
        ActionDefinition(
            action_type="material.read_payload",
            version=1,
            parameters=(
                ParameterSpec("item_id", "str"),
                ParameterSpec("reader_id", "str"),
            ),
            requires_actor=True,
            description="Read a sealed payload (requires knowledge of the item).",
        )
    )
    registry.register(
        ActionDefinition(
            action_type="agency.deliver_message",
            version=1,
            parameters=(
                ParameterSpec("message_id", "str"),
                ParameterSpec("to", "str"),
            ),
            requires_actor=True,
            description="Deliver a message (domain resolver provided by world packs).",
        )
    )
    registry.register(
        ActionDefinition(
            action_type="body.rest",
            version=1,
            parameters=(
                ParameterSpec("actor_id", "str"),
                ParameterSpec("ticks", "int"),
            ),
            requires_actor=False,
            description="Rest to restore energy.",
        )
    )
    registry.register(
        ActionDefinition(
            action_type="agency.inspect",
            version=1,
            parameters=(ParameterSpec("target", "str"),),
            requires_actor=True,
            description="Inspect a target the actor can perceive.",
        )
    )
