"""Shared playable application facade for CLI, API, and Studio routes."""

from __future__ import annotations

from typing import cast

from wanxiang_domain.errors import ContractError, NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.actions import IntentCompiler
from wanxiang_substrate.playable.catalog import WorldPlaza
from wanxiang_substrate.playable.entry import CharacterEntryService, EntryReceipt, active_lease
from wanxiang_substrate.playable.experience import (
    EntryMode,
    ExperiencePackage,
    experience_from_profile,
)
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.service_model import (
    EventLike,
    PlayableActionResult,
    SubmittedResult,
)
from wanxiang_substrate.playable.service_support import affordances, instance_dict
from wanxiang_substrate.playable.state_diff import CommittedStateDiff
from wanxiang_substrate.playable.store import (
    ExperienceInstanceRecord,
    InMemoryPlayableStore,
    PlayableStore,
)
from wanxiang_substrate.preview import PreviewInstall, PreviewRuntimePort, instantiate_preview


class PlayableService:
    """One composition facade; canonical state remains in the injected runtime."""

    def __init__(self, runtime: PreviewRuntimePort, store: PlayableStore | None = None) -> None:
        self.runtime = runtime
        self.store = store or InMemoryPlayableStore()
        self.plaza = WorldPlaza(self.store)
        self.entry = CharacterEntryService(self.store)
        self._packages: dict[str, WorldPackageDraft] = {}
        self._experiences: dict[str, ExperiencePackage] = {}
        self._installs: dict[str, PreviewInstall] = {}

    def register_package(
        self,
        package: WorldPackageDraft,
        *,
        owner_id: str = "",
        visibility: str = "public",
        display_name: str | None = None,
        allowed_actions: tuple[str, ...] = ("set_status",),
    ) -> PlayableWorldProfile:
        profile = profile_from_world_package(
            package,
            owner_id=owner_id,
            visibility=visibility,
            display_name=display_name,
        )
        experience = experience_from_profile(profile, allowed_actions=allowed_actions)
        self.store.save_profile(profile)
        self._packages[profile.profile_id] = package
        self._experiences[profile.profile_id] = experience
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
    ) -> None:
        profile.validate()
        self.store.save_profile(profile)
        self._packages[profile.profile_id] = package
        self._experiences[profile.profile_id] = experience or experience_from_profile(profile)
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
        self._save_instance(receipt, viewer_id, world.branch_id.value, updated_seq=1)
        return self.observe(receipt.instance_id, viewer_id)

    def continue_instance(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        record = self._owned_instance(instance_id, viewer_id)
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
        self._save_instance(
            receipt, viewer_id, record.branch_id, updated_seq=record.updated_seq + 1
        )
        return self.observe(instance_id, viewer_id)

    def leave(self, instance_id: str, *, viewer_id: str) -> dict[str, object]:
        record = self._owned_instance(instance_id, viewer_id)
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
        record = self._owned_instance(instance_id, viewer_id)
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
        record = self._owned_instance(instance_id, viewer_id)
        if record.mode != "embodiment" or not record.session_id or not record.actor_id:
            raise ContractError("only an embodied actor may submit a world action")
        if active_lease(self.entry, record.session_id) is None:
            raise ContractError("embodiment lease is not active")
        experience = self._experiences.get(record.profile_id)
        if experience is None:
            raise NotFound(f"experience {record.profile_id!r} not found")
        compiler = IntentCompiler(affordances(experience))
        common = {
            "session_id": record.session_id,
            "instance_id": record.instance_id,
            "branch_id": record.branch_id,
            "actor_id": record.actor_id,
        }
        result = (
            compiler.compile_structured(**common, action_type=action_type, payload=payload or {})
            if action_type
            else compiler.compile_text(**common, text=text)
        )
        if not result.proposal.accepted:
            raise ContractError(result.proposal.rejection_reason or result.proposal.clarification)
        before = self.runtime.current_state(
            WorldInstanceId(record.instance_id), BranchId(record.branch_id)
        )
        command = result.proposal.to_command(before.revision.value)
        submitted = cast(SubmittedResult, self.runtime.submit_command(command))
        event = cast(EventLike, submitted.event)
        event_id = str(getattr(event.event_id, "value", event.event_id))
        diff = CommittedStateDiff.from_states(
            before,
            submitted.state,
            event_id=event_id,
            viewer_actor_id=record.actor_id,
            allowed_categories=experience.state_diff_fields,
        )
        self.store.save_instance(
            ExperienceInstanceRecord(
                record.instance_id,
                record.profile_id,
                record.owner_id,
                record.branch_id,
                mode=record.mode,
                actor_id=record.actor_id,
                session_id=record.session_id,
                lease_id=record.lease_id,
                last_revision=submitted.state.revision.value,
                updated_seq=record.updated_seq + 1,
            )
        )
        return PlayableActionResult(
            result.proposal,
            event_id,
            submitted.state.revision.value,
            submitted.state.semantic_hash(),
            diff,
        )

    def _save_instance(
        self,
        receipt: EntryReceipt,
        owner_id: str,
        branch_id: str,
        *,
        updated_seq: int,
    ) -> None:
        state = self.runtime.current_state(
            WorldInstanceId(receipt.instance_id), BranchId(branch_id)
        )
        self.store.save_instance(
            ExperienceInstanceRecord(
                receipt.instance_id,
                receipt.profile_id,
                owner_id,
                branch_id,
                mode=receipt.mode,
                actor_id=receipt.actor_id,
                session_id=receipt.session_id,
                lease_id=receipt.lease_id,
                last_revision=state.revision.value,
                updated_seq=updated_seq,
            )
        )

    def _owned_instance(self, instance_id: str, viewer_id: str) -> ExperienceInstanceRecord:
        record = self.store.get_instance(instance_id)
        if record.owner_id != viewer_id:
            raise NotFound(f"playable instance {instance_id!r} not found")
        return record
