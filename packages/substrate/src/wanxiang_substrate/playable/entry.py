"""Character, observer presence, and embodiment entry over existing session ports."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError, NotFound
from wanxiang_domain.ids import WorldInstanceId

from wanxiang_substrate.playable.experience import EntryMode, ExperiencePackage
from wanxiang_substrate.playable.store import CharacterRecord, PlayableStore
from wanxiang_substrate.session import EmbodimentLease, LeaseService, SessionService


@dataclass(frozen=True, slots=True)
class EntryReceipt:
    session_id: str
    instance_id: str
    profile_id: str
    mode: EntryMode
    actor_id: str
    presence: bool
    lease_id: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "instance_id": self.instance_id,
            "profile_id": self.profile_id,
            "mode": self.mode,
            "actor_id": self.actor_id,
            "presence": self.presence,
            "lease_id": self.lease_id,
        }


class CharacterEntryService:
    """Application-facing entry facade; mutation still requires the runtime host."""

    def __init__(
        self,
        store: PlayableStore,
        *,
        sessions: SessionService | None = None,
        leases: LeaseService | None = None,
    ) -> None:
        self._store = store
        self.sessions = sessions or SessionService()
        self.leases = leases or LeaseService()
        self._sequence = 0
        self._lease_by_session: dict[str, str] = {}

    def create_character(
        self,
        owner_id: str,
        display_name: str,
        *,
        compatible_profile_ids: tuple[str, ...] = (),
        character_id: str | None = None,
    ) -> CharacterRecord:
        if not owner_id or not display_name.strip():
            raise ContractError("character creation requires owner and display name")
        number = len(self._store.list_characters(owner_id)) + 1
        character = CharacterRecord(
            character_id=character_id or f"character:{owner_id}:{number}",
            owner_id=owner_id,
            display_name=display_name.strip(),
            compatible_profile_ids=compatible_profile_ids,
        )
        self._store.save_character(character)
        return character

    def my_characters(self, owner_id: str) -> tuple[CharacterRecord, ...]:
        return self._store.list_characters(owner_id)

    def enter(
        self,
        package: ExperiencePackage,
        *,
        viewer_id: str,
        instance_id: str,
        branch_id: str,
        session_id: str,
        mode: EntryMode,
        character_id: str = "",
    ) -> EntryReceipt:
        if not package.can_enter(viewer_id):
            raise NotFound("experience is not available to this viewer")
        if not package.supports_entry(mode):
            raise ContractError(f"experience does not support entry mode {mode!r}")
        character = self._character_for_entry(package, viewer_id, character_id, mode)
        self._sequence += 1
        session_mode = "embody" if mode == "embodiment" else "observe"
        session = self.sessions.create(
            session_id,
            viewer_id,
            WorldInstanceId(instance_id),
            session_mode,
            self._sequence,
        )
        lease_id = ""
        actor_id = character.character_id if character is not None else ""
        if mode == "embodiment":
            if character is None:
                raise ContractError("embodiment requires a character")
            lease_id = f"lease:{session_id}:{actor_id}"
            lease = self.leases.acquire(
                session,
                actor_id,
                lease_id,
                acquired_seq=self._sequence,
                expires_seq=self._sequence + 100,
            )
            self._lease_by_session[session_id] = lease.lease_id
        return EntryReceipt(
            session_id=session_id,
            instance_id=instance_id,
            profile_id=package.experience_id,
            mode=mode,
            actor_id=actor_id,
            presence=mode != "embodiment",
            lease_id=lease_id,
        )

    def leave(self, session_id: str) -> EntryReceipt:
        session = self.sessions.require(session_id)
        lease_id = self._lease_by_session.pop(session_id, "")
        actor_id = ""
        if lease_id:
            lease = self.leases.release(lease_id, self._sequence + 1)
            actor_id = lease.actor_id
        return EntryReceipt(
            session_id=session_id,
            instance_id=session.instance_id.value,
            profile_id="",
            mode="embodiment" if lease_id else "observer",
            actor_id=actor_id,
            presence=False,
            lease_id=lease_id,
        )

    def lease_id_for_session(self, session_id: str) -> str:
        return self._lease_by_session.get(session_id, "")

    def _character_for_entry(
        self,
        package: ExperiencePackage,
        viewer_id: str,
        character_id: str,
        mode: EntryMode,
    ) -> CharacterRecord | None:
        if mode == "observer":
            if character_id:
                raise ContractError("observer entry cannot bind a character")
            return None
        if not character_id:
            raise ContractError("character and embodiment entry require a character")
        character = self._store.get_character(character_id)
        if character.owner_id != viewer_id or not character.compatible_with(package.experience_id):
            raise NotFound("character is not available for this experience")
        return character


def active_lease(service: CharacterEntryService, session_id: str) -> EmbodimentLease | None:
    """Return the existing lease for diagnostics without exposing a mutator."""

    lease_id = service.lease_id_for_session(session_id)
    if not lease_id:
        return None
    return service.leases.require(lease_id)
