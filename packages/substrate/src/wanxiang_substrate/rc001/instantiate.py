"""RC-001 world instantiation (G36A).

Instantiates the assembled RC-001 World Definition as a LIVING world: resolve
domains/runtime profile, Genesis through the single Commit Authority, generate
an immutable initial snapshot, and record the lineage root. Uses synthetic
anonymized content ONLY - real《红楼梦》 canon remains EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData, FieldValue
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    WorldDefinitionId,
    WorldInstanceId,
    WorldlineId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_domain.worldline import InstanceIdentity
from wanxiang_runtime.authority import CommitAuthority, CommitResult
from wanxiang_runtime.state import InMemoryCanonicalState, state_to_primitive

from wanxiang_substrate.worldpack.assembler import AssembledWorldPack


@dataclass(frozen=True, slots=True)
class RC001Profile:
    """Resolved domains + runtime profile for RC-001."""

    profile_id: str
    runtime_ref: str
    domain_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.profile_id or not self.runtime_ref:
            raise ValueError("profile requires id and runtime ref")


def resolve_rc001_profile() -> RC001Profile:
    """Resolve the RC-001 runtime profile (narrative/household domain + deterministic runtime)."""
    return RC001Profile(
        profile_id="rc001_profile",
        runtime_ref="runtime:deterministic",
        domain_refs=("narrative_domain",),
    )


@dataclass(frozen=True, slots=True)
class InitialSnapshot:
    """Immutable initial snapshot of the freshly instantiated world."""

    revision: int
    entity_count: int
    content_hash: str
    primitive: dict[str, object]


@dataclass(frozen=True, slots=True)
class RC001Instance:
    """A freshly instantiated RC-001 world (identity + snapshot + genesis commit)."""

    identity: InstanceIdentity
    snapshot: InitialSnapshot
    genesis_commit: CommitResult
    profile: RC001Profile


def genesis_delta(schema_version: SchemaVersion | None = None) -> ProposedWorldDelta:
    """Initial synthetic (anonymized) entities for RC-001.

    Explicitly synthetic content: generic places/characters/objects, no
    fabricated《红楼梦》 canon.
    """
    schema = schema_version or SchemaVersion(1)
    operations: list[EntityCreate] = [
        EntityCreate(
            entity_id=EntityId("place_garden"),
            entity_type="place",
            components=(_component("place_garden", "spatial.place", {"kind": "garden"}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("place_hall"),
            entity_type="place",
            components=(_component("place_hall", "spatial.place", {"kind": "hall"}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("c1"),
            entity_type="actor",
            components=(_component("c1", "agency.actor_state", {"active": True}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("c2"),
            entity_type="actor",
            components=(_component("c2", "agency.actor_state", {"active": True}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("c3"),
            entity_type="actor",
            components=(_component("c3", "agency.actor_state", {"active": True}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("letter_1"),
            entity_type="object",
            components=(_component("letter_1", "material.item", {"kind": "letter"}, schema),),
        ),
        EntityCreate(
            entity_id=EntityId("medicine_1"),
            entity_type="object",
            components=(_component("medicine_1", "material.item", {"kind": "medicine"}, schema),),
        ),
    ]
    return ProposedWorldDelta(operations=tuple(operations))


def _component(
    entity_id: str,
    kind: str,
    fields: Mapping[str, FieldValue],
    schema_version: SchemaVersion,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"{kind.replace('.', '_')}_{entity_id}"),
        component_type=kind,
        schema_version=schema_version,
        fields=fields,
    )


def _snapshot(state: InMemoryCanonicalState) -> InitialSnapshot:
    primitive = state_to_primitive(state)
    return InitialSnapshot(
        revision=state.revision.value,
        entity_count=len(state.entities()),
        content_hash=semantic_sha256(primitive),
        primitive=primitive,
    )


def instantiate_rc001(
    *,
    authority: CommitAuthority,
    state: InMemoryCanonicalState,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    worldline_id: WorldlineId,
    rule_version: RuntimeVersion,
    world_time: WorldTime,
    definition: AssembledWorldPack,
) -> RC001Instance:
    """Genesis/instantiate RC-001 through the single Commit Authority."""
    from wanxiang_runtime.authority import CommitRequest

    commit = authority.commit(
        state,
        CommitRequest(
            command_id=CommandId("cmd_rc001_genesis"),
            instance_id=instance_id,
            branch_id=branch_id,
            expected_revision=BranchRevision(0),
            delta=genesis_delta(),
            world_time=world_time,
            rule_version=rule_version,
            kind="state",
        ),
    )
    identity = InstanceIdentity(
        instance_id=instance_id,
        worldline_id=worldline_id,
        definition_ref=definition.definition.definition_id.value,
        genesis_ref=definition.genesis.genesis_id,
        constitution_ref=definition.definition.constitution_ref,
        runtime_ref=resolve_rc001_profile().runtime_ref,
    )
    return RC001Instance(
        identity=identity,
        snapshot=_snapshot(commit.state_after),
        genesis_commit=commit,
        profile=resolve_rc001_profile(),
    )


def record_lineage_root(
    graph: object,
    *,
    instance_id: WorldInstanceId,
    definition_id: WorldDefinitionId,
) -> None:
    """Record the lineage root node for the new instance (no second history)."""
    from wanxiang_domain.lineage import LineageNode

    graph.add_node(  # type: ignore[attr-defined]
        LineageNode(
            node_id=instance_id.value,
            kind="worldline",
            definition_ref=definition_id.value,
        )
    )
