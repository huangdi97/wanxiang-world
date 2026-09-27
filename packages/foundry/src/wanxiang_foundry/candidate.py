"""Capability candidates: proposal-only output of an Artifact2Capability provider.

INVARIANT: a candidate is a proposal. It can be neither registered nor invoked;
only a verified CapabilityPackage can be admitted by the registry. A candidate
carries no path to canonical world state.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from wanxiang_execution import SideEffectClass

from wanxiang_foundry.digest import canonical_sha256, is_hex_digest
from wanxiang_foundry.errors import CandidateError


class ArtifactKind(StrEnum):
    """The artifact kinds Artifact2Capability accepts (not paper-only)."""

    PAPER = "paper"
    REPO = "repo"
    API = "api"
    NOTEBOOK = "notebook"
    WORKFLOW = "workflow"


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """A reference to one external artifact.

    Attributes:
        kind: Artifact kind.
        uri: Non-empty locator.
        digest: sha256 hex digest of the captured artifact content.
        rights_basis: Declared rights basis for reuse. This may be empty on the
            reference; the provider refuses an empty value rather than assuming a
            right to reuse.
    """

    kind: ArtifactKind
    uri: str
    digest: str
    rights_basis: str

    def __post_init__(self) -> None:
        if not self.uri.strip():
            raise CandidateError("artifact uri must be a non-empty string")
        if not is_hex_digest(self.digest):
            raise CandidateError(
                f"artifact digest must be a 64-char lowercase hex sha256: got {self.digest!r}"
            )


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    """A provider's proposal for a new capability package.

    INVARIANT: a candidate is proposal-only. It cannot be registered or invoked;
    admission requires a verified package and a full-pass verification report.

    Attributes:
        candidate_id: Stable id for this proposal.
        capability_id: Id of the capability it would become.
        proposed_version: Proposed version string.
        artifact: The source artifact it was derived from.
        proposed_interface: Declared input/output contract (non-empty).
        environment_declaration: Declared execution environment.
        requested_side_effects: Side-effect classes the capability wants.
    """

    candidate_id: str
    capability_id: str
    proposed_version: str
    artifact: ArtifactRef
    proposed_interface: Mapping[str, object]
    environment_declaration: Mapping[str, object]
    requested_side_effects: tuple[SideEffectClass, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("candidate_id", self.candidate_id),
            ("capability_id", self.capability_id),
            ("proposed_version", self.proposed_version),
        ):
            if not value.strip():
                raise CandidateError(f"{name} must be a non-empty string")
        if not self.proposed_interface:
            raise CandidateError("candidate must declare a non-empty proposed_interface")

    def candidate_digest(self) -> str:
        """Return the canonical sha256 over the candidate fields."""
        return canonical_sha256(self._payload())

    def _payload(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "capability_id": self.capability_id,
            "proposed_version": self.proposed_version,
            "artifact": {
                "kind": self.artifact.kind.value,
                "uri": self.artifact.uri,
                "digest": self.artifact.digest,
                "rights_basis": self.artifact.rights_basis,
            },
            "proposed_interface": dict(self.proposed_interface),
            "environment_declaration": dict(self.environment_declaration),
            "requested_side_effects": [effect.value for effect in self.requested_side_effects],
        }
