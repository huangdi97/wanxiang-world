"""Public substrate seam for non-authoritative T3 spatial assets.

The API layer may depend on this module. Implementations stay internal and
retain no Commit Authority or canonical History write capability.
"""

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_spatial_jobs import (
    _DerivedSpatialAttachments,
    _InMemorySpatialJobStore,
    _LocalJsonSpatialJobStore,
    _SpatialGenerationCoordinator,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
    _SpatialJobStore,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.service_visual import _source_scene_key_allowed

DerivedSpatialAttachments = _DerivedSpatialAttachments
InMemorySpatialJobStore = _InMemorySpatialJobStore
LocalJsonSpatialJobStore = _LocalJsonSpatialJobStore
SpatialGenerationCoordinator = _SpatialGenerationCoordinator
SpatialGenerationProvider = _SpatialGenerationProvider
SpatialGenerationTicket = _SpatialGenerationTicket
SpatialJobStore = _SpatialJobStore


def plan_book_scene_assets(
    package: WorldPackageDraft,
    *,
    max_preview_scenes: int = 3,
    preferred_places: tuple[str, ...] = (),
):
    """Return a source-grounded, noncanonical visual plan for public adapters."""
    return _plan_book_scene_assets(
        package,
        max_preview_scenes=max_preview_scenes,
        preferred_places=preferred_places,
    )


def source_scene_key_allowed(package: WorldPackageDraft, scene_key: str) -> bool:
    """Check whether a derived scene key belongs to the package's source places."""
    return _source_scene_key_allowed(package, scene_key)


__all__ = [
    "DerivedSpatialAttachments",
    "InMemorySpatialJobStore",
    "LocalJsonSpatialJobStore",
    "SpatialGenerationCoordinator",
    "SpatialGenerationProvider",
    "SpatialGenerationTicket",
    "SpatialJobStore",
    "plan_book_scene_assets",
    "source_scene_key_allowed",
]
