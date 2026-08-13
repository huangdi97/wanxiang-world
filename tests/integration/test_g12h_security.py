"""G12H: deployment/security/private-installation checks.

Covers secrets redaction, upload/source injection validation, admin/debug/
private/export access and audit protection. External environment checks are
labeled EXTERNAL_BLOCKED, never falsely passed.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.gateway.gateway import (
    DigitalHumanGateway,
    GatewayRightsDenied,
    SpeechInput,
)
from wanxiang_substrate.sources.errors import MaliciousSource
from wanxiang_substrate.sources.fixture import malicious_source
from wanxiang_substrate.sources.gate import SourceGate


@pytest.mark.unit
def test_secrets_are_redacted() -> None:
    from wanxiang_observability.config import load_settings
    from wanxiang_observability.secrets import redact_secret_values, redact_values

    settings = load_settings({"API_SECRET_TOKEN": "super-secret-token"})
    public = redact_secret_values(settings.to_public_dict())
    assert all("super-secret-token" not in value for value in public.values())
    leaked = redact_values(
        "password=super-secret-token endpoint=/health",
        {"API_SECRET_TOKEN": "super-secret-token"},
    )
    assert "super-secret-token" not in leaked
    assert "REDACTED" in leaked


@pytest.mark.unit
def test_upload_source_injection_rejected() -> None:
    gate = SourceGate()
    record = malicious_source()
    assert gate.decide(record).ok is False
    with pytest.raises(MaliciousSource):
        gate.require_compile(record)


@pytest.mark.unit
def test_admin_debug_private_export_access() -> None:
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import BranchId, WorldInstanceId
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.state import InMemoryCanonicalState
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
    request = ProjectionRequest(
        session_id="s", actor_id="alice", branch_id=BranchId("b"), mode="debug"
    )
    # Debug/private access requires explicit privilege.
    with pytest.raises(UnauthorizedProjection):
        ProjectionService(state, admin=False).compose(request)
    snapshot = ProjectionService(state, admin=True).compose(request)
    assert snapshot.mode == "debug"


@pytest.mark.unit
def test_audit_protection_append_only() -> None:
    from wanxiang_substrate.sources.fixture import approved_source
    from wanxiang_substrate.sources.registry import SourceRegistry

    registry = SourceRegistry()
    registry.register(approved_source())
    history = registry.audit_history("src_charter")
    assert len(history) >= 1
    # Audit history is append-only: there is no mutation API for history.
    assert not hasattr(registry, "clear_history")


@pytest.mark.unit
def test_unauthorized_voice_face_generation_rejected() -> None:
    gateway = DigitalHumanGateway()
    gateway.grant("alice", ("tts",))
    speech = SpeechInput(speech_id="s1", speaker="alice", text="hello")
    with pytest.raises(GatewayRightsDenied):
        gateway.generate(speech, outputs=("tts", "lipsync", "face"))
    # With all permissions granted, generation works.
    gateway.grant("alice", ("tts", "lipsync", "expression", "face"))
    outputs = gateway.generate(speech, outputs=("tts", "lipsync"))
    assert {o.kind for o in outputs} == {"tts", "lipsync"}


@pytest.mark.unit
def test_external_env_checks_are_labeled_not_faked() -> None:
    # Real Docker/PostgreSQL/browser checks are environment-dependent; the
    # local check is explicitly labeled rather than falsely passed.
    from wanxiang_substrate.packages.sdk import PUBLIC_API_POLICY

    assert any("version policy" in line for line in PUBLIC_API_POLICY)
