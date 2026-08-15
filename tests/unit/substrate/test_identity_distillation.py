"""G35C: source-derived identity & alias distillation (mechanism; synthetic corpus).

Tests use an explicitly-labeled SYNTHETIC fixture ONLY - never real
《红楼梦》 canon. Real full-text acquisition remains EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.errors import SourceNotApproved
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.identity import (
    AliasClaim,
    IdentityCandidate,
    IdentityDistiller,
    IdentityReviewGate,
    identity_to_claim,
)
from wanxiang_substrate.sources.locator import SourceLocator, source_slice
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = "第一回\n林黛玉进贾府。黛玉与宝玉相见。\n第二回\n紫鹃服侍黛玉。鹃儿称颦颦为姑娘。\n"

ALIAS_TO_IDENTITY = {
    "林黛玉": "林黛玉",
    "黛玉": "林黛玉",
    "颦颦": "林黛玉",
    "贾宝玉": "贾宝玉",
    "宝玉": "贾宝玉",
    "紫鹃": "紫鹃",
    "鹃儿": "紫鹃",
}

KNOWN_ALIASES = frozenset(ALIAS_TO_IDENTITY)


def extract_known(text: str) -> tuple[str, ...]:
    return tuple(alias for alias in KNOWN_ALIASES if alias in text)


def resolve_alias(mention: str) -> str | None:
    return ALIAS_TO_IDENTITY.get(mention)


def distiller() -> IdentityDistiller:
    return IdentityDistiller(
        extract_mentions=extract_known,
        resolve_identity=resolve_alias,
    )


@pytest.mark.unit
def test_alias_resolves_to_canonical_identity_with_evidence() -> None:
    candidates = distiller().distill("src_rc_synth", SYNTHETIC)
    by_key = {c.identity_key: c for c in candidates}
    lin = by_key["林黛玉"]
    assert lin.display_name == "林黛玉"
    alias_names = {claim.alias for claim in lin.aliases}
    assert alias_names == {"林黛玉", "黛玉", "颦颦"}
    daiyu = next(claim for claim in lin.aliases if claim.alias == "黛玉")
    assert daiyu.has_evidence
    locator = daiyu.locators[0]
    # Evidence back-links to the exact source slice mentioning the alias.
    assert "黛玉" in source_slice(SYNTHETIC, locator)


@pytest.mark.unit
def test_distillation_is_deterministic() -> None:
    first = distiller().distill("src_rc_synth", SYNTHETIC)
    second = distiller().distill("src_rc_synth", SYNTHETIC)
    assert first == second
    assert [c.identity_key for c in first] == sorted({c.identity_key for c in first})


@pytest.mark.unit
def test_same_name_different_identities_never_merged() -> None:
    loc = SourceLocator(
        source_id="src",
        chapter="第一回",
        segment_id="s",
        start_offset=0,
        end_offset=1,
        locator="src#第一回:0-1",
    )
    candidates = (
        IdentityCandidate(
            candidate_id="ident_0001",
            identity_key="林黛玉",
            display_name="林黛玉",
            aliases=(AliasClaim(alias="黛玉", identity_key="林黛玉", locators=(loc,)),),
        ),
        IdentityCandidate(
            candidate_id="ident_0002",
            identity_key="李黛玉",
            display_name="李黛玉",
            aliases=(AliasClaim(alias="黛玉", identity_key="李黛玉", locators=(loc,)),),
        ),
    )
    assert {c.identity_key for c in candidates} == {"林黛玉", "李黛玉"}
    assert candidates[0].candidate_id != candidates[1].candidate_id


@pytest.mark.unit
def test_no_evidence_candidate_does_not_enter_canon() -> None:
    gate = IdentityReviewGate()
    no_aliases = IdentityCandidate(
        candidate_id="ident_0001",
        identity_key="贾雨村",
        display_name="贾雨村",
        aliases=(),
    )
    decision = gate.review(no_aliases, source_text=SYNTHETIC, reviewer="human")
    assert not decision.approved
    assert "evidence" in decision.reason
    # An alias whose locator cannot resolve is also rejected (rule gate).
    dangling = SourceLocator(
        source_id="src",
        chapter="第二回",
        segment_id="d",
        start_offset=100,
        end_offset=101,
        locator="src#第二回:100-101",
    )
    bad = IdentityCandidate(
        candidate_id="ident_0002",
        identity_key="紫鹃",
        display_name="紫鹃",
        aliases=(AliasClaim(alias="鹃儿", identity_key="紫鹃", locators=(dangling,)),),
    )
    decision = gate.review(bad, source_text=SYNTHETIC, reviewer="human")
    assert not decision.approved
    assert "does not resolve" in decision.reason


@pytest.mark.unit
def test_review_gate_requires_authorized_reviewer() -> None:
    candidates = distiller().distill("src_rc_synth", SYNTHETIC)
    gate = IdentityReviewGate()
    decision = gate.review(candidates[0], source_text=SYNTHETIC, reviewer="system")
    assert not decision.approved
    assert "not authorized" in decision.reason


@pytest.mark.unit
def test_approved_identity_becomes_eligible_and_converts_to_claim() -> None:
    candidates = distiller().distill("src_rc_synth", SYNTHETIC)
    lin = next(c for c in candidates if c.identity_key == "林黛玉")
    gate = IdentityReviewGate()
    decision = gate.review(lin, source_text=SYNTHETIC, reviewer="human")
    assert decision.approved
    eligible = lin.with_status("eligible")
    assert eligible.status == "eligible"
    claim = identity_to_claim(eligible)
    assert claim.status == "eligible"
    assert claim.evidence_links
    assert all(link.role == "supports" for link in claim.evidence_links)
    assert claim.claim_id.startswith("identity:")


@pytest.mark.unit
def test_distillation_composes_with_source_gate() -> None:
    rights = RightsEnvelope(owner="fixture", usage="corpus:test", approved=True, reviewer="system")
    record = SourceRecord(
        source_id="src_rc_synth",
        kind="text",
        content_hash=payload_hash(SYNTHETIC),
        content_ref="fixture://synthetic",
        stage="E3",
        rights=rights,
        payload=SYNTHETIC,
    )
    SourceGate().require_compile(record)  # approved source passes the gate
    candidates = distiller().distill(record.source_id, record.payload)
    assert candidates
    # A rejected (non-eligible) source must NOT feed canonical compilation.
    rejected = SourceRecord(
        source_id="src_bad",
        kind="text",
        content_hash=payload_hash("x"),
        content_ref="fixture://bad",
        stage="E0",
        rights=rights,
    )
    with pytest.raises(SourceNotApproved):
        SourceGate().require_compile(rejected)
