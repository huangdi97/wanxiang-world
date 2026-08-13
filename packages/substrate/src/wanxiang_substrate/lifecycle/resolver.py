"""Lifecycle resolver through the M1 authority (G06A)."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.lifecycle.errors import InvalidLifecycleTransition
from wanxiang_substrate.lifecycle.model import LIFECYCLE_MODES, LifecycleMode, can_transition

ACTION_SET_MODE = "lifecycle.set_mode"

LIFECYCLE_ENTITY = EntityId("host_lifecycle")
LIFECYCLE_COMPONENT = "lifecycle.mode"
LIFECYCLE_SCHEMA_VERSION = SchemaVersion(1)


def register_lifecycle_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_SET_MODE, _set_mode)


def _set_mode(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("set lifecycle requires current state")
    payload = dict(command.payload)
    raw_mode = payload.get("mode")
    if not isinstance(raw_mode, str) or raw_mode not in LIFECYCLE_MODES:
        raise ValidationRejected(f"unknown lifecycle mode {raw_mode!r}")
    mode: LifecycleMode = raw_mode  # type: ignore[assignment]
    tick = _int(payload, "tick", 0)
    current = _current_component(state)
    if current is not None and not can_transition(_mode_of(current), mode):
        raise InvalidLifecycleTransition(
            f"cannot transition lifecycle from {_mode_of(current)} to {mode}"
        )
    component = ComponentData(
        component_id=ComponentId("lifecycle_mode"),
        component_type=LIFECYCLE_COMPONENT,
        schema_version=LIFECYCLE_SCHEMA_VERSION,
        fields={
            "mode": mode,
            "tick": tick,
            "updated_revision": state.revision.value + 1,
        },
    )
    if state.entity(LIFECYCLE_ENTITY) is None:
        return ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=LIFECYCLE_ENTITY,
                    entity_type="host.lifecycle",
                    components=(component,),
                ),
            )
        )
    return ProposedWorldDelta(
        operations=(EntityUpdate(entity_id=LIFECYCLE_ENTITY, components=(component,)),)
    )


def _current_component(state: InMemoryCanonicalState) -> ComponentData | None:
    entity = state.entity(LIFECYCLE_ENTITY)
    if entity is None:
        return None
    return next(
        (c for c in entity.components.values() if c.component_type == LIFECYCLE_COMPONENT),
        None,
    )


def _mode_of(component: ComponentData) -> LifecycleMode:
    value = str(component.fields.get("mode") or "REALTIME")
    return value if value in LIFECYCLE_MODES else "REALTIME"  # type: ignore[return-value]


def _int(payload: Mapping[str, object], key: str, default: int) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value
