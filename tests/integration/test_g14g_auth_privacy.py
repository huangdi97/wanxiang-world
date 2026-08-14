"""G14G: authorization, rights, privacy & data-leak adversarial qualification.

- Guessed/cross-branch access does not leak another branch's content.
- Perspective filters prevent private knowledge leakage server-side (not UI).
- Revocation of rights/permissions invalidates future projection/export.
- Normal users cannot alter audit truth (append-only).
"""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.epistemic.components import belief_component
from wanxiang_substrate.gateway.gateway import (
    DigitalHumanGateway,
    GatewayRightsDenied,
    SpeechInput,
)
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService
from wanxiang_substrate.sources.errors import RightsDenied
from wanxiang_substrate.sources.fixture import approved_source, rejected_source
from wanxiang_substrate.sources.gate import SourceGate


def _state(branch_id: str = "b_g14g") -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("w_g14g"),
        branch_id=BranchId(branch_id),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


def _belief(belief_id: str, owner: str) -> EntityCreate:
    return EntityCreate(
        entity_id=EntityId(belief_id),
        entity_type="epistemic.belief",
        components=(
            belief_component(
                belief_id=EntityId(belief_id),
                actor_id=EntityId(owner),
                proposition=f"{owner} private thought",
                confidence=0.9,
                at_ticks=1,
            ),
        ),
    )


def _public(entity_id: str) -> EntityCreate:
    return EntityCreate(
        entity_id=EntityId(entity_id),
        entity_type="canon.thing",
        components=(
            ComponentData(
                component_id=ComponentId(f"cmp_{entity_id}"),
                component_type="note",
                schema_version=SchemaVersion(1),
                fields={"text": f"public {entity_id}"},
            ),
        ),
    )


def _project(state: InMemoryCanonicalState, actor: str) -> set[str]:
    snap = ProjectionService(state).compose(
        ProjectionRequest(session_id="s", actor_id=actor, branch_id=state.branch_id, mode="text")
    )
    return {i.entity_id for i in snap.items}


def test_cross_branch_guessed_access_does_not_leak() -> None:
    branch_a = _state("branch_a").apply(
        ProposedWorldDelta(operations=(_belief("b_a1", "alice"), _public("pub_a")))
    )
    branch_b = _state("branch_b").apply(
        ProposedWorldDelta(operations=(_belief("b_b1", "bob"), _public("pub_b")))
    )
    # Projecting branch A as bob exposes only branch A's public content, never
    # branch B, and never alice's private belief (no cross-branch leakage).
    ids = _project(branch_a, "bob")
    assert "pub_a" in ids
    assert "b_a1" not in ids
    assert "pub_b" not in ids
    # Branch B is independently projectable with its own content.
    assert "pub_b" in _project(branch_b, "alice")


def test_perspective_filters_prevent_knowledge_leakage() -> None:
    state = _state().apply(
        ProposedWorldDelta(operations=(_belief("b_1", "alice"), _public("pub_1")))
    )
    # Alice sees her own belief; bob does not (server-enforced, not UI hiding).
    assert "b_1" in _project(state, "alice")
    assert "b_1" not in _project(state, "bob")
    assert "pub_1" in _project(state, "bob")
    # Debug mode requires explicit privilege (admin); a normal user is denied.
    from wanxiang_substrate.projection.errors import UnauthorizedProjection

    with pytest.raises(UnauthorizedProjection):
        ProjectionService(state).compose(
            ProjectionRequest(
                session_id="s", actor_id="bob", branch_id=BranchId("b_g14g"), mode="debug"
            )
        )


def test_revocation_invalidates_future_export() -> None:
    gateway = DigitalHumanGateway()
    gateway.grant("alice", ("tts", "lipsync"))
    speech = SpeechInput(speech_id="s1", speaker="alice", text="hello")
    assert {o.kind for o in gateway.generate(speech, outputs=("tts", "lipsync"))} == {
        "tts",
        "lipsync",
    }
    # Revocation (permission removed): future generation is denied.
    gateway.grant("alice", ())
    with pytest.raises(GatewayRightsDenied):
        gateway.generate(speech, outputs=("tts",))


def test_revocation_invalidates_future_source_compilation() -> None:
    gate = SourceGate()
    approved = approved_source()
    assert gate.decide(approved).ok is True
    # Revoke rights: the same content is no longer canonical-eligible.
    from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord

    revoked = SourceRecord(
        source_id=approved.source_id,
        kind=approved.kind,
        content_hash=approved.content_hash,
        content_ref=approved.content_ref,
        stage="E3",
        rights=RightsEnvelope(owner="town-archive", usage="canonical", approved=False),
        payload=approved.payload,
        provenance=approved.provenance,
    )
    assert gate.decide(revoked).ok is False
    with pytest.raises(RightsDenied):
        gate.require_compile(revoked)


def test_normal_user_cannot_alter_audit_truth() -> None:
    from wanxiang_substrate.sources.registry import SourceRegistry

    registry = SourceRegistry()
    registry.register(approved_source())
    before = registry.audit_history("src_charter")
    assert len(before) >= 1
    # Audit/history is append-only: there is no mutation or clear API for a
    # normal user, and the accepted-path audit records live in append-only stores.
    for name in ("clear", "delete", "mutate", "rewrite", "reset"):
        assert not hasattr(registry, name), f"audit store must not expose {name}"
    # Registering another review only appends; history grows monotonically.
    registry.register(rejected_source())
    after = registry.audit_history("src_charter")
    assert len(after) >= len(before)
    assert before == after[: len(before)]
