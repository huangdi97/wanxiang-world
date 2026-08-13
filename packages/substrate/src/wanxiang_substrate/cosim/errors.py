"""Co-simulation error taxonomy (G11A-G11E)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class CoSimError(WanxiangError):
    """Base error for co-simulation failures."""

    code = "cosim_error"


class AdapterContractError(CoSimError):
    code = "simulation_adapter_contract"


class SimulationConflict(CoSimError):
    code = "simulation_proposal_conflict"


class OrchestrationError(CoSimError):
    code = "orchestration_error"
