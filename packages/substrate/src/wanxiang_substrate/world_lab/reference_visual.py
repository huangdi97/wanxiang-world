"""CI reference visual provider with no renderer or model dependency."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.world_lab.perspective_provider import PerspectiveVisualProvider
from wanxiang_substrate.world_lab.registry_support import ref
from wanxiang_substrate.world_lab.visual_models import ActorPerspective, VisualSceneState
from wanxiang_substrate.world_lab.visual_outputs import (
    VisualProjectionFrame,
    VisualProviderHealth,
)


@dataclass(frozen=True, slots=True)
class ReferenceVisualProvider:
    """Deterministic structured-scene adapter over the G96C policy provider."""

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
            capabilities=(
                "structured-scene",
                "actor-perspective",
                "state-refs",
                "event-refs",
                "non-generative",
            ),
        )

    def project(
        self,
        scene: VisualSceneState,
        perspective: ActorPerspective,
    ) -> VisualProjectionFrame:
        return PerspectiveVisualProvider(self.provider_id, self.provider_version).project(
            scene, perspective
        )


__all__ = ["ReferenceVisualProvider"]
