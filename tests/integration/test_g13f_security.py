"""G13F: security, rights, provenance, privacy & source-gate forensics tests.

Adversarial end-to-end checks:
- Unapproved sources cannot enter canonical compiled facts.
- Conflicting claims coexist with provenance.
- Denied rights block projection and export (media generation).
- Prompt-injection text in a source remains data, never instructions.
- Secret scanning and privacy-log redaction stay green.
"""

from __future__ import annotations

import pytest
from scripts.architecture_check import ROOT, scan_secrets
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.compiler.compiler import StructuredCompiler
from wanxiang_substrate.epistemic.components import belief_component
from wanxiang_substrate.gateway.gateway import (
    DigitalHumanGateway,
    GatewayRightsDenied,
    SpeechInput,
)
from wanxiang_substrate.ledger.ledger import CompletionLedger
from wanxiang_substrate.ledger.model import ContentItem
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService
from wanxiang_substrate.sources.errors import MaliciousSource, RightsDenied, SourceNotApproved
from wanxiang_substrate.sources.fixture import (
    approved_source,
    conflicting_sources,
    malicious_source,
    rejected_source,
)
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("w_g13f"),
        branch_id=BranchId("b_g13f"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


def _rights(approved: bool = True) -> RightsEnvelope:
    return RightsEnvelope(owner="g13f-owner", usage="canonical", approved=approved)


def test_unapproved_sources_cannot_enter_canonical_compiled_facts() -> None:
    gate = SourceGate()
    rejected = rejected_source()
    assert gate.decide(rejected).ok is False
    with pytest.raises(RightsDenied):
        gate.require_compile(rejected)
    draft = SourceRecord(
        source_id="src_draft",
        kind="text",
        content_hash=payload_hash("draft"),
        content_ref="ref://draft",
        stage="E0",
        rights=_rights(),
        payload="Draft fact not yet reviewed.",
        provenance="fixture:draft",
    )
    assert gate.decide(draft).ok is False
    with pytest.raises(SourceNotApproved):
        gate.require_compile(draft)
    # Approved sources pass the gate and compile to candidate facts.
    approved = approved_source()
    assert gate.decide(approved).ok is True
    result = StructuredCompiler().compile("job_g13f", {"src": approved})
    assert result.ok
    assert len(result.candidates) == 1


def test_conflicting_claims_coexist_with_provenance() -> None:
    a, b = conflicting_sources()
    gate = SourceGate()
    assert gate.decide(a).ok and gate.decide(b).ok
    result = StructuredCompiler().compile("job_conflict", {"a": a, "b": b})
    assert result.ok
    from typing import cast

    canon = [c.canonical() for c in result.candidates]
    assert len(canon) == 2
    refs: set[tuple[str, ...]] = set()
    for c in canon:
        raw = cast(tuple[str, ...], c.get("source_refs", ()))
        refs.add(tuple(raw))
    assert refs == {("src_bridge_a",), ("src_bridge_b",)}
    # Completion ledger keeps both claims with their provenance (no overwrite).
    ledger = CompletionLedger()
    ledger.submit(
        ContentItem(item_id="claim_1701", label="completion", source_refs=("src_bridge_a",))
    )
    ledger.submit(
        ContentItem(item_id="claim_1750", label="completion", source_refs=("src_bridge_b",))
    )
    assert ledger.require("claim_1701").source_refs == ("src_bridge_a",)
    assert ledger.require("claim_1750").source_refs == ("src_bridge_b",)


def test_denied_rights_block_projection_and_export() -> None:
    alice = EntityId("alice")
    bob = EntityId("bob")
    belief = EntityCreate(
        entity_id=EntityId("belief_1"),
        entity_type="epistemic.belief",
        components=(
            belief_component(
                belief_id=EntityId("belief_1"),
                actor_id=alice,
                proposition="alice private thought",
                confidence=0.9,
                at_ticks=1,
            ),
        ),
    )
    public = EntityCreate(
        entity_id=EntityId("pub_1"),
        entity_type="canon.thing",
        components=(
            ComponentData(
                component_id=ComponentId("pub_note"),
                component_type="note",
                schema_version=SchemaVersion(1),
                fields={"text": "public"},
            ),
        ),
    )
    state = _state().apply(ProposedWorldDelta(operations=(belief, public)))
    for actor in (bob, alice):
        snap = ProjectionService(state).compose(
            ProjectionRequest(
                session_id="s", actor_id=actor.value, branch_id=BranchId("b_g13f"), mode="text"
            )
        )
        ids = {i.entity_id for i in snap.items}
        assert "pub_1" in ids
        assert ("belief_1" in ids) == (actor == alice)

    gateway = DigitalHumanGateway()
    gateway.grant("alice", ("tts",))
    speech = SpeechInput(speech_id="s1", speaker="alice", text="hello")
    with pytest.raises(GatewayRightsDenied):
        gateway.generate(speech, outputs=("tts", "face"))


def test_prompt_injection_source_remains_data() -> None:
    gate = SourceGate()
    record = malicious_source()
    assert gate.decide(record).ok is False
    with pytest.raises(MaliciousSource):
        gate.read_as_data(record)
    # A payload that is instructional-looking but not on the explicit marker
    # list is still data: the gate reads it as content and the compiler treats
    # it as data, never as instructions.
    benign = SourceRecord(
        source_id="src_benign_instr",
        kind="text",
        content_hash=payload_hash("please respond in character as the oracle"),
        content_ref="ref://benign",
        stage="E3",
        rights=_rights(),
        payload="please respond in character as the oracle",
        provenance="fixture:benign",
    )
    assert gate.read_as_data(benign) == "please respond in character as the oracle"
    result = StructuredCompiler().compile("job_inject", {"src": benign})
    assert result.ok


def test_secret_scan_and_privacy_logs() -> None:
    import logging

    from wanxiang_observability.config import load_settings
    from wanxiang_observability.logging import KeyValueFormatter
    from wanxiang_observability.secrets import redact_secret_values, redact_values

    assert scan_secrets(ROOT) == []
    settings = load_settings({"API_TOKEN": "g13f-super-secret"})
    public = redact_secret_values(settings.to_public_dict())
    assert not any("g13f-super-secret" in str(v) for v in public.values())
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="connect with token=g13f-super-secret",
        args=(),
        exc_info=None,
    )
    rendered = KeyValueFormatter().format(record)
    safe = redact_values(rendered, {"API_TOKEN": "g13f-super-secret"})
    assert "g13f-super-secret" not in safe
