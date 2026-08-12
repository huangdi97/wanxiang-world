"""Population/scheduler component schema (versioned) on the M1 component model."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

POPULATION_SCHEMA_VERSION = SchemaVersion(1)

RESOLUTION_COMPONENT = "population.resolution"
SCHEDULER_RUN_COMPONENT = "population.scheduler_run"


def resolution_component(actor_id: EntityId, level: str, rate_ticks: int) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"resolution_{actor_id.value}"),
        component_type=RESOLUTION_COMPONENT,
        schema_version=POPULATION_SCHEMA_VERSION,
        fields={"actor_id": actor_id.value, "level": level, "rate_ticks": rate_ticks},
    )


def scheduler_run_component(
    run_id: EntityId, seed: int, horizon_ticks: int, events_submitted: int
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"run_{run_id.value}"),
        component_type=SCHEDULER_RUN_COMPONENT,
        schema_version=POPULATION_SCHEMA_VERSION,
        fields={
            "run_id": run_id.value,
            "seed": seed,
            "horizon_ticks": horizon_ticks,
            "events_submitted": events_submitted,
        },
    )
