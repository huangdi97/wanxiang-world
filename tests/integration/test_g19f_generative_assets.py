"""G19F: generative asset / scene pipeline & semantic binding research.

- Regeneration creates a new version, never a silent overwrite; world truth untouched.
- Rights/provenance travel with the asset into projections.
- Projection is rebuildable from semantic state (deterministic hash).
- Missing assets become explicit fallback markers.
- Research flag off => no core regression.
"""

from __future__ import annotations

from wanxiang_research.flags import DEFAULT_FLAGS
from wanxiang_research.generative_assets import (
    AssetFoundryPipeline,
    AssetSpec,
    DeterministicFoundry,
    SceneAnchor,
    SceneProjector,
)


def _spec(asset_id: str = "hero", kind: str = "three_d", rights: str = "source-gated") -> AssetSpec:
    return AssetSpec(
        asset_id=asset_id,
        kind=kind,
        entity_ref="ent_hero",
        package_ref="pack_hero",
        revision=7,
        rights=rights,
    )


def test_regeneration_creates_new_version_not_silent_overwrite() -> None:
    pipeline = AssetFoundryPipeline(DeterministicFoundry())
    first = pipeline.generate(_spec())
    second = pipeline.generate(_spec())
    assert first.version == 1
    assert second.version == 2
    assert first != second
    # Old manifest is retained in history, not overwritten.
    assert [m.version for m in pipeline.history("hero")] == [1, 2]
    # Discard removes only the active binding; history survives.
    assert pipeline.discard("hero") is True
    assert pipeline.active("hero") is None
    assert len(pipeline.history("hero")) == 2


def test_rights_and_provenance_travel_with_asset() -> None:
    pipeline = AssetFoundryPipeline(DeterministicFoundry(generator_id="foundry-x"))
    manifest = pipeline.generate(_spec(rights="family-heritage"))
    assert manifest.rights == "family-heritage"
    assert manifest.provenance == "foundry-x:v1"
    anchors = (SceneAnchor(slot="main", entity_ref="ent_hero", asset_id="hero"),)
    layout = SceneProjector(pipeline).project("scene_1", anchors)
    bound = layout.assets[0]
    assert bound.rights == "family-heritage"
    assert bound.provenance == "foundry-x:v1"
    assert bound.bind_key() == ("ent_hero", "pack_hero", 7)


def test_projection_rebuildable_from_semantic_state() -> None:
    pipeline = AssetFoundryPipeline(DeterministicFoundry())
    pipeline.generate(_spec())
    pipeline.generate(_spec(asset_id="bg", kind="visual"))
    anchors = (
        SceneAnchor(slot="main", entity_ref="ent_hero", asset_id="hero"),
        SceneAnchor(slot="bg", entity_ref="ent_bg", asset_id="bg"),
    )
    projector = SceneProjector(pipeline)
    layout1 = projector.project("scene_1", anchors)
    layout2 = projector.project("scene_1", anchors)
    assert layout1.rebuild_hash() == layout2.rebuild_hash()


def test_missing_asset_becomes_explicit_fallback_marker() -> None:
    pipeline = AssetFoundryPipeline(DeterministicFoundry())
    anchors = (SceneAnchor(slot="main", entity_ref="ent_hero", asset_id="hero"),)
    layout = SceneProjector(pipeline).project("scene_1", anchors)
    marker = layout.assets[0]
    assert marker.fallback is True
    assert marker.generated is False
    assert marker.provenance == "missing:fallback"
    assert marker.bind_key() == ("ent_hero", "", 0)


def test_flag_off_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("generative_assets") is False
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    result = StructuredCompiler().compile("stable_2", {"src": approved_source()})
    assert result.ok
