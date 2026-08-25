"""Character knowledge + object/rule/skill reference passes (G57F/G57G)."""

from __future__ import annotations

import re

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.gedcom import document_for_segment, identity_key
from wanxiang_substrate.distill.passes import (
    GEDCOM_BIRT_RE,
    GEDCOM_XREF_RE,
    PASS_VERSION,
    candidate_id,
    make_candidate,
)
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment


class CharacterKnowledgePass(Distiller):
    """G57F: persona/life arc/goal/belief/knowledge-boundary candidates."""

    name = "character_knowledge"
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
            document = document_for_segment(text)
            if document is not None:
                for indi in document.individuals:
                    for event in indi.events:
                        if event.tag == "BIRT":
                            candidates.append(
                                make_candidate(
                                    "character_knowledge",
                                    candidate_id(source_id, "life_arc", indi.xref),
                                    "life_arc",
                                    {
                                        "subject_key": identity_key(source_id, indi.xref),
                                        "start": event.date or "unknown",
                                        "date_precision": event.date_precision,
                                        "uncertain": str(event.uncertain).lower(),
                                    },
                                    source_refs=(ref,),
                                    confidence=0.75,
                                )
                            )
                if document.individuals or document.families or document.sources:
                    continue
            xref = GEDCOM_XREF_RE.search(text)
            birth = GEDCOM_BIRT_RE.search(text)
            if xref and birth:
                candidates.append(
                    make_candidate(
                        "character_knowledge",
                        candidate_id(source_id, "life_arc", xref.group(1)),
                        "life_arc",
                        {"subject_xref": xref.group(1), "start": birth.group(1)},
                        source_refs=(ref,),
                        confidence=0.7,
                    )
                )
            for line in text.splitlines():
                lowered = line.lower()
                if "believe" in lowered:
                    candidates.append(
                        make_candidate(
                            "character_knowledge",
                            candidate_id(
                                source_id,
                                "belief",
                                f"{segment.segment_id}|{lowered.index('believe')}",
                            ),
                            "belief",
                            {"subject_key": "", "statement": line.strip()},
                            source_refs=(ref,),
                            confidence=0.4,
                        )
                    )
                if "secret" in lowered or "knows not" in lowered:
                    candidates.append(
                        make_candidate(
                            "character_knowledge",
                            candidate_id(source_id, "kb", f"{segment.segment_id}|{len(line)}"),
                            "knowledge_boundary",
                            {"subject_key": "", "boundary": line.strip()},
                            source_refs=(ref,),
                            confidence=0.4,
                        )
                    )
        return tuple(candidates)


class ObjectRuleSkillPass(Distiller):
    """G57G: object/rule/norm/skill/affordance candidates."""

    name = "object_rule_skill"
    version = PASS_VERSION

    def distill(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for segment in segments:
            ref = segment.locator.to_string()
            for line in segment.text.splitlines():
                lowered = line.lower().strip()
                for marker, kind, confidence in (
                    ("object:", "object", 0.7),
                    ("rule:", "rule", 0.7),
                    ("norm:", "norm", 0.7),
                    ("skill:", "skill", 0.7),
                ):
                    if lowered.startswith(marker):
                        value = line.split(":", 1)[1].strip()
                        candidates.append(
                            make_candidate(
                                "object_rule_skill",
                                candidate_id(source_id, kind, f"{segment.segment_id}|{value}"),
                                kind,
                                {"name": value},
                                source_refs=(ref,),
                                confidence=confidence,
                            )
                        )
                if not lowered.startswith(("object:", "rule:", "norm:", "skill:")):
                    marker_match = re.search(
                        r"(?:^|\\n|\n|\b)(object|rule|norm|skill):\s*(.+)$",
                        line,
                        flags=re.IGNORECASE,
                    )
                    if marker_match:
                        kind = marker_match.group(1).lower()
                        value = marker_match.group(2).strip().strip("\"'")
                        candidates.append(
                            make_candidate(
                                "object_rule_skill",
                                candidate_id(source_id, kind, f"{segment.segment_id}|{value}"),
                                kind,
                                {"name": value},
                                source_refs=(ref,),
                                confidence=0.65,
                            )
                        )
                for marker, kind, confidence in (
                    ("object", "object", 0.65),
                    ("rule", "rule", 0.65),
                    ("norm", "norm", 0.65),
                    ("skill", "skill", 0.65),
                ):
                    match = re.search(
                        rf"[\"']{marker}[\"']\s*:\s*[\"']([^\"']+)[\"']",
                        line,
                        flags=re.IGNORECASE,
                    )
                    if match:
                        value = match.group(1).strip()
                        candidates.append(
                            make_candidate(
                                "object_rule_skill",
                                candidate_id(source_id, kind, f"{segment.segment_id}|{value}"),
                                kind,
                                {"name": value},
                                source_refs=(ref,),
                                confidence=confidence,
                            )
                        )
        return tuple(candidates)
