"""Package authoring CLI (G17B): scaffold, validate and dry-run build.

Generated packages depend only on the public SDK (wanxiang_domain +
wanxiang_substrate.packages); validation reports actionable errors and never
auto-fixes semantics.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent

_TEMPLATE = '''"""%(name)s package (scaffolded by wxpack)."""

from __future__ import annotations

from wanxiang_substrate.packages.model import (
    UNTRUSTED,
    PackageManifest,
    SemanticVersion,
)


def build_manifest() -> PackageManifest:
    return PackageManifest(
        package_id=%(package_id)r,
        kind=%(kind)r,
        version=SemanticVersion(1, 0, 0),
        name=%(name)r,
        dependencies=(),
        executable_trust=UNTRUSTED,
    ).with_hash()
'''

_TEST_TEMPLATE = '''"""%(name)s package: baseline scaffold test."""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

from %(module)s import build_manifest


def test_manifest_valid_and_registrable() -> None:
    manifest = build_manifest()
    assert manifest.package_id == %(package_id)r
    registry = InMemoryPackageRegistry()
    registry.register(manifest)
    assert registry.get(manifest.package_id, manifest.version) is not None
'''


def scaffold(target: pathlib.Path, package_id: str, kind: str, name: str) -> pathlib.Path:
    if not package_id or not name:
        raise ValueError("package_id and name are required")
    if kind not in ("domain", "world", "scenario"):
        raise ValueError(f"kind must be domain|world|scenario, got {kind!r}")
    module = package_id.replace("-", "_")
    pkg_dir = target / package_id
    pkg_dir.mkdir(parents=True, exist_ok=True)
    (pkg_dir / f"{module}.py").write_text(
        _TEMPLATE % {"name": name, "package_id": package_id, "kind": kind},
        encoding="utf-8",
    )
    (pkg_dir / "test_package.py").write_text(
        _TEST_TEMPLATE % {"name": name, "package_id": package_id, "module": module},
        encoding="utf-8",
    )
    (pkg_dir / "README.md").write_text(
        f"# {name}\n\nScaffolded Wanxiang package ({kind}).\n", encoding="utf-8"
    )
    return pkg_dir


def validate(target: pathlib.Path, package_id: str) -> list[str]:
    module = package_id.replace("-", "_")
    mod_path = target / package_id / f"{module}.py"
    if not mod_path.exists():
        return [f"missing module {mod_path.name} in {target / package_id}"]
    sys.path.insert(0, str(target / package_id))
    spec = __import__("importlib.util").util.spec_from_file_location(module, mod_path)
    if spec is None or spec.loader is None:
        return ["cannot load generated module"]
    mod = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    manifest = mod.build_manifest()
    errors: list[str] = []
    if manifest.package_id != package_id:
        errors.append(f"manifest package_id {manifest.package_id!r} != {package_id!r}")
    if manifest.version.major != 1:
        errors.append("scaffold version must be 1.x")
    return errors


def dry_run_build(target: pathlib.Path, package_id: str) -> dict[str, Any]:
    module = package_id.replace("-", "_")
    sys.path.insert(0, str(target / package_id))
    spec = __import__("importlib.util").util.spec_from_file_location(
        module, target / package_id / f"{module}.py"
    )
    assert spec is not None and spec.loader is not None
    mod = __import__("importlib.util").util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    registry = __import__(
        "wanxiang_substrate.packages.registry", fromlist=["InMemoryPackageRegistry"]
    ).InMemoryPackageRegistry()
    registry.register(mod.build_manifest())
    installer = __import__(
        "wanxiang_substrate.packages.install", fromlist=["PackageInstaller"]
    ).PackageInstaller()
    record = installer.install(registry, package_id)
    return {"lock_hash": record.lock_hash, "package_id": package_id}


def main(argv: list[str] | None = None) -> int:
    sys.path.insert(0, str(ROOT))
    parser = argparse.ArgumentParser(prog="wxpack")
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("scaffold")
    s.add_argument("target", type=pathlib.Path)
    s.add_argument("package_id")
    s.add_argument("--kind", default="domain", choices=("domain", "world", "scenario"))
    s.add_argument("--name", default="")
    v = sub.add_parser("validate")
    v.add_argument("target", type=pathlib.Path)
    v.add_argument("package_id")
    b = sub.add_parser("build")
    b.add_argument("target", type=pathlib.Path)
    b.add_argument("package_id")
    args = parser.parse_args(argv)
    if args.command == "scaffold":
        name = args.name or args.package_id
        print(scaffold(args.target, args.package_id, args.kind, name))
    elif args.command == "validate":
        errors = validate(args.target, args.package_id)
        if errors:
            for e in errors:
                print("ERROR:", e)
            return 1
        print("valid")
    elif args.command == "build":
        print(dry_run_build(args.target, args.package_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
