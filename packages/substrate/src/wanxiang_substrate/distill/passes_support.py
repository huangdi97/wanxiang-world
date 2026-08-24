"""Shared deterministic patterns and candidate construction helpers."""

from __future__ import annotations

import hashlib
import re

from wanxiang_substrate.candidates.envelope import CandidateEnvelope

PASS_VERSION = 1
DATE_RE = re.compile(r"\b(1[0-9]{3}|2[0-9]{3})\b")
PLACE_RE = re.compile(r"\b(?:at|in)\s+([A-Z][A-Za-z\u4e00-\u9fff]{1,24})\b")
GEDCOM_NAME_RE = re.compile(r"1 NAME\s+(\S+)\s*/([^/]+)/")
GEDCOM_XREF_RE = re.compile(r"0 @([^@]+)@ INDI")
GEDCOM_BIRT_RE = re.compile(r"2 DATE\s+([0-9-]{4,})")
GEDCOM_PLAC_RE = re.compile(r"[12] PLAC\s+(.+)")
GEDCOM_FAM_RE = re.compile(r"0 @([^@]+)@ FAM")
GEDCOM_HUSB_RE = re.compile(r"1 HUSB @([^@]+)@")
GEDCOM_WIFE_RE = re.compile(r"1 WIFE @([^@]+)@")
GEDCOM_CHIL_RE = re.compile(r"1 CHIL @([^@]+)@")
BOOK_CHARACTER_RE = re.compile(
    r"(?:^|\n)\s*(?:character|protagonist)\s*:\s*"
    r"([A-Z][A-Za-z]{1,24}(?:\s+[A-Z][A-Za-z]{1,24})?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
BOOK_ACTION_RE = re.compile(
    r"\b([A-Z][a-z]{2,24})\s+(?:arrived|returned|left|entered|met|visited)\b"
)
STRUCTURED_NAME_RE = re.compile(
    r"[\"'](?:display_name|name|person)[\"']\s*:\s*[\"']"
    r"([A-Z][A-Za-z]{1,24}(?:\s+[A-Z][A-Za-z]{1,24})?)[\"']"
)
CSV_NAME_RE = re.compile(r"^\s*([A-Z][A-Za-z]{1,24}(?:\s+[A-Z][A-Za-z]{1,24})?)\s*(?:,|\t|\|)")
CSV_PLACE_RE = re.compile(
    r"(?:,|\t|\|)\s*(?:19|20)\d{2}\s*(?:,|\t|\|)\s*"
    r"([A-Z][A-Za-z\u4e00-\u9fff]{1,24})"
)
RELATION_RE = re.compile(
    r"(?:relationship|relation)[\"']?\s*:\s*[\"']?"
    r"([A-Za-z][A-Za-z _-]{1,30})\s*(?:->|&|and)\s*([A-Za-z][A-Za-z _-]{1,30})",
    re.IGNORECASE,
)


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
