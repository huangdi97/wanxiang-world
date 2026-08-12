"""G02D: body/condition value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.body.model import BodyCondition, visible_facets


@pytest.mark.unit
def test_condition_ranges() -> None:
    assert BodyCondition().energy == 100
    assert BodyCondition(energy=50).is_fatigued() is False
    assert BodyCondition(energy=10).is_fatigued() is True
    with pytest.raises(ContractError):
        BodyCondition(energy=101)
    with pytest.raises(ContractError):
        BodyCondition(energy=-1)


@pytest.mark.unit
def test_mobility_capability() -> None:
    assert BodyCondition(mobility=100).mobility_capability() == "unrestricted"
    assert BodyCondition(mobility=30).mobility_capability() == "reduced"
    assert BodyCondition(mobility=0).mobility_capability() == "immobile"


@pytest.mark.unit
def test_visible_facets_excludes_private() -> None:
    condition = BodyCondition(health=70, energy=50, pain=80)
    public = visible_facets(condition, frozenset({"pain"}))
    assert "pain" not in public
    assert public["health"] == 70
    assert public["energy"] == 50
    full = visible_facets(condition, frozenset())
    assert "pain" in full


@pytest.mark.unit
def test_with_facet() -> None:
    condition = BodyCondition(energy=50)
    updated = condition.with_facet("energy", 80)
    assert updated.energy == 80
    assert condition.energy == 50  # immutable
