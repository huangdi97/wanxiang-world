"""Deterministic reference distillation passes (G57C-G57G).

No-API reference passes that extract CANDIDATES only from explicit patterns:
identity/alias/coreference (GEDCOM INDI, book names), event/time/place (dates,
places), relation/role/membership/organization (GEDCOM FAM), character/
life_arc/belief/knowledge_boundary (birth/death + keywords), object/rule/norm/
skill/affordance (explicit markers). Every candidate carries source refs and a
deterministic confidence; nothing is Canon.
"""

from __future__ import annotations

import re
from collections import Counter

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.passes_support import (
    BOOK_ACTION_RE,
    BOOK_CHARACTER_RE,
    CSV_NAME_RE,
    CSV_PLACE_RE,
    DATE_RE,
    GEDCOM_BIRT_RE,
    GEDCOM_CHIL_RE,
    GEDCOM_FAM_RE,
    GEDCOM_HUSB_RE,
    GEDCOM_NAME_RE,
    GEDCOM_PLAC_RE,
    GEDCOM_WIFE_RE,
    GEDCOM_XREF_RE,
    PASS_VERSION,
    PLACE_RE,
    RELATION_RE,
    STRUCTURED_NAME_RE,
    candidate_id,
    make_candidate,
)
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment


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
        seen_refs: dict[str, set[str]] = {}
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
                seen_refs.setdefault(key, set()).add(ref)
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
                continue
            generic_names = list(STRUCTURED_NAME_RE.findall(text))
            csv_name = CSV_NAME_RE.match(text)
            if csv_name:
                generic_names.append(csv_name.group(1).strip())
            character = BOOK_CHARACTER_RE.search(text)
            if character:
                generic_names.append(character.group(1).strip())
            action = BOOK_ACTION_RE.search(text)
            if action:
                generic_names.append(action.group(1).strip())
            for display in dict.fromkeys(generic_names):
                key = re.sub(r"[^a-z0-9]+", "|", display.lower()).strip("|")
                if not key:
                    continue
                seen_names[key] += 1
                seen_refs.setdefault(key, set()).add(ref)
                candidates.append(
                    make_candidate(
                        "identity",
                        candidate_id(source_id, "book_identity", key),
                        "identity",
                        {"key": key, "display_name": display},
                        source_refs=(ref,),
                        confidence=0.65,
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
                        source_refs=tuple(sorted(seen_refs.get(key, set()))),
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
            if not xref:
                places = tuple(PLACE_RE.finditer(text)) + tuple(CSV_PLACE_RE.finditer(text))
                for place_index, place in enumerate(places, start=1):
                    candidates.append(
                        make_candidate(
                            "event_time_space",
                            candidate_id(
                                source_id, "place", f"book|{place_index}|{place.group(1)}"
                            ),
                            "place",
                            {"name": place.group(1).strip()},
                            source_refs=(ref,),
                            confidence=0.55,
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
            if fam:
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
                                candidate_id(
                                    source_id, "membership", f"{fam_xref}|{child.group(1)}"
                                ),
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
            for relation_index, relation in enumerate(RELATION_RE.finditer(text), start=1):
                source_key = re.sub(r"[^a-z0-9]+", "|", relation.group(1).lower()).strip("|")
                target_key = re.sub(r"[^a-z0-9]+", "|", relation.group(2).lower()).strip("|")
                if source_key and target_key and source_key != target_key:
                    candidates.append(
                        make_candidate(
                            "relation_organization",
                            candidate_id(source_id, "text_relation", str(relation_index)),
                            "relation",
                            {
                                "source_key": source_key,
                                "target_key": target_key,
                                "relation_type": "related",
                            },
                            source_refs=(ref,),
                            confidence=0.65,
                        )
                    )
        return tuple(candidates)
