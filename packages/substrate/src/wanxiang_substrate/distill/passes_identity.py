"""Identity and alias distillation for GEDCOM and legacy reference formats."""

from __future__ import annotations

import re
from collections import Counter

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.gedcom import (
    claim_fields,
    document_for_segment,
    identity_key,
)
from wanxiang_substrate.distill.passes_support import (
    BOOK_ACTION_RE,
    BOOK_CHARACTER_RE,
    CSV_NAME_RE,
    GEDCOM_NAME_RE,
    GEDCOM_XREF_RE,
    PASS_VERSION,
    STRUCTURED_NAME_RE,
    candidate_id,
    make_candidate,
)
from wanxiang_substrate.distill.protocol import Distiller
from wanxiang_substrate.parsing.segment import Segment


class IdentityPass(Distiller):
    """Identity/alias candidates; GEDCOM identity is XREF-scoped."""

    name = "identity"
    version = PASS_VERSION

    def distill(
        self, segments: tuple[Segment, ...], *, source_id: str
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        seen_names: Counter[str] = Counter()
        seen_refs: dict[str, set[str]] = {}
        for segment in segments:
            text, ref = segment.text, segment.locator.to_string()
            document = document_for_segment(text)
            if document is not None:
                for indi in document.individuals:
                    key = identity_key(source_id, indi.xref)
                    display = (
                        " ".join(item for item in (indi.given_name, indi.surname) if item)
                        or indi.name
                    )
                    candidates.append(
                        make_candidate(
                            "identity",
                            candidate_id(source_id, "identity", indi.xref),
                            "identity",
                            {
                                "key": key,
                                "identity_key": key,
                                "display_name": display,
                                "xref": indi.xref,
                                "source_id": source_id,
                                "given": indi.given_name,
                                "surname": indi.surname,
                            },
                            source_refs=(ref,),
                            confidence=0.95,
                        )
                    )
                    candidates.append(
                        make_candidate(
                            "identity",
                            candidate_id(source_id, "claim_name", indi.xref),
                            "claim",
                            claim_fields(proposition="person.name", value=display, xref=indi.xref),
                            source_refs=(ref,),
                            confidence=0.95,
                        )
                    )
                    for alias_index, alias in enumerate(indi.aliases):
                        candidates.append(
                            make_candidate(
                                "identity",
                                candidate_id(
                                    source_id, "alias", f"{indi.xref}|{alias_index}|{alias}"
                                ),
                                "alias",
                                {"identity_key": key, "alias": alias, "xref": indi.xref},
                                source_refs=(ref,),
                                confidence=0.8,
                            )
                        )
                for source in document.sources:
                    value = (
                        " | ".join(
                            item for item in (source.title, source.author, source.note) if item
                        )
                        or source.xref
                    )
                    candidates.append(
                        make_candidate(
                            "identity",
                            candidate_id(source_id, "source", source.xref),
                            "claim",
                            {
                                "proposition": "gedcom.source",
                                "value": value,
                                "source_xref": source.xref,
                            },
                            source_refs=(ref,),
                            confidence=0.8,
                        )
                    )
                continue
            xref = GEDCOM_XREF_RE.search(text)
            name_match = GEDCOM_NAME_RE.search(text)
            if xref and name_match:
                given, surname = name_match.group(1).strip(), name_match.group(2).strip()
                display = f"{given} {surname}".strip()
                key = f"{given.lower()}|{surname.lower()}"
                seen_names[key] += 1
                seen_refs.setdefault(key, set()).add(ref)
                candidates.append(
                    make_candidate(
                        "identity",
                        candidate_id(source_id, "legacy_identity", xref.group(1)),
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
