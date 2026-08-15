"""G36B: RC-001 spatial run - visibility/acoustic/privacy + movement time.

Synthetic anonymized map ONLY - never real《红楼梦》canon.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.spatial import MovementProfile, travel_time
from wanxiang_substrate.spatial.components import (
    place_component,
    place_grant_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.spatial.query import SpatialQuery

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)

GARDEN = EntityId("garden")
HALL = EntityId("hall")
SICKROOM = EntityId("sickroom")
COURTYARD = EntityId("courtyard")
C1 = EntityId("c1")
C3 = EntityId("c3")


def _state(*, grant_sickroom: bool = False) -> InMemoryCanonicalState:
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    entities = [
        EntityCreate(
            entity_id=GARDEN, entity_type="place", components=(place_component(GARDEN, "garden"),)
        ),
        EntityCreate(
            entity_id=HALL, entity_type="place", components=(place_component(HALL, "hall"),)
        ),
        EntityCreate(
            entity_id=SICKROOM,
            entity_type="place",
            components=(place_component(SICKROOM, "sickroom", privacy="private"),),
        ),
        EntityCreate(
            entity_id=COURTYARD,
            entity_type="place",
            components=(place_component(COURTYARD, "courtyard"),),
        ),
        EntityCreate(
            entity_id=EntityId("portal_gh"),
            entity_type="portal",
            components=(portal_component(GARDEN, HALL, label="桥"),),
        ),
        EntityCreate(
            entity_id=EntityId("portal_hs"),
            entity_type="portal",
            components=(portal_component(HALL, SICKROOM, label="门"),),
        ),
        EntityCreate(
            entity_id=EntityId("portal_hc"),
            entity_type="portal",
            components=(
                portal_component(
                    HALL,
                    COURTYARD,
                    state="locked",
                    locked_key=EntityId("key_courtyard"),
                ),
            ),
        ),
        EntityCreate(
            entity_id=C1, entity_type="actor", components=(position_component(C1, GARDEN),)
        ),
    ]
    c3_components = [position_component(C3, HALL)]
    if grant_sickroom:
        c3_components.append(place_grant_component(SICKROOM))
    entities.append(
        EntityCreate(entity_id=C3, entity_type="actor", components=tuple(c3_components))
    )
    for entity in entities:
        state = state.apply(ProposedWorldDelta(operations=(entity,)))
    return state


@pytest.mark.unit
def test_visibility_and_acoustic_zones() -> None:
    query = SpatialQuery(_state())
    visible = query.visibility_zone(GARDEN)
    assert visible.visible_places == frozenset({HALL})
    acoustic = query.acoustic_zone(GARDEN)
    # Locked courtyard portal is excluded from sound; hall is audible.
    assert acoustic.audible_places == frozenset({HALL})


@pytest.mark.unit
def test_private_place_requires_grant() -> None:
    assert SpatialQuery(_state()).can_enter(SICKROOM, C3) is False
    assert SpatialQuery(_state(grant_sickroom=True)).can_enter(SICKROOM, C3) is True


@pytest.mark.unit
def test_locked_portal_blocks_reachability() -> None:
    query = SpatialQuery(_state())
    assert query.reachable(HALL, COURTYARD) is False
    assert query.path(HALL, COURTYARD, ignore_locked=True) is not None


@pytest.mark.unit
def test_movement_time_over_path() -> None:
    query = SpatialQuery(_state())
    path = query.path(GARDEN, SICKROOM)
    assert path is not None
    assert path.cost == 2
    assert travel_time(path) == 2
    profile = MovementProfile(
        "rc001", base_ticks_per_portal=3, portal_surcharges=(("portal_hs", 1),)
    )
    assert profile.travel_time(path) == 3 + (3 + 1)


@pytest.mark.unit
def test_position_continuity() -> None:
    query = SpatialQuery(_state())
    assert query.location(C1) == GARDEN
    assert query.location(C3) == HALL
