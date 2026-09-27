"""Capability package: the verified, self-describing unit the foundry ships.

A package declares what it can do (validity), what it needs to run (runtime),
what it may touch (world_effect) and how well it is known/admitted (levels). Its
package digest and provenance make it tamper-evident.

INVARIANT: a package is a proposal-side description. It carries no path to
canonical world state; WorldEffect only ever admits proposal-only output classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from wanxiang_execution import ExecutionClass

from wanxiang_foundry.digest import canonical_sha256, is_hex_digest
from wanxiang_foundry.errors import ArtifactError
from wanxiang_foundry.levels import KnowledgeLevel, PromotionLevel
from wanxiang_foundry.provenance import ProvenanceRecord, provenance_digest


class OutputClass(StrEnum):
    """The only world-facing output classes a package may declare.

    These are proposal-only. There is deliberately no member for a canonical
    write: a capability may observe, propose or project, never mutate canonical
    world state.
    """

    OBSERVATION = "observation"
    PROPOSAL = "proposal"
    PROJECTION = "projection"


@dataclass(frozen=True, slots=True)
class Validity:
    """The declared input domain and honest limits of a capability.

    Attributes:
        supported_inputs: Declared input domain, non-empty.
        known_limitations: Declared limits; may be empty.
        environment_hash: sha256 hex digest of the declared environment.
    """

    supported_inputs: tuple[str, ...]
    known_limitations: tuple[str, ...]
    environment_hash: str

    def __post_init__(self) -> None:
        if not self.supported_inputs:
            raise ArtifactError("validity must declare at least one supported input")
        if any(not item.strip() for item in self.supported_inputs):
            raise ArtifactError("supported_inputs entries must be non-empty strings")
        if any(not item.strip() for item in self.known_limitations):
            raise ArtifactError("known_limitations entries must be non-empty strings")
        if not is_hex_digest(self.environment_hash):
            raise ArtifactError(
                "validity environment_hash must be a 64-char lowercase hex sha256: "
                f"got {self.environment_hash!r}"
            )


@dataclass(frozen=True, slots=True)
class RuntimeRequirement:
    """What the capability needs from the execution fabric to run.

    Attributes:
        execution_class: Isolation class from the wanxiang_execution vocabulary.
        policy_fingerprint: sha256 hex digest of the ExecutionPolicy it needs.
    """

    execution_class: ExecutionClass
    policy_fingerprint: str

    def __post_init__(self) -> None:
        if not is_hex_digest(self.policy_fingerprint):
            raise ArtifactError(
                "runtime policy_fingerprint must be a 64-char lowercase hex sha256: "
                f"got {self.policy_fingerprint!r}"
            )


@dataclass(frozen=True, slots=True)
class WorldEffect:
    """What a capability may output toward the world.

    SAFETY: allowed_output_class is restricted to proposal-only values. A value
    that is not one of OBSERVATION/PROPOSAL/PROJECTION is refused, so a package
    can never declare a canonical write.
    """

    allowed_output_class: OutputClass

    @classmethod
    def from_output_class(cls, value: str) -> WorldEffect:
        """Build a WorldEffect from an untrusted string.

        Args:
            value: A declared output-class string.

        Returns:
            A WorldEffect whose class is proposal-only.

        Raises:
            ArtifactError: If value is not a proposal-only output class; any
                value implying a canonical write is refused.
        """
        try:
            resolved = OutputClass(value)
        except ValueError as exc:
            raise ArtifactError(
                "world_effect output class must be observation/proposal/projection; "
                f"canonical writes are refused: got {value!r}"
            ) from exc
        return cls(allowed_output_class=resolved)


@dataclass(frozen=True, slots=True)
class CapabilityPackage:
    """A self-describing, tamper-evident capability package (proposal-side).

    Attributes:
        capability_id: Non-empty capability id.
        version: Non-empty version string.
        artifact_digest: sha256 hex digest of the source artifact.
        interface_digest: sha256 hex digest of the declared interface.
        provenance: Non-empty tuple of provenance records.
        validity: Declared input domain and limits.
        runtime: Execution requirement.
        world_effect: Proposal-only output class it may produce.
        knowledge_level: How its behaviour is known.
        promotion_level: How far it has been admitted.
        verification_digest: Evidence digest of the granting report.
    """

    capability_id: str
    version: str
    artifact_digest: str
    interface_digest: str
    provenance: tuple[ProvenanceRecord, ...]
    validity: Validity
    runtime: RuntimeRequirement
    world_effect: WorldEffect
    knowledge_level: KnowledgeLevel
    promotion_level: PromotionLevel
    verification_digest: str

    def __post_init__(self) -> None:
        for name, value in (("capability_id", self.capability_id), ("version", self.version)):
            if not value.strip():
                raise ArtifactError(f"{name} must be a non-empty string")
        for name, digest in (
            ("artifact_digest", self.artifact_digest),
            ("interface_digest", self.interface_digest),
            ("verification_digest", self.verification_digest),
        ):
            if not is_hex_digest(digest):
                raise ArtifactError(
                    f"{name} must be a 64-char lowercase hex sha256: got {digest!r}"
                )
        if not self.provenance:
            raise ArtifactError("a package must carry at least one provenance record")

    def package_digest(self) -> str:
        """Return the canonical sha256 over every package field."""
        return canonical_sha256(self._payload())

    def _payload(self) -> dict[str, object]:
        ordered = sorted(self.provenance, key=lambda record: (record.layer.value, record.ref))
        return {
            "capability_id": self.capability_id,
            "version": self.version,
            "artifact_digest": self.artifact_digest,
            "interface_digest": self.interface_digest,
            "provenance_digest": provenance_digest(self.provenance),
            "provenance": [
                {
                    "layer": record.layer.value,
                    "ref": record.ref,
                    "digest": record.digest,
                    "note": record.note,
                }
                for record in ordered
            ],
            "validity": {
                "supported_inputs": list(self.validity.supported_inputs),
                "known_limitations": list(self.validity.known_limitations),
                "environment_hash": self.validity.environment_hash,
            },
            "runtime": {
                "execution_class": self.runtime.execution_class.value,
                "policy_fingerprint": self.runtime.policy_fingerprint,
            },
            "world_effect": {"allowed_output_class": self.world_effect.allowed_output_class.value},
            "knowledge_level": self.knowledge_level.value,
            "promotion_level": self.promotion_level.value,
            "verification_digest": self.verification_digest,
        }
