"""Evidence-bound reputation proposals and immutable review decisions (G93F)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.evolution.delta import EvolutionProvenance, StateDelta
from wanxiang_substrate.evolution.reputation_model import ReputationEvent, ReputationState


def reputation_field(state: ReputationState) -> str:
    """Encode the full projection key in the existing scalar StateDelta field."""
    observer = state.observer_actor_id.value if state.observer_actor_id is not None else "aggregate"
    return f"reputation:{state.scope}:{state.scope_ref}:{state.dimension}:{observer}"


@dataclass(frozen=True, slots=True)
class ReputationUpdateProposal:
    """A reviewed-later reputation change; construction never mutates a world."""

    proposal_id: str
    before: ReputationState
    after: ReputationState
    events: tuple[ReputationEvent, ...]
    state_delta: StateDelta
    provenance: EvolutionProvenance
    provider_ref: str
    approved: bool = False

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.provider_ref.strip():
            raise ContractError("reputation proposal requires id and provider")
        if self.provider_ref in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority cannot produce reputation proposals")
        if self.provenance.producer in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority cannot produce reputation proposals")
        if self.before.key != self.after.key:
            raise ContractError("reputation proposal state keys do not match")
        if self.after.updated_ticks < self.before.updated_ticks:
            raise ContractError("reputation proposal moves backwards in time")
        if not self.events:
            raise ContractError("reputation proposal requires social events")
        event_refs = tuple(event.event_ref for event in self.events)
        if len(set(event_refs)) != len(event_refs):
            raise ContractError("reputation proposal events must be unique")
        if any(event.event_ref not in self.after.event_refs for event in self.events):
            raise ContractError("reputation state is missing proposal event evidence")
        if self.state_delta.subject_id != self.before.subject_actor_id:
            raise ContractError("reputation delta subject does not match proposal")
        if self.state_delta.field != reputation_field(self.before):
            raise ContractError("reputation delta field does not match projection key")
        if (
            self.state_delta.before != self.before.score
            or self.state_delta.after != self.after.score
        ):
            raise ContractError("reputation delta values do not match proposal")
        if self.state_delta.provenance != self.provenance:
            raise ContractError("reputation delta provenance does not match proposal")
