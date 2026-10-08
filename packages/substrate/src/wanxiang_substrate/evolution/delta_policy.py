"""Proposal provenance and Commit Authority receipt policy for evolution."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.evolution.delta_common import EvolutionDeltaKind, text
from wanxiang_substrate.evolution.delta_records import (
    BeliefDelta,
    CapabilityEvolutionDelta,
    EvolutionDelta,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
    StateDelta,
)


@dataclass(frozen=True, slots=True)
class EvolutionCommitReceipt:
    """Evidence that the existing Commit Authority appended a delta effect."""

    delta_id: str
    delta_kind: EvolutionDeltaKind
    event_ref: str
    branch_revision: int
    authority_ref: str

    def __post_init__(self) -> None:
        text(self.delta_id, "delta_id")
        text(self.event_ref, "event_ref")
        text(self.authority_ref, "authority_ref")
        if type(self.branch_revision) is not int or self.branch_revision < 1:
            raise ContractError("committed evolution revision must be positive")


class EvolutionCommitPolicy:
    """Validate proposals and issue receipts without mutating canonical state."""

    @staticmethod
    def validate_proposal(delta: object) -> None:
        supported = (
            StateDelta,
            BeliefDelta,
            RelationshipDelta,
            CapabilityEvolutionDelta,
            PersonaDelta,
            OrganizationDelta,
        )
        if not isinstance(delta, supported):
            raise ContractError("unsupported evolution delta type")
        if not delta.provenance.source_refs and not delta.provenance.event_refs:
            raise ContractError("evolution proposal requires source or event provenance")
        if delta.provenance.producer in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority is a consumer, not a proposal producer")

    @classmethod
    def receipt(
        cls,
        delta: EvolutionDelta,
        *,
        event_ref: str,
        branch_revision: int,
        authority_ref: str,
    ) -> EvolutionCommitReceipt:
        cls.validate_proposal(delta)
        return EvolutionCommitReceipt(
            delta_id=delta.delta_id,
            delta_kind=delta.kind,
            event_ref=event_ref,
            branch_revision=branch_revision,
            authority_ref=authority_ref,
        )
