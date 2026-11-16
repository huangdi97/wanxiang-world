"""Studio input mistakes must be typed refusals, never 500s.

Measured defect (2026-11-13): an empty source list, an unknown source profile and a
profile/kind mismatch each escaped as `500 Internal Server Error` with no structured
body, because `OneClickAuthoring` raised a bare `ValueError` from its input validation
(and the pipeline did the same for an unsupported source kind).

A malformed request is a client mistake, so every shape below must answer 4xx with a
typed `code` and a non-empty `details.product_state`.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app

HEADERS = {"X-Wanxiang-User": "studio"}
BOOK = (
    "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Garden in 1985.\n"
    "Alice walked from Garden to Harbor.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)


def _source(source_id: str, content: str = BOOK, **overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
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
    record.update(overrides)
    return record


def _one_click(job_id: str, sources: list[dict[str, object]], profile: str = "book") -> Any:
    client: Any = TestClient(create_app(build_reference_runtime()))
    return client.post(
        "/studio/one-click",
        headers=HEADERS,
        json={
            "job_id": job_id,
            "profile": profile,
            "semantic_provider": "local",
            "sources": sources,
        },
    )


def _refusal(
    job_id: str, sources: list[dict[str, object]], profile: str = "book"
) -> tuple[str, str]:
    """Answer one input mistake and return (code, product_state)."""

    response = _one_click(job_id, sources, profile)
    assert response.status_code < 500, f"{job_id} answered {response.status_code}"
    assert response.status_code == 422, response.text
    body = cast(dict[str, Any], response.json())
    raw_details = body.get("details")
    assert isinstance(raw_details, dict) and raw_details, f"no details: {body}"
    details = cast(dict[str, Any], raw_details)
    state = details.get("product_state")
    assert isinstance(state, str) and state, f"no product state: {body}"
    return cast(str, body["code"]), state


def test_empty_source_list_is_refused_with_a_state() -> None:
    code, state = _refusal("input_empty", [])
    assert code == "authoring_request_rejected"
    assert state == "REQUEST_REJECTED"


def test_unknown_source_profile_is_refused_with_a_state() -> None:
    code, state = _refusal("input_profile", [_source("a")], profile="nonsense")
    assert code == "authoring_request_rejected"
    assert state == "REQUEST_REJECTED"


def test_profile_kind_mismatch_is_refused_with_a_state() -> None:
    code, state = _refusal("input_kind", [_source("a", kind="video")])
    assert code == "authoring_request_rejected"
    assert state == "REQUEST_REJECTED"


def test_mixed_profile_needs_two_sources_and_says_so() -> None:
    code, state = _refusal("input_mixed", [_source("a")], profile="mixed")
    assert code == "authoring_request_rejected"
    assert state == "REQUEST_REJECTED"


def test_an_unknown_kind_is_claimed_by_the_asset_adapter_not_refused() -> None:
    """Measured: the asset adapter claims kinds the book/structured adapters do not.

    A mixed bundle containing a `video` source therefore compiles (201) with a
    capability diagnostic, so the pipeline's `unsupported source kind` guard is
    defensive. It is typed as `UnsupportedSource` anyway, so it can never surface as
    a 500 if that registry changes.
    """

    response = _one_click(
        "input_asset_kind",
        [_source("a"), _source("b", kind="video")],
        profile="mixed",
    )
    assert response.status_code == 201, response.text
    status = cast(dict[str, Any], cast(dict[str, Any], response.json())["status"])
    diagnostics = cast(list[str], status["diagnostics"])
    assert any("requires capability" in item for item in diagnostics), diagnostics


def test_malformed_structured_source_is_refused_with_a_state() -> None:
    code, state = _refusal(
        "input_malformed",
        [_source("a", "{not json", kind="json")],
        profile="structured",
    )
    assert code == "malformed_source_content"
    assert state == "SOURCE_MALFORMED"
