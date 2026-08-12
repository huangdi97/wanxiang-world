"""G02A: spatial query semantics (containment, path, capacity, access, zones)."""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta
from wanxiang_substrate.spatial.fixture import house_delta
from wanxiang_substrate.spatial.model import PlaceTopology
from wanxiang_substrate.spatial.query import SpatialQuery


def _state() -> InMemoryCanonicalState:
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import BranchId, WorldInstanceId
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("wld_q"),
        branch_id=BranchId("br_q"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


@pytest.fixture
def house_state() -> InMemoryCanonicalState:
    return apply_delta(_state(), house_delta())


@pytest.mark.unit
def test_house_topology_extraction(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    assert set(query.places()) == {EntityId("hall"), EntityId("kitchen"), EntityId("garden")}
    hall = query.places()[EntityId("hall")]
    assert isinstance(hall, PlaceTopology)
    assert hall.region_id == EntityId("house")


@pytest.mark.unit
def test_neighbors_via_open_portals_only(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    hall_neighbors = {n.place_id for n in query.neighbors(EntityId("hall"))}
    assert hall_neighbors == {EntityId("kitchen")}  # garden door is locked


@pytest.mark.unit
def test_reachability_and_path_cost(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    assert query.reachable(EntityId("hall"), EntityId("kitchen"))
    assert query.reachable(EntityId("kitchen"), EntityId("garden"), ignore_locked=True)
    assert not query.reachable(EntityId("kitchen"), EntityId("garden"))
    path = query.path(EntityId("kitchen"), EntityId("garden"), ignore_locked=True)
    assert path is not None and path.cost == 2


@pytest.mark.unit
def test_occupancy_and_capacity(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    hall_occ = query.occupancy(EntityId("hall"))
    assert hall_occ.used == 2  # alice + no_key
    assert hall_occ.limit == 4
    assert not hall_occ.is_full
    kitchen_occ = query.occupancy(EntityId("kitchen"))
    assert kitchen_occ.limit == 2


@pytest.mark.unit
def test_portal_access_with_key(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    door_hg = EntityId("door_hall_garden")
    assert query.can_access_portal(door_hg, EntityId("alice")) is False
    assert query.can_access_portal(door_hg, EntityId("bob")) is True  # bob holds key
    assert query.can_access_portal(door_hg, None) is False


@pytest.mark.unit
def test_visibility_and_acoustic_zones(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    vis = query.visibility_zone(EntityId("hall"))
    assert vis.visible_places == frozenset({EntityId("kitchen")})
    aco = query.acoustic_zone(EntityId("hall"))
    # sound carries through open or closed (not locked) portals
    assert EntityId("kitchen") in aco.audible_places
    assert EntityId("garden") not in aco.audible_places


@pytest.mark.unit
def test_locations_of_actors(house_state: InMemoryCanonicalState) -> None:
    query = SpatialQuery(house_state)
    assert query.location(EntityId("alice")) == EntityId("hall")
    assert query.location(EntityId("bob")) == EntityId("kitchen")


@pytest.mark.unit
def test_disconnected_place_is_unreachable() -> None:
    from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
    from wanxiang_substrate.spatial.components import place_component

    base = house_delta()
    combined = ProposedWorldDelta(
        operations=base.operations
        + (
            EntityCreate(
                entity_id=EntityId("cellar"),
                entity_type="spatial.place",
                components=(place_component(EntityId("house"), "cellar", capacity=1),),
            ),
        )
    )
    state = apply_delta(_state(), combined)
    query = SpatialQuery(state)
    assert query.path(EntityId("hall"), EntityId("cellar")) is None
    assert not query.reachable(EntityId("hall"), EntityId("cellar"))
