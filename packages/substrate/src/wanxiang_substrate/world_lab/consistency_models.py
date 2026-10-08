"""Versioned proposal-only reality consistency records for M93/G96G."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.serialization import delta_from_primitive, delta_to_primitive

from wanxiang_substrate.world_lab.registry_support import integer, names, ref, sequence

REALITY_CONSISTENCY_SCHEMA_VERSION = 1
RealityOutputKind = Literal["visual_projection", "physical_resolution"]
RealityConsistencyStatus = Literal["consistent", "stale", "divergent", "rejected"]
ReconciliationAction = Literal[
    "retain",
    "refresh_projection",
    "recompute_physical",
    "review",
]
_OUTPUT_KINDS = frozenset({"visual_projection", "physical_resolution"})
_STATUSES = frozenset({"consistent", "stale", "divergent", "rejected"})
_ACTIONS = frozenset({"retain", "refresh_projection", "recompute_physical", "review"})


def _value(value: object, name: str, allowed: frozenset[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ContractError(f"unsupported {name} {value!r}")
    return value


def _reason(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ContractError(f"{name} must be non-empty one-line text")
    return value


@dataclass(frozen=True, slots=True)
class RealityReconciliationProposal:
    """A consumer instruction that never carries a canonical world delta."""

    proposal_ref: str
    output_kind: RealityOutputKind
    status: RealityConsistencyStatus
    action: ReconciliationAction
    canonical_ref: str
    canonical_revision: int
    observed_ref: str
    observed_revision: int
    reason: str
    proposed_delta: ProposedWorldDelta = ProposedWorldDelta()
    evidence_refs: tuple[str, ...] = ()
    schema_version: int = REALITY_CONSISTENCY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.proposal_ref, "proposal_ref")
        _value(self.output_kind, "output kind", _OUTPUT_KINDS)
        _value(self.status, "consistency status", _STATUSES)
        _value(self.action, "reconciliation action", _ACTIONS)
        ref(self.canonical_ref, "canonical_ref")
        ref(self.observed_ref, "observed_ref")
        integer(self.canonical_revision, "canonical_revision", minimum=0)
        integer(self.observed_revision, "observed_revision", minimum=0)
        _reason(self.reason, "reconciliation reason")
        if type(self.proposed_delta) is not ProposedWorldDelta:
            raise ContractError("reconciliation proposed_delta must be ProposedWorldDelta")
        if not self.proposed_delta.is_empty():
            raise ContractError("reconciliation proposal cannot carry a canonical delta")
        if self.schema_version != REALITY_CONSISTENCY_SCHEMA_VERSION:
            raise ContractError("unsupported reality consistency proposal schema")
        object.__setattr__(self, "evidence_refs", names(self.evidence_refs, "evidence_refs"))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "proposal_ref": self.proposal_ref,
            "output_kind": self.output_kind,
            "status": self.status,
            "action": self.action,
            "canonical_ref": self.canonical_ref,
            "canonical_revision": self.canonical_revision,
            "observed_ref": self.observed_ref,
            "observed_revision": self.observed_revision,
            "reason": self.reason,
            "proposed_delta": delta_to_primitive(self.proposed_delta),
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> RealityReconciliationProposal:
        raw_delta = data.get("proposed_delta")
        if not isinstance(raw_delta, Mapping):
            raise ContractError("reconciliation proposed_delta must be a mapping")
        raw_refs = sequence(data.get("evidence_refs", ()), "evidence_refs")
        return cls(
            proposal_ref=ref(data.get("proposal_ref"), "proposal_ref"),
            output_kind=cast(
                RealityOutputKind,
                _value(data.get("output_kind"), "output kind", _OUTPUT_KINDS),
            ),
            status=cast(
                RealityConsistencyStatus,
                _value(data.get("status"), "consistency status", _STATUSES),
            ),
            action=cast(
                ReconciliationAction,
                _value(data.get("action"), "reconciliation action", _ACTIONS),
            ),
            canonical_ref=ref(data.get("canonical_ref"), "canonical_ref"),
            canonical_revision=integer(
                data.get("canonical_revision"), "canonical_revision", minimum=0
            ),
            observed_ref=ref(data.get("observed_ref"), "observed_ref"),
            observed_revision=integer(
                data.get("observed_revision"), "observed_revision", minimum=0
            ),
            reason=_reason(data.get("reason"), "reconciliation reason"),
            proposed_delta=delta_from_primitive(cast(dict[str, object], raw_delta)),
            evidence_refs=tuple(ref(value, "evidence_refs item") for value in raw_refs),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class RealityConsistencyResult:
    """Auditable comparison between a canonical read model and provider output."""

    result_ref: str
    output_kind: RealityOutputKind
    status: RealityConsistencyStatus
    canonical_ref: str
    canonical_revision: int
    canonical_state_hash: str
    observed_ref: str
    observed_revision: int
    observed_state_hash: str | None
    mismatch_codes: tuple[str, ...]
    proposal: RealityReconciliationProposal
    evidence_refs: tuple[str, ...] = ()
    schema_version: int = REALITY_CONSISTENCY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.result_ref, "result_ref")
        _value(self.output_kind, "output kind", _OUTPUT_KINDS)
        _value(self.status, "consistency status", _STATUSES)
        ref(self.canonical_ref, "canonical_ref")
        ref(self.observed_ref, "observed_ref")
        integer(self.canonical_revision, "canonical_revision", minimum=0)
        integer(self.observed_revision, "observed_revision", minimum=0)
        ref(self.canonical_state_hash, "canonical_state_hash")
        if self.observed_state_hash is not None:
            ref(self.observed_state_hash, "observed_state_hash")
        object.__setattr__(self, "mismatch_codes", names(self.mismatch_codes, "mismatch_codes"))
        if type(self.proposal) is not RealityReconciliationProposal:
            raise ContractError("proposal must be RealityReconciliationProposal")
        if (
            self.proposal.output_kind != self.output_kind
            or self.proposal.status != self.status
            or self.proposal.canonical_ref != self.canonical_ref
            or self.proposal.canonical_revision != self.canonical_revision
            or self.proposal.observed_ref != self.observed_ref
            or self.proposal.observed_revision != self.observed_revision
        ):
            raise ContractError("reconciliation proposal does not match consistency result")
        if self.schema_version != REALITY_CONSISTENCY_SCHEMA_VERSION:
            raise ContractError("unsupported reality consistency result schema")
        object.__setattr__(self, "evidence_refs", names(self.evidence_refs, "evidence_refs"))

    @property
    def is_consistent(self) -> bool:
        return self.status == "consistent"

    @property
    def is_stale(self) -> bool:
        return self.status == "stale"

    @property
    def is_divergent(self) -> bool:
        return self.status == "divergent"

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "output_kind": self.output_kind,
            "status": self.status,
            "canonical_ref": self.canonical_ref,
            "canonical_revision": self.canonical_revision,
            "canonical_state_hash": self.canonical_state_hash,
            "observed_ref": self.observed_ref,
            "observed_revision": self.observed_revision,
            "observed_state_hash": self.observed_state_hash,
            "mismatch_codes": list(self.mismatch_codes),
            "proposal": self.proposal.to_dict(),
            "evidence_refs": list(self.evidence_refs),
        }

    @property
    def replay_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["result_ref"] = self.result_ref
        payload["replay_hash"] = self.replay_hash
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> RealityConsistencyResult:
        raw_proposal = data.get("proposal")
        if not isinstance(raw_proposal, Mapping):
            raise ContractError("consistency proposal must be a mapping")
        raw_mismatches = sequence(data.get("mismatch_codes", ()), "mismatch_codes")
        observed_hash = data.get("observed_state_hash")
        if observed_hash is not None and not isinstance(observed_hash, str):
            raise ContractError("observed_state_hash must be text or null")
        result = cls(
            result_ref=ref(data.get("result_ref"), "result_ref"),
            output_kind=cast(
                RealityOutputKind,
                _value(data.get("output_kind"), "output kind", _OUTPUT_KINDS),
            ),
            status=cast(
                RealityConsistencyStatus,
                _value(data.get("status"), "consistency status", _STATUSES),
            ),
            canonical_ref=ref(data.get("canonical_ref"), "canonical_ref"),
            canonical_revision=integer(
                data.get("canonical_revision"), "canonical_revision", minimum=0
            ),
            canonical_state_hash=ref(data.get("canonical_state_hash"), "canonical_state_hash"),
            observed_ref=ref(data.get("observed_ref"), "observed_ref"),
            observed_revision=integer(
                data.get("observed_revision"), "observed_revision", minimum=0
            ),
            observed_state_hash=observed_hash,
            mismatch_codes=tuple(ref(value, "mismatch_codes item") for value in raw_mismatches),
            proposal=RealityReconciliationProposal.from_dict(
                cast(Mapping[str, object], raw_proposal)
            ),
            evidence_refs=tuple(
                ref(value, "evidence_refs item")
                for value in sequence(data.get("evidence_refs", ()), "evidence_refs")
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )
        if data.get("replay_hash") != result.replay_hash:
            raise ContractError("reality consistency replay hash does not verify")
        return result


__all__ = [
    "REALITY_CONSISTENCY_SCHEMA_VERSION",
    "RealityConsistencyResult",
    "RealityConsistencyStatus",
    "RealityOutputKind",
    "RealityReconciliationProposal",
    "ReconciliationAction",
]
