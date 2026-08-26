"""G13D: false-completion, placeholder-guard, surface-truth and schema-drift tests.

- The production placeholder scanner and dead-code scanner must be clean.
- The architecture placeholder guard must actually catch EVERY marker pattern
  (regression for the `next(...)` first-pattern-only bug found in this Goal).
- The API vertical slice must consume real server state (not canned data).
- The TS SDK OpenAPI contract must match the server, and manual edits to the
  generated contract must be detected.
"""

from __future__ import annotations  # noqa: I001

import json
import pathlib
import uuid
import contextlib
from collections.abc import Iterator
from typing import Any

import pytest
from scripts.architecture_check import scan_placeholders
from scripts.export_openapi import build_contract
from scripts.false_completion_scan import (
    dead_code_scan,
    empty_body_scan,
    placeholder_scan,
    static_success_scan,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ARCH_TMP = ROOT / "tests" / "_arch_tmp"
CONTRACT = ROOT / "packages" / "sdk_ts" / "src" / "openapi-contract.json"


@pytest.fixture
def arch_tmp() -> Iterator[pathlib.Path]:
    ARCH_TMP.mkdir(parents=True, exist_ok=True)
    d = ARCH_TMP / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            with contextlib.suppress(OSError):
                p.unlink()
    with contextlib.suppress(OSError):
        d.rmdir()


def test_production_placeholder_scan_clean() -> None:
    assert placeholder_scan(ROOT) == []


def test_no_dead_production_modules() -> None:
    assert dead_code_scan(ROOT) == []


def test_no_empty_body_production_modules() -> None:
    """G29F: no pass-only production function/class bodies beyond documented markers."""
    assert empty_body_scan(ROOT) == []


def test_static_success_candidates_are_documented_only() -> None:
    """G29F: every static-success path is pinned and documented (no new ones)."""
    findings = static_success_scan(ROOT)
    documented = {
        ("packages/application/src/wanxiang_application/environment.py", "close"),
        ("packages/research/src/wanxiang_research/digital_human.py", "interrupt"),
        # G32A structural guard: world policy holds no platform mutation handle.
        (
            "packages/substrate/src/wanxiang_substrate/evolution/policy_stack.py",
            "assert_world_cannot_mutate_platform",
        ),
        # G55C/G55D/G55E/G55F stateless reference adapters: resume() is a
        # documented no-op (idempotent); progress is owned by JobService.
        ("packages/substrate/src/wanxiang_substrate/sources/adapter.py", "resume"),
        ("packages/substrate/src/wanxiang_substrate/sources/book.py", "resume"),
        ("packages/substrate/src/wanxiang_substrate/sources/structured.py", "resume"),
        ("packages/substrate/src/wanxiang_substrate/sources/asset.py", "resume"),
        # Actor cognition records expose an immutable false predicate so the
        # projection can never be mistaken for canonical World Truth.
        ("packages/substrate/src/wanxiang_substrate/epistemic/model.py", "is_world_truth"),
        (
            "packages/substrate/src/wanxiang_substrate/epistemic/belief_revision.py",
            "is_world_truth",
        ),
    }
    actual = {(f["file"], f["text"].removeprefix("def ")) for f in findings}
    assert actual == documented, f"unexpected static-success paths: {actual - documented}"


def test_placeholder_guard_catches_every_marker(arch_tmp: pathlib.Path) -> None:
    """Regression: the guard previously only checked the first pattern (TODO)."""
    markers = ["TODO", "FIXME", "XXX", "NotImplemented", "placeholder", "stub", "mock-only"]
    p = arch_tmp / "packages" / "domain" / "src" / "wanxiang_domain" / "evil.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(f"# {m} marker" for m in markers) + "\n", encoding="utf-8")
    findings = scan_placeholders(arch_tmp)
    seen = {f.line for f in findings}
    assert len(findings) == len(markers), f"expected {len(markers)} findings, got {len(findings)}"
    assert seen == set(range(1, len(markers) + 1))


def test_placeholder_guard_allows_return_notimplemented(arch_tmp: pathlib.Path) -> None:
    p = arch_tmp / "packages" / "domain" / "src" / "wanxiang_domain" / "cmp.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "def __lt__(self, other):\n    if not isinstance(other, int):\n        return NotImplemented\n",  # noqa: E501
        encoding="utf-8",
    )
    assert scan_placeholders(arch_tmp) == []


def test_e2e_smoke_server_truth_not_canned(persist_db_path: pathlib.Path) -> None:
    """The API vertical slice must reflect committed canonical state, never canned JSON."""
    from typing import cast

    from fastapi.testclient import TestClient
    from tests.conftest import upgrade_db
    from wanxiang_api.app import build_runtime, create_app
    from wanxiang_api.routes import reset_action_rate_limiter

    upgrade_db(persist_db_path)
    reset_action_rate_limiter()  # isolate this test from shared rate-limit state
    runtime = build_runtime(f"sqlite:///{persist_db_path.as_posix()}")
    app = create_app(runtime)
    client: Any = TestClient(app)
    with client:
        world = cast(
            dict[str, Any], client.post("/worlds", json={"instance_id": "wld_g13d"}).json()
        )
        instance: str = world["instance_id"]
        branch: str = world["root_branch_id"]
        resp = client.post(
            f"/worlds/{instance}/actions",
            json={
                "branch_id": branch,
                "expected_revision": 0,
                "action_type": "create_entity",
                "payload": {"entity_id": "ent_g13d", "count": 7},
            },
        )
        assert resp.status_code == 200
        action = cast(dict[str, Any], resp.json())
        assert action["event"] is not None
        state = cast(
            dict[str, Any],
            client.get(f"/worlds/{instance}/state", params={"branch_id": branch}).json(),
        )
        # The projected state must contain the committed entity: server truth, not canned.
        prim = cast(dict[str, Any], state["state"])
        entities = cast(list[dict[str, Any]], prim["entities"])
        assert any(str(e.get("id")) == "ent_g13d" for e in entities)


def test_openapi_contract_matches_server() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    from wanxiang_api.app import create_app

    fresh = build_contract(create_app())
    committed: dict[str, Any] = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert fresh == committed, (
        "openapi-contract.json drifted from the server; rerun scripts/export_openapi.py"
    )


def test_openapi_contract_detects_manual_edit() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    from wanxiang_api.app import create_app

    fresh = build_contract(create_app())
    tampered: dict[str, Any] = json.loads(CONTRACT.read_text(encoding="utf-8"))
    tampered["paths"]["/fabricated"] = {"get": {"operationId": "fake_operation"}}
    assert fresh != tampered, "a manually edited client must be detected as drift"
