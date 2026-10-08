"""Proposal-only provider run evidence with private payload redaction (G95E)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.providers import ProviderProposal
from wanxiang_substrate.world_lab.provider_models import PROVIDER_SCHEMA_VERSION
from wanxiang_substrate.world_lab.registry_support import integer, ref


@dataclass(frozen=True, slots=True)
class ProviderInvocation:
    """One proposal-only provider output, with payload excluded from evidence export."""

    member_ref: str
    provider_id: str
    provider_version: str
    input_hash: str
    control_transaction_id: str
    proposals: tuple[ProviderProposal, ...]

    def __post_init__(self) -> None:
        for name in (
            "member_ref",
            "provider_id",
            "provider_version",
            "input_hash",
            "control_transaction_id",
        ):
            ref(getattr(self, name), name)
        if any(type(proposal) is not ProviderProposal for proposal in self.proposals):
            raise ContractError("provider invocation output must contain ProviderProposal values")
        if any(proposal.provider_id != self.provider_id for proposal in self.proposals):
            raise ContractError("provider invocation contains a mismatched provider proposal")

    @property
    def proposal_ids(self) -> tuple[str, ...]:
        return tuple(proposal.proposal_id for proposal in self.proposals)

    def to_dict(self) -> dict[str, object]:
        return {
            "member_ref": self.member_ref,
            "provider_id": self.provider_id,
            "provider_version": self.provider_version,
            "input_hash": self.input_hash,
            "control_transaction_id": self.control_transaction_id,
            "proposal_ids": list(self.proposal_ids),
            "proposal_kinds": [proposal.kind for proposal in self.proposals],
            "proposal_count": len(self.proposals),
        }


@dataclass(frozen=True, slots=True)
class MultiProviderRun:
    """Sanitized evidence for mixed-provider execution; it owns no world state."""

    run_id: str
    policy_id: str
    policy_version: int
    input_hash: str
    invocations: tuple[ProviderInvocation, ...]
    control_transaction_ids: tuple[str, ...]
    schema_version: int = PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.run_id, "run_id")
        ref(self.policy_id, "policy_id")
        integer(self.policy_version, "policy_version", minimum=1)
        ref(self.input_hash, "input_hash")
        if self.schema_version != PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported multi-provider run schema")
        if not self.invocations:
            raise ContractError("multi-provider run requires provider invocations")
        if any(item.input_hash != self.input_hash for item in self.invocations):
            raise ContractError("provider invocations must use the same world input hash")
        refs = tuple(ref(item, "control transaction id") for item in self.control_transaction_ids)
        if len(refs) != len(set(refs)):
            raise ContractError("control transaction ids must be unique")
        object.__setattr__(self, "control_transaction_ids", refs)

    @property
    def provider_versions(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            sorted({(item.provider_id, item.provider_version) for item in self.invocations})
        )

    @property
    def proposal_count(self) -> int:
        return sum(len(item.proposals) for item in self.invocations)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "input_hash": self.input_hash,
            "provider_versions": [list(item) for item in self.provider_versions],
            "control_transaction_ids": list(self.control_transaction_ids),
            "invocations": [item.to_dict() for item in self.invocations],
            "proposal_count": self.proposal_count,
            "proposal_only": True,
        }


__all__ = ["MultiProviderRun", "ProviderInvocation"]
