"""G88E: character, observer presence, and embodiment lease rules."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError, NotFound
from wanxiang_substrate.playable import (
    CharacterEntryService,
    ExperiencePackage,
    InMemoryPlayableStore,
    active_lease,
)
from wanxiang_substrate.session import LeaseConflict


def package() -> ExperiencePackage:
    return ExperiencePackage(
        "exp:entry", "world:entry", "scenario:entry", "projection:player", visibility="public"
    )


def test_observer_has_presence_without_embodiment_lease() -> None:
    service = CharacterEntryService(InMemoryPlayableStore())
    receipt = service.enter(
        package(),
        viewer_id="alice",
        instance_id="instance_entry",
        branch_id="branch_entry",
        session_id="session:observer",
        mode="observer",
    )
    assert receipt.presence is True
    assert receipt.lease_id == ""
    assert active_lease(service, receipt.session_id) is None
    with pytest.raises(LeaseConflict):
        service.leases.acquire(
            service.sessions.require(receipt.session_id),
            "character:alice:1",
            "lease:bad",
            1,
            10,
        )


def test_embodiment_double_controller_rejects_and_leave_allows_resume() -> None:
    store = InMemoryPlayableStore()
    service = CharacterEntryService(store)
    character = service.create_character("alice", "Alice", compatible_profile_ids=("exp:entry",))
    first = service.enter(
        package(),
        viewer_id="alice",
        instance_id="instance_entry",
        branch_id="branch_entry",
        session_id="session:first",
        mode="embodiment",
        character_id=character.character_id,
    )
    assert active_lease(service, first.session_id) is not None
    with pytest.raises(LeaseConflict):
        service.enter(
            package(),
            viewer_id="alice",
            instance_id="instance_entry",
            branch_id="branch_entry",
            session_id="session:second",
            mode="embodiment",
            character_id=character.character_id,
        )
    service.leave(first.session_id)
    resumed = service.enter(
        package(),
        viewer_id="alice",
        instance_id="instance_entry",
        branch_id="branch_entry",
        session_id="session:resumed",
        mode="embodiment",
        character_id=character.character_id,
    )
    assert resumed.lease_id


def test_character_owner_and_compatibility_are_server_checked() -> None:
    store = InMemoryPlayableStore()
    service = CharacterEntryService(store)
    character = service.create_character("alice", "Alice", compatible_profile_ids=("other",))
    with pytest.raises(NotFound):
        service.enter(
            package(),
            viewer_id="bob",
            instance_id="instance_entry",
            branch_id="branch_entry",
            session_id="session:bad-owner",
            mode="character",
            character_id=character.character_id,
        )
    with pytest.raises(NotFound):
        service.enter(
            package(),
            viewer_id="alice",
            instance_id="instance_entry",
            branch_id="branch_entry",
            session_id="session:bad-compat",
            mode="character",
            character_id=character.character_id,
        )
    with pytest.raises(ContractError):
        service.enter(
            package(),
            viewer_id="alice",
            instance_id="instance_entry",
            branch_id="branch_entry",
            session_id="session:no-char",
            mode="embodiment",
        )
