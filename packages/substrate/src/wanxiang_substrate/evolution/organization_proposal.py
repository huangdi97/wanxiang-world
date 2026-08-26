"""Reviewed organization proposal record (G93E)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.evolution.delta import EvolutionProvenance, OrganizationDelta
from wanxiang_substrate.evolution.organization_model import (
    OrganizationLifecycleEvent,
    OrganizationLifecycleState,
)


@dataclass(frozen=True, slots=True)
class OrganizationLifecycleProposal:
    """A reviewed projection transition; it is not a canonical commit."""

    proposal_id: str
    before: OrganizationLifecycleState
    after: OrganizationLifecycleState
    event: OrganizationLifecycleEvent
    delta: OrganizationDelta
    provenance: EvolutionProvenance
    provider_ref: str
    approved: bool = False
    child_after: OrganizationLifecycleState | None = None

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.provider_ref.strip():
            raise ContractError("organization proposal requires id and provider")
        if self.provider_ref in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority cannot produce organization proposals")
        if self.event.organization_id != self.before.organization_id:
            raise ContractError("organization event does not target proposal state")
        if self.after.organization_id != self.before.organization_id:
            raise ContractError("organization proposal changes identity")
        if self.delta.organization_id != self.before.organization_id:
            raise ContractError("organization delta does not target proposal state")
        if self.event.action == "split" and self.child_after is None:
            raise ContractError("organization split proposal requires child projection")
        if self.event.action != "split" and self.child_after is not None:
            raise ContractError("only organization split may produce a child projection")
