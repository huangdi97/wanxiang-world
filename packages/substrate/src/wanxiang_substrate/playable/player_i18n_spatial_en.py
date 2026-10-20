"""English Player copy for optional T3 spatial-scene upgrades."""

from __future__ import annotations

_SPATIAL_STRINGS: dict[str, str] = {
    "spatial_stage_enter": "Enter spatial scene",
    "spatial_stage_exit": "Return to visual scene",
    "spatial_stage_error": (
        "The spatial renderer failed; the current visual scene remains available."
    ),
    "spatial_stage_reset": "Reset view",
    "spatial_stage_controls_hint": "Drag to rotate · wheel to zoom · arrows/WASD to look",
    "spatial_stage_point_count": "{place} · {count} pts",
    "spatial_upgrade_eyebrow": "Spatial upgrade",
    "spatial_upgrade_heading": "Upgrade this place into a spatial scene",
    "spatial_upgrade_submit": "Generate spatial scene",
    "spatial_upgrade_refresh": "Refresh generation status",
    "spatial_upgrade_available": (
        "{place} can be upgraded · estimated {cost}; {remaining} world budget unit(s) remain"
    ),
    "spatial_upgrade_pending": "Spatial scene for {place} is in progress · {state}",
    "spatial_upgrade_ambiguous": (
        "The remote submission outcome for {place} is unknown. Wanxiang will not resubmit "
        "automatically because that could cause duplicate billing; the current visual scene "
        "remains usable while the provider task or billing record is reconciled."
    ),
    "spatial_upgrade_ready": ("Spatial scene for {place} is ready · {count} spatial asset(s)"),
    "spatial_upgrade_terminal": (
        "Spatial task for {place}: {state}. The current scene remains usable."
    ),
    "spatial_upgrade_unavailable_provider": (
        "No spatial generator is configured; the current illustrated scene remains usable."
    ),
    "spatial_upgrade_unavailable_network": (
        "The spatial generator is not allowed to use the network; "
        + "the current scene remains usable."
    ),
    "spatial_upgrade_unavailable_rights": (
        "The source does not authorize external spatial generation; "
        "keep using local/existing visuals."
    ),
    "spatial_upgrade_unavailable_privacy": (
        "The configured spatial generator does not satisfy this source privacy policy."
    ),
    "spatial_upgrade_unavailable_budget": (
        "The current spatial generation budget is insufficient."
    ),
    "spatial_upgrade_state_submission_ambiguous": "submission outcome unknown",
    "spatial_upgrade_state_submitted": "submitted",
    "spatial_upgrade_state_queued": "queued",
    "spatial_upgrade_state_running": "generating",
    "spatial_upgrade_state_verified": "verified",
    "spatial_upgrade_state_attached": "ready",
    "spatial_upgrade_state_failed": "failed",
    "spatial_upgrade_state_cancelled": "cancelled",
    "spatial_upgrade_state_expired": "expired",
    "status_spatial_submitted": (
        "Spatial generation for {place} was submitted; " + "you can keep using the current world."
    ),
    "status_spatial_refreshed": "Spatial generation status refreshed.",
}
