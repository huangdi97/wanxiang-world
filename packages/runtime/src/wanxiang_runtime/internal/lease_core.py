"""Module-private core of the canonical-write lease brand (R7 Gate C).

This mirrors `packages/cordis_host/src/internal/capability-core.ts`: the set of
issued leases is the single source of truth, so an object that merely copies the
field shape (a "look-alike" credential) is never accepted. The functions are
underscore-private on purpose -- they are not re-exported from `wanxiang_runtime`
and `canonical_write.py` is their only importer.
"""

from __future__ import annotations

from typing import Final
from weakref import WeakSet

# Declared so the single sanctioned importer (`canonical_write.py`) does not read
# as dead code to static analysis; these names are still underscore-private.
__all__ = ["_is_issued", "_mint"]

# SECURITY: the sentinel is module-private; without it a hand-built object can
# never satisfy the brand check even if it reaches the WeakSet by accident.
_BRAND: Final[object] = object()

# Leases are held weakly: the credential itself is the only strong reference, so
# dropping it revokes the write authority without an explicit bookkeeping step.
_ISSUED: WeakSet[object] = WeakSet()


def _mint[T](value: T) -> T:
    """Brand and register an object as an issued lease, then return it."""
    object.__setattr__(value, "_brand", _BRAND)
    _ISSUED.add(value)
    return value


def _is_issued(value: object) -> bool:
    """Report whether a value is a lease minted by this module."""
    if value is None:
        return False
    return getattr(value, "_brand", None) is _BRAND and value in _ISSUED
