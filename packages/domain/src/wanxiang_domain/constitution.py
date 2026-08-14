"""World Constitution model and versioning (G30B).

A World Constitution bounds a world family's root rules: identity, causality,
time and evolution. It separates:

- immutable root constraints (never amendable by a world instance), and
- mutable law layers (ontology/law layers that may evolve through
  Ontology/Law commits under the single commit boundary).

The platform Reality Root has its own immutable constitution
(`ROOT_CONSTITUTION`); world instances can never modify it or the platform
policy. Old v5.0/v5.1 WorldPacks without a constitution bind to the
`legacy_default_constitution()` compat manifest.

World Definitions reference their constitution via `constitution_ref` (wired
when the World Definition type is introduced; the constitution manifest carries
`world_definition_ref` to record the binding at authoring time).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import ConstitutionId

CONSTITUTION_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class ConstitutionVersion:
    """Non-negative constitution version."""

    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or self.value < 0:
            raise ContractError(
                f"ConstitutionVersion must be a non-negative integer, got {self.value!r}"
            )

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class ConstitutionManifest:
    """Immutable, versioned constitution manifest.

    All fields are immutable value objects/tuples: two constitutions can never
    share mutable objects, and a world instance can never mutate the manifest.
    """

    constitution_id: ConstitutionId
    version: ConstitutionVersion
    name: str
    root_constraints: tuple[str, ...]
    mutable_law_layers: tuple[str, ...] = ("ontology", "law")
    provenance: tuple[str, ...] = ()
    rights_ref: str = "platform-default"
    evolution_policy: str = "canonical_replay"
    world_definition_ref: str | None = None
    schema_version: int = CONSTITUTION_SCHEMA_VERSION
    content_hash: str = field(default="", compare=False)

    def __post_init__(self) -> None:
        if not self.name:
            raise ContractError("constitution name must be non-empty")
        if not self.root_constraints:
            raise ContractError("constitution must declare at least one root constraint")
        if self.schema_version <= 0:
            raise ContractError("constitution schema_version must be positive")

    def canonical(self) -> dict[str, object]:
        return {
            "constitution_id": self.constitution_id.value,
            "version": self.version.value,
            "name": self.name,
            "schema_version": self.schema_version,
            "root_constraints": sorted(self.root_constraints),
            "mutable_law_layers": sorted(self.mutable_law_layers),
            "provenance": sorted(self.provenance),
            "rights_ref": self.rights_ref,
            "evolution_policy": self.evolution_policy,
            "world_definition_ref": self.world_definition_ref,
        }

    def compute_hash(self) -> str:
        payload = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> ConstitutionManifest:
        return ConstitutionManifest(
            constitution_id=self.constitution_id,
            version=self.version,
            name=self.name,
            root_constraints=self.root_constraints,
            mutable_law_layers=self.mutable_law_layers,
            provenance=self.provenance,
            rights_ref=self.rights_ref,
            evolution_policy=self.evolution_policy,
            world_definition_ref=self.world_definition_ref,
            schema_version=self.schema_version,
            content_hash=self.compute_hash(),
        )

    def to_primitive(self) -> dict[str, object]:
        # Preserve authoring order (canonical() sorts for hash stability).
        return {
            "constitution_id": self.constitution_id.value,
            "version": self.version.value,
            "name": self.name,
            "schema_version": self.schema_version,
            "root_constraints": list(self.root_constraints),
            "mutable_law_layers": list(self.mutable_law_layers),
            "provenance": list(self.provenance),
            "rights_ref": self.rights_ref,
            "evolution_policy": self.evolution_policy,
            "world_definition_ref": self.world_definition_ref,
            "content_hash": self.content_hash,
        }


def constitution_from_primitive(data: dict[str, object]) -> ConstitutionManifest:
    """Deserialize a constitution manifest primitive (validated round-trip)."""

    def as_str(value: object, name: str) -> str:
        if not isinstance(value, str):
            raise ContractError(f"{name} must be a string")
        return value

    def as_int(value: object, name: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ContractError(f"{name} must be an int")
        return value

    def as_tuple(value: object, name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise ContractError(f"{name} must be a list of strings")
        raw = cast(list[object], value)
        items = [v for v in raw if isinstance(v, str)]
        if len(items) != len(raw):
            raise ContractError(f"{name} must be a list of strings")
        return tuple(items)

    manifest = ConstitutionManifest(
        constitution_id=ConstitutionId(as_str(data.get("constitution_id"), "constitution_id")),
        version=ConstitutionVersion(as_int(data.get("version"), "version")),
        name=as_str(data.get("name"), "name"),
        root_constraints=as_tuple(data.get("root_constraints"), "root_constraints"),
        mutable_law_layers=as_tuple(data.get("mutable_law_layers"), "mutable_law_layers"),
        provenance=as_tuple(data.get("provenance"), "provenance"),
        rights_ref=as_str(data.get("rights_ref"), "rights_ref"),
        evolution_policy=as_str(data.get("evolution_policy"), "evolution_policy"),
        world_definition_ref=(
            as_str(data.get("world_definition_ref"), "world_definition_ref")
            if data.get("world_definition_ref") is not None
            else None
        ),
        schema_version=as_int(data.get("schema_version"), "schema_version"),
        content_hash=as_str(data.get("content_hash", ""), "content_hash"),
    )
    return manifest.with_hash() if manifest.content_hash else manifest


# The platform Reality Root constitution: immutable, world instances can never
# amend it (World Policy is strictly isolated from Platform Policy).
ROOT_CONSTITUTION = ConstitutionManifest(
    constitution_id=ConstitutionId("con_platform_root"),
    version=ConstitutionVersion(1),
    name="Wanxiang Platform Reality Root",
    root_constraints=(
        "single_commit_boundary",
        "append_only_history",
        "replayable_history",
        "no_self_amendment",
        "world_policy_cannot_modify_platform",
    ),
    mutable_law_layers=(),
    rights_ref="platform-default",
    evolution_policy="canonical_replay",
).with_hash()


def legacy_default_constitution() -> ConstitutionManifest:
    """Compat constitution for old v5.0/v5.1 WorldPacks without one.

    Imposes only the minimal platform invariants so legacy packs keep working;
    all world-specific law layers remain mutable for the pack author.
    """
    return ConstitutionManifest(
        constitution_id=ConstitutionId("con_legacy_v5"),
        version=ConstitutionVersion(1),
        name="Legacy v5.0/v5.1 WorldPack Constitution (compat)",
        root_constraints=(
            "single_commit_boundary",
            "append_only_history",
            "replayable_history",
        ),
        mutable_law_layers=("ontology", "law"),
        rights_ref="platform-default",
        evolution_policy="canonical_replay",
    ).with_hash()
