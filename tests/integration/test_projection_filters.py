"""G05D: projection API, perspective & rights filters.

Projections are server-composed DTOs: debug requires privilege, sealed payloads
are redacted, private beliefs never leak, restricted places are redacted
without permission.
"""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.epistemic.components import belief_component
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.material.resolver import register_material_resolvers
from wanxiang_substrate.projection.errors import UnauthorizedProjection
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService
from wanxiang_substrate.spatial.components import (
    place_component,
    position_component,
)
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_proj")
HALL = EntityId("hall")
VAULT = EntityId("vault")
ALICE = EntityId("alice")
BOB = EntityId("bob")
LETTER = EntityId("letter_sealed")
PAYLOAD = EntityId("payload_sealed")


def make_proj_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        register_epistemic_resolvers(registry)
        registry.register("proj.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=HALL,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "hall"),),
            ),
            EntityCreate(
                entity_id=VAULT,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "vault", privacy="restricted"),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HALL),),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(position_component(BOB, HALL),),
            ),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, ALICE),
                ),
            ),
            EntityCreate(
                entity_id=PAYLOAD,
                entity_type="material.info_payload",
                components=(
                    info_payload_component(LETTER, "ref://top_secret/body", state="sealed"),
                ),
            ),
            EntityCreate(
                entity_id=EntityId("belief_private"),
                entity_type="epistemic.belief",
                components=(
                    belief_component(
                        EntityId("belief_private"),
                        ALICE,
                        "vault_has_gold",
                        confidence=0.8,
                        at_ticks=5,
                        source_ref="ref://alice_observation",
                    ),
                ),
            ),
        )
    )


def _grant(runtime: WorldRuntime, w: CreateWorldResult, revision: int, actor: str) -> int:
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_grant_enter"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(revision),
            action_type="institution.grant_permission",
            payload={
                "permission_id": f"perm_enter_{actor}",
                "actor_id": actor,
                "permission": "enter",
                "target": "global",
                "granter_id": "admin",
                "start_ticks": 0,
                "end_ticks": 100_000,
            },
            world_time=WorldTime(revision + 1),
        )
    )
    return revision + 1


@pytest.fixture
def proj_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_proj_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_proj_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="proj.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


def _project(
    runtime: WorldRuntime, w: CreateWorldResult, actor: str, mode: str = "text", admin: bool = False
):
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    request = ProjectionRequest(
        session_id="s_proj",
        actor_id=actor,
        branch_id=w.root_branch_id,
        mode=mode,  # type: ignore[arg-type]
    )
    return ProjectionService(state, admin=admin).compose(request)


@pytest.mark.integration
def test_debug_projection_requires_admin(
    proj_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = proj_world
    with pytest.raises(UnauthorizedProjection):
        _project(runtime, w, ALICE.value, mode="debug", admin=False)
    snapshot = _project(runtime, w, ALICE.value, mode="debug", admin=True)
    assert snapshot.mode == "debug"


@pytest.mark.integration
def test_sealed_payload_is_redacted(
    proj_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = proj_world
    snapshot = _project(runtime, w, ALICE.value)
    item = snapshot.entity(PAYLOAD.value)
    assert item is not None
    assert item.redacted is True
    assert item.redaction_reason == "sealed_payload"
    # The secret content ref must never surface.
    assert "top_secret" not in str(item.fields)


@pytest.mark.integration
def test_private_belief_never_leaks_to_other_actor(
    proj_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = proj_world
    bob_view = _project(runtime, w, BOB.value)
    assert bob_view.entity("belief_private") is None
    alice_view = _project(runtime, w, ALICE.value)
    private = alice_view.entity("belief_private")
    assert private is not None
    assert private.label == "model_inference"


@pytest.mark.integration
def test_restricted_place_redacted_without_permission(
    proj_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = proj_world
    bob_view = _project(runtime, w, BOB.value)
    assert bob_view.entity(VAULT.value).redacted is True  # type: ignore[union-attr]
    # Grant alice the enter permission; the vault becomes visible to her.
    _grant(runtime, w, 1, ALICE.value)
    alice_view = _project(runtime, w, ALICE.value)
    vault = alice_view.entity(VAULT.value)
    assert vault is not None and vault.redacted is False
