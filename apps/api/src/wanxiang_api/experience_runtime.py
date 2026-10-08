"""R7 ExperienceRuntime: coordinate entry/continue/interaction/projection/distribution.

This is an experience/session coordinator, not a second Reality runtime. It owns
no canonical state or event store. Every mutation is delegated to the existing
ExperiencePlayerService, which submits through WorldRuntime / Commit Authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.playable.fabric import (
    DistributionAdapter,
    DistributionBuild,
    ExperienceBlueprint,
    InteractionProfile,
    build_distribution,
)

from wanxiang_api.experience_player_service import ExperiencePlayerService


@dataclass(frozen=True, slots=True)
class ExperienceSessionView:
    """Player-facing session projection derived from canonical World state."""

    experience_id: str
    world_id: str
    branch_id: str
    actor_id: str
    revision: int
    locale: str
    projection: Any
    distributions: tuple[DistributionBuild, ...]


@dataclass(frozen=True, slots=True)
class ExperienceActionView:
    """Committed action result plus refreshed player projection."""

    experience_id: str
    world_id: str
    branch_id: str
    revision: int
    state_hash: str
    duplicate: bool
    projection: Any


class ExperienceRuntime:
    """Coordinate one ExperienceBlueprint over the authoritative player path."""

    def __init__(
        self,
        player: ExperiencePlayerService,
        blueprint: ExperienceBlueprint,
        interaction: InteractionProfile,
        adapters: tuple[DistributionAdapter, ...],
    ) -> None:
        if blueprint.interaction_profile_ref != interaction.profile_id:
            raise ValueError("ExperienceBlueprint interaction profile does not match")
        adapter_ids = tuple(adapter.adapter_id for adapter in adapters)
        if set(adapter_ids) != set(blueprint.distribution_adapters):
            raise ValueError("ExperienceRuntime adapters must exactly match blueprint adapters")
        if len(set(adapter_ids)) != len(adapter_ids):
            raise ValueError("ExperienceRuntime adapters must be unique")
        self._player = player
        self._blueprint = blueprint
        self._interaction = interaction
        self._distributions = tuple(build_distribution(blueprint, adapter) for adapter in adapters)

    @property
    def blueprint(self) -> ExperienceBlueprint:
        return self._blueprint

    def enter(self, instance_id: WorldInstanceId, actor_id: str) -> ExperienceSessionView:
        """Enter the root/default branch and render the current canonical projection."""
        branch_id = self._player.start_session(instance_id)
        return self.continue_session(instance_id, branch_id, actor_id)

    def continue_session(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        actor_id: str,
    ) -> ExperienceSessionView:
        """Resume the same worldline; no local/client truth is reconstructed."""
        projection = self._player.project(instance_id, branch_id, actor_id)
        revision = _projection_revision(projection)
        return ExperienceSessionView(
            experience_id=self._blueprint.experience_id,
            world_id=instance_id.value,
            branch_id=branch_id.value,
            actor_id=actor_id,
            revision=revision,
            locale=self._blueprint.locale_default,
            projection=projection,
            distributions=self._distributions,
        )

    def act(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        expected_revision: int,
        action_type: str,
        payload: dict[str, Any],
        actor_id: str,
        command_id: str | None = None,
    ) -> ExperienceActionView:
        """Route one allowed action through the existing Commit Authority path."""
        if action_type not in self._interaction.allowed_actions:
            raise ValidationRejected(
                f"action {action_type!r} is not allowed by interaction profile "
                f"{self._interaction.profile_id!r}"
            )
        result = self._player.act(
            instance_id,
            branch_id,
            expected_revision,
            action_type,
            payload,
            actor_id,
            command_id,
        )
        projection = self._player.project(instance_id, branch_id, actor_id)
        return ExperienceActionView(
            experience_id=self._blueprint.experience_id,
            world_id=instance_id.value,
            branch_id=branch_id.value,
            revision=int(result["revision"]),
            state_hash=str(result["state_hash"]),
            duplicate=bool(result["duplicate"]),
            projection=projection,
        )


def _projection_revision(projection: Any) -> int:
    """Read revision from the existing projection contract without owning state."""
    revision = getattr(projection, "revision", None)
    if isinstance(revision, int):
        return revision
    if hasattr(revision, "value") and isinstance(revision.value, int):
        return revision.value
    snapshot = getattr(projection, "snapshot", None)
    snapshot_revision = getattr(snapshot, "revision", None)
    if isinstance(snapshot_revision, int):
        return snapshot_revision
    if hasattr(snapshot_revision, "value") and isinstance(snapshot_revision.value, int):
        return snapshot_revision.value
    raise ValueError("player projection does not expose a revision")


__all__ = ["ExperienceActionView", "ExperienceRuntime", "ExperienceSessionView"]
