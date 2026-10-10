"""Source-agnostic, no-cost scene planning; no real visuals claimed."""

# pyright: reportPrivateUsage=false

import json

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
    compiler_metadata: dict[str, str] | None = None,
) -> WorldPackageDraft:
    draft = WorldDraft(
        draft_id=book,
        revision=1,
        status="CREATED",
        places=places,
        entities=(("person-a", "甲"),),
        compiler_metadata=compiler_metadata or {},
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


def test_long_book_preview_ranks_places_by_evidence_coverage_not_name_order() -> None:
    evidence = [
        {
            "candidate_id": "place-garden",
            "name": "园林",
            "source_refs": ["book#chapter-1"],
            "confidence": 0.7,
            "cooccurring_candidates": [],
        },
        {
            "candidate_id": "place-gate",
            "name": "城门",
            "source_refs": [
                "book#chapter-2",
                "book#chapter-8",
                "book#chapter-19",
            ],
            "confidence": 0.65,
            "cooccurring_candidates": [{"kind": "character", "label": "守门人"}],
        },
        {
            "candidate_id": "place-study",
            "name": "书房",
            "source_refs": ["book#chapter-3", "book#chapter-9"],
            "confidence": 0.8,
            "cooccurring_candidates": [],
        },
    ]
    package = package_from_book(
        "long-book",
        ("园林", "书房", "城门", "码头"),
        compiler_metadata={
            "scene_evidence_v1": json.dumps(evidence, ensure_ascii=False),
        },
    )
    plan = _plan_book_scene_assets(package, max_preview_scenes=2)

    assert [scene.place_name for scene in plan.scene_requests] == ["城门", "书房"]
    assert plan.deferred_scene_count == 2


def test_explicit_source_place_can_be_prioritized_for_on_demand_generation() -> None:
    package = package_from_book("ondemand", ("园林", "书房", "城门", "码头", "山谷"))
    plan = _plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=("码头",),
    )

    assert [scene.place_name for scene in plan.scene_requests] == ["码头"]
    assert plan.deferred_scene_count == 4
    assert plan.place_names == ("园林", "书房", "城门", "码头", "山谷")


def test_large_generic_book_indexes_evidence_without_changing_scene_selection() -> None:
    places = tuple(f"Location-{index:04d}" for index in range(1200))
    evidence: list[dict[str, object]] = [
        {
            "name": name,
            "source_refs": [f"book#chapter-{index}"],
            "confidence": index / 1200,
            "cooccurring_candidates": [],
        }
        for index, name in enumerate(places)
    ]
    evidence[-1]["source_refs"] = ["book#chapter-1199", "book#chapter-1201"]
    package = package_from_book(
        "large-source-index",
        places,
        compiler_metadata={"scene_evidence_v1": json.dumps(evidence)},
    )
    first = _plan_book_scene_assets(package)
    again = _plan_book_scene_assets(package)

    assert first == again
    assert len(first.scene_requests) == 3
    assert first.scene_requests[0].place_name == "Location-1199"
    assert first.deferred_scene_count == 1197
    assert first.scene_requests[0].source_refs == ("book#chapter-1199", "book#chapter-1201")


def test_topology_requires_source_locator_and_bounded_confidence() -> None:
    valid = {
        "source_place": "海港",
        "target_place": "城门",
        "relation_type": "path",
        "source_refs": ["book#chapter-2"],
        "confidence": 0.84,
    }
    no_locator = {**valid, "source_refs": []}
    no_relation = {**valid, "relation_type": ""}
    zero_confidence = {**valid, "confidence": 0.0}
    excessive_confidence = {**valid, "confidence": 3.0}
    nonfinite_confidence = {**valid, "confidence": float("nan")}
    fake_place = {**valid, "target_place": "虚构山谷"}
    package = package_from_book(
        "topology-proof",
        ("海港", "城门"),
        compiler_metadata={
            "scene_topology_evidence_v1": json.dumps(
                [
                    no_locator,
                    no_relation,
                    zero_confidence,
                    excessive_confidence,
                    nonfinite_confidence,
                    fake_place,
                    valid,
                ],
                ensure_ascii=False,
            )
        },
    )
    plan = _plan_book_scene_assets(package)

    assert len(plan.topology_relations) == 1
    assert plan.topology_relations[0].source_refs == ("book#chapter-2",)
    assert plan.topology_relations[0].confidence == 0.84


def test_reviewed_scene_evidence_invalidates_pixels_without_changing_world_identity() -> None:
    def compile_with(label: str, locator: str) -> tuple[str, str, str]:
        book = package_from_book(
            "visual-evidence-revision",
            ("城门",),
            compiler_metadata={
                "scene_evidence_v1": json.dumps(
                    [
                        {
                            "name": "城门",
                            "source_refs": [locator],
                            "confidence": 0.9,
                            "cooccurring_candidates": [{"kind": "object", "label": label}],
                        }
                    ],
                    ensure_ascii=False,
                )
            },
        )
        request = _plan_book_scene_assets(book).scene_requests[0]
        return (request.stable_key, request.style_key, request.cache_key)

    first = compile_with("灯笼", "book#chapter-1")
    reviewed = compile_with("古钟", "book#chapter-1")
    newly_cited = compile_with("灯笼", "book#chapter-2")

    assert first[:2] == reviewed[:2] == newly_cited[:2]
    assert len({first[2], reviewed[2], newly_cited[2]}) == 3
