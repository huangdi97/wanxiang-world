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


def test_place_evidence_records_source_support_for_every_atlas_place() -> None:
    metadata = {
        "scene_evidence_v1": json.dumps(
            [
                {
                    "name": "Old Town",
                    "source_refs": ["src://a#1", "src://a#2"],
                    "confidence": 0.8,
                    "cooccurring_candidates": [
                        {"kind": "identity", "label": "Alice"},
                        {"kind": "event", "label": "arrival"},
                    ],
                },
                {"name": "Harbor", "source_refs": ["src://a#3"], "confidence": 0.9},
            ]
        )
    }
    package = package_from_book(
        "long-book",
        ("Old Town", "Harbor", "Tower"),
        compiler_metadata=metadata,
    )

    plan = _plan_book_scene_assets(package, max_preview_scenes=2)

    assert [request.place_name for request in plan.scene_requests] == ["Old Town", "Harbor"]
    evidence = {item.place_name: item for item in plan.place_evidence}
    assert evidence["Old Town"].source_ref_count == 2
    assert evidence["Old Town"].confidence == pytest.approx(0.8)
    assert evidence["Old Town"].clue_count == 2
    assert evidence["Tower"].source_ref_count == 0
    assert [item.place_name for item in plan.place_evidence] == ["Old Town", "Harbor", "Tower"]


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


def test_invalid_source_confidence_never_outranks_verified_place() -> None:
    evidence = [
        {"name": "虚影", "source_refs": ["book#one"], "confidence": float("nan")},
        {"name": "城门", "source_refs": ["book#two"], "confidence": 0.76},
        {"name": "港湾", "source_refs": ["book#three"], "confidence": float("inf")},
    ]
    package = package_from_book(
        "untrusted-rank",
        ("虚影", "城门", "港湾"),
        compiler_metadata={"scene_evidence_v1": json.dumps(evidence, ensure_ascii=False)},
    )
    plan = _plan_book_scene_assets(package)

    assert plan.scene_requests[0].place_name == "城门"
    by_place = {item.place_name: item.confidence for item in plan.scene_requests}
    assert by_place == {"城门": 0.76, "虚影": 0.0, "港湾": 0.0}


def test_duplicate_identical_sources_share_one_visual_identity() -> None:
    fingerprint = "b" * 64

    def plan_for(sources: dict[str, str]) -> tuple[str, str, int, int]:
        metadata = {
            "source_fingerprints_v1": json.dumps(sorted(sources.values())),
            "source_fingerprint_map_v1": json.dumps(sources),
            "scene_evidence_v1": json.dumps(
                [
                    {
                        "name": "Harbor",
                        "source_refs": [f"text://{source_id}#p1"],
                        "confidence": 0.7,
                    }
                    for source_id in sources
                ],
                ensure_ascii=False,
            ),
        }
        plan = _plan_book_scene_assets(
            package_from_book("bundle", ("Harbor",), compiler_metadata=metadata)
        )
        scene = plan.scene_requests[0]
        evidence = {item.place_name: item for item in plan.place_evidence}["Harbor"]
        return (
            plan.source_digest,
            scene.cache_key,
            evidence.source_ref_count,
            evidence.source_count,
        )

    single = plan_for({"s1": fingerprint})
    duplicate = plan_for({"s1": fingerprint, "s2": fingerprint})

    assert single[0] == duplicate[0]
    assert single[1] == duplicate[1]
    assert single[2] == 1
    assert duplicate[2] == 2
    assert single[3] == 1
    assert duplicate[3] == 2


def test_multi_source_bundle_merges_place_evidence_and_reacts_to_content_change() -> None:
    first_fingerprint, second_fingerprint = "1" * 64, "2" * 64

    def plan_for(second: str) -> tuple[str, str, int, int]:
        metadata = {
            "source_fingerprints_v1": json.dumps(sorted([first_fingerprint, second])),
            "source_fingerprint_map_v1": json.dumps({"s1": first_fingerprint, "s2": second}),
            "scene_evidence_v1": json.dumps(
                [
                    {
                        "name": "Harbor",
                        "source_refs": ["text://s1#p1"],
                        "confidence": 0.6,
                    },
                    {
                        "name": "Harbor",
                        "source_refs": ["text://s2#p2"],
                        "confidence": 0.9,
                    },
                ],
                ensure_ascii=False,
            ),
        }
        plan = _plan_book_scene_assets(
            package_from_book("bundle", ("Harbor",), compiler_metadata=metadata)
        )
        scene = plan.scene_requests[0]
        evidence = {item.place_name: item for item in plan.place_evidence}["Harbor"]
        return plan.source_digest, scene.cache_key, evidence.source_ref_count, evidence.source_count

    original = plan_for(second_fingerprint)
    changed = plan_for("3" * 64)

    assert original[2] == 2
    assert original[3] == 2
    assert original[0] != changed[0]
    assert original[1] != changed[1]


def test_same_source_fingerprint_reuses_cache_across_distinct_source_ids() -> None:
    fingerprint = "a" * 64

    def plan_for(source_id: str, locator: str) -> tuple[str, str, str]:
        metadata = {
            "source_fingerprints_v1": json.dumps([fingerprint]),
            "scene_evidence_v1": json.dumps(
                [
                    {
                        "name": "园林",
                        "source_refs": [f"text://{source_id}#paragraph/{locator}"],
                        "confidence": 0.83,
                        "cooccurring_candidates": [{"kind": "object", "label": "石碑"}],
                    }
                ],
                ensure_ascii=False,
            ),
        }
        plan = _plan_book_scene_assets(
            package_from_book(source_id, ("园林",), compiler_metadata=metadata)
        )
        scene = plan.scene_requests[0]
        return scene.stable_key, scene.cache_key, scene.source_refs[0]

    first = plan_for("job-a", "7")
    same_bytes = plan_for("job-b", "7")
    different_locator = plan_for("job-c", "8")

    assert first[0] == same_bytes[0] == different_locator[0]
    assert first[1] == same_bytes[1]
    assert first[2] != same_bytes[2]
    assert first[1] != different_locator[1]
