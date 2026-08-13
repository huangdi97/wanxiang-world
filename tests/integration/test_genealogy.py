"""G09A-G09C: GEDCOM interop, family semantic world, privacy/persona modes."""

from __future__ import annotations

import pytest
from wanxiang_substrate.genealogy.errors import (
    InvalidKinship,
    PrivacyDenied,
)
from wanxiang_substrate.genealogy.family import (
    FamilyClaim,
    FamilyWorld,
    Kinship,
    Person,
)
from wanxiang_substrate.genealogy.gedcom import parse_gedcom, serialize_gedcom
from wanxiang_substrate.genealogy.privacy import (
    ConsentState,
    LivingArchive,
    mode_label,
)

_SAMPLE = """0 HEAD
1 GEDC
2 VERS 5.5
0 @I1@ INDI
1 NAME Alice Smith
1 BIRT
2 DATE 1950
1 PLAC Springfield
1 SOUR @S1@
0 @I2@ INDI
1 NAME Bob Smith
1 BIRT
2 DATE 1975
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
0 @S1@ SOUR
1 TITL Family Records
0 TRLR
"""


@pytest.mark.unit
def test_gedcom_parse_and_roundtrip() -> None:
    doc = parse_gedcom(_SAMPLE)
    alice = doc.individual("I1")
    assert alice is not None
    assert alice.name == "Alice Smith"
    assert alice.birth_date == "1950"
    assert alice.source_refs == ("S1",)
    assert doc.families[0].child_xrefs == ("I2",)
    assert doc.sources[0].title == "Family Records"
    # Round-trip preserves the normalized individuals.
    serialized = serialize_gedcom(doc)
    reparsed = parse_gedcom(serialized)
    alice2 = reparsed.individual("I1")
    assert alice2 is not None
    assert alice2.name == "Alice Smith"
    assert alice2.birth_date == "1950"
    assert reparsed.families[0].child_xrefs == ("I2",)


@pytest.mark.unit
def test_unknown_extensions_preserved_not_dropped() -> None:
    text = "0 @I9@ INDI\n1 NAME Grace\n1 _MYEXT custom-value\n0 TRLR\n"
    doc = parse_gedcom(text)
    indi = doc.individual("I9")
    assert indi is not None
    assert ("_MYEXT", "custom-value") in indi.extensions


@pytest.mark.unit
def test_imported_facts_are_claims_not_truth() -> None:
    doc = parse_gedcom(_SAMPLE)
    family = FamilyWorld()
    alice = Person("I1", "Alice Smith", birth_year=1950)
    bob = Person("I2", "Bob Smith", birth_year=1975)
    family.add_person(alice)
    family.add_person(bob)
    alice_indi = doc.individual("I1")
    assert alice_indi is not None
    claim = FamilyClaim(
        claim_id="c1",
        person_id="I1",
        proposition="birth_year",
        value="1950",
        source_refs=alice_indi.source_refs,
    )
    family.add_claim(claim)
    # The imported fact is a claim with evidence, not unconditional truth.
    assert family.claims_for("I1")[0].value == "1950"
    assert family.claims_for("I1")[0].source_refs == ("S1",)


@pytest.mark.unit
def test_kinship_validity_and_lineage() -> None:
    family = FamilyWorld()
    family.add_person(Person("g", "Grandma"))
    family.add_person(Person("m", "Mom"))
    family.add_person(Person("c", "Child"))
    family.add_kinship(Kinship("k1", "g", "m", "parent"))
    family.add_kinship(Kinship("k2", "m", "c", "parent"))
    assert [p.person_id for p in family.parents("c")] == ["m"]
    assert [p.person_id for p in family.children("g")] == ["m"]
    # Self-loop is invalid.
    with pytest.raises(InvalidKinship):
        family.add_kinship(Kinship("k3", "c", "c", "parent"))
    # Cycle is invalid (child cannot become parent of its ancestor).
    with pytest.raises(InvalidKinship):
        family.add_kinship(Kinship("k4", "c", "g", "parent"))


@pytest.mark.unit
def test_living_person_privacy_and_persona_modes() -> None:
    archive = LivingArchive()
    archive.record_consent(ConsentState(person_id="I2", consent_granted=True))
    archive.add_private_item("I2", "mem://private_1")
    assert mode_label("evidence") == "evidence"
    assert mode_label("reconstructed_persona") == "reconstructed"
    assert mode_label("creative_legacy") == "creative"
    # Consent allows surfacing the private item in evidence mode.
    archive.require_surface("I2", "mem://private_1", "evidence")
    # Revocation blocks it.
    archive.revoke("I2")
    with pytest.raises(PrivacyDenied):
        archive.require_surface("I2", "mem://private_1", "evidence")
    # Someone else's private item cannot be surfaced.
    archive2 = LivingArchive()
    archive2.record_consent(ConsentState(person_id="I1", consent_granted=True))
    archive2.add_private_item("I2", "mem://secret")
    with pytest.raises(PrivacyDenied):
        archive2.require_surface("I1", "mem://secret", "evidence")


@pytest.mark.unit
def test_creative_legacy_requires_public_posthumous_policy() -> None:
    archive = LivingArchive()
    archive.record_consent(
        ConsentState(person_id="I1", consent_granted=True, posthumous_policy="private")
    )
    archive.add_private_item("I1", "mem://legacy")
    with pytest.raises(PrivacyDenied):
        archive.require_surface("I1", "mem://legacy", "creative_legacy")
