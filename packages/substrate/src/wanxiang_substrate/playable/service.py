"""Shared playable application facade for CLI, API, and Studio routes."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger
from wanxiang_substrate.assets.book_scene_visual import (
    _SceneImageProvider,
    _SceneVisualAsset,
    _VisualAssetCache,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.catalog import WorldPlaza
from wanxiang_substrate.playable.entry import CharacterEntryService
from wanxiang_substrate.playable.experience import ExperiencePackage
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.service_action import _perform_action
from wanxiang_substrate.playable.service_history import _history
from wanxiang_substrate.playable.service_lifecycle import (
    _continue_instance,
    _enter,
    _leave,
    _observe,
)
from wanxiang_substrate.playable.service_model import PlayableActionResult
from wanxiang_substrate.playable.service_registration import (
    _register_package,
    _register_profile,
)
from wanxiang_substrate.playable.service_replay import _replay_at
from wanxiang_substrate.playable.service_visual import (
    _attach_spatial_assets,
    _materialize_visual_place,
    _visible_spatial_assets,
    _visible_spatial_projection_frames,
    _visible_visual_assets,
    _visual_access_allowed,
)
from wanxiang_substrate.playable.service_worldline import _fork_worldline
from wanxiang_substrate.playable.service_worldlines import _compare_worldlines, _worldlines
from wanxiang_substrate.playable.store import InMemoryPlayableStore, PlayableStore
from wanxiang_substrate.preview import PreviewInstall, PreviewRuntimePort


class PlayableService:
    """One composition facade; canonical state remains in the injected runtime."""

    def __init__(
        self,
        runtime: PreviewRuntimePort,
        store: PlayableStore | None = None,
        *,
        visual_cache: _VisualAssetCache | None = None,
    ) -> None:
        self.runtime = runtime
        self.store = store or InMemoryPlayableStore()
        self._visual_cache = visual_cache or _VisualAssetCache()
        self._visual_assets: dict[str, tuple[_SceneVisualAsset, ...]] = {}
        self._visual_asset_refs: dict[str, tuple[AssetRef, ...]] = {}
        self._visual_budget: VisualBudgetLedger | None = None
        self._visual_deferred_limit: int = 0
        self._spatial_asset_refs: dict[str, dict[str, tuple[AssetRef, ...]]] = {}
        self._spatial_projection_frames: dict[str, dict[str, _SpatialProjectionFrame]] = {}
        self.plaza = WorldPlaza(self.store)
        self.entry = CharacterEntryService(self.store)
        self._packages: dict[str, WorldPackageDraft] = {}
        self._experiences: dict[str, ExperiencePackage] = {}
        self._installs: dict[str, PreviewInstall] = {}

    @property
    def packages(self) -> Mapping[str, WorldPackageDraft]:
        return self._packages

    def visual_access_allowed(self, profile_id: str, *, viewer_id: str) -> bool:
        """Gate every source-derived visual surface, including atlas and topology."""

        return _visual_access_allowed(self, profile_id, viewer_id=viewer_id)

    def visual_assets(
        self,
        profile_id: str,
        *,
        viewer_id: str,
    ) -> tuple[_SceneVisualAsset, ...]:
        """Return source-derived visual assets allowed for this viewer."""

        return _visible_visual_assets(self, profile_id, viewer_id=viewer_id)

    def spatial_assets(self, profile_id: str, *, viewer_id: str) -> dict[str, tuple[AssetRef, ...]]:
        return _visible_spatial_assets(self, profile_id, viewer_id=viewer_id)

    def spatial_projection_frames(
        self,
        profile_id: str,
        *,
        viewer_id: str,
    ) -> dict[str, _SpatialProjectionFrame]:
        return _visible_spatial_projection_frames(self, profile_id, viewer_id=viewer_id)

    def materialize_visual_place(
        self,
        profile_id: str,
        place_name: str,
        *,
        viewer_id: str,
        provider: _SceneImageProvider | None = None,
        allow_network: bool = False,
        max_cost_units: int = 0,
        max_deferred_generations: int = 0,
        fallback_to_t0: bool = True,
    ) -> _VisualMaterialization:
        return _materialize_visual_place(
            self,
            profile_id,
            place_name,
            viewer_id=viewer_id,
            provider=provider,
            allow_network=allow_network,
            max_cost_units=max_cost_units,
            max_deferred_generations=max_deferred_generations,
            fallback_to_t0=fallback_to_t0,
        )

    def attach_spatial_assets(
        self,
        profile_id: str,
        scene_key: str,
        asset_refs: tuple[AssetRef, ...],
        projection_frame: _SpatialProjectionFrame | None = None,
    ) -> None:
        """Attach verified T3 assets and projection metadata to the derived Player catalog."""
        _attach_spatial_assets(
            self,
            profile_id,
            scene_key,
            asset_refs,
            projection_frame=projection_frame,
        )

    def register_package(
        self,
        package: WorldPackageDraft,
        *,
        owner_id: str = "",
        visibility: str = "public",
        display_name: str | None = None,
        description: str | None = None,
        scenario_name: str | None = None,
        opening_hint: str | None = None,
        allowed_actions: tuple[str, ...] = ("set_status",),
        visual_provider: _SceneImageProvider | None = None,
        visual_allow_network: bool = False,
        visual_max_cost_units: int = 0,
    ) -> PlayableWorldProfile:
        return _register_package(
            self,
            package,
            owner_id=owner_id,
            visibility=visibility,
            display_name=display_name,
            description=description,
            scenario_name=scenario_name,
            opening_hint=opening_hint,
            allowed_actions=allowed_actions,
            visual_provider=visual_provider,
            visual_allow_network=visual_allow_network,
            visual_max_cost_units=visual_max_cost_units,
        )

    def register_profile(
        self,
        profile: PlayableWorldProfile,
        package: WorldPackageDraft,
        experience: ExperiencePackage | None = None,
        *,
        visual_provider: _SceneImageProvider | None = None,
        visual_allow_network: bool = False,
        visual_max_cost_units: int = 0,
    ) -> None:
        _register_profile(
            self,
            profile,
            package,
            experience,
            visual_provider=visual_provider,
            visual_allow_network=visual_allow_network,
            visual_max_cost_units=visual_max_cost_units,
        )

    def enter(
        self,
        profile_id: str,
        *,
        viewer_id: str,
        mode: str,
        session_id: str,
        character_id: str = "",
    ) -> dict[str, object]:
        return _enter(
            self,
            profile_id,
            viewer_id=viewer_id,
            mode=mode,
            session_id=session_id,
            character_id=character_id,
        )

    def continue_instance(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        return _continue_instance(self, instance_id, viewer_id=viewer_id)

    def leave(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        return _leave(self, instance_id, viewer_id=viewer_id)

    def observe(self, instance_id: str, viewer_id: str) -> dict[str, object]:
        return _observe(self, instance_id, viewer_id)

    def replay_at(
        self,
        instance_id: str,
        *,
        viewer_id: str,
        at_ticks: int,
        locale: str | None = None,
    ) -> dict[str, object]:
        """Read the instance as of a past world tick without changing canon."""
        return _replay_at(
            self,
            instance_id,
            viewer_id=viewer_id,
            at_ticks=at_ticks,
            locale=locale,
        )

    def history(
        self,
        instance_id: str,
        *,
        viewer_id: str,
        limit: int = 200,
        before: int | None = None,
        locale: str | None = None,
    ) -> dict[str, object]:
        """Return the player-safe chronicle, newest first."""
        return _history(
            self,
            instance_id,
            viewer_id=viewer_id,
            limit=limit,
            before=before,
            locale=locale,
        )

    def fork_worldline(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        """Fork the owned branch at its head into a detached Player worldline."""
        return _fork_worldline(self, instance_id, viewer_id=viewer_id)

    def worldlines(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        """List the viewer's worldlines for this instance's runtime branch set."""
        return _worldlines(self, instance_id, viewer_id=viewer_id)

    def compare_worldlines(
        self,
        instance_id: str,
        *,
        other_instance_id: str,
        viewer_id: str,
        locale: str | None = None,
    ) -> dict[str, object]:
        """Compare two owned worldlines of the same runtime instance."""
        return _compare_worldlines(
            self,
            instance_id,
            other_instance_id=other_instance_id,
            viewer_id=viewer_id,
            locale=locale,
        )

    def action(
        self,
        instance_id: str,
        *,
        viewer_id: str,
        text: str = "",
        action_type: str = "",
        payload: dict[str, object] | None = None,
    ) -> PlayableActionResult:
        return _perform_action(
            self,
            instance_id,
            viewer_id=viewer_id,
            text=text,
            action_type=action_type,
            payload=payload,
        )
