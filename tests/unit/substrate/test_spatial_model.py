"""G02A: spatial value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.spatial.model import (
    PlaceTopology,
    PortalLink,
    SpatialPath,
    validate_portal_state,
    validate_privacy,
)


@pytest.mark.unit
def test_portal_endpoints_must_differ() -> None:
    with pytest.raises(ContractError):
        PortalLink(
            portal_id=EntityId("p"),
            endpoint_a=EntityId("a"),
            endpoint_b=EntityId("a"),
        )


@pytest.mark.unit
def test_portal_state_validation() -> None:
    assert validate_portal_state("open") == "open"
    assert validate_portal_state("locked") == "locked"
    with pytest.raises(ContractError):
        validate_portal_state("ajar")


@pytest.mark.unit
def test_place_capacity_and_privacy_validation() -> None:
    with pytest.raises(ContractError):
        PlaceTopology(place_id=EntityId("r"), region_id=EntityId("x"), name="r", capacity=-1)
    with pytest.raises(ContractError):
        validate_privacy("secret")
    assert PlaceTopology(EntityId("r"), EntityId("x"), "room", capacity=3).capacity == 3


@pytest.mark.unit
def test_path_cost_is_portal_count() -> None:
    path = SpatialPath(portals=(EntityId("p1"), EntityId("p2")))
    assert path.cost == 2
    assert SpatialPath(portals=()).cost == 0


@pytest.mark.unit
def test_portal_other_endpoint() -> None:
    portal = PortalLink(EntityId("p"), EntityId("a"), EntityId("b"))
    assert portal.other_endpoint(EntityId("a")) == EntityId("b")
    assert portal.other_endpoint(EntityId("b")) == EntityId("a")
    with pytest.raises(ContractError):
        portal.other_endpoint(EntityId("c"))
