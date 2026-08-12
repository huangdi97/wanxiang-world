"""Structured spatial error taxonomy (world semantics, not rendering)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SpatialError(WanxiangError):
    """Base error for spatial substrate failures."""

    code = "spatial_error"


class PortalLocked(SpatialError):
    code = "portal_locked"


class PortalClosed(SpatialError):
    code = "portal_closed"


class SpatialAccessDenied(SpatialError):
    code = "spatial_access_denied"


class PlaceAtCapacity(SpatialError):
    code = "place_at_capacity"


class LocationNotReachable(SpatialError):
    code = "location_not_reachable"


class InvalidSpatialState(SpatialError):
    code = "invalid_spatial_state"
