"""R7 service contracts: stable seams a world composition may bind to."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from wanxiang_reality._contract_specs import CONTRACT_SPECS
from wanxiang_reality.errors import ContractError
from wanxiang_reality.hashing import canonical_digest


@dataclass(frozen=True, slots=True)
class ServiceContract:
    """One versioned service seam of the Wanxiang reality runtime."""

    namespace: str
    service_id: str
    api_version: str
    schema_version: str
    scope: str
    capabilities: tuple[str, ...]
    error_semantics: tuple[str, ...]
    compatibility: str

    def __post_init__(self) -> None:
        _validate_contract(self)

    @property
    def contract_id(self) -> str:
        """Return the stable ``namespace@api_version`` contract id."""
        return f"{self.namespace}@{self.api_version}"


def _validate_contract(contract: ServiceContract) -> None:
    required_text = (
        ("namespace", contract.namespace),
        ("service_id", contract.service_id),
        ("api_version", contract.api_version),
        ("schema_version", contract.schema_version),
        ("scope", contract.scope),
        ("compatibility", contract.compatibility),
    )
    for field_name, value in required_text:
        if not value.strip():
            raise ContractError(f"service contract {field_name} must not be empty")
    if not contract.capabilities:
        raise ContractError(f"service contract {contract.contract_id} needs capabilities")
    if not contract.error_semantics:
        raise ContractError(f"service contract {contract.contract_id} needs error semantics")
    if len(set(contract.capabilities)) != len(contract.capabilities):
        raise ContractError(f"service contract {contract.contract_id} has duplicate capabilities")


def _contract(
    name: str,
    scope: str,
    capabilities: tuple[str, ...],
    error_semantics: tuple[str, ...],
    compatibility: str,
) -> ServiceContract:
    return ServiceContract(
        namespace=f"wanxiang.{name}",
        service_id=name,
        api_version="1",
        schema_version="1",
        scope=scope,
        capabilities=capabilities,
        error_semantics=error_semantics,
        compatibility=compatibility,
    )


SERVICE_CONTRACTS: Final[tuple[ServiceContract, ...]] = tuple(
    _contract(*spec) for spec in CONTRACT_SPECS
)

_CONTRACTS_BY_ID: Final[dict[str, ServiceContract]] = {
    contract.contract_id: contract for contract in SERVICE_CONTRACTS
}


def get_contract(contract_id: str) -> ServiceContract:
    """Return the catalog contract for ``contract_id`` or raise ContractError."""
    contract = _CONTRACTS_BY_ID.get(contract_id)
    if contract is None:
        raise ContractError(f"unknown service contract: {contract_id!r}")
    return contract


def contract_manifest() -> dict[str, object]:
    """Return a JSON-serializable projection of the contract catalog."""
    return {"contracts": [_contract_entry(contract) for contract in SERVICE_CONTRACTS]}


def _contract_entry(contract: ServiceContract) -> dict[str, object]:
    return {
        "contract_id": contract.contract_id,
        "namespace": contract.namespace,
        "service_id": contract.service_id,
        "api_version": contract.api_version,
        "schema_version": contract.schema_version,
        "scope": contract.scope,
        "capabilities": list(contract.capabilities),
        "error_semantics": list(contract.error_semantics),
        "compatibility": contract.compatibility,
    }


def manifest_digest() -> str:
    """Return the canonical sha256 digest of the contract manifest."""
    return canonical_digest(contract_manifest())
