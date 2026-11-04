"""World-memory, consequence and world-card copy for the Player surface."""

# ruff: noqa: E501

from __future__ import annotations

STRINGS: dict[str, str] = {
    "visual_tier_t0": "T0 · offline scene",
    "visual_tier_t1": "T1 · high-quality scene",
    "visual_tier_t3": "T3 · 3D space",
    "change_status_from": "{subject}'s status: {before} → {after}",
    "delta_absent": "not recorded",
    "delta_removed": "removed",
    "delta_yes": "yes",
    "delta_no": "no",
    "chronicle_details": "record details",
    "observer_gate_copy": "You are observing this world: no character has moved and nothing changed because of you.",
    "observer_gate_action": "Choose a character to enter",
    "visual_tier_short_t0": "offline scene",
    "visual_tier_short_t1": "high-quality scene",
    "visual_tier_short_t2": "panorama scene",
    "visual_tier_short_t3": "explorable space",
    "world_card_visual_alt": "World visual for {world}",
    "world_card_place": "Latest place: {place}",
    "world_card_time": "World time {time}",
    "world_card_happening": "Latest event: {event}",
    "world_card_continue": "Continue",
    "world_card_enter": "Enter",
    "world_card_no_facts": "World state is read once you enter",
    "world_card_no_visual": "No world visual yet",
    "chronicle_who_you": "you",
}
