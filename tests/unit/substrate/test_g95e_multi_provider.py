"""G95E: versioned mixed-population assignments stay proposal-only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.authoring.providers import (
    Provider,
    ProviderCapability,
    ProviderProposal,
)
from wanxiang_substrate.capability.runtime_control import RuntimeControlLedger
from wanxiang_substrate.world_lab import (
    MultiProviderWorldlineRunner,
    ProviderAssignmentPolicy,
    ProviderRunInput,
)


@dataclass
class _RecordingProvider:
    capability: ProviderCapability

    def __post_init__(self) -> None:
        self.calls: list[tuple[tuple[str, ...], str]] = []

    def propose(self, source_refs: tuple[str, ...], payload: str) -> tuple[ProviderProposal, ...]:
        self.calls.append((source_refs, payload))
        return (
            ProviderProposal(
                proposal_id=f"proposal:{self.capability.provider_id}",
                kind="candidate",
                provider_id=self.capability.provider_id,
                source_refs=source_refs,
                payload=(("candidate_kind", "policy_observation"),),
                confidence=0.5,
            ),
        )


@dataclass
class _BadProposal:
    provider_id: str
    commit: str = "forbidden"


@dataclass
class _BadProvider:
    capability: ProviderCapability

    def propose(self, source_refs: tuple[str, ...], payload: str) -> tuple[_BadProposal, ...]:
        return (_BadProposal(self.capability.provider_id),)


def _input() -> ProviderRunInput:
    return ProviderRunInput(
        run_id="run:g95e:unit",
        world_package_ref="world:g95e",
        world_package_version="5.4.0",
        scenario_ref="scenario:g95e",
        scenario_version="1",
        source_refs=("source:g95e:chunk:1",),
        population_refs=("actor:alice", "actor:bob", "actor:carol"),
        seed=17,
        parameters=(("pressure", "medium"),),
        payload="PRIVATE SOURCE PAYLOAD MUST NOT BE EXPORTED",
        private_source=True,
        control_timestamp="2026-08-27T00:00:00Z",
    )


def _provider(provider_id: str) -> _RecordingProvider:
    return _RecordingProvider(
        ProviderCapability(
            provider_id=provider_id,
            kind="semantic",
            version="1.0.0",
            private_safe=True,
        )
    )


def test_round_robin_uses_same_input_and_records_runtime_controls() -> None:
    alpha = _provider("provider:alpha")
    beta = _provider("provider:beta")
    ledger = RuntimeControlLedger()
    policy = ProviderAssignmentPolicy(
        policy_id="policy:g95e:round-robin",
        version=2,
        mode="round_robin",
        provider_ids=("provider:alpha", "provider:beta"),
    )

    result = MultiProviderWorldlineRunner(
        {"provider:alpha": alpha, "provider:beta": beta}, ledger
    ).execute(_input(), policy)

    assert [item.provider_id for item in result.invocations] == [
        "provider:alpha",
        "provider:beta",
        "provider:alpha",
    ]
    expected_call = (("source:g95e:chunk:1",), "PRIVATE SOURCE PAYLOAD MUST NOT BE EXPORTED")
    assert alpha.calls == [expected_call, expected_call]
    assert beta.calls == [expected_call]
    assert {item.input_hash for item in result.invocations} == {_input().input_hash}
    assert result.proposal_count == 3
    assert all(
        type(proposal) is ProviderProposal
        for item in result.invocations
        for proposal in item.proposals
    )
    assert all(
        not hasattr(proposal, "commit")
        for item in result.invocations
        for proposal in item.proposals
    )
    assert len(ledger.entries()) == 2
    assert {item.operation for item in ledger.entries()} == {"activate"}

    exported = result.to_dict()
    assert exported["proposal_only"] is True
    assert "PRIVATE SOURCE PAYLOAD" not in repr(exported)
    assert "payload" not in repr(exported).casefold()


def test_policy_is_versioned_round_trippable_and_explicit_assignments_are_complete() -> None:
    policy = ProviderAssignmentPolicy(
        policy_id="policy:g95e:explicit",
        version=1,
        mode="explicit",
        provider_ids=("provider:alpha", "provider:beta"),
        explicit_assignments=(
            ("actor:bob", "provider:beta"),
            ("actor:alice", "provider:alpha"),
        ),
    )

    assert ProviderAssignmentPolicy.from_dict(policy.to_dict()) == policy
    assert [item.provider_id for item in policy.assign(("actor:alice", "actor:bob"))] == [
        "provider:alpha",
        "provider:beta",
    ]
    with pytest.raises(ContractError, match="no provider"):
        policy.assign(("actor:carol",))


def test_provider_cannot_return_a_commit_capable_output() -> None:
    bad = _BadProvider(
        ProviderCapability(
            provider_id="provider:bad",
            kind="semantic",
            version="1.0.0",
            private_safe=True,
        )
    )
    policy = ProviderAssignmentPolicy(
        policy_id="policy:g95e:bad",
        version=1,
        mode="homogeneous",
        provider_ids=("provider:bad",),
    )

    with pytest.raises(ContractError, match="ProviderProposal"):
        MultiProviderWorldlineRunner(
            {"provider:bad": cast(Provider, bad)}, RuntimeControlLedger()
        ).execute(_input(), policy)
