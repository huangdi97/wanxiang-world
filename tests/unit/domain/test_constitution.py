"""G30B: World Constitution model and versioning invariants."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from wanxiang_domain.constitution import (
    ROOT_CONSTITUTION,
    ConstitutionManifest,
    ConstitutionVersion,
    constitution_from_primitive,
    legacy_default_constitution,
)
from wanxiang_domain.ids import ConstitutionId


def _sample_constitution() -> ConstitutionManifest:
    return ConstitutionManifest(
        constitution_id=ConstitutionId("con_sample"),
        version=ConstitutionVersion(2),
        name="Sample World Constitution",
        root_constraints=(
            "single_commit_boundary",
            "append_only_history",
            "replayable_history",
        ),
        mutable_law_layers=("ontology", "law"),
        provenance=("ref://author-notes",),
        rights_ref="public-domain",
        evolution_policy="soft_canon",
        world_definition_ref="pack://sf-world@1.0.0",
    ).with_hash()


@pytest.mark.unit
def test_schema_round_trip_preserves_content_hash() -> None:
    manifest = _sample_constitution()
    primitive = manifest.to_primitive()
    restored = constitution_from_primitive(primitive)
    assert restored.constitution_id == manifest.constitution_id
    assert restored.version == manifest.version
    assert restored.root_constraints == manifest.root_constraints
    assert restored.mutable_law_layers == manifest.mutable_law_layers
    assert restored.evolution_policy == manifest.evolution_policy
    assert restored.world_definition_ref == manifest.world_definition_ref
    assert restored.content_hash == manifest.content_hash
    assert restored.compute_hash() == manifest.compute_hash()


@pytest.mark.unit
def test_different_constitutions_share_no_mutable_objects() -> None:
    a = _sample_constitution()
    b = legacy_default_constitution()
    # Distinct constitutions are distinct value objects with distinct hashes.
    assert a.constitution_id != b.constitution_id
    assert a.content_hash != b.content_hash
    # All manifest fields are immutable value objects/tuples; no mutable dict/list.
    assert isinstance(a.root_constraints, tuple)
    assert isinstance(a.mutable_law_layers, tuple)
    assert isinstance(a.provenance, tuple)
    assert not hasattr(a, "__dict__") or not any(
        isinstance(getattr(a, f), (dict, list)) for f in ("root_constraints", "mutable_law_layers")
    )
    # Mutation of the manifest type is impossible at the type level (frozen).
    with pytest.raises(FrozenInstanceError):
        a.root_constraints = ("hacked",)  # type: ignore[misc]


@pytest.mark.unit
def test_legacy_worldpack_binds_to_default_legacy_constitution() -> None:
    legacy = legacy_default_constitution()
    assert legacy.constitution_id == ConstitutionId("con_legacy_v5")
    assert "single_commit_boundary" in legacy.root_constraints
    assert "append_only_history" in legacy.root_constraints
    # Legacy packs keep mutable law layers so authors can evolve their world.
    assert "ontology" in legacy.mutable_law_layers
    assert legacy.compute_hash()  # content hash is stable
    # Round-trip of the legacy manifest is also valid.
    restored = constitution_from_primitive(legacy.to_primitive())
    assert restored.content_hash == legacy.content_hash


@pytest.mark.unit
def test_root_constitution_is_immutable_and_isolated() -> None:
    assert ROOT_CONSTITUTION.constitution_id == ConstitutionId("con_platform_root")
    # The platform root has NO mutable law layers: world policy cannot amend it.
    assert ROOT_CONSTITUTION.mutable_law_layers == ()
    assert "no_self_amendment" in ROOT_CONSTITUTION.root_constraints
    assert "world_policy_cannot_modify_platform" in ROOT_CONSTITUTION.root_constraints
    # A world instance has no API to mutate the root manifest.
    with pytest.raises(FrozenInstanceError):
        ROOT_CONSTITUTION.root_constraints = ()  # type: ignore[misc]


@pytest.mark.unit
def test_world_definition_binding_via_constitution_ref() -> None:
    manifest = _sample_constitution()
    assert manifest.world_definition_ref == "pack://sf-world@1.0.0"
    # The binding survives a serialization round-trip (authoring record).
    restored = constitution_from_primitive(manifest.to_primitive())
    assert restored.world_definition_ref == "pack://sf-world@1.0.0"
