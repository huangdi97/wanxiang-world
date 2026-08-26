"""Proposal-only multi-provider execution over the existing provider boundary."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.providers import Provider, ProviderProposal
from wanxiang_substrate.capability.runtime_control import (
    RuntimeControlLedger,
    RuntimeControlTransaction,
)
from wanxiang_substrate.world_lab.provider_evidence import MultiProviderRun, ProviderInvocation
from wanxiang_substrate.world_lab.provider_models import (
    ProviderAssignment,
    ProviderAssignmentPolicy,
    ProviderRunInput,
)


class MultiProviderWorldlineRunner:
    """Assigns the same input to providers and returns proposals only."""

    def __init__(
        self,
        providers: Mapping[str, Provider],
        control_ledger: RuntimeControlLedger,
    ) -> None:
        if not providers:
            raise ContractError("multi-provider runner requires providers")
        self._providers = dict(providers)
        self.control_ledger = control_ledger

    def execute(
        self,
        run_input: ProviderRunInput,
        policy: ProviderAssignmentPolicy,
    ) -> MultiProviderRun:
        assignments = policy.assign(run_input.population_refs)
        controls = self._activate(run_input, policy, assignments)
        invocations = tuple(
            self._invoke(run_input, assignment, controls[assignment.provider_id])
            for assignment in assignments
        )
        return MultiProviderRun(
            run_id=run_input.run_id,
            policy_id=policy.policy_id,
            policy_version=policy.version,
            input_hash=run_input.input_hash,
            invocations=invocations,
            control_transaction_ids=tuple(controls.values()),
        )

    run = execute

    def _activate(
        self,
        run_input: ProviderRunInput,
        policy: ProviderAssignmentPolicy,
        assignments: tuple[ProviderAssignment, ...],
    ) -> dict[str, str]:
        controls: dict[str, str] = {}
        for provider_id in dict.fromkeys(item.provider_id for item in assignments):
            provider = self._provider(provider_id, run_input.private_source)
            transaction_id = f"{run_input.run_id}:provider:{provider_id}"
            transaction = RuntimeControlTransaction(
                transaction_id=transaction_id,
                operation="activate",
                provider_id=provider_id,
                capability_name=provider.capability.kind,
                version=provider.capability.version,
                rationale=f"assignment:{policy.policy_id}:v{policy.version}",
                created_at=run_input.control_timestamp,
            )
            existing = next(
                (
                    item
                    for item in self.control_ledger.entries()
                    if item.transaction_id == transaction_id
                ),
                None,
            )
            if existing is None:
                self.control_ledger.record(transaction)
            elif existing != transaction:
                raise ContractError(f"control transaction {transaction_id!r} conflicts")
            controls[provider_id] = transaction_id
        return controls

    def _invoke(
        self,
        run_input: ProviderRunInput,
        assignment: ProviderAssignment,
        control_transaction_id: str,
    ) -> ProviderInvocation:
        provider = self._provider(assignment.provider_id, run_input.private_source)
        raw = provider.propose(run_input.source_refs, run_input.payload)
        if type(raw) is not tuple:
            raise ContractError("provider output must be a tuple of ProviderProposal")
        proposals: list[ProviderProposal] = []
        for proposal in raw:
            if type(proposal) is not ProviderProposal:
                raise ContractError("provider output must contain ProviderProposal values")
            if proposal.provider_id != assignment.provider_id:
                raise ContractError("provider output identifies the wrong provider")
            if not set(proposal.source_refs).issubset(set(run_input.source_refs)):
                raise ContractError("provider output references an unrequested source")
            if hasattr(proposal, "commit"):
                raise ContractError("provider output cannot expose commit authority")
            proposals.append(proposal)
        return ProviderInvocation(
            member_ref=assignment.member_ref,
            provider_id=assignment.provider_id,
            provider_version=provider.capability.version,
            input_hash=run_input.input_hash,
            control_transaction_id=control_transaction_id,
            proposals=tuple(proposals),
        )

    def _provider(self, provider_id: str, private_source: bool) -> Provider:
        provider = self._providers.get(provider_id)
        if provider is None:
            raise ContractError(f"provider {provider_id!r} is not registered")
        capability = provider.capability
        if capability.provider_id != provider_id:
            raise ContractError("provider map key does not match provider capability")
        if not capability.available:
            raise ContractError(f"provider {provider_id!r} is unavailable")
        if not capability.deterministic:
            raise ContractError(f"provider {provider_id!r} is not replay-safe")
        if private_source and not capability.private_safe:
            raise ContractError(f"provider {provider_id!r} is not private-safe")
        return provider


MixedPopulationProviderRunner = MultiProviderWorldlineRunner


__all__ = ["MixedPopulationProviderRunner", "MultiProviderWorldlineRunner"]
