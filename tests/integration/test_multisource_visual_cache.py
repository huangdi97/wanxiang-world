"""Equivalent multi-source bundles reuse visual assets without losing source provenance."""

# pyright: reportPrivateUsage=false

from wanxiang_substrate.assets.book_scene_visual import _VisualAssetCache
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source(source_id: str, character: str, place: str) -> SourceRecord:
    text = f"# Chapter\nCharacter: {character}\n{character} arrived in {place} in 1985.\n"
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(text),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        provenance=f"synthetic:multisource-cache:{source_id}",
        access="public",
    )


def test_equivalent_multisource_bundle_reuses_visual_cache_across_new_source_ids() -> None:
    cache = _VisualAssetCache()
    first = OneClickAuthoring(visual_cache=cache).run(
        "bundle-first",
        (
            _source("first-a", "Alice", "Garden"),
            _source("first-b", "Bob", "Harbor"),
        ),
        profile="book",
    )
    second = OneClickAuthoring(visual_cache=cache).run(
        "bundle-second",
        (
            _source("second-a", "Alice", "Garden"),
            _source("second-b", "Bob", "Harbor"),
        ),
        profile="book",
    )

    assert first.visual_plan is not None and second.visual_plan is not None
    assert first.visual_plan.source_digest == second.visual_plan.source_digest
    assert first.visual_provider_calls == len(first.visual_assets) == 2
    assert second.visual_provider_calls == 0
    assert second.visual_cache_hits == len(second.visual_assets) == 2
    assert {item.content_sha256 for item in first.visual_assets} == {
        item.content_sha256 for item in second.visual_assets
    }
    first_refs = {ref for scene in first.visual_plan.scene_requests for ref in scene.source_refs}
    second_refs = {ref for scene in second.visual_plan.scene_requests for ref in scene.source_refs}
    assert first_refs != second_refs
    assert all("first-" in ref for ref in first_refs)
    assert all("second-" in ref for ref in second_refs)
