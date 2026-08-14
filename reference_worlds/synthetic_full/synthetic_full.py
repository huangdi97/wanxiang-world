"""Synthetic Full Reference World Pack (G15B) — explicitly synthetic content.

This package lives outside Core and is built/installed/instantiated only through
public Wanxiang contracts (package SDK, application runtime, substrate domain
builders). All people/places/organizations are invented; nothing here is real
or presented as factual. Source provenance is synthetic and source-gate
semantics are still exercised.

Contents: 5 places, 4 people with bodies/roles/membership in a guild, 3 objects
(pouch with custody, sealed letter payload, market stall), a clock + recurring
duty schedule, public/private beliefs, scenario seeds (autonomous living,
human takeover, branching, failure) and worldness eval cases.
"""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.body.components import condition_component
from wanxiang_substrate.epistemic.components import belief_component
from wanxiang_substrate.institution.components import (
    duty_component,
    membership_component,
    role_component,
)
from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.population.components import resolution_component
from wanxiang_substrate.spatial.components import place_component, position_component
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_sf")
DAY = 100

SQUARE = EntityId("sf_square")
MARKET = EntityId("sf_market")
TEMPLE = EntityId("sf_temple")
GUILD_HALL = EntityId("sf_guild_hall")
HOUSE = EntityId("sf_house")
MAYOR = EntityId("sf_mayor")
SMITH = EntityId("sf_smith")
APPRENTICE = EntityId("sf_apprentice")
VISITOR = EntityId("sf_visitor")
GUILD = EntityId("sf_guild")
ROLE_MAYOR = EntityId("sf_role_mayor")
ROLE_GUILD_MASTER = EntityId("sf_role_guild_master")
ROLE_APPRENTICE = EntityId("sf_role_apprentice")
DUTY_ROUNDS = EntityId("sf_duty_rounds")
POUCH = EntityId("sf_pouch")
LETTER = EntityId("sf_letter")
STALL = EntityId("sf_stall")
PUBLIC_BELIEF = EntityId("sf_belief_public")
PRIVATE_BELIEF = EntityId("sf_belief_private")


def build_manifests():
    from wanxiang_substrate.packages.model import UNTRUSTED, PackageManifest, SemanticVersion

    domain = PackageManifest(
        package_id="sf-domain",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="Synthetic Full Domain",
        executable_trust=UNTRUSTED,
    ).with_hash()
    world = PackageManifest(
        package_id="sf-world",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Synthetic Full World",
        dependencies=(("sf-domain", "==1.0.0"),),
        executable_trust=UNTRUSTED,
    ).with_hash()
    scenario = PackageManifest(
        package_id="sf-scenario",
        kind="scenario",
        version=SemanticVersion(1, 0, 0),
        name="Synthetic Full Scenario",
        dependencies=(("sf-world", "==1.0.0"), ("sf-domain", "==1.0.0")),
        executable_trust=UNTRUSTED,
    ).with_hash()
    return domain, world, scenario


def build_registry():
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    registry = InMemoryPackageRegistry()
    for manifest in build_manifests():
        registry.register(manifest)
    return registry


def install_pack(registry=None):
    """Install through the public package path (no Core modification)."""
    from wanxiang_substrate.packages.install import PackageInstaller

    registry = registry or build_registry()
    return PackageInstaller().install(
        registry,
        "sf-scenario",
        install_id="install_sf",
        rights_refs=("ref://sf-rights",),
        evidence_refs=("ref://sf-evidence",),
        asset_refs=("ref://sf-assets",),
    )


def instantiate_delta() -> ProposedWorldDelta:
    """Create all synthetic world entities in one authoritative proposal."""
    ops = [
        EntityCreate(
            entity_id=CLOCK_ENTITY,
            entity_type="temporal.clock",
            components=(clock_component(0, paused=False),),
        ),
        EntityCreate(
            entity_id=SQUARE,
            entity_type="spatial.place",
            components=(place_component(SQUARE, "town_square", capacity=100, privacy="public"),),
        ),
        EntityCreate(
            entity_id=MARKET,
            entity_type="spatial.place",
            components=(place_component(MARKET, "market", capacity=60, privacy="public"),),
        ),
        EntityCreate(
            entity_id=TEMPLE,
            entity_type="spatial.place",
            components=(place_component(TEMPLE, "temple", capacity=40, privacy="public"),),
        ),
        EntityCreate(
            entity_id=GUILD_HALL,
            entity_type="spatial.place",
            components=(
                place_component(GUILD_HALL, "guild_hall", capacity=30, privacy="restricted"),
            ),
        ),
        EntityCreate(
            entity_id=HOUSE,
            entity_type="spatial.place",
            components=(place_component(HOUSE, "mayor_house", capacity=10, privacy="restricted"),),
        ),
    ]
    people = [
        (MAYOR, 100, 90, 80, 100, "duty", 25),
        (SMITH, 100, 85, 75, 100, "focus", 30),
        (APPRENTICE, 95, 80, 85, 100, "lightweight", 50),
        (VISITOR, 100, 95, 90, 100, "lightweight", 60),
    ]
    for entity_id, health, energy, sleep, mobility, strategy, rate in people:
        ops.append(
            EntityCreate(
                entity_id=entity_id,
                entity_type="person",
                components=(
                    condition_component(
                        health=health, energy=energy, sleep=sleep, mobility=mobility
                    ),
                    resolution_component(entity_id, strategy, rate_ticks=rate),
                    position_component(entity_id, SQUARE),
                ),
            )
        )
    ops += [
        EntityCreate(
            entity_id=GUILD,
            entity_type="institution.organization",
            components=(),
        ),
        EntityCreate(
            entity_id=ROLE_MAYOR,
            entity_type="institution.role",
            components=(role_component(ROLE_MAYOR, "mayor", ("enter", "administer")),),
        ),
        EntityCreate(
            entity_id=ROLE_GUILD_MASTER,
            entity_type="institution.role",
            components=(role_component(ROLE_GUILD_MASTER, "guild_master", ("enter", "trade")),),
        ),
        EntityCreate(
            entity_id=ROLE_APPRENTICE,
            entity_type="institution.role",
            components=(role_component(ROLE_APPRENTICE, "apprentice", ("enter",)),),
        ),
        EntityCreate(
            entity_id=EntityId("sf_mem_mayor"),
            entity_type="institution.membership",
            components=(
                membership_component(EntityId("sf_mem_mayor"), MAYOR, ROLE_MAYOR, GUILD, 0),
            ),
        ),
        EntityCreate(
            entity_id=EntityId("sf_mem_smith"),
            entity_type="institution.membership",
            components=(
                membership_component(EntityId("sf_mem_smith"), SMITH, ROLE_GUILD_MASTER, GUILD, 0),
            ),
        ),
        EntityCreate(
            entity_id=EntityId("sf_mem_app"),
            entity_type="institution.membership",
            components=(
                membership_component(EntityId("sf_mem_app"), APPRENTICE, ROLE_APPRENTICE, GUILD, 0),
            ),
        ),
        EntityCreate(
            entity_id=DUTY_ROUNDS,
            entity_type="institution.duty",
            components=(duty_component(DUTY_ROUNDS, SMITH, "guild_rounds", due_ticks=DAY),),
        ),
        EntityCreate(
            entity_id=POUCH,
            entity_type="material.item",
            components=(
                item_component(POUCH, "coin_pouch", state="intact"),
                custody_component(POUCH, MAYOR),
                position_component(POUCH, GUILD_HALL),
            ),
        ),
        EntityCreate(
            entity_id=LETTER,
            entity_type="material.item",
            components=(
                item_component(LETTER, "letter", state="sealed"),
                info_payload_component(LETTER, "ref://sf-letter-payload", state="sealed"),
                custody_component(LETTER, MAYOR),
                position_component(LETTER, HOUSE),
            ),
        ),
        EntityCreate(
            entity_id=STALL,
            entity_type="material.item",
            components=(
                item_component(STALL, "market_stall", state="intact"),
                position_component(STALL, MARKET),
            ),
        ),
        EntityCreate(
            entity_id=PUBLIC_BELIEF,
            entity_type="epistemic.belief",
            components=(
                belief_component(PUBLIC_BELIEF, MAYOR, "the market opens at dawn", 0.9, at_ticks=0),
            ),
        ),
        EntityCreate(
            entity_id=PRIVATE_BELIEF,
            entity_type="epistemic.belief",
            components=(
                belief_component(
                    PRIVATE_BELIEF, MAYOR, "a private plan for the guild", 0.7, at_ticks=0
                ),
            ),
        ),
    ]
    return ProposedWorldDelta(operations=tuple(ops))


def register_resolvers(registry) -> None:
    """Register the substrate resolvers plus the synthetic instantiate action."""
    from wanxiang_substrate.body.resolver import register_body_resolvers
    from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
    from wanxiang_substrate.institution.resolver import register_institution_resolvers
    from wanxiang_substrate.material.resolver import register_material_resolvers
    from wanxiang_substrate.population.resolver import register_population_resolvers
    from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
    from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

    register_temporal_resolvers(registry)
    register_body_resolvers(registry)
    register_institution_resolvers(registry)
    register_material_resolvers(registry)
    register_population_resolvers(registry)
    register_spatial_resolvers(registry)
    register_epistemic_resolvers(registry)
    registry.register("sf.instantiate", lambda _command, _state: instantiate_delta())


def make_runtime(path):
    from tests.conftest import make_world_runtime

    return make_world_runtime(path, extra_resolvers=register_resolvers)


def instantiate_command(branch: BranchId, revision: int = 0) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId("sf_instantiate"),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="sf.instantiate",
        payload={},
        world_time=WorldTime(revision + 1),
    )
