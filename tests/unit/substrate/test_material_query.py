"""G02C: material query semantics."""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta
from wanxiang_substrate.material.components import (
    contained_component,
    container_component,
    custody_component,
    item_component,
)
from wanxiang_substrate.material.fixture import LETTER, MESSENGER, package_delta
from wanxiang_substrate.material.query import MaterialQuery


def _state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("wld_mq"),
        branch_id=BranchId("br_mq"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


@pytest.fixture
def package_state() -> InMemoryCanonicalState:
    return apply_delta(_state(), package_delta())


@pytest.mark.unit
def test_custody_and_payload_separation(package_state: InMemoryCanonicalState) -> None:
    query = MaterialQuery(package_state)
    assert query.custodian(LETTER) == MESSENGER
    assert query.owner(LETTER) == EntityId("writer")
    info = query.payload(LETTER)
    assert info is not None and info.state == "sealed" and info.readers == ()


@pytest.mark.unit
def test_container_chain_custody_resolution() -> None:
    box = EntityId("box")
    crate = EntityId("crate")
    key = EntityId("key")
    holder = EntityId("holder")
    created = apply_delta(
        _state(),
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=box,
                    entity_type="material.container",
                    components=(container_component(box, 4),),
                ),
                EntityCreate(
                    entity_id=crate,
                    entity_type="material.container",
                    components=(container_component(crate, 4),),
                ),
                EntityCreate(
                    entity_id=key,
                    entity_type="material.item",
                    components=(item_component(key, "key"),),
                ),
            )
        ),
    )
    state = apply_delta(
        created,
        ProposedWorldDelta(
            operations=(
                EntityUpdate(entity_id=key, components=(contained_component(key, box),)),
                EntityUpdate(entity_id=box, components=(contained_component(box, crate),)),
                EntityUpdate(entity_id=crate, components=(custody_component(crate, holder),)),
            )
        ),
    )
    query = MaterialQuery(state)
    # key -> box -> crate -> holder
    assert query.custodian(key) == holder
    assert query.contents(crate, recursive=True) == (box, key)
    assert query.container_of(key) == box


def test_containment_cycle_detection_via_query() -> None:
    box = EntityId("box")
    key = EntityId("key")
    created = apply_delta(
        _state(),
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=box,
                    entity_type="material.container",
                    components=(container_component(box, 4),),
                ),
                EntityCreate(
                    entity_id=key,
                    entity_type="material.item",
                    components=(item_component(key, "key"),),
                ),
            )
        ),
    )
    state = apply_delta(
        created,
        ProposedWorldDelta(
            operations=(EntityUpdate(entity_id=key, components=(contained_component(key, box),)),)
        ),
    )
    query = MaterialQuery(state)
    # placing box inside key would be a cycle: key is already inside box.
    assert query.in_chain(key, box) is True
