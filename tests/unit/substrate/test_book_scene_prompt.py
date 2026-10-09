"""Story visual style and scene prompts stay bounded and source-traceable."""

# pyright: reportPrivateUsage=false

from wanxiang_substrate.assets.book_scene_plan import (
    _SourceSceneRequest,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_prompt import (
    _compile_scene_generation_brief,
    _story_visual_profile,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec


def _request(place: str, key: str, style_key: str) -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name=place,
        stable_key=key,
        spec=SemanticSceneSpec(
            spec_id=f"scene-{key}",
            semantic_id=f"place:{key}",
            kind="illustrated-environment",
            requirements=(
                f"source_place_name:{place}",
                "source_context_candidate:character:沈砚",
                "source_context_candidate:event:入城",
                "no_unverified_character_placement",
            ),
        ),
        cache_key=f"cache-{key}",
        source_refs=("book#chapter-1:paragraph-3",),
        confidence=0.81,
        style_key=style_key,
    )


def test_one_world_reuses_one_visual_profile_across_scenes() -> None:
    style_key = "story-style-001"
    plan = _SourceVisualPlan(
        package_id="world:style",
        source_digest="e" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(
            _request("城门", "gate", style_key),
            _request("书房", "study", style_key),
        ),
        deferred_scene_count=0,
    )
    profile = _story_visual_profile(plan)
    first = _compile_scene_generation_brief(plan.scene_requests[0], profile)
    second = _compile_scene_generation_brief(plan.scene_requests[1], profile)

    assert first.style_profile_id == second.style_profile_id == profile.profile_id
    assert first.style_key == second.style_key == style_key
    assert first.semantic_prompt != second.semantic_prompt


def test_scene_brief_contains_structured_context_not_full_source_text() -> None:
    request = _request("机关桥", "bridge", "story-style-002")
    plan = _SourceVisualPlan(
        package_id="world:privacy",
        source_digest="f" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(request,),
        deferred_scene_count=0,
    )
    profile = _story_visual_profile(plan)
    brief = _compile_scene_generation_brief(request, profile)

    assert brief.full_source_included is False
    assert brief.source_refs == ("book#chapter-1:paragraph-3",)
    assert "机关桥" in brief.semantic_prompt
    assert "character:沈砚" in brief.semantic_prompt
    assert "event:入城" in brief.semantic_prompt
    assert "book#chapter-1:paragraph-3" not in brief.semantic_prompt
    assert len(brief.semantic_prompt) < 1800
    assert "do-not-invent-geographic-topology" in brief.negative_constraints
