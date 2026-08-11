"""GOAL_01A: identifier value-object tests."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    EntityId,
    WanxiangId,
    WorldInstanceId,
)


@pytest.mark.unit
def test_generated_ids_are_valid_and_unique() -> None:
    a = EntityId.generate()
    b = EntityId.generate()
    assert a != b
    assert str(a).startswith("ent_")


@pytest.mark.unit
def test_same_value_same_type_are_equal() -> None:
    assert WorldInstanceId("wld_1") == WorldInstanceId("wld_1")
    assert hash(WorldInstanceId("wld_1")) == hash(WorldInstanceId("wld_1"))


@pytest.mark.unit
def test_distinct_id_types_are_not_equal_even_with_same_value() -> None:
    assert WorldInstanceId("wld_x") != BranchId("wld_x")


@pytest.mark.unit
def test_invalid_id_values_are_rejected() -> None:
    for bad in ("", "has space", "UPPER", "with/slash", "a" * 129):
        with pytest.raises(ContractError):
            WorldInstanceId(bad)


@pytest.mark.unit
def test_round_trip_via_value() -> None:
    original = CommandId("cmd_abc")
    assert CommandId(original.value) == original


@pytest.mark.unit
def test_ids_are_immutable() -> None:
    value = EntityId("ent_1")
    with pytest.raises(AttributeError):
        value.value = "ent_2"  # type: ignore[misc]
    assert isinstance(value, WanxiangId)
