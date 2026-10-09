"""Shared playable application facade for CLI, API, and Studio routes."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive

from wanxiang_substrate.assets.book_scene_visual import (
    _SceneImageProvider,
    _SceneVisualAsset,
    _VisualAssetCache,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.catalog import WorldPlaza
from wanxiang_substrate.playable.entry import CharacterEntryService
from wanxiang_substrate.playable.experience import (
    EntryMode,
    ExperiencePackage,
    experience_from_profile,
)
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.service_action import _perform_action
from wanxiang_substrate.playable.service_model import PlayableActionResult
from wanxiang_substrate.playable.service_session import _owned_instance, _save_instance
from wanxiang_substrate.playable.service_support import instance_dict
from wanxiang_substrate.playable.service_visual import (
    _attach_package_visuals,
    _materialize_visual_place,
    _visible_visual_assets,
    _visual_access_allowed,
)
from wanxiang_substrate.playable.store import (
    ExperienceInstanceRecord,
    InMemoryPlayableStore,
    PlayableStore,
)
from wanxiang_substrate.preview import PreviewInstall, PreviewRuntimePort, instantiate_preview


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
        self.plaza = WorldPlaza(self.store)
        self.entry = CharacterEntryService(self.store)
        self._packages: dict[str, WorldPackageDraft] = {}
        self._experiences: dict[str, ExperiencePackage] = {}
        self._installs: dict[str, PreviewInstall] = {}

    @property
    def packages(self) -> Mapping[str, WorldPackageDraft]:
        """Expose package metadata to read-only projection adapters."""

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

    def materialize_visual_place(
        self,
        profile_id: str,
        place_name: str,
        *,
        viewer_id: str,
        provider: _SceneImageProvider | None = None,
        allow_network: bool = False,
        max_cost_units: int = 0,
    ) -> _VisualMaterialization:
        """Generate/cache one already-source-grounded place without changing Canon."""

        return _materialize_visual_place(
            self,
            profile_id,
            place_name,
            viewer_id=viewer_id,
            provider=provider,
            allow_network=allow_network,
            max_cost_units=max_cost_units,
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
        profile = profile_from_world_package(
            package,
            owner_id=owner_id,
            visibility=visibility,
            display_name=display_name,
            description=description,
            scenario_name=scenario_name,
            opening_hint=opening_hint,
        )
        experience = experience_from_profile(profile, allowed_actions=allowed_actions)
        self.store.save_profile(profile)
        self._packages[profile.profile_id] = package
        self._experiences[profile.profile_id] = experience
        _attach_package_visuals(
            self,
            profile.profile_id,
            package,
            provider=visual_provider,
            allow_network=visual_allow_network,
            max_cost_units=visual_max_cost_units,
        )
        self._installs[profile.profile_id] = PreviewInstall(
            preview_id=f"playable_{len(self._installs) + 1}",
            package_id=package.package_id,
            draft_id=package.draft_id,
            package_hash=package.manifest.content_hash,
        )
        return profile

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
        profile.validate()
        self.store.save_profile(profile)
        self._packages[profile.profile_id] = package
        self._experiences[profile.profile_id] = experience or experience_from_profile(profile)
        _attach_package_visuals(
            self,
            profile.profile_id,
            package,
            provider=visual_provider,
            allow_network=visual_allow_network,
            max_cost_units=visual_max_cost_units,
        )
        self._installs[profile.profile_id] = PreviewInstall(
            f"playable_{len(self._installs) + 1}",
            package.package_id,
            package.draft_id,
            package.manifest.content_hash,
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
        self.plaza.require_access(profile_id, viewer_id)
        package = self._packages.get(profile_id)
        experience = self._experiences.get(profile_id)
        install = self._installs.get(profile_id)
        if package is None or experience is None or install is None:
            raise NotFound(f"playable package {profile_id!r} not found")
        world = instantiate_preview(self.runtime, package, install)
        receipt = self.entry.enter(
            experience,
            viewer_id=viewer_id,
            instance_id=world.instance_id.value,
            branch_id=world.branch_id.value,
            session_id=session_id,
            mode=cast(EntryMode, mode),
            character_id=character_id,
        )
        _save_instance(self, receipt, viewer_id, world.branch_id.value, updated_seq=1)
        return self.observe(receipt.instance_id, viewer_id)

    def continue_instance(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        record = _owned_instance(self, instance_id, viewer_id)
        profile = self.plaza.require_access(record.profile_id, viewer_id)
        experience = self._experiences.get(profile.profile_id)
        if experience is None:
            raise NotFound(f"experience {profile.profile_id!r} not found")
        next_session = f"resume_{record.instance_id}_{record.updated_seq + 1}"
        receipt = self.entry.enter(
            experience,
            viewer_id=viewer_id,
            instance_id=record.instance_id,
            branch_id=record.branch_id,
            session_id=next_session,
            mode=cast(EntryMode, record.mode),
            character_id=record.actor_id,
        )
        _save_instance(
            self,
            receipt,
            viewer_id,
            record.branch_id,
            updated_seq=record.updated_seq + 1,
        )
        return self.observe(instance_id, viewer_id)

    def leave(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        record = _owned_instance(self, instance_id, viewer_id)
        if record.session_id:
            self.entry.leave(record.session_id)
        state = self.runtime.current_state(
            WorldInstanceId(record.instance_id), BranchId(record.branch_id)
        )
        self.store.save_instance(
            ExperienceInstanceRecord(
                record.instance_id,
                record.profile_id,
                record.owner_id,
                record.branch_id,
                mode=record.mode,
                actor_id=record.actor_id,
                last_revision=state.revision.value,
                updated_seq=record.updated_seq + 1,
            )
        )
        return {"instance_id": instance_id, "status": "left", "revision": state.revision.value}

    def observe(self, instance_id: str, viewer_id: str) -> dict[str, object]:
        record = _owned_instance(self, instance_id, viewer_id)
        state = self.runtime.current_state(
            WorldInstanceId(record.instance_id), BranchId(record.branch_id)
        )
        return {
            "instance": instance_dict(record),
            "state": state_to_primitive(state),
            "state_hash": state.semantic_hash(),
            "revision": state.revision.value,
        }

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
