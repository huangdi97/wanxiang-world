"""Private compatibility facade for the source-to-visual asset pipeline."""

from wanxiang_substrate.assets.book_scene_cache import (
    LocalJsonVisualCacheIndex as _LocalJsonVisualCacheIndex,
)
from wanxiang_substrate.assets.book_scene_cache import (
    VisualAssetCache as _VisualAssetCache,
)
from wanxiang_substrate.assets.book_scene_cache import (
    _InMemoryVisualCacheIndex,
    _VisualCacheIndex,
    _VisualCacheRecord,
)
from wanxiang_substrate.assets.book_scene_materialize import (
    _materialize_visual_plan,
    _render_visual_plan,
)
from wanxiang_substrate.assets.book_scene_render import (
    _ProceduralSvgSceneProvider,
    _render_world_atlas,
)
from wanxiang_substrate.assets.book_scene_types import (
    SceneImageProvider as _SceneImageProvider,
)
from wanxiang_substrate.assets.book_scene_types import (
    _SceneVisualAsset,
    _VisualMaterialization,
)
