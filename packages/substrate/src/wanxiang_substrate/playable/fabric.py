"""R7 World Experience / Distribution Fabric contracts.

These objects describe how a World is entered, interacted with, projected and
distributed. They contain references and product policy only; none can own
canonical state or bypass the existing Playable/Commit boundary.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.experience import ExperiencePackage

ExperienceType = Literal[
    "explore",
    "roleplay",
    "observe",
    "direct",
    "investigate",
    "learn",
    "build",
    "simulate",
    "experiment",
    "agent_benchmark",
    "hybrid_reality",
]
ProjectionCapability = Literal["text", "map_2d", "scene_3d", "video", "ar", "vr"]
DistributionChannel = Literal[
    "web",
    "toy",
    "mini_program",
    "app",
    "steam",
    "museum_kiosk",
    "vr_ar",
    "embedded",
    "api_agent",
]


def _unique_non_empty(values: tuple[str, ...], name: str, *, allow_empty: bool = False) -> None:
    if not allow_empty and not values:
        raise ContractError(f"{name} must not be empty")
    if any(not value.strip() for value in values):
        raise ContractError(f"{name} must contain non-empty values")
    if len(set(values)) != len(values):
        raise ContractError(f"{name} must not contain duplicates")


@dataclass(frozen=True, slots=True)
class InteractionProfile:
    """How user/agent inputs become proposals before World authority."""

    profile_id: str
    version: int = 1
    input_models: tuple[str, ...] = ("natural_language", "ui")
    allowed_actions: tuple[str, ...] = ("set_status",)
    authority_mode: Literal["proposal_only", "world_authority"] = "world_authority"

    def __post_init__(self) -> None:
        if not self.profile_id.strip() or self.version < 1:
            raise ContractError("interaction profile id/version are required")
        _unique_non_empty(self.input_models, "input_models")
        _unique_non_empty(self.allowed_actions, "allowed_actions")
        if self.authority_mode not in {"proposal_only", "world_authority"}:
            raise ContractError(f"unsupported authority_mode {self.authority_mode!r}")


@dataclass(frozen=True, slots=True)
class ProjectionProfile:
    """Replaceable projection policy; reads World truth and owns no write authority."""

    profile_id: str
    provider_ref: str
    capabilities: tuple[ProjectionCapability, ...]
    version: int = 1
    state_source: Literal["canonical_read_model", "committed_state_diff"] = (
        "canonical_read_model"
    )
    write_authority: Literal["none"] = "none"
    fallback: ProjectionCapability = "text"

    def __post_init__(self) -> None:
        if not self.profile_id.strip() or not self.provider_ref.strip() or self.version < 1:
            raise ContractError("projection profile id/provider/version are required")
        _unique_non_empty(self.capabilities, "projection capabilities")
        if self.state_source not in {"canonical_read_model", "committed_state_diff"}:
            raise ContractError(f"unsupported projection state_source {self.state_source!r}")
        if self.write_authority != "none":
            raise ContractError("projection profiles can never own World write authority")
        if self.fallback not in self.capabilities:
            raise ContractError("projection fallback must be one of the declared capabilities")


@dataclass(frozen=True, slots=True)
class DistributionAdapter:
    """Declared terminal/channel capability; never a canonical-state owner."""

    adapter_id: str
    channel: DistributionChannel
    version: int = 1
    capability_matrix: tuple[str, ...] = ()
    input_model: str = "web"
    auth_model: str = "wanxiang_session"
    storage_model: str = "cache_only"
    sharing: str = "deep_link"
    content_policy: str = "inherit_experience"
    asset_limits: str = "profile_defined"
    latency_budget: str = "best_effort"
    telemetry: tuple[str, ...] = ("entry", "error", "latency")
    update_channel: str = "versioned"
    rights_restrictions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.adapter_id.strip() or self.version < 1:
            raise ContractError("distribution adapter id/version are required")
        for name in (
            "input_model",
            "auth_model",
            "storage_model",
            "sharing",
            "content_policy",
            "asset_limits",
            "latency_budget",
            "update_channel",
        ):
            if not str(getattr(self, name)).strip():
                raise ContractError(f"{name} must be non-empty")
        _unique_non_empty(self.capability_matrix, "capability_matrix", allow_empty=True)
        _unique_non_empty(self.telemetry, "telemetry")
        _unique_non_empty(self.rights_restrictions, "rights_restrictions", allow_empty=True)
        if self.storage_model not in {"none", "cache_only", "local_preferences"}:
            raise ContractError("distribution storage cannot be canonical-state storage")


@dataclass(frozen=True, slots=True)
class ExperienceBlueprint:
    """First-class product description for one way to experience a World."""

    experience_id: str
    world_ref: str
    interaction_profile_ref: str
    projection_profile_ref: str
    version: int = 1
    locale_default: str = "zh-CN"
    experience_type: ExperienceType = "roleplay"
    entry_mode: str = "select_or_create_character"
    default_scenario: str = "default"
    continue_enabled: bool = True
    summary_on_return: bool = True
    same_worldline_required: bool = True
    world_changes_visibility: str = "player_friendly"
    raw_debug_visibility: str = "studio_only"
    sharing: str = "allowed"
    derivative_creation: str = "review_required"
    distribution_adapters: tuple[str, ...] = ("web",)
    metrics: tuple[str, ...] = (
        "comprehension",
        "agency",
        "consequence_visibility",
        "continuation_quality",
    )

    def __post_init__(self) -> None:
        for name in (
            "experience_id",
            "world_ref",
            "interaction_profile_ref",
            "projection_profile_ref",
            "locale_default",
            "entry_mode",
            "default_scenario",
        ):
            if not str(getattr(self, name)).strip():
                raise ContractError(f"{name} must be non-empty")
        if self.version < 1:
            raise ContractError("experience blueprint version must be positive")
        _unique_non_empty(self.distribution_adapters, "distribution_adapters")
        _unique_non_empty(self.metrics, "metrics")
        if self.raw_debug_visibility != "studio_only":
            raise ContractError("raw debug visibility is Studio-only")

    @classmethod
    def from_package(
        cls,
        package: ExperiencePackage,
        *,
        interaction_profile_ref: str,
        experience_type: ExperienceType = "roleplay",
        locale_default: str = "zh-CN",
        distribution_adapters: tuple[str, ...] = ("web",),
    ) -> ExperienceBlueprint:
        return cls(
            experience_id=package.experience_id,
            world_ref=package.world_package_ref,
            interaction_profile_ref=interaction_profile_ref,
            projection_profile_ref=package.projection_profile_ref,
            version=package.version,
            locale_default=locale_default,
            experience_type=experience_type,
            default_scenario=package.scenario_ref,
            continue_enabled=package.embodiment_policy.resume_after_leave,
            distribution_adapters=distribution_adapters,
        )


@dataclass(frozen=True, slots=True)
class DistributionBuild:
    """Deterministic build descriptor; contains refs, never world state."""

    build_id: str
    experience_id: str
    experience_version: int
    world_ref: str
    adapter_id: str
    adapter_version: int
    channel: DistributionChannel
    locale: str


@dataclass(frozen=True, slots=True)
class WorldExperienceCard:
    """Safe discovery/entry projection for one Experience."""

    world_ref: str
    experience_id: str
    title: str
    promise: str
    experience_type: ExperienceType
    recommended_role: str
    continue_enabled: bool
    locale: str
    sharing: str
    deep_link: str = ""


def build_distribution(
    blueprint: ExperienceBlueprint,
    adapter: DistributionAdapter,
) -> DistributionBuild:
    """Build a deterministic channel descriptor without duplicating World state."""
    if adapter.adapter_id not in blueprint.distribution_adapters:
        raise ContractError(
            f"adapter {adapter.adapter_id!r} is not enabled by {blueprint.experience_id!r}"
        )
    payload = {
        "experience_id": blueprint.experience_id,
        "experience_version": blueprint.version,
        "world_ref": blueprint.world_ref,
        "adapter_id": adapter.adapter_id,
        "adapter_version": adapter.version,
        "channel": adapter.channel,
        "locale": blueprint.locale_default,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
    ).hexdigest()
    return DistributionBuild(
        build_id=f"dist:{digest}",
        experience_id=blueprint.experience_id,
        experience_version=blueprint.version,
        world_ref=blueprint.world_ref,
        adapter_id=adapter.adapter_id,
        adapter_version=adapter.version,
        channel=adapter.channel,
        locale=blueprint.locale_default,
    )


def experience_card(
    blueprint: ExperienceBlueprint,
    *,
    title: str,
    promise: str,
    recommended_role: str,
    deep_link: str = "",
) -> WorldExperienceCard:
    if not title.strip() or not promise.strip() or not recommended_role.strip():
        raise ContractError("experience card title/promise/recommended_role are required")
    return WorldExperienceCard(
        world_ref=blueprint.world_ref,
        experience_id=blueprint.experience_id,
        title=title,
        promise=promise,
        experience_type=blueprint.experience_type,
        recommended_role=recommended_role,
        continue_enabled=blueprint.continue_enabled,
        locale=blueprint.locale_default,
        sharing=blueprint.sharing,
        deep_link=deep_link,
    )


__all__ = [
    "DistributionAdapter",
    "DistributionBuild",
    "ExperienceBlueprint",
    "InteractionProfile",
    "ProjectionProfile",
    "WorldExperienceCard",
    "build_distribution",
    "experience_card",
]
