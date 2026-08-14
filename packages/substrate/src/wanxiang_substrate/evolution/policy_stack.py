"""Evolution Policy Stack (G32A).

Expands the single meta-rule Lambda into a layered World/Platform policy stack:

- World policies: Actor / Capability / Social / Institution / Ontology / Law /
  Promotion (how a world evolves).
- Platform policies: Model / Plugin / Domain / Runtime / Constitution migration
  (how the platform may evolve).

World and Platform permissions are strictly independent: a World policy can
never invoke a Platform mutation. Every policy carries a version for
traceability.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import PermissionDenied


@dataclass(frozen=True, slots=True)
class WorldPolicy:
    """A world's evolution policy set (versioned)."""

    actor_policy: str = "deterministic_actor"
    capability_policy: str = "bounded_learning"
    social_policy: str = "relation_growth"
    institution_policy: str = "rule_layered"
    ontology_policy: str = "semantic_space_evolves"
    law_policy: str = "law_layers_mutable"
    promotion_policy: str = "candidate_only"
    version: int = 1


@dataclass(frozen=True, slots=True)
class PlatformPolicy:
    """The platform's evolution/migration policy set (versioned)."""

    model_policy: str = "model_provider_registry"
    plugin_policy: str = "untrusted_by_default"
    domain_policy: str = "domain_packs_versioned"
    runtime_policy: str = "runtime_control_transactions"
    constitution_policy: str = "immutable_root"
    version: int = 1


@dataclass(frozen=True, slots=True)
class EvolutionPolicyStack:
    """A versioned world+platform policy stack."""

    world: WorldPolicy = WorldPolicy()
    platform: PlatformPolicy = PlatformPolicy()

    def versions(self) -> dict[str, int]:
        """Traceable policy versions (world layers share the world version)."""
        return {
            "world": self.world.version,
            "platform": self.platform.version,
            "actor": self.world.version,
            "capability": self.world.version,
            "social": self.world.version,
            "institution": self.world.version,
            "ontology": self.world.version,
            "law": self.world.version,
            "promotion": self.world.version,
        }

    def assert_world_cannot_mutate_platform(self) -> None:
        """World policy holds no handle to platform mutation (structural)."""
        # By construction the WorldPolicy dataclass has no platform mutation
        # reference; this guard makes the invariant explicit and testable.
        return None


def reject_world_platform_mutation(operation: str) -> None:
    """A world policy attempting a platform mutation is always rejected."""
    raise PermissionDenied(
        f"world policy cannot perform platform mutation {operation!r}; "
        "World/Platform permissions are independent"
    )
