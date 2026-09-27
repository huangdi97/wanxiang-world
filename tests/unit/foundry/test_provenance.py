"""Provenance digest stability and tamper detection."""

from __future__ import annotations

import hashlib

import pytest
from wanxiang_foundry.errors import ArtifactError
from wanxiang_foundry.provenance import (
    ProvenanceLayer,
    ProvenanceRecord,
    provenance_digest,
)


def _record(layer: ProvenanceLayer, ref: str, note: str) -> ProvenanceRecord:
    return ProvenanceRecord(
        layer=layer,
        ref=ref,
        digest=hashlib.sha256(ref.encode("utf-8")).hexdigest(),
        note=note,
    )


@pytest.mark.unit
def test_provenance_digest_is_stable_across_record_order() -> None:
    first = _record(ProvenanceLayer.SOURCE_METHOD, "a", "one")
    second = _record(ProvenanceLayer.GENERATED_WRAPPER, "b", "two")

    assert provenance_digest((first, second)) == provenance_digest((second, first))


@pytest.mark.unit
def test_provenance_digest_changes_when_a_record_changes() -> None:
    original = _record(ProvenanceLayer.SOURCE_METHOD, "a", "one")
    tampered = ProvenanceRecord(
        layer=original.layer,
        ref=original.ref,
        digest=original.digest,
        note="tampered",
    )

    assert provenance_digest((original,)) != provenance_digest((tampered,))


@pytest.mark.unit
def test_provenance_record_rejects_empty_ref() -> None:
    with pytest.raises(ArtifactError):
        _record(ProvenanceLayer.SOURCE_METHOD, "", "one")


@pytest.mark.unit
def test_provenance_record_rejects_non_hex_digest() -> None:
    with pytest.raises(ArtifactError):
        ProvenanceRecord(
            layer=ProvenanceLayer.SOURCE_METHOD,
            ref="a",
            digest="not-a-digest",
            note="one",
        )
