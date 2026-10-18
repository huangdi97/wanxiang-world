"""Compose the Player facade with optional durable catalog storage."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING

from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.playable.restore import restore_playable_service
from wanxiang_substrate.playable.store import PlayableStore
from wanxiang_substrate.preview import PreviewRuntimePort

if TYPE_CHECKING:
    from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger


def build_playable_service(
    runtime: PreviewRuntimePort,
    *,
    visual_cache: VisualAssetCache,
    playable_store: PlayableStore | None = None,
    visual_budget: VisualBudgetLedger | None = None,
    deferred_limit: int = 0,
) -> PlayableService:
    store = playable_store
    if store is None:
        configured = os.environ.get("WANXIANG_PLAYABLE_STORE_PATH", "").strip()
        if configured:
            store = LocalJsonPlayableStore(pathlib.Path(configured))
    service = PlayableService(runtime, store=store, visual_cache=visual_cache)
    restore_playable_service(service)
    service._visual_budget = visual_budget
    service._visual_deferred_limit = deferred_limit
    return service
