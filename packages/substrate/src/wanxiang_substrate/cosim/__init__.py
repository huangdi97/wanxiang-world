"""Co-simulation substrate (G11A-G11E)."""

from wanxiang_substrate.cosim.adapter import (
    FakeSimulator,
    FakeSimulatorState,
    SimulationAdapter,
)
from wanxiang_substrate.cosim.campaign import CampaignDomain, Order, Region, Unit
from wanxiang_substrate.cosim.errors import (
    AdapterContractError,
    CoSimError,
    OrchestrationError,
    SimulationConflict,
)
from wanxiang_substrate.cosim.orchestrator import (
    ArbitrationResult,
    CoSimOrchestrator,
    SimRegistration,
)

__all__ = [
    "AdapterContractError",
    "ArbitrationResult",
    "CampaignDomain",
    "CoSimError",
    "CoSimOrchestrator",
    "FakeSimulator",
    "FakeSimulatorState",
    "Order",
    "OrchestrationError",
    "Region",
    "SimRegistration",
    "SimulationAdapter",
    "SimulationConflict",
    "Unit",
]
