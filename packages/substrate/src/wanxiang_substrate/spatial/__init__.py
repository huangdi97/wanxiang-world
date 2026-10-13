"""Spatial substrate: topology, access, occupancy, and public T3 projection seams."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_identity import _source_scene_key
from wanxiang_substrate.assets.book_scene_plan import (
    _plan_book_scene_assets,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_spatial_http_gateway import _build_http_spatial_provider
from wanxiang_substrate.assets.book_spatial_jobs import (
    _DerivedSpatialAttachments,
    _SpatialGenerationCoordinator,
)
from wanxiang_substrate.assets.book_spatial_recovery import (
    _RecoverableInMemorySpatialJobStore,
    _RecoverableLocalJsonSpatialJobStore,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
    _SpatialJobStore,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.service_visual import _source_scene_key_allowed
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
from wanxiang_substrate.spatial.movement import MovementProfile, travel_time
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers

DerivedSpatialAttachments = _DerivedSpatialAttachments
InMemorySpatialJobStore = _RecoverableInMemorySpatialJobStore
LocalJsonSpatialJobStore = _RecoverableLocalJsonSpatialJobStore
SpatialGenerationCoordinator = _SpatialGenerationCoordinator
SpatialGenerationProvider = _SpatialGenerationProvider
SpatialGenerationTicket = _SpatialGenerationTicket
SpatialJobStore = _SpatialJobStore
build_http_spatial_provider = _build_http_spatial_provider


def plan_book_scene_assets(
    package: WorldPackageDraft,
    *,
    max_preview_scenes: int = 3,
    preferred_places: tuple[str, ...] = (),
) -> _SourceVisualPlan:
    """Return a source-grounded visual plan without granting canonical authority."""
    return _plan_book_scene_assets(
        package,
        max_preview_scenes=max_preview_scenes,
        preferred_places=preferred_places,
    )


def source_scene_key(source_digest: str, place_name: str) -> str:
    """Return the stable source-derived scene identity used by projection assets."""
    return _source_scene_key(source_digest, place_name)


def source_scene_key_allowed(package: WorldPackageDraft, scene_key: str) -> bool:
    """Check whether a derived scene key belongs to the package's source places."""
    return _source_scene_key_allowed(package, scene_key)


__all__ = [
    "DerivedSpatialAttachments",
    "InMemorySpatialJobStore",
    "LocalJsonSpatialJobStore",
    "LocationNotReachable",
    "MovementProfile",
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
    "SpatialGenerationCoordinator",
    "SpatialGenerationProvider",
    "SpatialGenerationTicket",
    "SpatialJobStore",
    "SpatialQuery",
    "SpatialSnapshot",
    "build_house_fixture_commands",
    "build_http_spatial_provider",
    "plan_book_scene_assets",
    "register_spatial_resolvers",
    "source_scene_key",
    "source_scene_key_allowed",
    "travel_time",
]
