"""Provider policy and honest no-provider fallbacks (M62/G65)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from wanxiang_substrate.sources.errors import CapabilityUnavailable, OcrRequired

ProviderKind = Literal["llm", "embedding", "ocr", "asr", "vision", "linking", "temporal"]
ProposalKind = Literal["observation", "candidate", "claim", "completion", "repair", "asset"]


@dataclass(frozen=True, slots=True)
class ProviderCapability:
    provider_id: str
    kind: ProviderKind
    version: str
    available: bool = True
    cost_units: int = 1
    deterministic: bool = True
    private_safe: bool = False


@dataclass(frozen=True, slots=True)
class ProviderProposal:
    """Provider result; it cannot contain a Commit or canonical mutation."""

    proposal_id: str
    kind: ProposalKind
    provider_id: str
    source_refs: tuple[str, ...]
    payload: tuple[tuple[str, str], ...]
    confidence: float

    def __post_init__(self) -> None:
        if not self.proposal_id or not self.provider_id:
            raise ValueError("provider proposal requires ids")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("provider proposal confidence must be within [0,1]")


class Provider(Protocol):
    capability: ProviderCapability

    def propose(
        self, source_refs: tuple[str, ...], payload: str
    ) -> tuple[ProviderProposal, ...]: ...


class ReferenceProvider:
    """Deterministic provider used in CI and offline authoring."""

    def __init__(self, capability: ProviderCapability) -> None:
        self.capability = capability

    def propose(self, source_refs: tuple[str, ...], payload: str) -> tuple[ProviderProposal, ...]:
        if not self.capability.available:
            if self.capability.kind == "ocr":
                raise OcrRequired("OCR_REQUIRED: no OCR provider is available")
            return ()
        return (
            ProviderProposal(
                proposal_id=f"proposal_{self.capability.provider_id}",
                kind="candidate",
                provider_id=self.capability.provider_id,
                source_refs=source_refs,
                payload=(("content_hash", str(len(payload))),),
                confidence=0.0,
            ),
        )


class ProviderRouter:
    """Routes optional capabilities while retaining deterministic fallback."""

    def __init__(self, providers: tuple[Provider, ...] = ()) -> None:
        self._providers = {provider.capability.kind: provider for provider in providers}

    def capability(self, kind: ProviderKind) -> ProviderCapability | None:
        provider = self._providers.get(kind)
        return provider.capability if provider else None

    def propose(
        self, kind: ProviderKind, source_refs: tuple[str, ...], payload: str
    ) -> tuple[ProviderProposal, ...]:
        provider = self._providers.get(kind)
        if provider is None:
            if kind == "ocr":
                raise OcrRequired("OCR_REQUIRED: no OCR provider is registered")
            raise CapabilityUnavailable(f"CAPABILITY_UNAVAILABLE: no {kind} provider is registered")
        return provider.propose(source_refs, payload)

    def require(self, kind: ProviderKind, source_refs: tuple[str, ...] = ()) -> ProviderCapability:
        """Return a capability or raise an explicit provider requirement."""
        capability = self.capability(kind)
        if capability is None or not capability.available:
            if kind == "ocr":
                raise OcrRequired("OCR_REQUIRED: no OCR provider is available")
            raise CapabilityUnavailable(
                f"CAPABILITY_UNAVAILABLE: {kind} required for {','.join(source_refs)}"
            )
        return capability

    def select(
        self,
        kind: ProviderKind,
        *,
        private_source: bool = False,
        require_deterministic: bool = True,
        max_cost_units: int | None = None,
        source_refs: tuple[str, ...] = (),
    ) -> ProviderCapability:
        """Select a capability under privacy, determinism, and cost policy."""
        capability = self.require(kind, source_refs)
        if private_source and not capability.private_safe:
            raise CapabilityUnavailable(
                f"CAPABILITY_UNAVAILABLE: {kind} provider is not private-safe"
            )
        if require_deterministic and not capability.deterministic:
            raise CapabilityUnavailable(
                f"CAPABILITY_UNAVAILABLE: {kind} provider is nondeterministic"
            )
        if max_cost_units is not None and capability.cost_units > max_cost_units:
            raise CapabilityUnavailable(f"CAPABILITY_UNAVAILABLE: {kind} cost exceeds budget")
        return capability
