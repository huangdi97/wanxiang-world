"""G89F: portable character entries and explicit interworld compatibility."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.actor_continuity import (
    CharacterPassport,
    DeterministicPassportTranslationPolicy,
    PassportEntry,
    PassportTranslationContext,
)
from wanxiang_substrate.playable.store import CharacterRecord


def passport() -> CharacterPassport:
    character = CharacterRecord("char_a", "user_a", "Ava", ("profile_target",))
    return CharacterPassport.from_character(
        character,
        origin_world_refs=("world:origin",),
        entries=(
            PassportEntry(
                "memory_1", "memory", "memory:map", "world:origin", "portable", privacy="private"
            ),
            PassportEntry(
                "skill_1",
                "skill",
                "skill:climb",
                "world:origin",
                "portable",
                ("physical",),
                "public",
            ),
            PassportEntry(
                "item_1", "item", "item:key", "world:origin", "conditional", ("metal",), "public"
            ),
            PassportEntry(
                "item_blocked", "item", "item:secret", "world:origin", "blocked", privacy="private"
            ),
        ),
    )


@pytest.mark.unit
def test_translation_rejects_impossible_entries_without_silent_import() -> None:
    proposal = DeterministicPassportTranslationPolicy().propose(
        passport(),
        PassportTranslationContext(
            requester_id="user_a",
            target_world_ref="world:target",
            target_profile_id="profile_target",
            supported_kinds=("memory", "skill", "item"),
            available_refs=("skill:climb", "item:key"),
            compatibility_tags=("metal",),
        ),
    )
    statuses = {item.entry_id: item.status for item in proposal.decisions}
    assert statuses == {
        "item_1": "conditional",
        "item_blocked": "rejected",
        "memory_1": "rejected",
        "skill_1": "accepted",
    }
    assert proposal.accepted_entry_ids == ("item_1", "skill_1")


@pytest.mark.unit
def test_passport_privacy_and_incompatible_profile_are_explicit() -> None:
    private_view = passport().to_dict("other_user")
    assert private_view["owner_id"] is None
    entries = cast(list[dict[str, object]], private_view["entries"])
    assert all(item["entry_id"] != "memory_1" for item in entries)
    with pytest.raises(ContractError):
        DeterministicPassportTranslationPolicy().propose(
            passport(),
            PassportTranslationContext(
                requester_id="other_user",
                target_world_ref="world:target",
                target_profile_id="profile_target",
                supported_kinds=("skill",),
            ),
        )
    proposal = DeterministicPassportTranslationPolicy().propose(
        passport(),
        PassportTranslationContext(
            requester_id="user_a",
            target_world_ref="world:other",
            target_profile_id="profile_other",
            supported_kinds=("skill",),
            available_refs=("skill:climb",),
        ),
    )
    assert all(item.status == "rejected" for item in proposal.decisions)
