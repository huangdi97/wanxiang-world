"""G17G: black-box external sample pack (built outside Core repository internals).

Authors a nontrivial sample package as if by a third party, using only the
public SDK (wanxiang_domain + wanxiang_substrate) and docs — no Core-private
imports. The sample includes a custom domain rule/action via the permitted
resolver extension mechanism.
"""

from __future__ import annotations

import pathlib

SAMPLE_MODULE = '''"""Black-box external sample (G17G) - public SDK only."""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

from wanxiang_substrate.packages.model import (
    UNTRUSTED,
    PackageManifest,
    SemanticVersion,
)

ACTOR = EntityId("sample_hero")
HEALTH = ComponentId("sample_health")


def build_manifest(version: tuple[int, int, int] = (1, 0, 0)) -> PackageManifest:
    return PackageManifest(
        package_id="blackbox-sample",
        kind="domain",
        version=SemanticVersion(*version),
        name="Blackbox Sample Domain",
        dependencies=(),
        executable_trust=UNTRUSTED,
    ).with_hash()


def instantiate(_command: CommandEnvelope, _state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=ACTOR,
                entity_type="person",
                components=(
                    ComponentData(
                        component_id=HEALTH,
                        component_type="body.condition",
                        schema_version=SchemaVersion(1),
                        fields={"health": 100, "energy": 100},
                    ),
                ),
            ),
        )
    )


def heal(_command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=ACTOR,
                components=(
                    ComponentData(
                        component_id=HEALTH,
                        component_type="body.condition",
                        schema_version=SchemaVersion(1),
                        fields={"health": 100, "energy": 100},
                    ),
                ),
            ),
        )
    )


def register(registry) -> None:
    registry.register("sample.instantiate", instantiate)
    registry.register("sample.heal", heal)
'''

SAMPLE_TEST = '''"""Blackbox sample baseline test."""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

from sample import build_manifest


def test_manifest_valid() -> None:
    m = build_manifest()
    reg = InMemoryPackageRegistry()
    reg.register(m)
    assert reg.get(m.package_id, m.version) is not None
'''


def create_external_sample(
    directory: pathlib.Path, version: tuple[int, int, int] = (1, 0, 0)
) -> pathlib.Path:
    """Write the sample package into an external directory."""
    directory.mkdir(parents=True, exist_ok=True)
    module = directory / "sample.py"
    text = SAMPLE_MODULE
    if version != (1, 0, 0):
        text = text.replace(
            "def build_manifest(version: tuple[int, int, int] = (1, 0, 0)) -> PackageManifest:",
            "def build_manifest(version: tuple[int, int, int] = %r) -> PackageManifest:"  # noqa: UP031
            % (version,),
        )
    module.write_text(text, encoding="utf-8")
    (directory / "test_sample.py").write_text(SAMPLE_TEST, encoding="utf-8")
    (directory / "README.md").write_text("# Blackbox Sample\n", encoding="utf-8")
    return directory
