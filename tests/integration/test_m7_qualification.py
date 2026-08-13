"""M7 qualification: multiple unrelated domains prove core generality.

Mansion/literature (7-day living world), family genealogy/archive (GEDCOM +
conflicting claims + privacy), and heritage/museum (IIIF + Linked Art + twin +
biography) - all through the same authoritative core, with Source Gate gates.
"""

from __future__ import annotations

import json

import pytest
from wanxiang_substrate.compiler.compiler import StructuredCompiler
from wanxiang_substrate.genealogy.family import (
    FamilyClaim,
    FamilyWorld,
    Person,
)
from wanxiang_substrate.genealogy.gedcom import parse_gedcom, serialize_gedcom
from wanxiang_substrate.genealogy.privacy import ConsentState, LivingArchive
from wanxiang_substrate.heritage.iiif import IiifIngester
from wanxiang_substrate.heritage.linkedart import LinkedArtEvent, LinkedArtMapper
from wanxiang_substrate.heritage.museum import (
    BiographyEntry,
    MuseumBiography,
)
from wanxiang_substrate.heritage.twin import ConservationEntry, HeritageTwin
from wanxiang_substrate.sources.errors import RightsDenied
from wanxiang_substrate.sources.fixture import approved_source, rejected_source
from wanxiang_substrate.sources.gate import SourceGate


@pytest.mark.unit
def test_m7_red_chamber_source_gate_positive_and_negative() -> None:
    gate = SourceGate()
    # Approved synthetic red-chamber source compiles through the gate.
    approved = approved_source()
    assert gate.decide(approved).ok is True
    compiled = StructuredCompiler().compile("red_chamber_slice", {approved.source_id: approved})
    assert compiled.ok is True
    # Unapproved/rights-denied text cannot enter canonical compilation:
    # the Source Gate refuses it before any compile step.
    rejected = rejected_source()
    assert gate.decide(rejected).ok is False
    assert rejected.canonical_eligible() is False
    with pytest.raises(RightsDenied):
        gate.require_compile(rejected)


@pytest.mark.unit
def test_m7_family_gedcom_claims_and_privacy() -> None:
    sample = (
        "0 @I1@ INDI\n1 NAME Grandmother\n1 BIRT\n2 DATE 1900\n"
        "0 @I2@ INDI\n1 NAME Parent\n1 BIRT\n2 DATE 1930\n"
        "0 @I3@ INDI\n1 NAME Living Child\n1 _PRIV\n"
        "0 @F1@ FAM\n1 HUSB @I1@\n1 CHIL @I2@\n"
        "0 @F2@ FAM\n1 HUSB @I2@\n1 CHIL @I3@\n0 TRLR\n"
    )
    doc = parse_gedcom(sample)
    serialized = serialize_gedcom(doc)
    reparsed = parse_gedcom(serialized)
    parent = reparsed.individual("I2")
    assert parent is not None
    assert parent.birth_date == "1930"
    # Conflicting claims coexist as evidence-backed candidates.
    family = FamilyWorld()
    family.add_person(Person("I2", "Parent", birth_year=1930))
    family.add_claim(FamilyClaim("c_a", "I2", "birth_year", "1930", source_refs=("S1",)))
    family.add_claim(FamilyClaim("c_b", "I2", "birth_year", "1929", source_refs=("S2",)))
    claims = family.claims_for("I2")
    assert {c.value for c in claims} == {"1930", "1929"}
    # Living-person privacy: the living child needs consent.
    archive = LivingArchive()
    archive.record_consent(ConsentState(person_id="I3", consent_granted=False))
    archive.add_private_item("I3", "mem://private")
    from wanxiang_substrate.genealogy.errors import PrivacyDenied

    with pytest.raises(PrivacyDenied):
        archive.require_surface("I3", "mem://private", "evidence")


@pytest.mark.unit
def test_m7_heritage_twin_iiif_and_biography() -> None:
    manifest = IiifIngester().ingest(
        json.dumps(
            {
                "id": "https://museum.example/iiif/vase",
                "label": {"en": ["Vase"]},
                "rights": "https://creativecommons.org/publicdomain/",
                "items": [
                    {
                        "id": "https://museum.example/iiif/vase/c1",
                        "label": {"en": ["View"]},
                        "items": [
                            {
                                "id": "https://museum.example/iiif/vase/a1",
                                "body": {"id": "https://museum.example/img/vase.jpg"},
                            }
                        ],
                    }
                ],
            },
            sort_keys=True,
        )
    )
    assert manifest.canvases[0].service_refs[0].endswith("vase.jpg")
    mapper = LinkedArtMapper()
    mapper.map_object(
        "vase",
        external_ids=("https://linked.art/object/vase",),
        events=(
            LinkedArtEvent("e1", "vase", "production", actor="Kiln", timespan="1700"),
            LinkedArtEvent("e2", "vase", "conservation", actor="Lab", timespan="2020"),
        ),
    )
    assert [e.kind for e in mapper.provenance_chain("vase")] == ["production", "conservation"]
    # Physical object, digital surrogate, semantic twin, reconstruction distinct.
    twin = HeritageTwin(
        "phys_vase",
        digital_surrogate="digi_vase",
        twin_id="twin_vase",
        reconstruction_id="recon_vase",
    )
    twin.require_distinct()
    twin.add_conservation(ConservationEntry("c1", "stable", version=1))
    twin.add_conservation(ConservationEntry("c2", "restored", version=2))
    assert [e.version for e in twin.conservation_history()] == [1, 2]
    biography = MuseumBiography()
    biography.add(BiographyEntry("b1", "production", "Made in 1700", label="evidence"))
    biography.add(BiographyEntry("b2", "reconstruction", "Reconstructed", label="reconstructed"))
    labels = {e.entry_id: e.label for e in biography.entries()}
    assert labels["b1"] == "evidence"
    assert labels["b2"] == "reconstructed"
