"""Read-only query projections used by the World Capability Gateway.

This module contains no authentication, authority or commit path. The gateway
validates session scope/expiry first, then delegates pure read projections here
so the public adapter stays within the repository maintainability budget.
"""

from __future__ import annotations

from wanxiang_application.gateway_contract import AgentSessionIdentity
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.ids import BranchId, WorldInstanceId


def inspect_world_metadata(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> dict[str, object]:
    schema_version, rule_version, created_world_time = runtime.persistence.instances.get(
        instance_id
    )
    state = runtime.current_state(instance_id, branch_id)
    return {
        "world_id": instance_id.value,
        "branch_id": branch_id.value,
        "revision": state.revision.value,
        "state_hash": state.semantic_hash(),
        "schema_version": schema_version.value,
        "rule_version": rule_version.value,
        "created_world_time": created_world_time.ticks,
    }


def inspect_world_schema(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
) -> dict[str, object]:
    schema_version, rule_version, _created = runtime.persistence.instances.get(instance_id)
    return {
        "schema_version": schema_version.value,
        "rule_version": rule_version.value,
        "action_types": runtime.action_types(),
        "state_shape": ("entities", "relations", "revision"),
    }


def query_entities(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> tuple[dict[str, object], ...]:
    state = runtime.current_state(instance_id, branch_id)
    return tuple(
        {
            "id": entity.entity_id.value,
            "type": entity.entity_type,
            "components": tuple(
                {
                    "id": component.component_id.value,
                    "type": component.component_type,
                    "version": component.schema_version.value,
                    "fields": dict(component.fields),
                }
                for component in entity.components.values()
            ),
        }
        for entity in state.entities()
    )


def query_relations(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> tuple[dict[str, object], ...]:
    state = runtime.current_state(instance_id, branch_id)
    return tuple(
        {
            "id": relation.relation_id.value,
            "type": relation.relation_type,
            "source": relation.source_id.value,
            "target": relation.target_id.value,
            "attributes": dict(relation.attributes),
        }
        for relation in state.relations()
    )


def query_worldline(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> dict[str, object]:
    branch = runtime.persistence.branches.get(branch_id)
    if branch.instance_id != instance_id:
        raise PermissionDenied("branch does not belong to the session world")
    state = runtime.current_state(instance_id, branch_id)
    ancestry = branch.ancestry
    return {
        "world_id": instance_id.value,
        "branch_id": branch_id.value,
        "revision": state.revision.value,
        "parent_branch_id": (
            ancestry.parent_branch_id.value if ancestry.parent_branch_id is not None else None
        ),
        "fork_revision": (
            ancestry.fork_revision.value if ancestry.fork_revision is not None else None
        ),
        "fork_event_seq": (
            ancestry.fork_event_seq.value if ancestry.fork_event_seq is not None else None
        ),
    }


def list_capabilities(
    runtime: WorldRuntime,
    session: AgentSessionIdentity,
) -> dict[str, tuple[str, ...]]:
    return {
        "session_scopes": tuple(sorted(session.capability_scope)),
        "action_types": (
            runtime.action_types() if "world.propose" in session.capability_scope else ()
        ),
    }


__all__ = [
    "inspect_world_metadata",
    "inspect_world_schema",
    "list_capabilities",
    "query_entities",
    "query_relations",
    "query_worldline",
]
