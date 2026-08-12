"""G03A: observation value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.observation.model import (
    EntityVisibility,
    ObservationFact,
    channel_confidence,
)


@pytest.mark.unit
def test_observation_fact_field_lookup() -> None:
    fact = ObservationFact(
        kind="movement",
        subject="alice",
        place=EntityId("kitchen"),
        fields=(("entity", "alice"), ("place", "kitchen")),
    )
    assert fact.field("place") == "kitchen"
    assert fact.field("missing") is None


@pytest.mark.unit
def test_channel_confidence_is_deterministic() -> None:
    assert channel_confidence("visual") == 1.0
    assert channel_confidence("acoustic") == 0.8
    assert channel_confidence("textual") == 0.9


@pytest.mark.unit
def test_entity_visibility_validation() -> None:
    assert EntityVisibility(EntityId("a"), "public").level == "public"
    with pytest.raises(ContractError):
        EntityVisibility(EntityId("a"), "top_secret")  # type: ignore[arg-type]
    with pytest.raises(ContractError):
        EntityVisibility(EntityId("a"), "group", group_id=None)
    assert EntityVisibility(EntityId("a"), "group", EntityId("club")).group_id == EntityId("club")
