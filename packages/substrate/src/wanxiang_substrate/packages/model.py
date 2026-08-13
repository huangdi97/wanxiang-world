"""Portable package manifest value objects (G04A).

Domain/World/Scenario packages carry semantic versions, dependency constraints,
a content hash and an executable trust class. Manifests are frozen value
objects; hashing is over the canonical serialization.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.packages.errors import InvalidManifest

PackageKind = Literal["domain", "world", "scenario"]
TrustClass = Literal["trusted", "untrusted"]

MANIFEST_SCHEMA_VERSION = 1
TRUSTED = "trusted"
UNTRUSTED = "untrusted"

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_CONSTRAINT_RE = re.compile(r"^(==|>=|<=|>|<|\^)?\s*(\d+)\.(\d+)(?:\.(\d+))?$")


@dataclass(frozen=True, slots=True)
class SemanticVersion:
    """Semantic version major.minor.patch with deterministic ordering."""

    major: int
    minor: int
    patch: int = 0

    def __post_init__(self) -> None:
        for name in ("major", "minor", "patch"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ContractError(f"{name} must be a non-negative integer")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) <= (other.major, other.minor, other.patch)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) >= (other.major, other.minor, other.patch)

    @classmethod
    def parse(cls, value: str) -> SemanticVersion:
        match = _VERSION_RE.match(value.strip())
        if match is None:
            raise InvalidManifest(f"invalid semantic version {value!r}")
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))


@dataclass(frozen=True, slots=True)
class VersionConstraint:
    """Single constraint expression on a semantic version."""

    raw: str
    op: str = "=="
    major: int = 0
    minor: int = 0
    patch: int = 0

    def __post_init__(self) -> None:
        stripped = self.raw.strip()
        if stripped == "*":
            object.__setattr__(self, "op", "*")
            return
        match = _CONSTRAINT_RE.match(stripped)
        if match is None:
            raise InvalidManifest(f"invalid version constraint {self.raw!r}")
        object.__setattr__(self, "op", match.group(1) or "==")
        object.__setattr__(self, "major", int(match.group(2)))
        object.__setattr__(self, "minor", int(match.group(3)))
        object.__setattr__(self, "patch", int(match.group(4)) if match.group(4) else 0)

    def matches(self, version: SemanticVersion) -> bool:
        op = self.op
        if op == "*":
            return True
        pinned = SemanticVersion(self.major, self.minor, self.patch)
        if op == "==":
            return version == pinned
        if op == ">=":
            return version >= pinned
        if op == "<=":
            return version <= pinned
        if op == ">":
            return version > pinned
        if op == "<":
            return version < pinned
        if op == "^":
            # ^1.2 allows >=1.2.0 and <2.0.0 (same major).
            return version.major == self.major and version >= pinned
        return False


@dataclass(frozen=True, slots=True)
class PackageManifest:
    """Portable domain/world/scenario package manifest."""

    package_id: str
    kind: PackageKind
    version: SemanticVersion
    name: str
    dependencies: tuple[tuple[str, str], ...] = ()
    schema_version: int = MANIFEST_SCHEMA_VERSION
    content_hash: str = ""
    executable_trust: TrustClass = UNTRUSTED
    compat: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.package_id or len(self.package_id) > 64:
            raise InvalidManifest("package_id must be a non-empty string <= 64 chars")
        if self.schema_version <= 0:
            raise InvalidManifest("manifest schema_version must be positive")
        for dep_id, constraint in self.dependencies:
            if not dep_id:
                raise InvalidManifest("dependency package id must be non-empty")
            try:
                VersionConstraint(constraint)
            except ContractError as exc:
                raise InvalidManifest(f"invalid constraint for {dep_id!r}: {exc}") from exc
        if self.executable_trust not in (TRUSTED, UNTRUSTED):
            raise InvalidManifest(f"unknown executable_trust {self.executable_trust!r}")

    def canonical(self) -> dict[str, object]:
        """Canonical serialization for content hashing (sorted, stable)."""
        return {
            "package_id": self.package_id,
            "kind": self.kind,
            "version": str(self.version),
            "name": self.name,
            "schema_version": self.schema_version,
            "dependencies": [
                {"package": dep_id, "constraint": constraint}
                for dep_id, constraint in sorted(self.dependencies)
            ],
            "executable_trust": self.executable_trust,
            "compat": sorted(self.compat),
        }

    def compute_hash(self) -> str:
        payload = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> PackageManifest:
        return PackageManifest(
            package_id=self.package_id,
            kind=self.kind,
            version=self.version,
            name=self.name,
            dependencies=self.dependencies,
            schema_version=self.schema_version,
            content_hash=self.compute_hash(),
            executable_trust=self.executable_trust,
            compat=self.compat,
        )


@dataclass(frozen=True, slots=True)
class PackageLock:
    """Deterministic resolution result pinning every package version."""

    root_package: str
    root_version: SemanticVersion
    pins: tuple[tuple[str, SemanticVersion], ...]

    def version_for(self, package_id: str) -> SemanticVersion | None:
        for pinned_id, version in self.pins:
            if pinned_id == package_id:
                return version
        return None

    def compute_hash(self) -> str:
        payload = {
            "root": self.root_package,
            "root_version": str(self.root_version),
            "pins": [[pid, str(ver)] for pid, ver in self.pins],
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
