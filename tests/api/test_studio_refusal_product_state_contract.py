"""A refusal must always name a product state.

Measured defect (2026-11-04 handover, step 1): a two-source bundle whose sources
carry the same content was refused with `422 duplicate_source` and an **empty**
`details` object, so the client received no diagnosis at all, while an
under-covering bundle was refused with `details.product_state == "ZERO_COVERAGE"`.

The refusing path was `wanxiang_substrate.sources.errors.DuplicateSource`: it
declared no product state, and the API boundary forwarded `details` verbatim.
These specs pin both halves of the fix: the source taxonomy states every source
failure, and the API boundary names a state even for an error that declares none.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.errors import error_payload, product_state_for
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.sources.errors import (
    SourceError,
    SourceNotApproved,
    ZeroCoverage,
)

HEADERS = {"X-Wanxiang-User": "studio"}

BOOK = (
    "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Garden in 1985.\n"
    "Alice visited Harbor.\n"
    "Alice walked from Garden to Harbor.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)
NOTES = (
    "# Travel notes\nCharacter: Alice\n"
    "Alice visited Garden.\n"
    "Alice walked from Harbor to Garden.\n"
    "rule: visitors register\n"
)


def _client() -> Any:
    """A fresh app per check: the source registry is content-addressed per runtime."""

    return TestClient(create_app(build_reference_runtime()))


def _source(source_id: str, content: str, **overrides: object) -> dict[str, object]:
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


def _refusal_state(response: Any) -> tuple[str, str]:
    assert response.status_code == 422, response.text
    body = cast(dict[str, Any], response.json())
    raw_details = body.get("details")
    assert isinstance(raw_details, dict) and raw_details, f"no details: {body}"
    details = cast(dict[str, Any], raw_details)
    state = details.get("product_state")
    assert isinstance(state, str) and state, f"refusal names no product state: {body}"
    return cast(str, body.get("code")), state


def test_two_source_bundle_with_identical_content_is_refused_with_a_state() -> None:
    """The measured defect: this refusal used to arrive with `details == {}`."""

    client = _client()
    response = _bundle(
        client,
        "refusal_duplicate",
        [_source("a", BOOK), _source("b", BOOK)],
    )
    code, state = _refusal_state(response)
    assert code == "duplicate_source"
    assert state == "SOURCE_DUPLICATE"


def test_two_source_bundle_that_under_covers_keeps_its_zero_coverage_state() -> None:
    client = _client()
    response = _bundle(
        client,
        "refusal_coverage",
        [_source("book", BOOK), _source("notes", NOTES)],
    )
    code, state = _refusal_state(response)
    assert code == "contract_error"
    assert state == "ZERO_COVERAGE"


def test_refusal_that_declares_no_state_still_receives_one() -> None:
    """The boundary guarantee: a bare ContractError cannot reach a client unnamed."""

    client = _client()
    assert _bundle(client, "refusal_reuse", [_source("a", BOOK)]).status_code == 201
    response = _bundle(client, "refusal_reuse", [_source("b", NOTES)])
    code, state = _refusal_state(response)
    assert code == "contract_error"
    assert state == "REJECTED"


def test_oversized_payload_refusal_names_its_state() -> None:
    client = _client()
    response = client.post(
        "/worlds/missing/actions",
        headers=HEADERS,
        json={
            "command_id": "c1",
            "branch_id": "main",
            "expected_revision": 0,
            "action_type": "noop",
            "payload": {"blob": "x" * (70 * 1024)},
        },
    )
    assert response.status_code == 413, response.text
    body = cast(dict[str, Any], response.json())
    assert body["code"] == "payload_too_large"
    assert cast(dict[str, Any], body["details"])["product_state"] == "PAYLOAD_TOO_LARGE"


def _source_error_classes() -> list[type[SourceError]]:
    found: list[type[SourceError]] = []

    def walk(cls: type[SourceError]) -> None:
        for sub in cls.__subclasses__():
            found.append(sub)
            walk(sub)

    walk(SourceError)
    return found


def test_every_source_error_declares_a_product_state() -> None:
    classes = _source_error_classes()
    assert len(classes) >= 14, [cls.__name__ for cls in classes]
    missing = [
        cls.__name__
        for cls in classes
        if not isinstance(getattr(cls, "product_state", ""), str)
        or not getattr(cls, "product_state", "")
    ]
    assert missing == [], f"source errors without a product state: {missing}"


def test_boundary_names_a_state_and_never_overwrites_the_declared_one() -> None:
    declared = {"reason": "under coverage"}
    payload = error_payload(ContractError("bare refusal", details=dict(declared)))
    assert payload["details"] == {**declared, "product_state": "REJECTED"}
    covered = error_payload(ZeroCoverage("no candidates", details={"batches": "2"}))
    assert covered["details"]["product_state"] == "ZERO_COVERAGE"
    assert covered["details"]["batches"] == "2"
    assert product_state_for(SourceNotApproved("not approved")) == "RIGHTS_ACTION_REQUIRED"


def test_boundary_does_not_mutate_the_error_details() -> None:
    details: dict[str, Any] = {"reason": "under coverage"}
    error = ContractError("bare refusal", details=details)
    payload = error_payload(error)
    assert payload["details"] == {"reason": "under coverage", "product_state": "REJECTED"}
    assert details == {"reason": "under coverage"}, "details must not be mutated in place"
    assert error.details == {"reason": "under coverage"}
