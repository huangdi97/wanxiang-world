"""Event, time, place, and claim distillation for reference sources."""

from __future__ import annotations

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.gedcom import (
    claim_fields,
    document_for_segment,
    event_fields,
    family_key,
    identity_key,
)
from wanxiang_substrate.distill.passes_support import (
    CSV_PLACE_RE,
    DATE_RE,
    GEDCOM_BIRT_RE,
    GEDCOM_PLAC_RE,
    GEDCOM_XREF_RE,
    PASS_VERSION,
    PLACE_RE,
    candidate_id,
    make_candidate,
)
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment


class EventTimeSpacePass(Distiller):
    """Event, time-uncertainty, place, and explicit fact-claim candidates."""

    name = "event_time_space"
    version = PASS_VERSION

    def distill(
        self, segments: tuple[Segment, ...], *, source_id: str
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for segment in segments:
            text, ref = segment.text, segment.locator.to_string()
            document = document_for_segment(text)
            if document is not None:
                for indi in document.individuals:
                    subject = identity_key(source_id, indi.xref)
                    for index, event in enumerate(indi.events):
                        fields = event_fields(event, subject_xref=subject)
                        salt = f"{indi.xref}|{event.tag}|{index}|{event.date}|{event.place}"
                        candidates.extend(
                            (
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "event", salt),
                                    "event",
                                    fields,
                                    source_refs=(ref,),
                                    confidence=0.9,
                                ),
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "time", salt),
                                    "time",
                                    {
                                        "date": fields["date"],
                                        "date_raw": fields["date_raw"],
                                        "date_precision": fields["date_precision"],
                                        "uncertain": fields["uncertain"],
                                        "subject_xref": subject,
                                    },
                                    source_refs=(ref,),
                                    confidence=0.85,
                                ),
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "claim", salt),
                                    "claim",
                                    claim_fields(
                                        proposition=f"person.{fields['event_type']}.date",
                                        value=fields["date"],
                                        xref=indi.xref,
                                    ),
                                    source_refs=(ref,),
                                    confidence=0.9,
                                ),
                            )
                        )
                        if event.place:
                            candidates.append(
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "place", salt),
                                    "place",
                                    {
                                        "name": event.place,
                                        "subject_xref": subject,
                                        "place_role": fields["event_type"],
                                    },
                                    source_refs=(ref,),
                                    confidence=0.85,
                                )
                            )
                    if indi.place and not any(event.place == indi.place for event in indi.events):
                        candidates.append(
                            make_candidate(
                                "event_time_space",
                                candidate_id(source_id, "place", f"{indi.xref}|record"),
                                "place",
                                {
                                    "name": indi.place,
                                    "subject_xref": subject,
                                    "place_role": "record",
                                },
                                source_refs=(ref,),
                                confidence=0.7,
                            )
                        )
                for family in document.families:
                    family_ref = family_key(source_id, family.xref)
                    for index, event in enumerate(family.events):
                        fields = event_fields(event, family_xref=family_ref)
                        salt = f"{family.xref}|{event.tag}|{index}|{event.date}|{event.place}"
                        candidates.extend(
                            (
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "event", salt),
                                    "event",
                                    fields,
                                    source_refs=(ref,),
                                    confidence=0.9,
                                ),
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "time", salt),
                                    "time",
                                    {
                                        "date": fields["date"],
                                        "date_raw": fields["date_raw"],
                                        "date_precision": fields["date_precision"],
                                        "uncertain": fields["uncertain"],
                                        "family_xref": family_ref,
                                    },
                                    source_refs=(ref,),
                                    confidence=0.85,
                                ),
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "claim", salt),
                                    "claim",
                                    claim_fields(
                                        proposition=f"family.{fields['event_type']}.date",
                                        value=fields["date"],
                                        family_xref=family.xref,
                                    ),
                                    source_refs=(ref,),
                                    confidence=0.9,
                                ),
                            )
                        )
                        if event.place:
                            candidates.append(
                                make_candidate(
                                    "event_time_space",
                                    candidate_id(source_id, "place", salt),
                                    "place",
                                    {
                                        "name": event.place,
                                        "family_xref": family_ref,
                                        "place_role": fields["event_type"],
                                    },
                                    source_refs=(ref,),
                                    confidence=0.85,
                                )
                            )
                continue
            xref = GEDCOM_XREF_RE.search(text)
            birth = GEDCOM_BIRT_RE.search(text)
            place_match = GEDCOM_PLAC_RE.search(text)
            if xref and birth:
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(source_id, "legacy_event", f"{xref.group(1)}|birth"),
                        "event",
                        {
                            "subject_xref": xref.group(1),
                            "event_type": "birth",
                            "date": birth.group(1),
                            "date_raw": birth.group(1),
                            "date_precision": "unknown",
                            "uncertain": "true",
                        },
                        source_refs=(ref,),
                        confidence=0.85,
                    )
                )
            if xref and place_match:
                candidates.append(
                    make_candidate(
                        "event_time_space",
                        candidate_id(
                            source_id, "legacy_place", f"{xref.group(1)}|{place_match.group(1)}"
                        ),
                        "place",
                        {"name": place_match.group(1).strip(), "subject_xref": xref.group(1)},
                        source_refs=(ref,),
                        confidence=0.6,
                    )
                )
            if not xref:
                for place_index, place in enumerate(
                    tuple(PLACE_RE.finditer(text)) + tuple(CSV_PLACE_RE.finditer(text)), start=1
                ):
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
                        {"date": year, "uncertain": "true", "date_precision": "year"},
                        source_refs=(ref,),
                        confidence=0.4,
                    )
                )
        return tuple(candidates)
