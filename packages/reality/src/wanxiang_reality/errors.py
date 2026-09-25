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
