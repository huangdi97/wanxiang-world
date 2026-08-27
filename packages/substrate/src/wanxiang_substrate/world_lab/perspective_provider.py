"""Deterministic actor-scoped visual projection policy (M93/G96C)."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.registry_support import ref
from wanxiang_substrate.world_lab.visual_models import (
    ActorPerspective,
    VisualSceneObject,
    VisualSceneState,
)
from wanxiang_substrate.world_lab.visual_outputs import (
    VisualProjectedObject,
    VisualProjectionFrame,
    VisualProviderHealth,
)


@dataclass(frozen=True, slots=True)
class PerspectiveVisualProvider:
    """Pure provider that filters scene inputs into one actor's frame."""

    provider_id: str
    provider_version: str

    def __post_init__(self) -> None:
        ref(self.provider_id, "provider_id")
        ref(self.provider_version, "provider_version")

    def health(self) -> VisualProviderHealth:
        return VisualProviderHealth(
            provider_id=self.provider_id,
            version=self.provider_version,
            available=True,
            deterministic=True,
            capabilities=("actor-perspective", "occlusion-filter", "rights-filter"),
        )

    def project(
        self,
        scene: VisualSceneState,
        perspective: ActorPerspective,
    ) -> VisualProjectionFrame:
        eligible = tuple(item for item in scene.objects if self._eligible(item, perspective))
        visible = tuple(
            item
            for item in eligible
            if not any(self._blocks(blocker, item, perspective) for blocker in eligible)
        )
        projected = tuple(
            VisualProjectedObject(
                object_ref=item.object_ref,
                entity_ref=item.entity_ref,
                position=item.position,
                asset_ref=item.asset_ref,
            )
            for item in visible
        )
        event_refs = tuple(sorted({event_ref for item in visible for event_ref in item.event_refs}))
        asset_refs = tuple(item.asset_ref for item in visible if item.asset_ref is not None)
        frame_ref = self._frame_ref(scene, perspective, projected, event_refs)
        return VisualProjectionFrame(
            frame_ref=frame_ref,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            scene_ref=scene.scene_ref,
            snapshot_ref=scene.snapshot_ref,
            snapshot_revision=scene.revision,
            actor_ref=perspective.actor_ref,
            perspective_ref=perspective.perspective_ref,
            status="projected",
            objects=projected,
            asset_refs=asset_refs,
            event_refs=event_refs,
            state_hash=scene.state_hash,
        )

    @staticmethod
    def _eligible(item: VisualSceneObject, perspective: ActorPerspective) -> bool:
        if item.audience_refs and perspective.actor_ref not in item.audience_refs:
            return False
        if item.object_ref in perspective.denied_object_refs:
            return False
        if (
            perspective.allowed_object_refs
            and item.object_ref not in perspective.allowed_object_refs
        ):
            return False
        if (
            hypot(
                item.position[0] - perspective.origin[0],
                item.position[1] - perspective.origin[1],
            )
            > perspective.view_radius
        ):
            return False
        return item.asset_ref is None or item.asset_ref.rights in perspective.allowed_rights

    @staticmethod
    def _blocks(
        blocker: VisualSceneObject,
        target: VisualSceneObject,
        perspective: ActorPerspective,
    ) -> bool:
        if blocker.object_ref == target.object_ref or blocker.occlusion_radius == 0.0:
            return False
        start_x, start_y = perspective.origin
        target_x, target_y = target.position
        line_x, line_y = target_x - start_x, target_y - start_y
        length_squared = line_x * line_x + line_y * line_y
        if length_squared == 0.0:
            return False
        blocker_x, blocker_y = blocker.position
        along = ((blocker_x - start_x) * line_x + (blocker_y - start_y) * line_y) / length_squared
        if not 0.0 < along < 1.0:
            return False
        nearest_x = start_x + along * line_x
        nearest_y = start_y + along * line_y
        return hypot(blocker_x - nearest_x, blocker_y - nearest_y) <= blocker.occlusion_radius

    def _frame_ref(
        self,
        scene: VisualSceneState,
        perspective: ActorPerspective,
        objects: tuple[VisualProjectedObject, ...],
        event_refs: tuple[str, ...],
    ) -> str:
        return "frame:" + semantic_sha256(
            {
                "provider_id": self.provider_id,
                "provider_version": self.provider_version,
                "scene_ref": scene.scene_ref,
                "snapshot_ref": scene.snapshot_ref,
                "revision": scene.revision,
                "actor_ref": perspective.actor_ref,
                "perspective_ref": perspective.perspective_ref,
                "object_refs": [item.object_ref for item in objects],
                "event_refs": list(event_refs),
            }
        )


__all__ = ["PerspectiveVisualProvider"]
