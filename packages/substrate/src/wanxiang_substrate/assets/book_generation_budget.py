"""Strict integer validation for provider-controlled visual generation budgets."""

# pyright: reportUnusedFunction=false

from __future__ import annotations


def _require_nonnegative_int(value: object, *, label: str) -> int:
    """Reject booleans/floats so billing units remain discrete and auditable."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value
