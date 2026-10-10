"""Private compatibility facade for the source-to-visual asset pipeline."""

# pyright: reportPrivateUsage=false

import wanxiang_substrate.assets.book_scene_cache as _cache
import wanxiang_substrate.assets.book_scene_materialize as _materialize
import wanxiang_substrate.assets.book_scene_render as _render
import wanxiang_substrate.assets.book_scene_types as _types

_LocalJsonVisualCacheIndex = _cache.LocalJsonVisualCacheIndex
_VisualAssetCache = _cache.VisualAssetCache
_InMemoryVisualCacheIndex = _cache._InMemoryVisualCacheIndex
_VisualCacheIndex = _cache._VisualCacheIndex
_VisualCacheRecord = _cache._VisualCacheRecord
_materialize_visual_plan = _materialize._materialize_visual_plan
_render_visual_plan = _materialize._render_visual_plan
_ProceduralSvgSceneProvider = _render._ProceduralSvgSceneProvider
_render_world_atlas = _render._render_world_atlas
_SceneImageProvider = _types.SceneImageProvider
_SceneVisualAsset = _types._SceneVisualAsset
_VisualMaterialization = _types._VisualMaterialization
