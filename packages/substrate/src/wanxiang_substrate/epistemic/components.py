"""Epistemic component schema (versioned) on the M1 component model."""

from __future__ import annotations

import json

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

EPISTEMIC_SCHEMA_VERSION = SchemaVersion(1)

MEMORY_COMPONENT = "epistemic.memory"
BELIEF_COMPONENT = "epistemic.belief"
MEMORY_ACCESS_COMPONENT = "epistemic.memory_access"


def memory_component(
    memory_id: EntityId,
    actor_id: EntityId,
    kind: str,
    content_ref: str,
    at_ticks: int,
    salience: float = 0.5,
    source_obs_ref: str | None = None,
    forgotten: bool = False,
    source_perception_refs: tuple[str, ...] = (),
    decay_rate: float = 0.0,
    reinforcement_count: int = 0,
    last_reinforced_ticks: int | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"mem_{memory_id.value}"),
        component_type=MEMORY_COMPONENT,
        schema_version=EPISTEMIC_SCHEMA_VERSION,
        fields={
            "memory_id": memory_id.value,
            "actor_id": actor_id.value,
            "kind": kind,
            "content_ref": content_ref,
            "at_ticks": at_ticks,
            "salience": salience,
            "source_obs_ref": source_obs_ref,
            "forgotten": forgotten,
            "source_perception_refs": json.dumps(list(source_perception_refs), sort_keys=True),
            "decay_rate": decay_rate,
            "reinforcement_count": reinforcement_count,
            "last_reinforced_ticks": last_reinforced_ticks,
        },
    )


def belief_component(
    belief_id: EntityId,
    actor_id: EntityId,
    proposition: str,
    confidence: float,
    at_ticks: int,
    source_ref: str | None = None,
    status: str = "active",
    supersedes: EntityId | None = None,
    corrected_by: EntityId | None = None,
    stance: str = "unknown",
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"belief_{belief_id.value}"),
        component_type=BELIEF_COMPONENT,
        schema_version=EPISTEMIC_SCHEMA_VERSION,
        fields={
            "belief_id": belief_id.value,
            "actor_id": actor_id.value,
            "proposition": proposition,
            "confidence": confidence,
            "at_ticks": at_ticks,
            "source_ref": source_ref,
            "status": status,
            "supersedes": supersedes.value if supersedes else None,
            "corrected_by": corrected_by.value if corrected_by else None,
            "stance": stance,
        },
    )


def memory_access_component(owner_id: EntityId, authorized_actor: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"mem_access_{owner_id.value}_{authorized_actor.value}"),
        component_type=MEMORY_ACCESS_COMPONENT,
        schema_version=EPISTEMIC_SCHEMA_VERSION,
        fields={"owner_id": owner_id.value, "authorized_actor": authorized_actor.value},
    )
