"""Generic GEDCOM branch for the private-safe local semantic provider."""

from __future__ import annotations

import hashlib
import json

from wanxiang_substrate.authoring.providers import ProviderProposal
from wanxiang_substrate.distill.gedcom import (
    document_for_segment,
    event_fields,
    family_key,
    identity_key,
)


def extract_gedcom(locator: str, text: str, provider_id: str) -> tuple[ProviderProposal, ...]:
    document = document_for_segment(text)
    if document is None:
        return ()
    source_id = locator.partition("://")[2].partition("#")[0]
    proposals: list[ProviderProposal] = []
    for indi in document.individuals:
        key = identity_key(source_id, indi.xref)
        display = " ".join(item for item in (indi.given_name, indi.surname) if item) or indi.name
        proposals.append(
            _proposal(
                provider_id,
                "identity",
                {
                    "key": key,
                    "identity_key": key,
                    "display_name": display,
                    "xref": indi.xref,
                    "source_id": source_id,
                },
                locator,
                0.8,
            )
        )
        proposals.append(
            _proposal(
                provider_id,
                "character",
                {"subject_key": key, "display_name": display, "xref": indi.xref},
                locator,
                0.75,
            )
        )
        for event in indi.events:
            fields = event_fields(event, subject_xref=key)
            proposals.append(_proposal(provider_id, "event", fields, locator, 0.74))
            proposals.append(
                _proposal(
                    provider_id,
                    "time",
                    {
                        key: value
                        for key, value in fields.items()
                        if key
                        in ("date", "date_raw", "date_precision", "uncertain", "subject_xref")
                    },
                    locator,
                    0.7,
                )
            )
            if event.place:
                proposals.append(
                    _proposal(
                        provider_id,
                        "place",
                        {
                            "name": event.place,
                            "subject_xref": key,
                            "place_role": fields["event_type"],
                        },
                        locator,
                        0.7,
                    )
                )
        if indi.place and not any(event.place == indi.place for event in indi.events):
            proposals.append(
                _proposal(
                    provider_id,
                    "place",
                    {"name": indi.place, "subject_xref": key, "place_role": "record"},
                    locator,
                    0.68,
                )
            )
    for family in document.families:
        fkey = family_key(source_id, family.xref)
        proposals.append(
            _proposal(
                provider_id,
                "organization",
                {
                    "key": fkey,
                    "display_name": f"Family {family.xref}",
                    "family_xref": family.xref,
                    "entity_type": "family",
                },
                locator,
                0.8,
            )
        )
        if family.husband_xref and family.wife_xref:
            proposals.append(
                _proposal(
                    provider_id,
                    "relation",
                    {
                        "source_key": identity_key(source_id, family.husband_xref),
                        "target_key": identity_key(source_id, family.wife_xref),
                        "relation_type": "spouse",
                        "family_xref": family.xref,
                    },
                    locator,
                    0.76,
                )
            )
        for parent in (family.husband_xref, family.wife_xref):
            for child in family.child_xrefs:
                if parent:
                    proposals.append(
                        _proposal(
                            provider_id,
                            "relation",
                            {
                                "source_key": identity_key(source_id, parent),
                                "target_key": identity_key(source_id, child),
                                "relation_type": "parent",
                                "family_xref": family.xref,
                            },
                            locator,
                            0.74,
                        )
                    )
        for child in family.child_xrefs:
            proposals.append(
                _proposal(
                    provider_id,
                    "membership",
                    {
                        "source_key": identity_key(source_id, child),
                        "target_key": fkey,
                        "family_xref": family.xref,
                        "role": "child",
                    },
                    locator,
                    0.72,
                )
            )
        for event in family.events:
            fields = event_fields(event, family_xref=fkey)
            proposals.append(_proposal(provider_id, "event", fields, locator, 0.74))
            proposals.append(
                _proposal(
                    provider_id,
                    "time",
                    {
                        key: value
                        for key, value in fields.items()
                        if key in ("date", "date_raw", "date_precision", "uncertain", "family_xref")
                    },
                    locator,
                    0.7,
                )
            )
            if event.place:
                proposals.append(
                    _proposal(
                        provider_id,
                        "place",
                        {
                            "name": event.place,
                            "family_xref": fkey,
                            "place_role": fields["event_type"],
                        },
                        locator,
                        0.7,
                    )
                )
    for source in document.sources:
        value = (
            " | ".join(item for item in (source.title, source.author, source.note) if item)
            or source.xref
        )
        proposals.append(
            _proposal(
                provider_id,
                "claim",
                {"proposition": "gedcom.source", "value": value, "source_xref": source.xref},
                locator,
                0.7,
            )
        )
    return tuple(proposals)


def _proposal(
    provider_id: str, kind: str, fields: dict[str, str], locator: str, confidence: float
) -> ProviderProposal:
    normalized = tuple(sorted((key, value) for key, value in fields.items() if value))
    digest = hashlib.sha256(
        json.dumps([kind, normalized, locator], ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()[:20]
    return ProviderProposal(
        proposal_id=f"semantic_{digest}",
        kind="candidate",
        provider_id=provider_id,
        source_refs=(locator,),
        payload=(
            ("candidate_kind", kind),
            ("schema_version", "semantic-candidate-v1"),
            *normalized,
        ),
        confidence=confidence,
    )


__all__ = ["extract_gedcom"]
