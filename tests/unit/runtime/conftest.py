"""Shared fixtures for runtime tests."""

from __future__ import annotations

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    WorldInstanceId,
)
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState

INSTANCE = WorldInstanceId("wld_t1")
BRANCH = BranchId("br_t1")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


@pytest.fixture
def empty_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def make_create_delta(entity_id: str = "ent_a", count: int = 5) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(entity_id),
                entity_type="token_holder",
                components=(
                    ComponentData(
                        component_id=ComponentId(f"cmp_{entity_id}"),
                        component_type="resource",
                        schema_version=SCHEMA,
                        fields={"count": count},
                    ),
                ),
            ),
        )
    )


def make_command(action: str = "create_entity", expected: int = 0) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(f"cmd_{action}_{expected}"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(expected),
        action_type=action,
        payload={"entity_id": "ent_a", "count": 5},
    )
