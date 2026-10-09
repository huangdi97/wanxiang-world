"""World Asset Foundry seam substrate (G12F)."""

from wanxiang_substrate.assets.book_scene_visual import (
    LocalJsonVisualCacheIndex,
    SceneImageProvider,
    VisualAssetCache,
)

from wanxiang_substrate.assets.foundry import (
    AssetCandidate,
    AssetFoundry,
    AssetGenerator,
    SemanticSceneSpec,
    SyntheticAssetGenerator,
    validate_geometry,
)

__all__ = [
    "LocalJsonVisualCacheIndex",
    "SceneImageProvider",
    "VisualAssetCache",
    "AssetCandidate",
    "AssetFoundry",
    "AssetGenerator",
    "SemanticSceneSpec",
    "SyntheticAssetGenerator",
    "validate_geometry",
]
