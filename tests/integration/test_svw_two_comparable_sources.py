"""A bundle of two comparable-weight sources compiles, and its disagreements show.

Measured 2026-11-04: a rich book plus short pasted notes is refused (`422`,
`COMPLETION_REQUIRED`), which was read as "no two-source bundle can compile". The
refusal is a **conflict** refusal, not a coverage one — the draft covers 0.833 of
the required capabilities and carries four unresolved conflicts, because the notes
repeat semantic keys (Alice, Garden, Harbor, the rule) with different payloads
while the same text as one source compiles with zero conflicts.

This spec pins the shape that does compile — two sources of comparable weight —
and the two surfaces where a cross-source disagreement is visible: the marked
consumer atlas, and the Studio job/draft status when the conflict blocks compile.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app

HEADERS = {"X-Wanxiang-User": "studio"}

CHAPTER_A = (
    "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Garden in 1985.\n"
    "Alice visited Harbor.\n"
    "Alice walked from Garden to Harbor.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)
# Short notes: same semantic keys as the chapter, different payloads.
SHORT_NOTES = (
    "# Travel notes\nCharacter: Alice\n"
    "Alice visited Garden.\n"
    "Alice walked from Harbor to Garden.\n"
    "rule: visitors register\n"
)
# Comparable weight: two people, two places, a walk, a relation, a rule of its own.
CHAPTER_B = (
    "# Chapter B\nCharacter: Carol\nCharacter: Dave\n"
    "Carol arrived in Market in 1990.\n"
    "Carol visited Station.\n"
    "Carol walked from Market to Station.\n"
    "relationship: Carol -> Dave\nrule: traders declare goods\n"
)
# Comparable weight, but it disagrees with the chapter about Garden/Harbor.
CHAPTER_B_REVERSED = (
    "# Chapter B\nCharacter: Carol\nCharacter: Dave\n"
    "Carol arrived in Market in 1990.\n"
    "Alice walked from Harbor to Garden.\n"
    "Carol walked from Market to Station.\n"
    "relationship: Carol -> Dave\nrule: traders declare goods\n"
)


def _source(source_id: str, content: str) -> dict[str, object]:
    return {
        "source_id": source_id,
        "kind": "text",
        "content": content,
        "stage": "E3",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
    }


def _client() -> Any:
    """A fresh app per check: the source registry is content-addressed per runtime."""

    return TestClient(create_app(build_reference_runtime()))


def _bundle(client: Any, job_id: str, sources: list[dict[str, object]]) -> Any:
    return client.post(
        "/studio/one-click",
        headers=HEADERS,
        json={
            "job_id": job_id,
            "profile": "book",
            "semantic_provider": "local",
            "sources": sources,
        },
    )


def _draft(client: Any, job_id: str) -> dict[str, Any]:
    response = client.get(f"/studio/jobs/{job_id}/draft", headers=HEADERS)
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json()["draft"])


def test_two_comparable_sources_compile_and_publish_one_world() -> None:
    client = _client()
    created = _bundle(
        client,
        "svw_pair",
        [_source("a", CHAPTER_A), _source("b", CHAPTER_B)],
    )
    assert created.status_code == 201, created.text
    body = cast(dict[str, Any], created.json())
    assert body["publishable"] is True
    assert body["publish_reasons"] == []

    draft = _draft(client, "svw_pair")
    assert draft["status"] == "READY_TO_COMPILE"
    assert draft["unresolved_conflicts"] == []
    # Both sources' places survive into the one world.
    assert set(cast(list[str], draft["places"])) == {"Garden", "Harbor", "Market", "Station"}
    assert draft["source_refs"] == ["a", "b"]

    published = client.post("/studio/jobs/svw_pair/publish", headers=HEADERS)
    assert published.status_code == 200, published.text
    assert cast(dict[str, Any], published.json())["status"]["stage"] == "published"


def test_cross_source_disagreement_is_marked_on_the_consumer_atlas() -> None:
    """The disagreement is carried as marked data, it does not silently vanish."""

    client = _client()
    created = _bundle(
        client,
        "svw_pair_conflict",
        [_source("a", CHAPTER_A), _source("b", CHAPTER_B_REVERSED)],
    )
    assert created.status_code == 201, created.text
    draft = _draft(client, "svw_pair_conflict")
    assert draft["status"] == "READY_TO_COMPILE"

    profile = client.post(
        "/studio/jobs/svw_pair_conflict/playable-profile",
        headers=HEADERS,
        json={"owner_id": "studio", "visibility": "private", "display_name": "Pair"},
    )
    assert profile.status_code == 200, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])
    detail = client.get(f"/experience/player/worlds/{profile_id}", headers=HEADERS)
    assert detail.status_code == 200, detail.text
    topology = cast(list[dict[str, Any]], detail.json()["world"]["visual"]["topology"])
    marked = {(item["from"], item["to"]) for item in topology if item["conflicting"]}
    assert ("Garden", "Harbor") in marked
    assert ("Harbor", "Garden") in marked
    disputed = [item for item in topology if {item["from"], item["to"]} == {"Garden", "Harbor"}]
    assert disputed and all(item["conflicting"] for item in disputed)


def test_blocking_cross_source_conflict_is_visible_on_the_studio_surfaces() -> None:
    client = _client()
    refused = _bundle(
        client,
        "svw_pair_refused",
        [_source("a", CHAPTER_A), _source("b", SHORT_NOTES)],
    )
    assert refused.status_code == 422, refused.text
    details = cast(dict[str, Any], cast(dict[str, Any], refused.json())["details"])
    assert isinstance(details.get("product_state"), str) and details["product_state"]

    status = client.get("/studio/jobs/svw_pair_refused", headers=HEADERS)
    assert status.status_code == 200, status.text
    conflict_count = cast(int, status.json()["conflict_count"])
    assert conflict_count >= 1, status.text
    assert status.json()["product_state"] == "REVIEW_REQUIRED"

    draft = _draft(client, "svw_pair_refused")
    assert draft["status"] == "COMPLETION_REQUIRED"
    assert len(cast(list[str], draft["unresolved_conflicts"])) == conflict_count
    # The refusal is about the conflict, not about missing coverage.
    assert cast(float, draft["coverage"]) > 0.0


def test_the_same_text_as_one_source_has_no_cross_source_conflict() -> None:
    """Control: the conflict above exists only because two sources disagree."""

    client = _client()
    created = _bundle(
        client,
        "svw_pair_joined",
        [_source("a", CHAPTER_A + SHORT_NOTES)],
    )
    assert created.status_code == 201, created.text
    draft = _draft(client, "svw_pair_joined")
    assert draft["status"] == "READY_TO_COMPILE"
    assert draft["unresolved_conflicts"] == []
