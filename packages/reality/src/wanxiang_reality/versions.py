"""Strict dotted versions used by contracts, profiles and runtime locks."""

from __future__ import annotations

import re
from dataclasses import dataclass

from wanxiang_reality.errors import VersionError

# ``fullmatch`` anchors both ends, so only plain decimal components are accepted.
_VERSION_PATTERN = re.compile(r"([0-9]+)(?:\.([0-9]+))?(?:\.([0-9]+))?")


@dataclass(frozen=True, slots=True, order=True)
class Version:
    """A ``major.minor.patch`` version with strict parsing and total ordering."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, text: str) -> Version:
        """Parse ``"1"``, ``"1.2"`` or ``"1.2.3"``; raise VersionError otherwise."""
        match = _VERSION_PATTERN.fullmatch(text)
        if match is None:
            raise VersionError(f"invalid version: {text!r}")
        major, minor, patch = (int(part) if part is not None else 0 for part in match.groups())
        return cls(major=major, minor=minor, patch=patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def compatible(self, other: Version) -> bool:
        """Return True when both versions share the same major number."""
        return self.major == other.major

    def is_major_upgrade_from(self, other: Version) -> bool:
        """Return True only when this version has a strictly higher major number."""
        return self.major > other.major
