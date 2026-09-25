"""Behaviour of the R7 service contract catalog and its manifest digest."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest
from wanxiang_reality import contracts as contracts_module
from wanxiang_reality.contracts import (
    SERVICE_CONTRACTS,
    ServiceContract,
    contract_manifest,
    get_contract,
    manifest_digest,
)
from wanxiang_reality.errors import ContractError
from wanxiang_reality.hashing import canonical_digest

pytestmark = pytest.mark.unit

REQUIRED_CONTRACT_IDS = {
    "wanxiang.identity@1",
    "wanxiang.reality.observe@1",
    "wanxiang.reality.proposal@1",
    "wanxiang.reality.policy@1",
    "wanxiang.authority@1",
    "wanxiang.history@1",
    "wanxiang.branch@1",
    "wanxiang.lineage@1",
    "wanxiang.replay@1",
    "wanxiang.evidence@1",
    "wanxiang.rights@1",
    "wanxiang.execution@1",
    "wanxiang.actor@1",
    "wanxiang.model@1",
    "wanxiang.capability@1",
    "wanxiang.reality.profile@1",
}

CONTRACT_SCOPES = {"root", "tenant", "world", "worldline"}


def test_catalog_contains_every_required_contract_id_exactly_once() -> None:
    ids = [contract.contract_id for contract in SERVICE_CONTRACTS]

    assert len(ids) == len(set(ids)) == len(REQUIRED_CONTRACT_IDS)
    assert set(ids) == REQUIRED_CONTRACT_IDS


def test_every_contract_is_version_one_with_valid_scope_and_unique_capabilities() -> None:
    for contract in SERVICE_CONTRACTS:
        assert contract.api_version == "1"
        assert contract.namespace.startswith("wanxiang.")
        assert contract.scope in CONTRACT_SCOPES
        assert contract.capabilities
        assert len(set(contract.capabilities)) == len(contract.capabilities)
        assert contract.error_semantics


def test_contract_rejects_empty_namespace() -> None:
    with pytest.raises(ContractError):
        ServiceContract(
            namespace="",
            service_id="identity",
            api_version="1",
            schema_version="1",
            scope="root",
            capabilities=("identity.authenticate",),
            error_semantics=("identity-unresolved",),
            compatibility="additive-minor",
        )


def test_contract_rejects_duplicate_capability_names() -> None:
    with pytest.raises(ContractError):
        ServiceContract(
            namespace="wanxiang.identity",
            service_id="identity",
            api_version="1",
            schema_version="1",
            scope="root",
            capabilities=("identity.authenticate", "identity.authenticate"),
            error_semantics=("identity-unresolved",),
            compatibility="additive-minor",
        )


def test_get_contract_returns_the_catalog_entry() -> None:
    contract = get_contract("wanxiang.history@1")

    assert contract.service_id == "history"
    assert contract.namespace == "wanxiang.history"


def test_unknown_contract_id_is_rejected() -> None:
    with pytest.raises(ContractError):
        get_contract("wanxiang.unknown@1")


def test_manifest_is_json_serializable_and_names_every_contract() -> None:
    rendered = json.dumps(contract_manifest())

    for contract_id in REQUIRED_CONTRACT_IDS:
        assert contract_id in rendered


def test_manifest_digest_is_stable_across_calls() -> None:
    first = manifest_digest()

    assert manifest_digest() == first
    assert len(first) == 64


def test_manifest_digest_changes_when_a_manifest_copy_is_mutated() -> None:
    baseline = manifest_digest()
    mutated = contract_manifest()
    mutated["contracts"] = []

    assert canonical_digest(mutated) != baseline


def test_manifest_digest_changes_when_a_contract_changes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline = manifest_digest()
    original = get_contract("wanxiang.history@1")
    changed = replace(original, compatibility="additive-minor")
    assert changed != original
    updated = tuple(changed if contract == original else contract for contract in SERVICE_CONTRACTS)
    monkeypatch.setattr(contracts_module, "SERVICE_CONTRACTS", updated)

    assert manifest_digest() != baseline
