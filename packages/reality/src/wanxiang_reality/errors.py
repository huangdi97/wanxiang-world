"""Typed error hierarchy for the Wanxiang R7 reality package."""

from __future__ import annotations


class WanxiangRealityError(Exception):
    """Base class for every error raised by ``wanxiang_reality``."""


class ContractError(WanxiangRealityError):
    """Raised when a service contract is invalid or unknown."""


class ProfileError(WanxiangRealityError):
    """Raised when a reality or world profile violates its invariants."""


class RuntimeLockError(WanxiangRealityError):
    """Raised when a runtime lock is incomplete or inconsistent."""


class VersionError(WanxiangRealityError):
    """Raised when a version string cannot be parsed."""


class LockStoreError(WanxiangRealityError):
    """Raised when a persisted runtime lock cannot be read or written."""


class LockMissingError(LockStoreError):
    """Raised when a worldline has no persisted runtime lock."""


class LockTamperedError(LockStoreError):
    """Raised when a persisted runtime lock is ill-shaped or fails its digest.

    A tampered record is never repaired in place: the caller gets the offending
    detail and must treat the worldline as unsafe to start.
    """


class LockImmutableError(LockStoreError):
    """Raised when a write would overwrite an existing runtime lock."""


class LockDriftError(WanxiangRealityError):
    """Raised when a worldline's current runtime facts no longer match its lock.

    ``drifted_dimensions`` names the compared dimensions that disagreed, so an
    operator CLI can report them without re-deriving the comparison. Identity
    mismatches raise with an empty tuple.
    """

    drifted_dimensions: tuple[str, ...]

    def __init__(self, message: str, *, drifted_dimensions: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.drifted_dimensions = drifted_dimensions


class WorldlineOpenError(WanxiangRealityError):
    """Raised when a worldline cannot be opened safely at all."""
