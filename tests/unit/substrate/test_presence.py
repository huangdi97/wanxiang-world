"""G31E: Interworld identity and presence."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId, WorldInstanceId, WorldlineId
from wanxiang_substrate.lineage.presence import (
    OriginIdentity,
    PresenceRef,
    PresenceRegistry,
)

ORIGIN = OriginIdentity(
    entity_id=EntityId("lin_daiyu"),
    origin_worldline_id=WorldlineId("wl_rc"),
    origin_instance_id=WorldInstanceId("wld_rc"),
    canonical_ref="rc://person/lin_daiyu",
)


@pytest.mark.unit
def test_enter_generates_explicit_presence_policy() -> None:
    registry = PresenceRegistry()
    presence = registry.enter(
        "pres_1",
        ORIGIN,
        WorldlineId("wl_guest"),
        translation_policy="isolated",
        sync_policy="none",
    )
    assert isinstance(presence, PresenceRef)
    assert presence.sync_policy == "none"
    assert registry.can_sync_back(presence) is False  # no implicit write-back


@pytest.mark.unit
def test_b_world_experiences_do_not_write_back_to_a() -> None:
    registry = PresenceRegistry()
    presence = registry.enter("pres_1", ORIGIN, WorldlineId("wl_guest"))
    # Guest-world events happen; without an explicit sync policy nothing goes
    # back to the origin worldline (no dual write, no history copy).
    assert registry.can_sync_back(presence) is False
    # Even with a policy, the write-back is a separate explicit step.
    explicit = registry.enter(
        "pres_2",
        ORIGIN,
        WorldlineId("wl_guest2"),
        sync_policy="explicit_only",
    )
    assert registry.can_sync_back(explicit) is True


@pytest.mark.unit
def test_identity_conflict_rejected_or_mapped() -> None:
    registry = PresenceRegistry()
    # Host world already has the id -> only mapped policy is accepted.
    with pytest.raises(ContractError):
        registry.enter("pres_1", ORIGIN, WorldlineId("wl_guest"), existing_local=True)
    mapped = registry.enter(
        "pres_2",
        ORIGIN,
        WorldlineId("wl_guest"),
        existing_local=True,
        translation_policy="mapped",
    )
    assert mapped.mapped_local_id is not None
    assert mapped.mapped_local_id != ORIGIN.entity_id


@pytest.mark.unit
def test_presence_round_trip_and_leave() -> None:
    registry = PresenceRegistry()
    registry.enter("pres_1", ORIGIN, WorldlineId("wl_guest"))
    prim = registry.get("pres_1").to_primitive()  # type: ignore[union-attr]
    origin = prim["origin"]
    assert isinstance(origin, dict)
    assert origin["entity_id"] == "lin_daiyu"
    assert registry.leave("pres_1").presence_id == "pres_1"
    with pytest.raises(ContractError):
        registry.leave("pres_1")
