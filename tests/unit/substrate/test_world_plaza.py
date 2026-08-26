"""G88D: World Plaza authorization and continue ordering."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import NotFound
from wanxiang_substrate.playable import (
    ExperienceInstanceRecord,
    InMemoryPlayableStore,
    PlayableWorldProfile,
    WorldPlaza,
)


def _profile(profile_id: str, visibility: str, owner_id: str = "") -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id,
        f"world:{profile_id}",
        "default",
        "runtime:reference",
        f"experience:{profile_id}",
        "projection:player",
        visibility=visibility,  # type: ignore[arg-type]
        owner_id=owner_id,
        display_name=profile_id,
    )


def test_plaza_filters_private_profiles_and_orders_continue() -> None:
    store = InMemoryPlayableStore()
    store.save_profile(_profile("public", "public"))
    store.save_profile(_profile("alice", "private", "alice"))
    store.save_profile(_profile("bob", "private", "bob"))
    store.save_instance(ExperienceInstanceRecord("i1", "alice", "alice", "b1", updated_seq=2))
    store.save_instance(ExperienceInstanceRecord("i2", "alice", "alice", "b2", updated_seq=4))
    store.save_instance(ExperienceInstanceRecord("ib", "bob", "bob", "bb", updated_seq=9))
    plaza = WorldPlaza(store)
    assert [card.profile_id for card in plaza.explore_worlds()] == ["public"]
    assert [card.profile_id for card in plaza.my_worlds("alice")] == ["alice"]
    assert plaza.continue_last("alice").instance_id == "i2"  # type: ignore[union-attr]
    assert [card.instance_id for card in plaza.recent_sessions("alice")] == ["i2", "i1"]


def test_private_profile_access_does_not_leak_existence() -> None:
    store = InMemoryPlayableStore()
    store.save_profile(_profile("alice", "private", "alice"))
    with pytest.raises(NotFound):
        WorldPlaza(store).require_access("alice", "bob")
