"""Bridge source-generated scene assets into the existing G96 visual projection ABI.

Layout coordinates are projection-only and never canonical geography.
"""

# pyright: reportPrivateUsage=false
# pyright: reportUnusedFunction=false

from __future__ import annotations

import math

from wanxiang_substrate.assets.book_scene_plan import _SourceVisualPlan
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.world_lab.visual_models import VisualSceneObject, VisualSceneState


def _visual_scene_state_from_book_assets(
    plan: _SourceVisualPlan,
    asset_refs: tuple[AssetRef, ...],
    *,
    snapshot_ref: str,
    world_instance_ref: str,
    branch_ref: str,
    revision: int,
    world_time_ticks: int,
    state_hash: str,
) -> VisualSceneState:
    """Create a projection-layout scene without inventing physical coordinates."""
    if len(asset_refs) != len(plan.scene_requests):
        raise ValueError("scene asset refs must align with planned scene requests")

    count = len(plan.scene_requests)
    radius = max(1.0, float(count))
    objects: list[VisualSceneObject] = []
    for index, (request, asset_ref) in enumerate(zip(plan.scene_requests, asset_refs, strict=True)):
        angle = 0.0 if count <= 1 else (2.0 * math.pi * index / count)
        position = (
            round(radius * math.cos(angle), 6),
            round(radius * math.sin(angle), 6),
        )
        objects.append(
            VisualSceneObject(
                object_ref=f"visual-scene:{request.stable_key}",
                entity_ref=f"place:{request.stable_key}",
                position=position,
                asset_ref=asset_ref,
            )
        )

    return VisualSceneState(
        scene_ref=f"book-visual:{plan.source_digest[:24]}",
        snapshot_ref=snapshot_ref,
        world_instance_ref=world_instance_ref,
        branch_ref=branch_ref,
        revision=revision,
        world_time_ticks=world_time_ticks,
        state_hash=state_hash,
        objects=tuple(objects),
        asset_refs=asset_refs,
    )
