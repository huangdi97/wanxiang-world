"""Family containers, kinship, membership, and text relation distillation."""

from __future__ import annotations

import re

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.gedcom import document_for_segment, family_key, identity_key
from wanxiang_substrate.distill.passes_support import (
    GEDCOM_CHIL_RE,
    GEDCOM_FAM_RE,
    GEDCOM_HUSB_RE,
    GEDCOM_WIFE_RE,
    PASS_VERSION,
    RELATION_RE,
    candidate_id,
    make_candidate,
)
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment


class RelationOrganizationPass(Distiller):
    """Family containers, XREF kinship, membership, and text relations."""

    name = "relation_organization"
    version = PASS_VERSION

    def distill(
        self, segments: tuple[Segment, ...], *, source_id: str
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for segment in segments:
            text, ref = segment.text, segment.locator.to_string()
            document = document_for_segment(text)
            if document is not None:
                for family in document.families:
                    fkey = family_key(source_id, family.xref)
                    candidates.append(
                        make_candidate(
                            "relation_organization",
                            candidate_id(source_id, "family", family.xref),
                            "organization",
                            {
                                "key": fkey,
                                "display_name": f"Family {family.xref}",
                                "family_xref": family.xref,
                                "entity_type": "family",
                            },
                            source_refs=(ref,),
                            confidence=0.95,
                        )
                    )
                    if family.husband_xref and family.wife_xref:
                        candidates.append(
                            make_candidate(
                                "relation_organization",
                                candidate_id(source_id, "spouse", family.xref),
                                "relation",
                                {
                                    "source_key": identity_key(source_id, family.husband_xref),
                                    "target_key": identity_key(source_id, family.wife_xref),
                                    "relation_type": "spouse",
                                    "family_xref": family.xref,
                                },
                                source_refs=(ref,),
                                confidence=0.95,
                            )
                        )
                    for parent in (family.husband_xref, family.wife_xref):
                        if not parent:
                            continue
                        for child in family.child_xrefs:
                            salt = f"{family.xref}|{parent}|{child}"
                            candidates.append(
                                make_candidate(
                                    "relation_organization",
                                    candidate_id(source_id, "parent", salt),
                                    "relation",
                                    {
                                        "source_key": identity_key(source_id, parent),
                                        "target_key": identity_key(source_id, child),
                                        "relation_type": "parent",
                                        "family_xref": family.xref,
                                    },
                                    source_refs=(ref,),
                                    confidence=0.9,
                                )
                            )
                    for child in family.child_xrefs:
                        member = identity_key(source_id, child)
                        candidates.append(
                            make_candidate(
                                "relation_organization",
                                candidate_id(source_id, "membership", f"{family.xref}|{child}"),
                                "membership",
                                {
                                    "source_key": member,
                                    "target_key": fkey,
                                    "member_key": member,
                                    "family_xref": family.xref,
                                    "role": "child",
                                },
                                source_refs=(ref,),
                                confidence=0.85,
                            )
                        )
                for indi in document.individuals:
                    ikey = identity_key(source_id, indi.xref)
                    for family in indi.family_child_refs:
                        candidates.append(
                            make_candidate(
                                "relation_organization",
                                candidate_id(source_id, "famc", f"{indi.xref}|{family}"),
                                "membership",
                                {
                                    "source_key": ikey,
                                    "target_key": family_key(source_id, family),
                                    "family_xref": family,
                                    "role": "child",
                                },
                                source_refs=(ref,),
                                confidence=0.85,
                            )
                        )
                    for family in indi.family_spouse_refs:
                        candidates.append(
                            make_candidate(
                                "relation_organization",
                                candidate_id(source_id, "fams", f"{indi.xref}|{family}"),
                                "membership",
                                {
                                    "source_key": ikey,
                                    "target_key": family_key(source_id, family),
                                    "family_xref": family,
                                    "role": "spouse",
                                },
                                source_refs=(ref,),
                                confidence=0.85,
                            )
                        )
                continue
            fam = GEDCOM_FAM_RE.search(text)
            if fam:
                husband, wife = GEDCOM_HUSB_RE.search(text), GEDCOM_WIFE_RE.search(text)
                if husband and wife:
                    candidates.append(
                        make_candidate(
                            "relation_organization",
                            candidate_id(source_id, "legacy_relation", f"{fam.group(1)}|spouse"),
                            "relation",
                            {
                                "source_key": husband.group(1),
                                "target_key": wife.group(1),
                                "relation_type": "spouse",
                                "family_xref": fam.group(1),
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
                                    source_id,
                                    "legacy_membership",
                                    f"{fam.group(1)}|{child.group(1)}",
                                ),
                                "membership",
                                {
                                    "source_key": child.group(1),
                                    "target_key": fam.group(1),
                                    "family_xref": fam.group(1),
                                    "role": "child",
                                },
                                source_refs=(ref,),
                                confidence=0.8,
                            )
                        )
            for index, relation in enumerate(RELATION_RE.finditer(text), start=1):
                source_key = re.sub(r"[^a-z0-9]+", "|", relation.group(1).lower()).strip("|")
                target_key = re.sub(r"[^a-z0-9]+", "|", relation.group(2).lower()).strip("|")
                if source_key and target_key and source_key != target_key:
                    candidates.append(
                        make_candidate(
                            "relation_organization",
                            candidate_id(source_id, "text_relation", str(index)),
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
