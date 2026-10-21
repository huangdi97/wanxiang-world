"""English Player copy for explicit T2 panorama upgrades."""

from __future__ import annotations

_PANORAMA_STRINGS: dict[str, str] = {
    "panorama_stage_enter": "Enter panorama",
    "panorama_stage_exit": "Return to visual scene",
    "panorama_stage_error": (
        "Panorama renderer failed; the current visual scene is still available."
    ),
    "panorama_upgrade_eyebrow": "Panorama upgrade",
    "panorama_upgrade_heading": "Upgrade this place to an explorable panorama",
    "panorama_upgrade_submit": "Generate panorama",
    "panorama_upgrade_ready": ("{place} has an interactive panorama ready for world entry."),
    "panorama_upgrade_available": (
        "{place} can be upgraded · estimated reservation {cost}; "
        "world budget remaining {remaining}/{budget}"
    ),
    "panorama_upgrade_unavailable_provider": (
        "No usable panorama provider is configured; the current visual scene remains available."
    ),
    "panorama_upgrade_unavailable_network": (
        "The panorama provider is not allowed to use the network."
    ),
    "panorama_upgrade_unavailable_rights": (
        "The source does not authorize external panorama generation."
    ),
    "panorama_upgrade_unavailable_privacy": (
        "The configured panorama provider does not meet this source's privacy requirements."
    ),
    "panorama_upgrade_unavailable_budget": (
        "The remaining world panorama budget is insufficient for another generation."
    ),
    "status_panorama_generated": "The panorama for {place} was generated and cached.",
}
