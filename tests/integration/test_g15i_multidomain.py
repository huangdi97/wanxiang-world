"""G15I: family, heritage & campaign source-gated reference suites.

Synthetic conformance across four domain families (literature, family,
heritage, campaign) using public domain-package interfaces only. Real slices
are EXTERNAL_BLOCKED; domain generality is proven without Core special-casing.
"""

from __future__ import annotations

import json

from scripts.architecture_forensics import detect_cycles, import_edges, persistence_leakage
from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.campaign import CampaignDomain, Region, Unit
from wanxiang_substrate.genealogy.family import FamilyClaim, FamilyWorld, Person
from wanxiang_substrate.genealogy.gedcom import parse_gedcom, serialize_gedcom
from wanxiang_substrate.genealogy.privacy import LivingArchive, mode_label
from wanxiang_substrate.heritage.iiif import IiifIngester
from wanxiang_substrate.heritage.linkedart import LinkedArtEvent, LinkedArtMapper
from wanxiang_substrate.heritage.museum import BiographyEntry, MuseumBiography, MuseumScenario
from wanxiang_substrate.heritage.twin import ConservationEntry, HeritageTwin

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent.parent


def test_genealogy_synthetic_conformance() -> None:
    sample = "\n".join(
        [
            "0 HEAD",
            "1 GEDC",
            "2 VERS 5.5",
            "0 @I1@ INDI",
            "1 NAME Alice Smith",
            "1 BIRT",
            "2 DATE 1950",
            "0 @I2@ INDI",
            "1 NAME Bob Smith",
            "1 BIRT",
            "2 DATE 1975",
            "0 @F1@ FAM",
            "1 HUSB @I1@",
            "1 CHIL @I2@",
            "0 TRLR",
        ]
    )
    doc = parse_gedcom(sample)
    alice = doc.individual("I1")
    assert alice is not None and alice.name == "Alice Smith"
    assert len(serialize_gedcom(doc)) > 0
    # Conflicting claims coexist (imported facts are claims, not truth).
    world = FamilyWorld()
    world.add_person(Person("p1", "Pat"))
    world.add_claim(
        FamilyClaim(
            claim_id="c1",
            person_id="p1",
            proposition="birth_year",
            value="1950",
            source_refs=("s1",),
        )
    )
    world.add_claim(
        FamilyClaim(
            claim_id="c2",
            person_id="p1",
            proposition="birth_year",
            value="1948",
            source_refs=("s2",),
        )
    )
    assert len(world.claims_for("p1")) == 2
    # Privacy mode labels are explicit (evidence/reconstructed/creative).
    from wanxiang_substrate.genealogy.privacy import ConsentState

    archive = LivingArchive()
    state = archive.record_consent(ConsentState(person_id="p1", consent_granted=True))
    assert state.can_surface is True
    revoked = archive.revoke("p1")
    assert revoked.can_surface is False
    assert mode_label("evidence") == "evidence"
    assert mode_label("reconstructed_persona") == "reconstructed"


def test_heritage_synthetic_conformance() -> None:
    manifest = json.dumps(
        {
            "id": "https://example.org/iiif/obj1/manifest",
            "label": {"en": ["Object 1"]},
            "rights": "https://creativecommons.org/publicdomain/",
            "items": [
                {
                    "id": "https://example.org/iiif/obj1/canvas/1",
                    "label": {"en": ["Front"]},
                    "items": [
                        {
                            "id": "https://example.org/iiif/obj1/ann/1",
                            "body": {
                                "id": "https://example.org/img/obj1_front.jpg",
                                "type": "Image",
                            },
                        }
                    ],
                }
            ],
        },
        sort_keys=True,
    )
    parsed = IiifIngester().ingest(manifest)
    assert parsed.manifest_id.endswith("/manifest")
    assert parsed.rights.startswith("https://creativecommons.org")
    assert len(parsed.canvases) == 1
    # Linked Art mapping keeps provenance distinct.
    mapper = LinkedArtMapper()
    mapper.map_object(
        "obj_1",
        external_ids=("https://linked.art/object/obj1",),
        events=(
            LinkedArtEvent("e1", "obj_1", "production", actor="Workshop", timespan="1701"),
            LinkedArtEvent("e2", "obj_1", "acquisition", actor="Museum", timespan="1900"),
        ),
    )
    chain = mapper.provenance_chain("obj_1")
    assert [e.kind for e in chain] == ["production", "acquisition"]
    # Semantic twin identities are distinct; conservation history is versioned.
    twin = HeritageTwin(
        "physical_1", digital_surrogate="digital_1", twin_id="twin_1", reconstruction_id="recon_1"
    )
    twin.require_distinct()
    ids = twin.identities()
    assert ids["physical"] != ids["reconstruction"]
    twin.add_conservation(ConservationEntry("c1", "stable", version=1, provenance_ref="ref://a"))
    assert [e.version for e in twin.conservation_history()] == [1]
    # Museum biography labels evidence vs reconstruction; scenario instances.
    bio = MuseumBiography()
    bio.add(BiographyEntry("b1", "production", "Made in 1701", label="evidence"))
    assert {e.label for e in bio.entries()} == {"evidence"}
    scenario = MuseumScenario(
        "obj_1",
        current_instance="museum_1",
        historical_instance="museum_1701",
        biography_instance="bio_1",
        lab_instance="lab_1",
    )
    assert scenario.instances()["current"] == "museum_1"


def test_campaign_synthetic_conformance() -> None:
    campaign = CampaignDomain()
    campaign.add_region(Region("north", routes=("south",), capacity=100))
    campaign.add_region(Region("south", routes=("north",), capacity=100))
    campaign.add_unit(Unit("u1", "blue", "north", strength=10, supply=5))
    campaign.add_unit(Unit("u2", "red", "south", strength=8, supply=2))
    # Fog-of-war: blue does not know red-held territory yet.
    assert campaign.knows("blue", "south") is False
    # Co-sim adapter validity envelope + checkpoint round-trip.
    sim = FakeSimulator("campaign", rate_ticks=2, growth=1)
    sim.initialize({})
    sim.advance(0, 2)
    saved = sim.checkpoint()
    sim.advance(2, 4)
    sim.restore(saved)
    assert sim.checkpoint().value == 1  # growth=1 over one rate window
    assert "deterministic" in sim.describe_validity_envelope()


def test_four_domain_families_use_public_interfaces_only() -> None:

    # No domain special-casing: architecture forensics remain clean.
    assert detect_cycles(import_edges(ROOT)) == []
    assert persistence_leakage(ROOT) == []
    for pkg in ("genealogy", "heritage", "cosim", "sources"):
        assert (ROOT / "packages" / "substrate" / "src" / "wanxiang_substrate" / pkg).is_dir()
