"""Source-agnostic, no-cost scene planning; no real visuals claimed."""

import pytest
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion


def package_from_book(
    book: str,
    places: tuple[str, ...],
    *,
    rights_ok: bool = True,
    source_pinned: bool = True,
) -> WorldPackageDraft:
    draft = WorldDraft(
        draft_id=book,
        revision=1,
        status="CREATED",
        places=places,
        entities=(("person-a", "甲"),),
    )
    manifest = PackageManifest(
        package_id=f"world:{book}",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name=f"World {book}",
    ).with_hash()
    return WorldPackageDraft(
        package_id=manifest.package_id,
        draft_id=book,
        draft_revision=1,
        manifest=manifest,
        source_versions=((book, "v1"),) if source_pinned else (),
        domain_versions=(),
        evidence_coverage=1.0,
        unresolved_gaps=(),
        rights_ok=rights_ok,
        for_preview=True,
        draft=draft,
    )


def test_two_unrelated_books_use_identical_generic_pipeline() -> None:
    a = _plan_book_scene_assets(package_from_book("fiction", ("园林", "书房", "城门", "码头")))
    b = _plan_book_scene_assets(package_from_book("history", ("堡垒", "港口")))
    assert a.status == b.status == "READY_FOR_ASSET_PROVIDER"
    assert [s.place_name for s in a.scene_requests] == ["园林", "书房", "城门"]
    assert [s.place_name for s in b.scene_requests] == ["堡垒", "港口"]
    assert a.deferred_scene_count == 1
    assert b.deferred_scene_count == 0
    assert all(
        "no_unverified_character_placement" in item.spec.requirements
        for item in a.scene_requests + b.scene_requests
    )
    assert a.image_provider_calls == b.image_provider_calls == 0


def test_no_invented_place_rights_and_budget_fail_closed() -> None:
    empty = _plan_book_scene_assets(package_from_book("unknown", ()))
    blocked = _plan_book_scene_assets(package_from_book("private", ("私有地点",), rights_ok=False))
    missing = _plan_book_scene_assets(
        package_from_book("unversioned", ("地点",), source_pinned=False)
    )
    zero = _plan_book_scene_assets(package_from_book("budget", ("山谷",)), max_preview_scenes=0)
    assert empty.status == "PLACES_NOT_EXTRACTED"
    assert blocked.status == "RIGHTS_BLOCKED"
    assert missing.status == "SOURCE_PINS_MISSING"
    assert zero.status == "BUDGET_ZERO"
    assert not empty.scene_requests
    assert not blocked.scene_requests
    assert not missing.scene_requests
    assert not zero.scene_requests


def test_plan_is_content_addressed_and_avoids_duplicate_place_spend() -> None:
    package = package_from_book("repeat", ("竹林", "竹林", "溪谷"))
    first = _plan_book_scene_assets(package)
    again = _plan_book_scene_assets(package)
    assert first == again
    assert len(first.scene_requests) == 2
    assert len({item.cache_key for item in first.scene_requests}) == 2
    with pytest.raises(ValueError):
        _plan_book_scene_assets(package, max_preview_scenes=13)
