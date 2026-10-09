"""Deterministic local semantic extraction keeps people and places distinct."""

from __future__ import annotations

import json

from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider


def _payload_dict(payload: tuple[tuple[str, str], ...]) -> dict[str, str]:
    return dict(payload)


def test_english_narrative_place_is_not_also_emitted_as_identity() -> None:
    locator = "book#chapter-1"
    text = (
        "Character: Alice\n"
        "Character: Bob\n"
        "Alice arrived in Beijing in 1985.\n"
        "Bob visited Beijing.\n"
    )
    proposals = LocalSemanticProvider().propose(
        (locator,),
        json.dumps([{"locator": locator, "text": text}]),
    )
    rows = [_payload_dict(item.payload) for item in proposals]
    identities = {
        row.get("display_name", "")
        for row in rows
        if row.get("candidate_kind") == "identity"
    }
    places = {
        row.get("name", "")
        for row in rows
        if row.get("candidate_kind") == "place"
    }

    assert {"Alice", "Bob"}.issubset(identities)
    assert "Beijing" not in identities
    assert "Beijing" in places
