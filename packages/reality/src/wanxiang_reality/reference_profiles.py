"""Reference reality/world profiles for the CLI, tests and R7 reference worlds.

These are honestly-labelled *reference* profiles: the smallest complete
composition that binds every service-contract seam. They are not product
profiles and must never be shipped as a real world definition.
"""

from __future__ import annotations

from typing import Final

from wanxiang_reality.contracts import SERVICE_CONTRACTS
from wanxiang_reality.profiles import RealityProfile, WorldProfile
from wanxiang_reality.versions import Version

REFERENCE_REALITY_PROFILE_ID = "reality.reference"
REFERENCE_REALITY_PROFILE_VERSION: Final[Version] = Version(1, 0, 0)
REFERENCE_WORLD_PROFILE_ID = "world.reference"
REFERENCE_WORLD_PROFILE_VERSION: Final[Version] = Version(1, 0, 0)

#: Providers a reference world declares; each ``provider_versions`` key matches.
_REFERENCE_PROVIDERS: Final[tuple[str, ...]] = (
    "provider.physical.reference",
    "provider.history.memory",
    "provider.model.reference",
)

_REFERENCE_SCHEMA_VERSIONS: Final[dict[str, str]] = {
    "wanxiang.schema.canonical": "1",
    "wanxiang.schema.history": "1",
}

_REQUIRED_WORLD_DIMENSIONS: Final[tuple[str, ...]] = (
    "actors",
    "capabilities",
    "distribution",
    "experience",
    "memory",
    "projection",
    "simulation",
    "space",
    "time",
)


def reference_reality_profile() -> RealityProfile:
    """Return the reference RealityProfile binding every known service seam."""
    return RealityProfile(
        profile_id=REFERENCE_REALITY_PROFILE_ID,
        version=REFERENCE_REALITY_PROFILE_VERSION,
        required_seams=tuple(sorted(contract.contract_id for contract in SERVICE_CONTRACTS)),
    )


def reference_world_profile() -> WorldProfile:
    """Return the reference WorldProfile with all nine dimensions declared."""
    return WorldProfile(
        profile_id=REFERENCE_WORLD_PROFILE_ID,
        version=REFERENCE_WORLD_PROFILE_VERSION,
        reality_profile_ref=(f"{REFERENCE_REALITY_PROFILE_ID}@{REFERENCE_REALITY_PROFILE_VERSION}"),
        providers=_REFERENCE_PROVIDERS,
        dimensions={name: name for name in _REQUIRED_WORLD_DIMENSIONS},
    )


def reference_provider_versions() -> dict[str, str]:
    """Return the version pin for every reference provider."""
    return dict.fromkeys(_REFERENCE_PROVIDERS, "1.0.0")


def reference_schema_versions() -> dict[str, str]:
    """Return the reference schema version pins."""
    return dict(_REFERENCE_SCHEMA_VERSIONS)


__all__ = [
    "REFERENCE_REALITY_PROFILE_ID",
    "REFERENCE_WORLD_PROFILE_ID",
    "reference_provider_versions",
    "reference_reality_profile",
    "reference_schema_versions",
    "reference_world_profile",
]
