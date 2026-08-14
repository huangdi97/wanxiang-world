"""G18F: heritage / museum workbench completion.

- Physical/digital/reconstruction states are visibly distinct.
- Rights prevent restricted projection/export.
- Conservation history remains auditable.
"""

from __future__ import annotations

import pytest
from wanxiang_api.heritage_workbench_service import HeritageRightsDenied, HeritageWorkbenchService
from wanxiang_substrate.heritage.museum import BiographyEntry, MuseumBiography
from wanxiang_substrate.heritage.twin import ConservationEntry, HeritageTwin


def _fixture() -> HeritageWorkbenchService:
    twin = HeritageTwin(
        "physical_1", digital_surrogate="digital_1", twin_id="twin_1", reconstruction_id="recon_1"
    )
    twin.require_distinct()
    twin.add_conservation(ConservationEntry("c1", "stable", version=1, provenance_ref="ref://a"))
    twin.add_conservation(ConservationEntry("c2", "restored", version=2, provenance_ref="ref://b"))
    bio = MuseumBiography()
    bio.add(BiographyEntry("b1", "production", "Made in 1701", label="evidence"))
    bio.add(BiographyEntry("b2", "reconstruction", "Reconstructed shape", label="reconstructed"))
    return HeritageWorkbenchService(twin, bio)


def test_physical_digital_reconstruction_states_visibly_distinct() -> None:
    service = _fixture()
    view = service.object_view("physical_1", curator=True)
    ids = view["identities"]
    assert ids["physical"] != ids["digital_surrogate"]
    assert ids["semantic_twin"] != ids["reconstruction"]
    # Reconstructions are labeled (never presented as original fact).
    assert view["reconstruction_labeled"] is True
    labels = {e["label"] for e in view["timeline"]}
    assert "evidence" in labels and "reconstructed" in labels


def test_rights_prevent_restricted_projection_export() -> None:
    service = _fixture()
    with pytest.raises(HeritageRightsDenied):
        service.export("physical_1", curator=False)
    exported = service.export("physical_1", curator=True)
    assert exported["exported"] is True


def test_conservation_history_auditable() -> None:
    service = _fixture()
    history = service.conservation_history()
    assert history["auditable"] is True
    assert [e["version"] for e in history["entries"]] == [1, 2]
    assert history["entries"][1]["state"] == "restored"
