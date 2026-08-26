"""Hybrid Genesis fusion with explicit E0-E5 precedence and dissent records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.completion.candidates import CompletionCandidate
from wanxiang_substrate.workshop.genesis_contract import PromptGenesisContract

EvidenceClass = Literal["E0", "E1", "E2", "E3", "E4", "E5"]
ClaimOrigin = Literal["source", "prompt"]
Precedence = Literal["source", "prompt", "preserve_dissent"]


@dataclass(frozen=True, slots=True)
class HybridClaim:
    """One source or prompt claim retained as an auditable alternative."""

    claim_id: str
    key: str
    value: str
    origin: ClaimOrigin
    evidence_class: EvidenceClass
    source_refs: tuple[str, ...] = ()
    intent_ref: str = ""

    def __post_init__(self) -> None:
        if not self.claim_id or not self.key or not self.value.strip():
            raise ContractError("hybrid claim requires id, key and value")
        if self.origin not in {"source", "prompt"}:
            raise ContractError("hybrid claim origin is invalid")
        if self.origin == "source" and not self.source_refs:
            raise ContractError("source claim requires source refs")
        if self.origin == "prompt" and not self.intent_ref:
            raise ContractError("prompt claim requires intent ref")


@dataclass(frozen=True, slots=True)
class HybridGenesisPolicy:
    """Precedence is a selection hint; alternatives are never discarded."""

    precedence: Precedence = "source"
    preserve_dissent: bool = True

    def __post_init__(self) -> None:
        if self.precedence not in {"source", "prompt", "preserve_dissent"}:
            raise ContractError(f"unsupported hybrid precedence {self.precedence!r}")
        if not self.preserve_dissent:
            raise ContractError("hybrid genesis must preserve dissent alternatives")


@dataclass(frozen=True, slots=True)
class HybridTrace:
    claim_id: str
    origin: ClaimOrigin
    evidence_class: EvidenceClass
    source_refs: tuple[str, ...]
    intent_ref: str
    parent_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "claim_id": self.claim_id,
            "origin": self.origin,
            "evidence_class": self.evidence_class,
            "source_refs": list(self.source_refs),
            "intent_ref": self.intent_ref,
            "parent_refs": list(self.parent_refs),
        }


@dataclass(frozen=True, slots=True)
class HybridConflict:
    key: str
    claim_ids: tuple[str, ...]
    selected_claim_id: str | None
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "key": self.key,
            "claim_ids": list(self.claim_ids),
            "selected_claim_id": self.selected_claim_id,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class HybridGenesisResult:
    claims: tuple[HybridClaim, ...]
    traces: tuple[HybridTrace, ...]
    conflicts: tuple[HybridConflict, ...]
    policy: HybridGenesisPolicy
    fingerprint: str

    @property
    def review_required(self) -> bool:
        return bool(self.conflicts) or any(claim.origin == "prompt" for claim in self.claims)

    @property
    def selected_claim_ids(self) -> tuple[str, ...]:
        return tuple(
            conflict.selected_claim_id
            for conflict in self.conflicts
            if conflict.selected_claim_id is not None
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "claims": [
                {
                    "claim_id": claim.claim_id,
                    "key": claim.key,
                    "value": claim.value,
                    "origin": claim.origin,
                    "evidence_class": claim.evidence_class,
                    "source_refs": list(claim.source_refs),
                    "intent_ref": claim.intent_ref,
                }
                for claim in self.claims
            ],
            "traces": [trace.to_dict() for trace in self.traces],
            "conflicts": [conflict.to_dict() for conflict in self.conflicts],
            "precedence": self.policy.precedence,
            "fingerprint": self.fingerprint,
        }


def claim_from_candidate(
    candidate: CandidateEnvelope, *, evidence_class: EvidenceClass = "E3"
) -> HybridClaim:
    """Adapt an existing source candidate without creating a second candidate fabric."""
    fields = candidate.fields
    key = fields.get("key") or fields.get("name") or candidate.kind
    value = (
        fields.get("value")
        or fields.get("display_name")
        or json.dumps(fields, ensure_ascii=False, sort_keys=True)
    )
    return HybridClaim(
        candidate.candidate_id,
        f"{candidate.kind}:{key}",
        value,
        "source",
        evidence_class,
        candidate.source_refs,
    )


def _prompt_claims(contract: PromptGenesisContract) -> tuple[HybridClaim, ...]:
    claims: list[HybridClaim] = []
    for item in contract.constraints:
        claims.append(
            HybridClaim(
                item.constraint_id,
                f"{item.kind}:{item.kind}",
                item.value,
                "prompt",
                "E5",
                intent_ref=contract.intent.intent_id,
            )
        )
    for item in contract.claims:
        claims.append(_prompt_completion(item, contract.intent.intent_id))
    return tuple(claims)


def _prompt_completion(item: CompletionCandidate, intent_id: str) -> HybridClaim:
    return HybridClaim(
        item.completion_id,
        "completion:" + item.completion_id,
        item.description,
        "prompt",
        "E5",
        intent_ref=intent_id,
    )


def fuse_hybrid_genesis(
    source_claims: tuple[HybridClaim, ...],
    prompt: PromptGenesisContract,
    *,
    policy: HybridGenesisPolicy | None = None,
) -> HybridGenesisResult:
    """Fuse source and prompt proposals while retaining all conflicting claims."""
    active_policy = policy or HybridGenesisPolicy()
    prompt_claims = _prompt_claims(prompt)
    claims = tuple(sorted((*source_claims, *prompt_claims), key=lambda item: item.claim_id))
    by_key: dict[str, list[HybridClaim]] = {}
    for claim in claims:
        by_key.setdefault(claim.key, []).append(claim)
    conflicts: list[HybridConflict] = []
    for key in sorted(by_key):
        alternatives = by_key[key]
        values = {item.value for item in alternatives}
        if len(values) < 2:
            continue
        source = next((item for item in alternatives if item.origin == "source"), None)
        prompt_claim = next((item for item in alternatives if item.origin == "prompt"), None)
        selected: str | None = None
        if active_policy.precedence == "source" and source is not None:
            selected = source.claim_id
        elif active_policy.precedence == "prompt" and prompt_claim is not None:
            selected = prompt_claim.claim_id
        conflicts.append(
            HybridConflict(
                key,
                tuple(item.claim_id for item in alternatives),
                selected,
                "alternatives preserved; selected value requires explicit review",
            )
        )
    traces = tuple(
        HybridTrace(
            claim.claim_id,
            claim.origin,
            claim.evidence_class,
            claim.source_refs,
            claim.intent_ref,
        )
        for claim in claims
    )
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "claims": [(item.claim_id, item.key, item.value) for item in claims],
                "conflicts": [(item.key, item.claim_ids) for item in conflicts],
                "precedence": active_policy.precedence,
            },
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return HybridGenesisResult(claims, traces, tuple(conflicts), active_policy, fingerprint)


__all__ = [
    "HybridClaim",
    "HybridConflict",
    "HybridGenesisPolicy",
    "HybridGenesisResult",
    "HybridTrace",
    "claim_from_candidate",
    "fuse_hybrid_genesis",
]
