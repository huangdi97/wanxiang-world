"""G34B: WorldPack Definition v5.2 schema migration."""

from __future__ import annotations

import pathlib
import subprocess
import sys

import pytest
from wanxiang_substrate.packages.migration import (
    LEGACY_CONSTITUTION_REF,
    V52_SCHEMA_VERSION,
    is_v52,
    legacy_constitution_ref,
    migrate_to_v52,
)
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion


def _legacy() -> PackageManifest:
    return PackageManifest(
        package_id="sf-world",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Synthetic Full World",
        dependencies=(("sf-domain", "==1.0.0"),),
        executable_trust="untrusted",
    ).with_hash()


def _v52() -> PackageManifest:
    return PackageManifest(
        package_id="rc-world",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Red Chamber World",
        constitution_ref="con_legacy_v5",
        genesis_ref="genesis://rc",
        evolution_policy_ref="canonical_replay",
        lineage_ref="wl_rc_001",
    ).with_hash()


@pytest.mark.unit
def test_legacy_package_round_trip_hash_unchanged() -> None:
    legacy = _legacy()
    canonical = legacy.canonical()
    # v5.2 refs are NOT injected into legacy canonical (hash preserved).
    assert "constitution_ref" not in canonical
    assert is_v52(legacy) is False
    migrated = migrate_to_v52(legacy)
    assert migrated.constitution_ref == legacy_constitution_ref()
    assert migrated.schema_version == V52_SCHEMA_VERSION
    assert migrated.package_id == legacy.package_id
    assert migrated.version == legacy.version


@pytest.mark.unit
def test_v52_package_export_import_semantic_equivalence() -> None:
    manifest = _v52()
    canonical = manifest.canonical()
    assert canonical["constitution_ref"] == "con_legacy_v5"
    assert canonical["genesis_ref"] == "genesis://rc"
    assert canonical["evolution_policy_ref"] == "canonical_replay"
    assert canonical["lineage_ref"] == "wl_rc_001"
    # Stable hash; migration is idempotent for v5.2 manifests.
    first = manifest.compute_hash()
    second = manifest.with_hash().content_hash
    assert first == second
    assert migrate_to_v52(manifest) is manifest


@pytest.mark.unit
def test_legacy_and_v52_hashes_differ_but_legacy_stays_stable() -> None:
    legacy = _legacy()
    legacy_before = legacy.content_hash
    migrated = migrate_to_v52(legacy)
    assert migrated.content_hash != legacy_before  # v5.2 adds refs
    assert legacy.content_hash == legacy_before  # legacy untouched
    assert LEGACY_CONSTITUTION_REF == "con_legacy_v5"


@pytest.mark.unit
def test_wxpack_cli_has_migrate_subcommand() -> None:
    wxpack = pathlib.Path(__file__).resolve().parents[3] / "scripts" / "wxpack.py"
    result = subprocess.run(
        [sys.executable, str(wxpack), "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "migrate" in result.stdout
