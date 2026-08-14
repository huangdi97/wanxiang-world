"""G32A: Evolution Policy Stack (World/Platform layered policies)."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_substrate.evolution import (
    EvolutionPolicyStack,
    PlatformPolicy,
    WorldPolicy,
    reject_world_platform_mutation,
)


@pytest.mark.unit
def test_world_policy_cannot_mutate_platform() -> None:
    stack = EvolutionPolicyStack()
    stack.assert_world_cannot_mutate_platform()  # no platform handle by construction
    with pytest.raises(PermissionDenied):
        reject_world_platform_mutation("activate_runtime_provider")
    with pytest.raises(PermissionDenied):
        reject_world_platform_mutation("amend_platform_constitution")


@pytest.mark.unit
def test_world_and_platform_policies_are_independent() -> None:
    world = WorldPolicy(promotion_policy="candidate_only", version=1)
    platform = PlatformPolicy(constitution_policy="immutable_root", version=3)
    stack = EvolutionPolicyStack(world=world, platform=platform)
    # World policy config never affects platform policy and vice versa.
    assert stack.world.promotion_policy == "candidate_only"
    assert stack.platform.constitution_policy == "immutable_root"
    assert stack.world.version == 1
    assert stack.platform.version == 3


@pytest.mark.unit
def test_policy_versions_are_traceable() -> None:
    stack = EvolutionPolicyStack(world=WorldPolicy(version=2), platform=PlatformPolicy(version=5))
    versions = stack.versions()
    assert versions["world"] == 2
    assert versions["platform"] == 5
    # Every world policy layer traces to the world version.
    for layer in ("actor", "capability", "social", "institution", "ontology", "law", "promotion"):
        assert versions[layer] == 2
