"""R7 service contracts: the stable seams a world composition may bind to.

A contract id is ``<namespace>@<api_version>`` (for example
``wanxiang.history@1``). The catalog below is the single source of truth for
``get_contract``, the JSON manifest and its digest.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

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
    """Build one catalog entry with the fixed ``wanxiang.<name>@1`` identity."""
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


SERVICE_CONTRACTS: Final[tuple[ServiceContract, ...]] = (
    _contract(
        "identity",
        "root",
        ("identity.authenticate", "identity.delegate"),
        ("identity-unresolved", "credential-rejected"),
        "same-major-provider-swap",
    ),
    _contract(
        "reality.observe",
        "world",
        ("reality.observe.read", "reality.observe.stream"),
        ("observation-rejected", "scope-denied"),
        "additive-minor",
    ),
    _contract(
        "reality.proposal",
        "world",
        ("reality.propose.command", "reality.propose.delta"),
        ("proposal-rejected", "stale-revision"),
        "additive-minor",
    ),
    _contract(
        "reality.policy",
        "tenant",
        ("reality.policy.evaluate", "reality.policy.publish"),
        ("policy-conflict", "policy-unsatisfied"),
        "same-major-provider-swap",
    ),
    _contract(
        "authority",
        "root",
        ("authority.commit", "authority.audit"),
        ("not-commit-authority", "stale-revision"),
        "same-major-provider-swap",
    ),
    _contract(
        "history",
        "worldline",
        ("history.append", "history.read"),
        ("append-conflict", "history-gap"),
        "same-major-provider-swap",
    ),
    _contract(
        "branch",
        "worldline",
        ("branch.fork", "branch.merge"),
        ("branch-diverged", "stale-branch-revision"),
        "additive-minor",
    ),
    _contract(
        "lineage",
        "worldline",
        ("lineage.trace", "lineage.verify"),
        ("lineage-broken", "unknown-ancestor"),
        "same-major-provider-swap",
    ),
    _contract(
        "replay",
        "worldline",
        ("replay.from-event", "replay.verify"),
        ("replay-divergence", "history-unavailable"),
        "same-major-provider-swap",
    ),
    _contract(
        "evidence",
        "world",
        ("evidence.record", "evidence.verify"),
        ("evidence-missing", "digest-mismatch"),
        "additive-minor",
    ),
    _contract(
        "rights",
        "tenant",
        ("rights.grant", "rights.revoke"),
        ("right-denied", "right-unknown"),
        "additive-minor",
    ),
    _contract(
        "execution",
        "world",
        ("execution.schedule", "execution.cancel"),
        ("execution-rejected", "runtime-unavailable"),
        "same-major-provider-swap",
    ),
    _contract(
        "actor",
        "world",
        ("actor.observe", "actor.control"),
        ("actor-unresolved", "control-denied"),
        "additive-minor",
    ),
    _contract(
        "model",
        "tenant",
        ("model.invoke", "model.qualify"),
        ("model-unavailable", "qualification-failed"),
        "same-major-provider-swap",
    ),
    _contract(
        "capability",
        "root",
        ("capability.register", "capability.resolve"),
        ("capability-unknown", "capability-conflict"),
        "additive-minor",
    ),
    _contract(
        "reality.profile",
        "world",
        ("reality.profile.read", "reality.profile.lock"),
        ("profile-unknown", "profile-mismatch"),
        "additive-minor",
    ),
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
