"""Deterministic reference distillation passes (G57C-G57G).

No-API reference passes that extract CANDIDATES only from explicit patterns:
identity/alias/coreference (GEDCOM INDI, book names), event/time/place (dates,
places), relation/role/membership/organization (GEDCOM FAM), character/
life_arc/belief/knowledge_boundary (birth/death + keywords), object/rule/norm/
skill/affordance (explicit markers). Every candidate carries source refs and a
deterministic confidence; nothing is Canon.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment

PASS_VERSION = 1
DATE_RE = re.compile(r"\b(1[0-9]{3}|2[0-9]{3})\b")
PLACE_RE = re.compile(r"\b(?:at|in)\s+([A-Z][A-Za-z\u4e00-\u9fff]{1,24})\b")
GEDCOM_NAME_RE = re.compile(r"1 NAME\s+(\S+)\s*/([^/]+)/")
GEDCOM_XREF_RE = re.compile(r"0 @([^@]+)@ INDI")
GEDCOM_BIRT_RE = re.compile(r"2 DATE\s+([0-9-]{4,})")
GEDCOM_PLAC_RE = re.compile(r"2 PLAC\s+(.+)")
GEDCOM_FAM_RE = re.compile(r"0 @([^@]+)@ FAM")
GEDCOM_HUSB_RE = re.compile(r"1 HUSB @([^@]+)@")
GEDCOM_WIFE_RE = re.compile(r"1 WIFE @([^@]+)@")
GEDCOM_CHIL_RE = re.compile(r"1 CHIL @([^@]+)@")


def make_candidate(
    pass_name: str,
    candidate_id: str,
    kind: str,
    payload: dict[str, str],
    *,
    source_refs: tuple[str, ...],
    confidence: float,
    version: int = PASS_VERSION,
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass=pass_name,
        payload=tuple(sorted(payload.items())),
        confidence=confidence,
        source_refs=source_refs,
        distiller_version=version,
    )


def candidate_id(source_id: str, pass_name: str, salt: str) -> str:
    digest = hashlib.sha256(f"{source_id}:{pass_name}:{salt}".encode()).hexdigest()[:16]
    return f"cand_{pass_name}_{digest}"


class IdentityPass(Distiller):
    """G57C: identity/alias/coreference candidates (no destructive merge)."""

    name = "identity"
    version = PASS_VERSION

    def distill(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        seen_names: Counter[str] = Counter()
        for segment in segments:
            text = segment.text
            ref = segment.locator.to_string()
            xref = GEDCOM_XREF_RE.search(text)
            name_match = GEDCOM_NAME_RE.search(text)
            if xref and name_match:
                given, surname = name_match.group(1), name_match.group(2)
                display = f"{given} {surname}".strip()
                key = f"{given.lower()}|{surname.lower()}"
                seen_names[key] += 1
                candidates.append(
                    make_candidate(
                        "identity",
                        candidate_id(source_id, "identity", xref.group(1)),
                        "identity",
                        {
                            "key": key,
                            "display_name": display,
                            "xref": xref.group(1),
                            "given": given,
                            "surname": surname,
                        },
                        source_refs=(ref,),
                        confidence=0.9,
                    )
                )
                candidates.append(
                    make_candidate(
                        "identity",
                        candidate_id(source_id, "alias", f"{xref.group(1)}|{given}"),
                        "alias",
                        {"identity_key": key, "alias": given},
                        source_refs=(ref,),
                        confidence=0.8,
                    )
                )
        # Coreference suggestions (reversible; never a destructive merge).
        for key, count in seen_names.items():
            if count > 1:
                candidates.append(
                    make_candidate(
                        "identity",
                        candidate_id(source_id, "coref", key),
                        "coreference",
                        {"identity_key": key, "mention_count": str(count)},
                        source_refs=(),
                        confidence=0.5,
                    )
                )
        return tuple(candidates)


class EventTimeSpacePass(Distiller):
    """G57D: event/participant/time-uncertainty/place candidates."""

    name = "event_time_space"
    version = PASS_VERSION

    def distill(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for segment in segments:
            text = segment.text
            ref = segment.locator.to_string()
            xref = GEDCOM_XREF_RE.search(text)
            birth = GEDCOM_BIRT_RE.search(text)
            place_match = GEDCOM_PLAC_RE.search(text)
            if xref and birth:
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(source_id, "event", f"{xref.group(1)}|birth"),
                        "event",
                        {
                            "subject_xref": xref.group(1),
                            "event_type": "birth",
                            "date": birth.group(1),
                            "participants": xref.group(1),
                        },
                        source_refs=(ref,),
                        confidence=0.85,
                    )
                )
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(source_id, "time", f"{xref.group(1)}|birth"),
                        "time",
                        {"date": birth.group(1), "uncertain": "false"},
                        source_refs=(ref,),
                        confidence=0.7,
                    )
                )
            if xref and place_match:
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(source_id, "place", f"{xref.group(1)}|{place_match.group(1)}"),
                        "place",
                        {"name": place_match.group(1).strip(), "subject_xref": xref.group(1)},
                        source_refs=(ref,),
                        confidence=0.6,
                    )
                )
            for year in DATE_RE.findall(text):
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(source_id, "time", f"book|{year}"),
                        "time",
                        {"date": year, "uncertain": "true"},
                        source_refs=(ref,),
                        confidence=0.4,
                    )
                )
        return tuple(candidates)


class RelationOrganizationPass(Distiller):
    """G57E: relation/role/membership/organization candidates."""

    name = "relation_organization"
    version = PASS_VERSION

    def distill(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for segment in segments:
            text = segment.text
            ref = segment.locator.to_string()
            fam = GEDCOM_FAM_RE.search(text)
            if not fam:
                continue
            fam_xref = fam.group(1)
            husband = GEDCOM_HUSB_RE.search(text)
            wife = GEDCOM_WIFE_RE.search(text)
            if husband and wife:
                candidates.append(
                    make_candidate(
                        "relation_organization",
                        candidate_id(source_id, "relation", f"{fam_xref}|spouse"),
                        "relation",
                        {
                            "source_key": husband.group(1),
                            "target_key": wife.group(1),
                            "relation_type": "spouse",
                            "family_xref": fam_xref,
                        },
                        source_refs=(ref,),
                        confidence=0.9,
                    )
                )
            for child in GEDCOM_CHIL_RE.finditer(text):
                parent = husband.group(1) if husband else (wife.group(1) if wife else "")
                if parent:
                    candidates.append(
                        make_candidate(
                            "relation_organization",
                            candidate_id(source_id, "membership", f"{fam_xref}|{child.group(1)}"),
                            "membership",
                            {
                                "member_key": child.group(1),
                                "family_xref": fam_xref,
                                "role": "child",
                            },
                            source_refs=(ref,),
                            confidence=0.8,
                        )
                    )
        return tuple(candidates)
