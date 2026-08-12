"""G02C: material value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.material.model import (
    ContainerSpec,
    Custody,
    InfoPayload,
    MaterialItem,
    Ownership,
)


@pytest.mark.unit
def test_item_validation() -> None:
    assert MaterialItem(EntityId("i"), "apple").state == "intact"
    with pytest.raises(ContractError):
        MaterialItem(EntityId("i"), "")
    with pytest.raises(ContractError):
        MaterialItem(EntityId("i"), "apple", state="vapor")  # type: ignore[arg-type]


@pytest.mark.unit
def test_container_accepts_kinds() -> None:
    spec = ContainerSpec(EntityId("c"), capacity=2, accepts_kinds=("letter",))
    assert spec.accepts("letter") is True
    assert spec.accepts("sword") is False
    with pytest.raises(ContractError):
        ContainerSpec(EntityId("c"), capacity=0)


@pytest.mark.unit
def test_payload_validation() -> None:
    info = InfoPayload(EntityId("i"), "ref://x", state="sealed")
    assert info.readers == ()
    with pytest.raises(ContractError):
        InfoPayload(EntityId("i"), "")
    with pytest.raises(ContractError):
        InfoPayload(EntityId("i"), "ref://x", state="open")  # type: ignore[arg-type]


@pytest.mark.unit
def test_custody_and_ownership_are_distinct() -> None:
    custody = Custody(EntityId("i"), EntityId("holder"))
    ownership = Ownership(EntityId("i"), EntityId("owner"))
    assert custody.custodian_id != ownership.owner_id
