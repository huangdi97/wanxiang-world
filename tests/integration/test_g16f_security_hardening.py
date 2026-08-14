"""G16F: production security hardening, authn/authz, rate limits & supply chain.

- Abusive request profile is bounded (API rate limit -> 429).
- Oversized payload rejected (413).
- Unauthorized actions denied server-side (projection admin gate, gateway rights).
- SBOM inventory exists; no secrets baked into artifacts.
"""

from __future__ import annotations

import pathlib
from typing import Any

import pytest
from scripts.architecture_check import ROOT, scan_secrets


def _client(persist_db_path: pathlib.Path) -> tuple[Any, Any]:
    from fastapi.testclient import TestClient
    from tests.conftest import upgrade_db
    from wanxiang_api.app import build_runtime, create_app

    upgrade_db(persist_db_path)
    runtime = build_runtime(f"sqlite:///{persist_db_path.as_posix()}")
    app = create_app(runtime)
    return TestClient(app), runtime


def test_abusive_request_profile_bounded(persist_db_path: pathlib.Path) -> None:
    client, _runtime = _client(persist_db_path)
    with client:
        world = client.post("/worlds", json={"instance_id": "wld_rate"}).json()
        instance = world["instance_id"]
        branch = world["root_branch_id"]
        body = {
            "branch_id": branch,
            "expected_revision": 0,
            "action_type": "create_entity",
            "payload": {"entity_id": "a", "count": 1},
        }
        statuses: list[int] = []
        for _ in range(12):
            r = client.post(f"/worlds/{instance}/actions", json=body)
            statuses.append(r.status_code)
        # The first burst is served; the abusive profile is bounded (429).
        assert statuses[-1] == 429
        assert 429 in statuses


def test_oversized_payload_rejected(persist_db_path: pathlib.Path) -> None:
    client, _runtime = _client(persist_db_path)
    with client:
        world = client.post("/worlds", json={"instance_id": "wld_big"}).json()
        instance = world["instance_id"]
        branch = world["root_branch_id"]
        big = "x" * (64 * 1024 + 10)
        r = client.post(
            f"/worlds/{instance}/actions",
            json={
                "branch_id": branch,
                "expected_revision": 0,
                "action_type": "create_entity",
                "payload": {"entity_id": big, "count": 1},
            },
        )
        assert r.status_code == 413
        assert r.json()["code"] == "payload_too_large"


def test_unauthorized_actions_denied_server_side() -> None:
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import BranchId, WorldInstanceId
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.state import InMemoryCanonicalState
    from wanxiang_substrate.gateway.gateway import (
        DigitalHumanGateway,
        GatewayRightsDenied,
        SpeechInput,
    )
    from wanxiang_substrate.projection.errors import UnauthorizedProjection
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    state = InMemoryCanonicalState(
        instance_id=WorldInstanceId("w"),
        branch_id=BranchId("b"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    # Debug projection requires explicit admin (server-enforced, not UI hiding).
    with pytest.raises(UnauthorizedProjection):
        ProjectionService(state, admin=False).compose(
            ProjectionRequest(session_id="s", actor_id="a", branch_id=BranchId("b"), mode="debug")
        )
    # Media generation without permission is denied server-side.
    gateway = DigitalHumanGateway()
    gateway.grant("alice", ())
    with pytest.raises(GatewayRightsDenied):
        gateway.generate(SpeechInput(speech_id="s1", speaker="alice", text="hi"), outputs=("tts",))


def test_sbom_exists_and_no_secrets_in_artifacts() -> None:
    import json
    from pathlib import Path

    sbom = Path("artifacts/sbom.json")
    assert sbom.exists()
    payload = json.loads(sbom.read_text(encoding="utf-8"))
    assert len(payload["python"]) > 0 and len(payload["javascript"]) > 0
    assert scan_secrets(ROOT) == []
    # Secrets are not baked into the SBOM inventory.
    text = sbom.read_text(encoding="utf-8")
    assert "sk-" not in text and "secret" not in text.lower() or "secret" in payload["note"]
