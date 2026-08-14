"""World Definition / Worldline identity model (G31A).

Formalizes the identity relationships between World Definition (read-only,
versioned), Instance, Worldline/Branch, and Derived World:

- A World Definition is a read-only versioned birth definition; running history
  never writes back to it.
- A Worldline is the continuous-history view of one world; its root branch is
  the starting history node.
- A Branch fork IS a Worldline fork relationship (reusing BranchAncestry) ?
  there is no second history object.
- An Instance records definition/genesis/constitution/runtime refs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import (
    BranchId,
    WorldDefinitionId,
    WorldInstanceId,
    WorldlineId,
)


@dataclass(frozen=True, slots=True)
class WorldDefinition:
    """Read-only, versioned birth definition of a world (immutable)."""

    definition_id: WorldDefinitionId
    version: int
    name: str
    constitution_ref: str
    genesis_ref: str
    package_ref: str | None = None
    schema_version: int = 1
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ContractError("world definition name must be non-empty")
        if self.version < 1:
            raise ContractError("world definition version must be >= 1")
        if not self.constitution_ref or not self.genesis_ref:
            raise ContractError("world definition requires constitution_ref and genesis_ref")

    def canonical(self) -> dict[str, object]:
        return {
            "definition_id": self.definition_id.value,
            "version": self.version,
            "name": self.name,
            "constitution_ref": self.constitution_ref,
            "genesis_ref": self.genesis_ref,
            "package_ref": self.package_ref,
            "schema_version": self.schema_version,
        }

    def compute_hash(self) -> str:
        payload = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> WorldDefinition:
        return WorldDefinition(
            definition_id=self.definition_id,
            version=self.version,
            name=self.name,
            constitution_ref=self.constitution_ref,
            genesis_ref=self.genesis_ref,
            package_ref=self.package_ref,
            schema_version=self.schema_version,
            content_hash=self.compute_hash(),
        )

    def to_primitive(self) -> dict[str, object]:
        return {**self.canonical(), "content_hash": self.content_hash}


@dataclass(frozen=True, slots=True)
class WorldlineIdentity:
    """Continuous-history view identity; root branch is the start node."""

    worldline_id: WorldlineId
    instance_id: WorldInstanceId
    root_branch_id: BranchId
    definition_ref: str
    constitution_ref: str

    def to_primitive(self) -> dict[str, object]:
        return {
            "worldline_id": self.worldline_id.value,
            "instance_id": self.instance_id.value,
            "root_branch_id": self.root_branch_id.value,
            "definition_ref": self.definition_ref,
            "constitution_ref": self.constitution_ref,
        }


@dataclass(frozen=True, slots=True)
class InstanceIdentity:
    """An instance records its definition/genesis/constitution/runtime refs."""

    instance_id: WorldInstanceId
    worldline_id: WorldlineId
    definition_ref: str
    genesis_ref: str
    constitution_ref: str
    runtime_ref: str

    def to_primitive(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id.value,
            "worldline_id": self.worldline_id.value,
            "definition_ref": self.definition_ref,
            "genesis_ref": self.genesis_ref,
            "constitution_ref": self.constitution_ref,
            "runtime_ref": self.runtime_ref,
        }


@dataclass(frozen=True, slots=True)
class WorldlineFork:
    """A branch fork IS a worldline fork relationship (reuses BranchAncestry)."""

    parent_worldline_id: WorldlineId
    parent_branch_id: BranchId
    child_branch_id: BranchId
    fork_revision: int
    fork_event_seq: int

    def to_primitive(self) -> dict[str, object]:
        return {
            "parent_worldline_id": self.parent_worldline_id.value,
            "parent_branch_id": self.parent_branch_id.value,
            "child_branch_id": self.child_branch_id.value,
            "fork_revision": self.fork_revision,
            "fork_event_seq": self.fork_event_seq,
        }
