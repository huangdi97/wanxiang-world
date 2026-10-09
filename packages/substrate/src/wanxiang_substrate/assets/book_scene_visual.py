"""Compatibility facade for the source-to-visual asset pipeline.

Implementation is split into focused modules so rendering, cache metadata and
provider governance remain independently testable and under architecture limits.
"""

from wanxiang_substrate.assets.book_scene_cache import (
    InMemoryVisualCacheIndex,
    LocalJsonVisualCacheIndex,
    VisualAssetCache,
    VisualCacheIndex,
    VisualCacheRecord,
)
from wanxiang_substrate.assets.book_scene_materialize import (
    materialize_visual_plan,
    render_visual_plan,
)
from wanxiang_substrate.assets.book_scene_render import (
    ProceduralSvgSceneProvider,
    render_world_atlas,
)
from wanxiang_substrate.assets.book_scene_types import (
    SceneImageProvider,
    SceneVisualAsset,
    VisualMaterialization,
)

# Private compatibility aliases retained for existing substrate callers/tests.
_InMemoryVisualCacheIndex = InMemoryVisualCacheIndex
_LocalJsonVisualCacheIndex = LocalJsonVisualCacheIndex
_VisualAssetCache = VisualAssetCache
_VisualCacheIndex = VisualCacheIndex
_VisualCacheRecord = VisualCacheRecord
_materialize_visual_plan = materialize_visual_plan
_render_visual_plan = render_visual_plan
_ProceduralSvgSceneProvider = ProceduralSvgSceneProvider
_render_world_atlas = render_world_atlas
_SceneImageProvider = SceneImageProvider
_SceneVisualAsset = SceneVisualAsset
_VisualMaterialization = VisualMaterialization

__all__ = [
    "InMemoryVisualCacheIndex",
    "LocalJsonVisualCacheIndex",
    "ProceduralSvgSceneProvider",
    "SceneImageProvider",
    "SceneVisualAsset",
    "VisualAssetCache",
    "VisualCacheIndex",
    "VisualCacheRecord",
    "VisualMaterialization",
    "materialize_visual_plan",
    "render_visual_plan",
    "render_world_atlas",
]
