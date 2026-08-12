"""Population resolvers through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.population.components import (
    resolution_component,
    scheduler_run_component,
)
from wanxiang_substrate.population.model import VALID_LEVELS

ACTION_SET_RESOLUTION = "population.set_resolution"
ACTION_RECORD_RUN = "population.record_run"
ACTION_INSTANTIATE = "population.instantiate"


def register_population_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_SET_RESOLUTION, _set_resolution)
    registry.register(ACTION_RECORD_RUN, _record_run)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _set_resolution(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    level = _str(payload, "level")
    if level not in VALID_LEVELS:
        raise ValidationRejected(f"invalid population level {level!r}")
    rate = _int(payload, "rate_ticks", 50)
    if rate <= 0:
        raise ValidationRejected("resolution rate ticks must be positive")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=actor_id,
                components=(resolution_component(actor_id, level, rate),),
            ),
        )
    )


def _record_run(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    run_id = EntityId(_str(payload, "run_id"))
    seed = _int(payload, "seed")
    horizon = _int(payload, "horizon_ticks")
    events = _int(payload, "events_submitted")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=run_id,
                entity_type="population.scheduler_run",
                components=(scheduler_run_component(run_id, seed, horizon, events),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic population fixture via the authority."""
    from wanxiang_substrate.population.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
