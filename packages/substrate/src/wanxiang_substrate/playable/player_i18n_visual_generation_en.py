"""Visual-generation governance copy for the English Player UI."""

from __future__ import annotations

STRINGS: dict[str, str] = {
    "error_visual_attempt_reserved": (
        "This paid scene attempt has an unresolved outcome. Automatic retry is blocked "
        "to prevent duplicate billing; existing scenes remain available."
    ),
    "error_visual_budget_exhausted": (
        "This world's on-demand visual generation budget is exhausted; existing scenes "
        "remain available."
    ),
}
