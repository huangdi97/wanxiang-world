"""G35A: Red Chamber source registration mechanics (real source EXTERNAL_BLOCKED).

The registration mechanism is verified with a synthetic, explicitly-labeled
fixture (NOT real《红楼梦》 text). The real full-text source acquisition is
EXTERNAL_BLOCKED until a legal, traceable edition is available; no model memory
is used as Canon.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


@pytest.mark.unit
def test_source_checksum_is_reproducible() -> None:
    # Synthetic placeholder ONLY: never real Hongloumeng canon.
    payload = "fixture:red_chamber_source_registration (synthetic, not canonical text)"
    first = payload_hash(payload)
    second = payload_hash(payload)
    assert first == second
    assert len(first) == 64


@pytest.mark.unit
def test_rights_and_review_status_are_non_empty_for_registration() -> None:
    rights = RightsEnvelope(
        owner="public-domain-check-required",
        usage="corpus:red_chamber",
        approved=True,
        reviewer="system",
    )
    record = SourceRecord(
        source_id="src_red_chamber_synthetic",
        kind="text",
        content_hash=payload_hash("fixture:synthetic"),
        content_ref="fixture://red_chamber_synthetic",
        stage="E3",
        rights=rights,
        provenance="fixture:synthetic",
    )
    assert record.content_hash
    assert record.rights is not None
    assert record.rights.owner and record.rights.usage
    assert record.stage  # review_status non-empty
    assert record.canonical_eligible() is True


@pytest.mark.unit
def test_real_canon_is_not_fabricated_from_model_memory() -> None:
    # The repository must NOT contain any claimed《红楼梦》 canonical text derived
    # from model memory: the red_chamber sources dir holds templates only.
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    rc_dir = root / "sources" / "red_chamber"
    files = {p.name for p in rc_dir.iterdir() if p.is_file()}
    assert files == {"README.md", "MANIFEST_TEMPLATE.yaml"}, (
        f"unexpected red_chamber source files (model-memory canon forbidden): {files}"
    )
