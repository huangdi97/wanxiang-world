"""Spatial substrate: topology, access, occupancy (G02A)."""

from wanxiang_substrate.spatial.components import (
    PLACE_COMPONENT,
    PORTAL_COMPONENT,
    POSITION_COMPONENT,
    REGION_COMPONENT,
)
from wanxiang_substrate.spatial.errors import (
    LocationNotReachable,
    PlaceAtCapacity,
    PortalLocked,
    SpatialAccessDenied,
    SpatialError,
)
from wanxiang_substrate.spatial.fixture import build_house_fixture_commands
from wanxiang_substrate.spatial.model import (
    PlaceTopology,
    PortalLink,
    PortalState,
    PrivacyLevel,
    SpatialSnapshot,
)
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers

__all__ = [
    "LocationNotReachable",
    "PLACE_COMPONENT",
    "PORTAL_COMPONENT",
    "POSITION_COMPONENT",
    "PlaceAtCapacity",
    "PlaceTopology",
    "PortalLink",
    "PortalLocked",
    "PortalState",
    "PrivacyLevel",
    "REGION_COMPONENT",
    "SpatialAccessDenied",
    "SpatialError",
    "SpatialQuery",
    "SpatialSnapshot",
    "build_house_fixture_commands",
    "register_spatial_resolvers",
]
