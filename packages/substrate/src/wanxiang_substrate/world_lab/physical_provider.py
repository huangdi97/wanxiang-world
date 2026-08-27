"""Provider-only physical simulation ABI (M93/G96A)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from wanxiang_substrate.world_lab.physical_models import PhysicalSimulationRequest, PhysicalSnapshot
from wanxiang_substrate.world_lab.physical_outputs import PhysicalProviderHealth, PhysicalResolution


@runtime_checkable
class PhysicalWorldProvider(Protocol):
    """Read snapshot in, proposal/evidence out; never a canonical writer."""

    def health(self) -> PhysicalProviderHealth: ...

    def simulate(
        self,
        snapshot: PhysicalSnapshot,
        request: PhysicalSimulationRequest,
    ) -> PhysicalResolution: ...


__all__ = ["PhysicalWorldProvider"]
