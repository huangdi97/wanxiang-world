"""Wanxiang living-world substrate (P2)."""

from wanxiang_substrate.spatial import (
    SpatialQuery,
    build_house_fixture_commands,
    register_spatial_resolvers,
)

__version__ = "0.1.0"

__all__ = [
    "SpatialQuery",
    "build_house_fixture_commands",
    "register_spatial_resolvers",
]
