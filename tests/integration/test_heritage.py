"""G10A-G10D: IIIF ingest, Linked Art mapping, semantic twin, museum biography."""

from __future__ import annotations

import json

import pytest
from wanxiang_substrate.heritage.errors import IiifParseError, TwinError
from wanxiang_substrate.heritage.iiif import IiifIngester
from wanxiang_substrate.heritage.linkedart import LinkedArtEvent, LinkedArtMapper
from wanxiang_substrate.heritage.museum import (
    BiographyEntry,
    MuseumBiography,
    MuseumScenario,
)
from wanxiang_substrate.heritage.twin import ConservationEntry, HeritageTwin

_MANIFEST = json.dumps(
    {
        "id": "https://example.org/iiif/obj1/manifest",
        "label": {"en": ["Object 1"]},
        "rights": "https://creativecommons.org/publicdomain/",
        "attribution": "Example Museum",
        "items": [
            {
                "id": "https://example.org/iiif/obj1/canvas/1",
                "label": {"en": ["Front"]},
                "items": [
                    {
                        "id": "https://example.org/iiif/obj1/ann/1",
                        "body": {"id": "https://example.org/img/obj1_front.jpg", "type": "Image"},
                    }
                ],
            }
        ],
    },
    sort_keys=True,
)


@pytest.mark.unit
def test_iiif_manifest_ingest() -> None:
    ingester = IiifIngester()
    manifest = ingester.ingest(_MANIFEST)
    assert manifest.manifest_id.endswith("/manifest")
    assert manifest.rights.startswith("https://creativecommons.org")
    assert len(manifest.canvases) == 1
    assert manifest.canvases[0].service_refs == ("https://example.org/img/obj1_front.jpg",)
    assert ingester.get(manifest.manifest_id) is manifest


@pytest.mark.unit
def test_iiif_invalid_manifest_rejected() -> None:
    ingester = IiifIngester()
    with pytest.raises(IiifParseError):
        ingester.ingest("not json")
    with pytest.raises(IiifParseError):
        ingester.ingest(json.dumps({"id": "x"}))


@pytest.mark.unit
def test_linked_art_mapping_and_provenance_chain() -> None:
    mapper = LinkedArtMapper()
    mapper.map_object(
        "obj_1",
        external_ids=("https://linked.art/object/obj1",),
        events=(
            LinkedArtEvent("e1", "obj_1", "production", actor="Workshop", timespan="1701"),
            LinkedArtEvent("e2", "obj_1", "acquisition", actor="Museum", timespan="1900"),
            LinkedArtEvent("e3", "obj_1", "conservation", actor="Lab", timespan="2020"),
        ),
    )
    mapping = mapper.get("obj_1")
    assert mapping is not None
    assert mapping.external_ids == ("https://linked.art/object/obj1",)
    chain = mapper.provenance_chain("obj_1")
    assert [e.kind for e in chain] == ["production", "acquisition", "conservation"]
    assert chain[0].timespan == "1701"


@pytest.mark.unit
def test_semantic_twin_identities_are_distinct() -> None:
    twin = HeritageTwin(
        "physical_1",
        digital_surrogate="digital_1",
        twin_id="twin_1",
        reconstruction_id="recon_1",
    )
    twin.require_distinct()
    ids = twin.identities()
    assert ids["physical"] != ids["digital_surrogate"]
    assert ids["semantic_twin"] != ids["reconstruction"]
    # Duplicate identities violate distinctness.
    bad = HeritageTwin("x", digital_surrogate="x")
    with pytest.raises(TwinError):
        bad.require_distinct()


@pytest.mark.unit
def test_conservation_history_is_versioned_and_replayable() -> None:
    twin = HeritageTwin("physical_1")
    twin.add_conservation(ConservationEntry("c1", "stable", version=1, provenance_ref="ref://a"))
    twin.add_conservation(ConservationEntry("c2", "restored", version=2, provenance_ref="ref://b"))
    history = twin.conservation_history()
    assert [e.version for e in history] == [1, 2]
    assert history[1].state == "restored"


@pytest.mark.unit
def test_museum_biography_labels_and_curator_gate() -> None:
    biography = MuseumBiography()
    biography.add(BiographyEntry("b1", "production", "Made in 1701", label="evidence"))
    biography.add(
        BiographyEntry("b2", "reconstruction", "Reconstructed shape", label="reconstructed")
    )
    labels = {e.entry_id: e.label for e in biography.entries()}
    assert labels["b1"] == "evidence"
    assert labels["b2"] == "reconstructed"
    biography.add(BiographyEntry("b3", "conservation", "Private note", rights="private"))
    with pytest.raises(ValueError):
        biography.require_rights("b3")
    biography.require_rights("b3", curator=True)
    scenario = MuseumScenario(
        "obj_1",
        current_instance="museum_1",
        historical_instance="museum_1701",
        biography_instance="bio_1",
        lab_instance="lab_1",
    )
    assert scenario.instances()["current"] == "museum_1"
    assert scenario.curator_note("approved")["mode"] == "curator"
