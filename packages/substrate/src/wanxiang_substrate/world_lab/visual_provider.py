"""Provider-only visual projection ABI (M93/G96B)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from wanxiang_substrate.world_lab.visual_models import ActorPerspective, VisualSceneState
from wanxiang_substrate.world_lab.visual_outputs import (
    VisualProjectionFrame,
    VisualProviderHealth,
)


@runtime_checkable
class VisualWorldProvider(Protocol):
    """Scene/perspective in, projection-only frame out; no canonical writer."""

    def health(self) -> VisualProviderHealth: ...

    def project(
        self,
        scene: VisualSceneState,
        perspective: ActorPerspective,
    ) -> VisualProjectionFrame: ...


__all__ = ["VisualWorldProvider"]
