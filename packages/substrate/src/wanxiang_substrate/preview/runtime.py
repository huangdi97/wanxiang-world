"""Reference Preview runtime over the existing WorldRuntime port (G60F/G60G).

The substrate owns the preview protocol and deterministic proposal resolvers.
The application injects its existing Runtime implementation; no application
import or second canonical mutation path is introduced here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, cast

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta, RelationCreate
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    RelationId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import SchemaVersion
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.host import WorldHost
from wanxiang_substrate.preview.scope import PreviewInstall
from wanxiang_substrate.runtime_port import WorldRuntimePort

PREVIEW_CREATE_ENTITY = "preview.create_entity"
PREVIEW_CREATE_RELATION = "preview.create_relation"
_SCHEMA = SchemaVersion(1)
_DEFAULT_WORLD_TIME = WorldTime(0)


class CreatedWorld(Protocol):
    instance_id: WorldInstanceId
    root_branch_id: BranchId


class ReplayResult(Protocol):
    state: InMemoryCanonicalState


class PreviewRuntimePort(WorldRuntimePort, Protocol):
    """Application-owned runtime methods required by preview composition."""

    def create_world(
        self,
        instance_id: WorldInstanceId | None = None,
        world_time: WorldTime = _DEFAULT_WORLD_TIME,
    ) -> object: ...

    def restore_and_replay(self, instance_id: WorldInstanceId, branch_id: BranchId) -> object: ...


def _text(command: CommandEnvelope, key: str, *, required: bool = True) -> str | None:
    value = command.payload.get(key)
    if isinstance(value, str) and value:
        return value
    if not required and value is None:
        return None
    raise ValidationRejected(f"preview payload field {key!r} must be a non-empty string")


def _preview_entity(
    command: CommandEnvelope, _state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    raw_id = _text(command, "entity_id")
    entity_type = _text(command, "entity_type", required=False) or "actor"
    display_name = _text(command, "display_name", required=False)
    fields: dict[str, str] = {}
    if display_name is not None:
        fields["display_name"] = display_name
    role = _text(command, "role", required=False)
    if role is not None:
        fields["role"] = role
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(raw_id or ""),
                entity_type=entity_type,
                components=(
                    ComponentData(
                        component_id=ComponentId(f"profile_{raw_id}"),
                        component_type="profile",
                        schema_version=_SCHEMA,
                        fields=fields,
                    ),
                ),
            ),
        )
    )


def _preview_relation(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    source = _text(command, "source_id")
    target = _text(command, "target_id")
    relation_type = _text(command, "relation_type")
    if source == target:
        raise ValidationRejected("preview relations require distinct endpoints")
    if state is None:
        raise ValidationRejected("preview relation requires current state")
    if state.entity(EntityId(source or "")) is None or state.entity(EntityId(target or "")) is None:
        raise ValidationRejected("preview relation endpoint does not exist")
    relation_id = _text(command, "relation_id")
    return ProposedWorldDelta(
        operations=(
            RelationCreate(
                relation_id=RelationId(relation_id or ""),
                relation_type=relation_type or "relation",
                source_id=EntityId(source or ""),
                target_id=EntityId(target or ""),
            ),
        )
    )


def register_preview_resolvers(registry: ResolverRegistry) -> None:
    """Register only proposal-producing preview actions."""
    registry.register(PREVIEW_CREATE_ENTITY, _preview_entity)
    registry.register(PREVIEW_CREATE_RELATION, _preview_relation)


def _safe_id(raw: str, index: int, used: set[str]) -> str:
    value = re.sub(r"[^a-z0-9_-]+", "_", raw.lower()).strip("_-")
    base = f"ent_{value or index}"
    candidate = base
    if candidate in used:
        candidate = f"{base}_{index}"
    while candidate in used:
        index += 1
        candidate = f"{base}_{index}"
    return candidate


@dataclass(frozen=True, slots=True)
class PreviewWorld:
    """A running preview bound to one package and one isolated instance."""

    install: PreviewInstall
    runtime: PreviewRuntimePort
    host: WorldHost
    instance_id: WorldInstanceId
    branch_id: BranchId

    def observe(self) -> dict[str, object]:
        from wanxiang_runtime.state import state_to_primitive

        return state_to_primitive(self.runtime.current_state(self.instance_id, self.branch_id))

    def step(self, action_type: str, payload: dict[str, str]) -> dict[str, object]:
        state = self.runtime.current_state(self.instance_id, self.branch_id)
        command = CommandEnvelope(
            command_id=CommandId.generate(),
            instance_id=self.instance_id,
            branch_id=self.branch_id,
            expected_revision=BranchRevision(state.revision.value),
            action_type=action_type,
            payload=payload,
            world_time=WorldTime(state.revision.value + 1),
        )
        self.host.submit(command)
        return self.observe()

    def replay_hash(self) -> str:
        replayed = cast(
            ReplayResult,
            self.runtime.restore_and_replay(self.instance_id, self.branch_id),
        )
        return replayed.state.semantic_hash()


def instantiate_preview(
    runtime: PreviewRuntimePort,
    package: WorldPackageDraft,
    install: PreviewInstall,
) -> PreviewWorld:
    """Instantiate draft entities and relations through the existing Host."""
    if (
        install.package_id != package.package_id
        or install.package_hash != package.manifest.content_hash
    ):
        raise ValidationRejected("preview install does not match the package manifest")
    instance_id = WorldInstanceId(f"prv_{install.preview_id}")
    created = cast(CreatedWorld, runtime.create_world(instance_id=instance_id))
    host = WorldHost(runtime, created.instance_id, created.root_branch_id)
    identity: dict[str, str] = {}
    used_entity_ids: set[str] = set()
    for index, (key, display_name) in enumerate(package.draft.entities, start=1):
        # Stable semantic keys remain the identity map; the readable runtime
        # id is only a presentation handle and is collision-safe for same-name
        # people from distinct XREFs.
        readable_key = display_name if key.startswith("gedcom:") else key
        entity_id = _safe_id(readable_key, index, used_entity_ids)
        used_entity_ids.add(entity_id)
        identity[key] = entity_id
        PreviewWorld(install, runtime, host, instance_id, created.root_branch_id).step(
            PREVIEW_CREATE_ENTITY,
            {"entity_id": entity_id, "entity_type": "actor", "display_name": display_name},
        )
    for index, (source, target, relation_type) in enumerate(package.draft.relations, start=1):
        if source in identity and target in identity:
            PreviewWorld(install, runtime, host, instance_id, created.root_branch_id).step(
                PREVIEW_CREATE_RELATION,
                {
                    "relation_id": f"rel_preview_{index}",
                    "source_id": identity[source],
                    "target_id": identity[target],
                    "relation_type": relation_type,
                },
            )
    return PreviewWorld(install, runtime, host, instance_id, created.root_branch_id)
