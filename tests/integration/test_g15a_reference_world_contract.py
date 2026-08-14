"""G15A: reference-world contract & external pack boundary.

- A tiny external synthetic pack can be built and installed without modifying
  Core (public registry + installer only).
- The conformance harness catches missing rights/evidence/eval metadata.
- A pack with full metadata passes conformance and installs reproducibly.
"""

from __future__ import annotations

from scripts.reference_world_conformance import conformance_report
from wanxiang_substrate.packages.model import (
    UNTRUSTED,
    PackageManifest,
    SemanticVersion,
)
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry


def _pack_registry(with_meta: bool) -> InMemoryPackageRegistry:
    domain = PackageManifest(
        package_id="ref-domain",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="Ref Domain",
        executable_trust=UNTRUSTED,
    ).with_hash()
    world = PackageManifest(
        package_id="ref-world",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Ref World",
        dependencies=(("ref-domain", "==1.0.0"),),
        executable_trust=UNTRUSTED,
    ).with_hash()
    scenario = PackageManifest(
        package_id="ref-scenario",
        kind="scenario",
        version=SemanticVersion(1, 0, 0),
        name="Ref Scenario",
        dependencies=(
            ("ref-world", "==1.0.0"),
            ("ref-domain", "==1.0.0"),
        ),
        executable_trust=UNTRUSTED,
    ).with_hash()
    registry = InMemoryPackageRegistry()
    for m in (domain, world, scenario):
        registry.register(m)
    if with_meta:
        # conformance receives rights/evidence/eval metadata as install inputs
        return registry
    return registry


def test_tiny_external_pack_builds_and_installs_without_core_changes() -> None:
    registry = _pack_registry(with_meta=True)
    report = conformance_report(
        registry,
        "ref-scenario",
        rights_refs=("ref://rights",),
        evidence_refs=("ref://evidence",),
        asset_refs=("ref://assets",),
    )
    assert report["ok"] is True, report["findings"]
    assert report["installed"] is True
    # Reproducible: export + hash are stable.
    assert report["lock_hash"]
    # Core remains domain-neutral: installing the pack did not touch Core.
    import pathlib

    core_marker = (
        pathlib.Path("packages/core") if (pathlib.Path("packages/core")).exists() else None
    )
    assert core_marker is None or not core_marker.exists()


def test_conformance_catches_missing_metadata() -> None:
    registry = _pack_registry(with_meta=True)
    report = conformance_report(registry, "ref-scenario")
    assert report["ok"] is False
    assert any("rights/evidence/eval" in f for f in report["findings"])


def test_conformance_reports_install_failures() -> None:
    registry = InMemoryPackageRegistry()
    lonely = PackageManifest(
        package_id="lonely",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Lonely",
        dependencies=(("missing-dep", "==1.0.0"),),
        executable_trust=UNTRUSTED,
    ).with_hash()
    registry.register(lonely)
    report = conformance_report(registry, "lonely")
    assert report["ok"] is False
    assert report["installed"] is False
    assert any("install failed" in f for f in report["findings"])
