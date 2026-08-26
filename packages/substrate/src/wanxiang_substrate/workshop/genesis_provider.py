"""Prompt Genesis provider adapter over the shared ProviderRouter boundary."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.authoring.providers import (
    ProviderCapability,
    ProviderProposal,
    ProviderRouter,
)
from wanxiang_substrate.completion.candidates import CompletionCandidate
from wanxiang_substrate.sources.errors import SemanticProviderSchemaError
from wanxiang_substrate.workshop.genesis_contract import (
    CreatorIntent,
    DomainSuggestion,
    GenesisReviewGate,
    IntentConstraint,
    PromptGenesisContract,
    build_prompt_contract,
    extract_constraints,
)


class PromptGenesisProvider(Protocol):
    capability: ProviderCapability

    def propose(
        self, source_refs: tuple[str, ...], payload: str
    ) -> tuple[ProviderProposal, ...]: ...


class LocalPromptGenesisProvider:
    """Deterministic local provider for offline authoring and contract tests."""

    def __init__(self, provider_id: str = "local_prompt_genesis_v1") -> None:
        self.capability = ProviderCapability(
            provider_id=provider_id,
            kind="llm",
            version="1.0.0",
            available=True,
            cost_units=1,
            deterministic=True,
            private_safe=True,
        )

    def propose(self, source_refs: tuple[str, ...], payload: str) -> tuple[ProviderProposal, ...]:
        if len(source_refs) != 1:
            raise SemanticProviderSchemaError("prompt genesis requires one intent ref")
        try:
            raw = json.loads(payload)
            intent = CreatorIntent(str(raw["intent_id"]), str(raw["author_id"]), str(raw["text"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise SemanticProviderSchemaError("prompt genesis input schema is invalid") from exc
        if intent.intent_id != source_refs[0]:
            raise SemanticProviderSchemaError("prompt genesis intent ref does not match request")
        contract = build_prompt_contract(intent)
        proposals: list[ProviderProposal] = []
        for constraint in contract.constraints:
            proposals.append(
                self._proposal(
                    source_refs[0],
                    "constraint",
                    {
                        "constraint_id": constraint.constraint_id,
                        "constraint_kind": constraint.kind,
                        "value": constraint.value,
                    },
                )
            )
        for suggestion in contract.domain_suggestions:
            proposals.append(
                self._proposal(
                    source_refs[0],
                    "domain_suggestion",
                    {
                        "suggestion_id": suggestion.suggestion_id,
                        "domain_id": suggestion.domain_id,
                        "reason": suggestion.reason,
                        "score": str(suggestion.score),
                    },
                )
            )
        for claim in contract.claims:
            proposals.append(
                self._proposal(
                    source_refs[0],
                    "claim",
                    {
                        "completion_id": claim.completion_id,
                        "description": claim.description,
                        "confidence": str(claim.confidence),
                    },
                )
            )
        return tuple(proposals)

    def _proposal(
        self, intent_id: str, output_kind: str, values: Mapping[str, str]
    ) -> ProviderProposal:
        payload = (
            ("output_kind", output_kind),
            ("schema_version", "prompt-genesis-v1"),
            ("evidence_class", "E5"),
            *tuple(sorted((str(key), str(value)) for key, value in values.items())),
        )
        return ProviderProposal(
            proposal_id=f"{self.capability.provider_id}:{output_kind}:{len(values)}:{intent_id}",
            kind="candidate",
            provider_id=self.capability.provider_id,
            source_refs=(intent_id,),
            payload=payload,
            confidence=0.3,
        )


@dataclass(frozen=True, slots=True)
class PromptGenesisCheckpoint:
    intent_id: str
    provider_id: str
    attempts: int
    proposal_count: int
    complete: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "intent_id": self.intent_id,
            "provider_id": self.provider_id,
            "attempts": self.attempts,
            "proposal_count": self.proposal_count,
            "complete": self.complete,
        }


@dataclass(frozen=True, slots=True)
class PromptGenesisRun:
    contract: PromptGenesisContract
    provider_id: str
    proposals: tuple[ProviderProposal, ...]
    checkpoint: PromptGenesisCheckpoint

    @property
    def can_preview(self) -> bool:
        return self.contract.review_gate.ready_for_preview


class PromptGenesisProviderService:
    """Calls one selected provider and accepts only schema-valid candidates."""

    def __init__(self, router: ProviderRouter, *, retry_limit: int = 1) -> None:
        if retry_limit < 0:
            raise ValueError("retry_limit cannot be negative")
        self._router = router
        self._retry_limit = retry_limit

    def generate(self, intent: CreatorIntent, *, private_source: bool = True) -> PromptGenesisRun:
        capability = self._router.select(
            "llm",
            private_source=private_source,
            require_deterministic=True,
            source_refs=(intent.intent_id,),
        )
        payload = json.dumps(intent.to_dict(), ensure_ascii=False, sort_keys=True)
        proposals: tuple[ProviderProposal, ...] = ()
        attempts = 0
        for attempt in range(self._retry_limit + 1):
            attempts += 1
            try:
                proposals = self._router.propose("llm", (intent.intent_id,), payload)
                self._validate(proposals, intent, capability.provider_id)
                break
            except SemanticProviderSchemaError:
                if attempt >= self._retry_limit:
                    raise
        contract = self._contract_from_proposals(intent, proposals)
        checkpoint = PromptGenesisCheckpoint(
            intent.intent_id,
            capability.provider_id,
            attempts,
            len(proposals),
            True,
        )
        return PromptGenesisRun(contract, capability.provider_id, proposals, checkpoint)

    @staticmethod
    def _validate(
        proposals: tuple[ProviderProposal, ...], intent: CreatorIntent, provider_id: str
    ) -> None:
        for proposal in proposals:
            values = dict(proposal.payload)
            if (
                proposal.provider_id != provider_id
                or proposal.kind != "candidate"
                or proposal.source_refs != (intent.intent_id,)
                or values.get("schema_version") != "prompt-genesis-v1"
                or values.get("evidence_class") != "E5"
                or not values.get("output_kind")
            ):
                raise SemanticProviderSchemaError("prompt genesis provider output is invalid")
            if "commit" in values or "canonical_state" in values:
                raise SemanticProviderSchemaError("prompt provider cannot return authority fields")

    @staticmethod
    def _contract_from_proposals(
        intent: CreatorIntent, proposals: tuple[ProviderProposal, ...]
    ) -> PromptGenesisContract:
        base = build_prompt_contract(intent)
        constraints: list[IntentConstraint] = list(extract_constraints(intent))
        suggestions: list[DomainSuggestion] = []
        claims: list[CompletionCandidate] = []
        for proposal in proposals:
            values = dict(proposal.payload)
            output_kind = values.get("output_kind")
            if output_kind == "constraint" and values.get("constraint_kind"):
                kind = values["constraint_kind"]
                if kind not in (
                    "setting",
                    "genre",
                    "actor",
                    "place",
                    "rule",
                    "tone",
                    "time",
                    "goal",
                ):
                    raise SemanticProviderSchemaError("prompt constraint kind is invalid")
                constraints.append(
                    IntentConstraint(
                        values.get("constraint_id", proposal.proposal_id),
                        kind,
                        values.get("value", ""),
                        intent.intent_id,
                    )
                )
            elif output_kind == "domain_suggestion":
                try:
                    score = float(values.get("score", "0"))
                except ValueError as exc:
                    raise SemanticProviderSchemaError("prompt domain score is invalid") from exc
                suggestions.append(
                    DomainSuggestion(
                        values.get("suggestion_id", proposal.proposal_id),
                        values.get("domain_id", ""),
                        values.get("reason", ""),
                        intent.intent_id,
                        score,
                    )
                )
            elif output_kind == "claim":
                try:
                    confidence = float(values.get("confidence", "0"))
                except ValueError as exc:
                    raise SemanticProviderSchemaError("prompt claim confidence is invalid") from exc
                claims.append(
                    CompletionCandidate(
                        values.get("completion_id", proposal.proposal_id),
                        values.get("description", ""),
                        "E5",
                        (intent.intent_id,),
                        confidence,
                    )
                )
        unique_constraints = tuple({item.constraint_id: item for item in constraints}.values())
        unique_suggestions = tuple({item.suggestion_id: item for item in suggestions}.values())
        final_claims = tuple(claims) or base.claims
        return PromptGenesisContract(
            base.contract_id,
            intent,
            unique_constraints,
            unique_suggestions or base.domain_suggestions,
            final_claims,
            GenesisReviewGate(f"review_{base.contract_id}"),
        )


__all__ = [
    "LocalPromptGenesisProvider",
    "PromptGenesisCheckpoint",
    "PromptGenesisProvider",
    "PromptGenesisProviderService",
    "PromptGenesisRun",
]
