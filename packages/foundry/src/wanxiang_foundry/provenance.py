"""Provenance layers: how a capability package's knowledge can be traced.

INVARIANT: provenance records document *where* a capability's claims came from;
they never assert that a claim is true. A package's provenance is digestible so
it is tamper-evident, but a valid provenance digest is not evidence of truth.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from wanxiang_foundry.digest import canonical_sha256, is_hex_digest
from wanxiang_foundry.errors import ArtifactError


class ProvenanceLayer(StrEnum):
    """The four design-master provenance layers.

    SOURCE_METHOD is the original human/machine method; GENERATED_WRAPPER is
    code a provider synthesized around it; VALIDATION_FIXTURE is test evidence;
    RUNTIME_ADAPTER binds the capability to its execution environment.
    """

    SOURCE_METHOD = "source_method"
    GENERATED_WRAPPER = "generated_wrapper"
    VALIDATION_FIXTURE = "validation_fixture"
    RUNTIME_ADAPTER = "runtime_adapter"


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    """One traceable provenance link for a capability package.

    Attributes:
        layer: Which provenance layer this record belongs to.
        ref: Non-empty reference (uri, id, commit, path).
        digest: sha256 hex digest of the referenced content.
        note: Non-empty explanation of what the record establishes.
    """

    layer: ProvenanceLayer
    ref: str
    digest: str
    note: str

    def __post_init__(self) -> None:
        if not self.ref.strip():
            raise ArtifactError("provenance ref must be a non-empty string")
        if not is_hex_digest(self.digest):
            raise ArtifactError(
                f"provenance digest must be a 64-char lowercase hex sha256: got {self.digest!r}"
            )
        if not self.note.strip():
            raise ArtifactError("provenance note must be a non-empty string")


def provenance_digest(records: Sequence[ProvenanceRecord]) -> str:
    """Return a tamper-evident sha256 over provenance records.

    Records are sorted by layer then ref so the digest is order-independent for a
    given set of records and changes if any layer, ref, digest or note changes.

    Args:
        records: Provenance records to digest.

    Returns:
        Lowercase hex sha256 digest.
    """
    ordered = sorted(records, key=lambda record: (record.layer.value, record.ref))
    payload = [
        {
            "layer": record.layer.value,
            "ref": record.ref,
            "digest": record.digest,
            "note": record.note,
        }
        for record in ordered
    ]
    return canonical_sha256(payload)
