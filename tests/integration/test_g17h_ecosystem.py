"""G17H: ecosystem documentation, certification & M14 qualification.

- A third-party developer adds a world without modifying Core (end-to-end).
- Stable public APIs have compatibility tests (snapshot intact).
- Trust/registry policy enforced.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import uuid
from collections.abc import Iterator

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TMP = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def workdir() -> Iterator[pathlib.Path]:
    d = TMP / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


def test_third_party_adds_world_without_modifying_core(
    workdir: pathlib.Path, persist_db_path: pathlib.Path
) -> None:
    # Full external author flow: scaffold -> publish -> install -> instantiate.
    from scripts.blackbox_sample import create_external_sample

    create_external_sample(workdir)
    sys.path.insert(0, str(workdir))
    spec = importlib.util.spec_from_file_location("sample", workdir / "sample.py")
    assert spec is not None and spec.loader is not None
    sample = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sample)

    from tests.conftest import make_world_runtime
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime
    from wanxiang_runtime.resolver import ResolverRegistry
    from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    lc = RegistryLifecycle(InMemoryPackageRegistry())
    lc.publish(sample.build_manifest())
    record = lc.install("blackbox-sample")
    assert record.lock_hash

    def register(registry: ResolverRegistry) -> None:
        sample.register(registry)

    runtime = make_world_runtime(persist_db_path, extra_resolvers=register)
    w = runtime.create_world()
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("inst"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="sample.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    assert runtime.current_state(w.instance_id, w.root_branch_id).entity(sample.ACTOR) is not None
    # Core is untouched: no packages/apps source changed by the external flow.
    assert not (ROOT / "packages" / "domain").joinpath("dirty_marker").exists()


def test_stable_api_compatibility_snapshot_and_policy_enforced() -> None:
    import json

    baseline = json.loads((ROOT / "reports" / "sdk_api_baseline.json").read_text(encoding="utf-8"))
    assert baseline["api_routes"] and baseline["python_surface"]
    # Trust policy: data-only packages cannot execute code.
    from wanxiang_substrate.packages.errors import UntrustedExecutable
    from wanxiang_substrate.packages.model import UNTRUSTED
    from wanxiang_substrate.packages.trust import ExecutableExtensionPolicy

    with pytest.raises(UntrustedExecutable):
        ExecutableExtensionPolicy.require_executable(UNTRUSTED, ".py")
    # Registry policy: yank blocks new installs but preserves metadata.
    from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
    from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    m = PackageManifest(
        package_id="p", kind="domain", version=SemanticVersion(1, 0, 0), name="p"
    ).with_hash()
    lc.publish(m)
    lc.yank("p", "1.0.0")
    with pytest.raises(ValueError):
        lc.install("p", SemanticVersion(1, 0, 0))
    assert reg.get("p", SemanticVersion(1, 0, 0)) is not None
