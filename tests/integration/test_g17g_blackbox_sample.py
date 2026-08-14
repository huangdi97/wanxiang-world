"""G17G: black-box external sample pack built outside Core repository internals.

- The sample works without Core source-tree imports (public SDK only).
- An old instance stays pinned/replayable after v2 is published.
- A new instance can use v2 after explicit install.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import uuid
from collections.abc import Iterator

import pytest
from scripts.blackbox_sample import create_external_sample

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TMP = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def external_dir() -> Iterator[pathlib.Path]:
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


def _load_sample(directory: pathlib.Path):
    sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location("sample", directory / "sample.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_blackbox_sample_works_without_core_imports(
    external_dir: pathlib.Path, persist_db_path: pathlib.Path
) -> None:
    create_external_sample(external_dir)
    sample = _load_sample(external_dir)

    # Build/publish via the public registry lifecycle.
    from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(sample.build_manifest())
    record = lc.install("blackbox-sample")
    assert record.lock_hash

    # Instantiate + run the custom domain action through the public runtime.
    from tests.conftest import make_world_runtime
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        sample.register(registry)

    runtime = make_world_runtime(persist_db_path, extra_resolvers=register)
    w = runtime.create_world()
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("sample_inst"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="sample.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("sample_heal"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(1),
            action_type="sample.heal",
            payload={},
            world_time=WorldTime(2),
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(sample.ACTOR) is not None


def test_old_instance_pinned_and_v2_explicit_upgrade(
    external_dir: pathlib.Path, persist_db_path: pathlib.Path
) -> None:
    create_external_sample(external_dir, version=(1, 0, 0))
    sample = _load_sample(external_dir)
    from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(sample.build_manifest((1, 0, 0)))
    v1 = lc.install("blackbox-sample", sample.build_manifest((1, 0, 0)).version)

    # Publish v2; the v1 install record is unchanged (pinned).
    lc.publish(sample.build_manifest((2, 0, 0)))
    assert v1.package_version == sample.build_manifest((1, 0, 0)).version
    assert (
        lc.upgrade_candidate("blackbox-sample", sample.build_manifest((1, 0, 0)).version)
        == sample.build_manifest((2, 0, 0)).version
    )
    # A new instance explicitly installs v2.
    v2 = lc.install("blackbox-sample", sample.build_manifest((2, 0, 0)).version)
    assert v2.package_version == sample.build_manifest((2, 0, 0)).version
    # Old v1 install remains reproducible (export hash stable).
    from wanxiang_substrate.packages.install import export_install, install_export_hash

    assert install_export_hash(export_install(v1)) == install_export_hash(export_install(v1))
