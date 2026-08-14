"""G15A: reference-world conformance harness.

Validates a World Pack (registry + root package id) against the reference-world
contract using only public package/runtime contracts. Catches missing
rights/evidence/eval metadata and proves install works without Core changes.
"""

from __future__ import annotations

import sys
from typing import Any

ROOT = None


def _require_imports() -> tuple[type, type]:
    from wanxiang_substrate.packages.install import PackageInstaller
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    return PackageInstaller, InMemoryPackageRegistry


def conformance_report(
    registry: Any,
    root_id: str,
    *,
    rights_refs: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    asset_refs: tuple[str, ...] = (),
    require_eval_metadata: bool = True,
) -> dict[str, Any]:
    """Run the reference-world contract checks and return a structured report."""
    PackageInstaller, InMemoryPackageRegistry = _require_imports()
    findings: list[str] = []
    if not isinstance(registry, InMemoryPackageRegistry):
        findings.append("registry must be the public InMemoryPackageRegistry")
    manifests: list[Any] = []
    root: Any = None
    for pid in registry.versions(root_id):
        m = registry.get(root_id, pid)
        if m is not None:
            manifests.append(m)
            root = m
    if root is None:
        return {"ok": False, "findings": ["root package not found"], "installed": False}
    if not root.package_id or not root.version:
        findings.append("missing package id/version")
    if not root.dependencies:
        findings.append("world pack must declare domain/world dependencies")
    if root.executable_trust != "untrusted" and not rights_refs:
        findings.append("trusted pack missing rights refs")
    if require_eval_metadata and not (rights_refs or evidence_refs or asset_refs):
        findings.append("missing rights/evidence/eval metadata")
    try:
        record = PackageInstaller().install(
            registry,
            root_id,
            rights_refs=rights_refs,
            evidence_refs=evidence_refs,
            asset_refs=asset_refs,
        )
        installed = True
    except Exception as exc:  # noqa: BLE001 - conformance reports the failure
        return {
            "ok": False,
            "findings": findings + [f"install failed: {exc}"],
            "installed": False,
        }
    return {
        "ok": not findings,
        "findings": findings,
        "installed": installed,
        "lock_hash": record.lock_hash,
    }


if __name__ == "__main__":
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
    print("reference-world conformance module; use the Python API.")
