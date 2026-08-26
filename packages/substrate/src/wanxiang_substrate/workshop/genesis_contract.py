"""Prompt Genesis contracts: intent becomes reviewed E5 candidates, never truth."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.completion.candidates import CompletionCandidate

ConstraintKind = Literal["setting", "genre", "actor", "place", "rule", "tone", "time", "goal"]
VALID_CONSTRAINTS = (
    "setting",
    "genre",
    "actor",
    "place",
    "rule",
    "tone",
    "time",
    "goal",
)


@dataclass(frozen=True, slots=True)
class CreatorIntent:
    """User-authored intent kept in a data channel with stable provenance."""

    intent_id: str
    author_id: str
    text: str
    source_channel: str = "creator_intent"
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.intent_id or not self.author_id or not self.text.strip():
            raise ContractError("creator intent requires id, author and text")
        if self.source_channel != "creator_intent" or self.schema_version != 1:
            raise ContractError("creator intent channel or schema is unsupported")

    @property
    def text_hash(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "intent_id": self.intent_id,
            "author_id": self.author_id,
            "text": self.text,
            "source_channel": self.source_channel,
            "text_hash": self.text_hash,
        }


@dataclass(frozen=True, slots=True)
class IntentConstraint:
    """An explicit user constraint; it is not a source-backed fact."""

    constraint_id: str
    kind: ConstraintKind
    value: str
    intent_id: str
    explicit: bool = True
    evidence_class: Literal["E5"] = "E5"

    def __post_init__(self) -> None:
        if not self.constraint_id or not self.intent_id or not self.value.strip():
            raise ContractError("intent constraint requires id, intent and value")
        if self.kind not in VALID_CONSTRAINTS:
            raise ContractError(f"unsupported intent constraint kind {self.kind!r}")
        if self.evidence_class != "E5":
            raise ContractError("prompt constraints must remain E5")

    def to_dict(self) -> dict[str, object]:
        return {
            "constraint_id": self.constraint_id,
            "kind": self.kind,
            "value": self.value,
            "intent_id": self.intent_id,
            "explicit": self.explicit,
            "evidence_class": self.evidence_class,
        }


@dataclass(frozen=True, slots=True)
class DomainSuggestion:
    """Candidate domain selection with explainable prompt provenance."""

    suggestion_id: str
    domain_id: str
    reason: str
    intent_id: str
    score: float
    evidence_class: Literal["E5"] = "E5"

    def __post_init__(self) -> None:
        if not self.suggestion_id or not self.domain_id or not self.reason:
            raise ContractError("domain suggestion requires id, domain and reason")
        if not self.intent_id or not 0.0 <= self.score <= 1.0:
            raise ContractError("domain suggestion requires intent and bounded score")
        if self.evidence_class != "E5":
            raise ContractError("prompt domain suggestions must remain E5")

    def to_dict(self) -> dict[str, object]:
        return {
            "suggestion_id": self.suggestion_id,
            "domain_id": self.domain_id,
            "reason": self.reason,
            "intent_id": self.intent_id,
            "score": self.score,
            "evidence_class": self.evidence_class,
        }


@dataclass(frozen=True, slots=True)
class GenesisReviewGate:
    """Explicit review boundary before an E5 prompt draft can be previewed."""

    gate_id: str
    required_actions: tuple[str, ...] = ("review_e5", "accept_constraints", "preview")
    accepted_actions: tuple[str, ...] = ()

    @property
    def ready_for_preview(self) -> bool:
        return set(self.required_actions).issubset(self.accepted_actions)

    def accept(self, action: str) -> GenesisReviewGate:
        if action not in self.required_actions:
            raise ContractError(f"unknown genesis review action {action!r}")
        return GenesisReviewGate(
            self.gate_id,
            self.required_actions,
            tuple(dict.fromkeys((*self.accepted_actions, action))),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "required_actions": list(self.required_actions),
            "accepted_actions": list(self.accepted_actions),
            "ready_for_preview": self.ready_for_preview,
        }


@dataclass(frozen=True, slots=True)
class PromptGenesisContract:
    """Structured prompt output whose generated claims are all E5."""

    contract_id: str
    intent: CreatorIntent
    constraints: tuple[IntentConstraint, ...]
    domain_suggestions: tuple[DomainSuggestion, ...]
    claims: tuple[CompletionCandidate, ...]
    review_gate: GenesisReviewGate

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ContractError("prompt genesis contract requires an id")
        if any(claim.completion_class != "E5" for claim in self.claims):
            raise ContractError("all prompt-generated claims must be E5")
        if any(claim.can_enter_canon for claim in self.claims):
            raise ContractError("prompt claims cannot enter canon before review")

    @property
    def generated_fact_ids(self) -> tuple[str, ...]:
        return tuple(claim.completion_id for claim in self.claims)

    def accept(self, action: str) -> PromptGenesisContract:
        return PromptGenesisContract(
            self.contract_id,
            self.intent,
            self.constraints,
            self.domain_suggestions,
            self.claims,
            self.review_gate.accept(action),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "contract_id": self.contract_id,
            "intent": self.intent.to_dict(),
            "constraints": [item.to_dict() for item in self.constraints],
            "domain_suggestions": [item.to_dict() for item in self.domain_suggestions],
            "claims": [
                {
                    "completion_id": claim.completion_id,
                    "description": claim.description,
                    "completion_class": claim.completion_class,
                    "support_refs": list(claim.support_refs),
                    "confidence": claim.confidence,
                }
                for claim in self.claims
            ],
            "review_gate": self.review_gate.to_dict(),
        }


_EXPLICIT = re.compile(
    r"(?im)^\s*(setting|genre|actor|place|rule|tone|time|goal)\s*[:：]\s*([^\n]+)"
)
_DIRECTIVE = re.compile(r"(?i)\b(ignore|system message|developer message|execute|tool call)\b")


def extract_constraints(intent: CreatorIntent) -> tuple[IntentConstraint, ...]:
    """Parse only explicit labelled data; directive-like text is never executed."""
    found: list[IntentConstraint] = []
    for index, match in enumerate(_EXPLICIT.finditer(intent.text), start=1):
        kind = match.group(1).lower()
        value = " ".join(match.group(2).split()).strip(" ,，。.;；")
        if not value:
            continue
        found.append(IntentConstraint(f"constraint_{index}", kind, value, intent.intent_id))  # type: ignore[arg-type]
    return tuple(found)


def build_prompt_contract(intent: CreatorIntent) -> PromptGenesisContract:
    """Create a deterministic E5 contract while preserving unparsed intent."""
    constraints = extract_constraints(intent)
    values = " ".join(item.value.lower() for item in constraints)
    markers = (
        ("spatial", ("place", "city", "garden", "地点", "城市"), "explicit place or spatial cue"),
        ("family", ("family", "genealogy", "家庭", "家族"), "family cue in creator intent"),
        ("household", ("rule", "norm", "institution", "规则", "制度"), "rule or institution cue"),
        ("narrative", ("actor", "character", "goal", "story", "角色", "目标"), "actor or goal cue"),
    )
    suggestions = tuple(
        DomainSuggestion(
            f"domain_{index}",
            domain_id,
            reason,
            intent.intent_id,
            min(0.9, 0.5 + 0.1 * sum(marker in values for marker in markers)),
        )
        for index, (domain_id, markers, reason) in enumerate(markers, start=1)
        if any(marker in values for marker in markers)
    )
    claims = tuple(
        CompletionCandidate(
            completion_id=f"prompt_claim_{index}",
            description=f"{item.kind}: {item.value}",
            completion_class="E5",
            support_refs=(intent.intent_id,),
            confidence=0.3,
        )
        for index, item in enumerate(constraints, start=1)
    )
    if not claims and not _DIRECTIVE.search(intent.text):
        claims = (
            CompletionCandidate(
                "prompt_claim_freeform",
                "creator-authored world intent requires review",
                "E5",
                (intent.intent_id,),
                0.2,
            ),
        )
    contract_id = f"genesis_{intent.text_hash[:16]}"
    return PromptGenesisContract(
        contract_id,
        intent,
        constraints,
        suggestions,
        claims,
        GenesisReviewGate(f"review_{contract_id}"),
    )


__all__ = [
    "CreatorIntent",
    "DomainSuggestion",
    "GenesisReviewGate",
    "IntentConstraint",
    "PromptGenesisContract",
    "build_prompt_contract",
    "extract_constraints",
]
