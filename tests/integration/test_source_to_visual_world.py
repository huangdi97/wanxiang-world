"""One book -> visual world uses the same generic pipeline for unrelated books."""

from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_projection import player_world_detail
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _book(source_id: str, character: str, place: str) -> SourceRecord:
    text = (
        f"# Chapter\nCharacter: {character}\n"
        f"{character} arrived in {place} in 1985.\n"
        "rule: visitors register\n"
    )
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(text),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        provenance=f"synthetic:source-to-visual:{source_id}",
        access="public",
    )


def _profile(package_id: str, name: str) -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id=f"profile:{name}",
        world_package_ref=package_id,
        scenario_ref=f"scenario:{name}",
        runtime_profile_ref="runtime:reference",
        experience_package_ref=f"experience:{name}",
        projection_profile_ref="projection:player",
        visibility="public",
        display_name=name,
    )


def test_two_books_automatically_create_different_visual_assets_without_custom_code() -> None:
    fiction = OneClickAuthoring().run(
        "visual_fiction",
        (_book("fiction_source", "Alice", "Garden"),),
        profile="book",
    )
    history = OneClickAuthoring().run(
        "visual_history",
        (_book("history_source", "Clara", "Fortress"),),
        profile="book",
    )

    assert fiction.visual_plan is not None
    assert history.visual_plan is not None
    assert fiction.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert history.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert fiction.visual_assets
    assert history.visual_assets
    assert fiction.visual_plan.scene_requests[0].source_refs
    assert history.visual_plan.scene_requests[0].source_refs
    assert fiction.visual_plan.scene_requests[0].confidence > 0
    assert history.visual_plan.scene_requests[0].confidence > 0
    assert fiction.visual_assets[0].place_name == "Garden"
    assert history.visual_assets[0].place_name == "Fortress"
    assert fiction.visual_assets[0].content_sha256 != history.visual_assets[0].content_sha256

    fiction_view = player_world_detail(
        _profile(fiction.package.package_id, "Fiction"),
        fiction.package,
        locale="en-US",
        include_visual=True,
    )
    history_view = player_world_detail(
        _profile(history.package.package_id, "History"),
        history.package,
        locale="en-US",
        include_visual=True,
    )

    fiction_visual = fiction_view["visual"]
    history_visual = history_view["visual"]
    assert isinstance(fiction_visual, dict)
    assert isinstance(history_visual, dict)
    fiction_scenes = fiction_visual["scenes"]
    history_scenes = history_visual["scenes"]
    assert isinstance(fiction_scenes, list)
    assert isinstance(history_scenes, list)
    assert str(fiction_scenes[0]["data_uri"]).startswith("data:image/svg+xml;base64,")
    assert str(history_scenes[0]["data_uri"]).startswith("data:image/svg+xml;base64,")
