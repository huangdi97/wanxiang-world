"""G90C: shared provider boundary, deterministic local path, no authority output."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.sources.errors import SemanticProviderSchemaError
from wanxiang_substrate.workshop import (
    CreatorIntent,
    LocalPromptGenesisProvider,
    PromptGenesisProviderService,
)


def test_missing_llm_provider_is_typed_and_does_not_fallback_silently() -> None:
    with pytest.raises(Exception, match="CAPABILITY_UNAVAILABLE"):
        PromptGenesisProviderService(ProviderRouter()).generate(
            CreatorIntent("intent_no_provider", "author", "setting: a town")
        )


def test_local_provider_generates_schema_valid_e5_candidates() -> None:
    router = ProviderRouter((LocalPromptGenesisProvider(),))
    run = PromptGenesisProviderService(router).generate(
        CreatorIntent("intent_local", "author", "setting: a town\nactor: keeper"),
        private_source=True,
    )
    assert run.checkpoint.complete is True
    assert run.provider_id == "local_prompt_genesis_v1"
    assert run.proposals
    assert all(dict(item.payload)["evidence_class"] == "E5" for item in run.proposals)
    assert all("commit" not in dict(item.payload) for item in run.proposals)
    assert all(claim.completion_class == "E5" for claim in run.contract.claims)


class InvalidProvider(LocalPromptGenesisProvider):
    def propose(self, source_refs: tuple[str, ...], payload: str):
        _ = source_refs, payload
        return (self._proposal("wrong-intent", "claim", {"description": "bad"}),)


def test_provider_provenance_is_checked_before_contract_creation() -> None:
    with pytest.raises(SemanticProviderSchemaError):
        PromptGenesisProviderService(ProviderRouter((InvalidProvider(),))).generate(
            CreatorIntent("intent_bad_provider", "author", "setting: a town")
        )
