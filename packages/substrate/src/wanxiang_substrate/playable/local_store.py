"""Durable JSON-backed Player catalog for restart-safe worlds.

This store only holds product descriptors (profiles, instances, characters and
their compiled world package). Canonical state and History remain in the
runtime's append-only event store; this adapter never writes them.
"""

from __future__ import annotations

import json
import pathlib
import threading
from dataclasses import asdict
from typing import TYPE_CHECKING, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.store import (
    CharacterRecord,
    ExperienceInstanceRecord,
    InMemoryPlayableStore,
)

if TYPE_CHECKING:
    from wanxiang_substrate.playable.experience import ExperiencePackage

_STORE_VERSION = 1


class LocalJsonPlayableStore(InMemoryPlayableStore):
    """Atomic-file Player catalog that survives an application restart."""

    def __init__(self, path: pathlib.Path | str) -> None:
        super().__init__()
        self.path = pathlib.Path(path)
        self._lock = threading.RLock()
        self._load()

    def _load(self) -> None:
        with self._lock:
            if not self.path.exists():
                return
            try:
                decoded = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ContractError(f"playable store {self.path} is unreadable") from exc
            if not isinstance(decoded, dict):
                raise ContractError("playable store payload must be an object")
            data = cast(dict[str, object], decoded)
            if data.get("version") != _STORE_VERSION:
                raise ContractError("unsupported playable store version")
            for raw in self._list(data.get("profiles")):
                profile = PlayableWorldProfile.from_dict(cast(dict[str, object], raw))
                self._profiles[profile.profile_id] = profile
            for raw in self._list(data.get("instances")):
                record = self._instance(cast(dict[str, object], raw))
                self._instances[f"{record.owner_id}:{record.instance_id}"] = record
            for raw in self._list(data.get("characters")):
                character = self._character(cast(dict[str, object], raw))
                self._characters[character.character_id] = character
            packages = data.get("packages", {})
            if not isinstance(packages, dict):
                raise ContractError("playable store packages must be an object")
            for profile_id, payload in cast(dict[object, object], packages).items():
                if not isinstance(profile_id, str) or not isinstance(payload, dict):
                    raise ContractError("playable store package payload is invalid")
                entry = cast(dict[str, object], payload)
                package_payload = entry.get("package")
                if isinstance(package_payload, dict):
                    self._packages[profile_id] = cast(dict[str, object], package_payload)
                    experience_payload = entry.get("experience")
                    if isinstance(experience_payload, dict):
                        self._experiences[profile_id] = cast(dict[str, object], experience_payload)
                else:
                    # Legacy version-1 files stored the package payload directly.
                    self._packages[profile_id] = entry

    @staticmethod
    def _list(value: object) -> list[object]:
        if not isinstance(value, list):
            raise ContractError("playable store collections must be lists")
        return cast(list[object], value)

    @staticmethod
    def _instance(data: dict[str, object]) -> ExperienceInstanceRecord:
        try:
            return ExperienceInstanceRecord(
                instance_id=str(data["instance_id"]),
                profile_id=str(data["profile_id"]),
                owner_id=str(data["owner_id"]),
                branch_id=str(data["branch_id"]),
                mode=str(data.get("mode", "observer")),
                actor_id=str(data.get("actor_id", "")),
                session_id=str(data.get("session_id", "")),
                lease_id=str(data.get("lease_id", "")),
                last_revision=int(cast(int, data.get("last_revision", 0))),
                updated_seq=int(cast(int, data.get("updated_seq", 0))),
                runtime_instance_id=str(data.get("runtime_instance_id", "")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ContractError("playable store instance record is invalid") from exc

    @staticmethod
    def _character(data: dict[str, object]) -> CharacterRecord:
        compatible = data.get("compatible_profile_ids", [])
        if not isinstance(compatible, list):
            raise ContractError("character compatible_profile_ids must be a list")
        compatible_items = cast(list[object], compatible)
        try:
            return CharacterRecord(
                character_id=str(data["character_id"]),
                owner_id=str(data["owner_id"]),
                display_name=str(data["display_name"]),
                compatible_profile_ids=tuple(str(item) for item in compatible_items),
                identity=str(data.get("identity", "")),
                intro=str(data.get("intro", "")),
                stance=str(data.get("stance", "")),
                starting_location=str(data.get("starting_location", "")),
                knowledge_boundary=str(data.get("knowledge_boundary", "")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ContractError("playable store character record is invalid") from exc

    def _persist(self) -> None:
        with self._lock:
            payload = {
                "version": _STORE_VERSION,
                "profiles": [self._profiles[key].to_dict() for key in sorted(self._profiles)],
                "instances": [asdict(self._instances[key]) for key in sorted(self._instances)],
                "characters": [asdict(self._characters[key]) for key in sorted(self._characters)],
                "packages": {key: self._package_entry(key) for key in sorted(self._packages)},
            }
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_name(self.path.name + ".tmp")
            temporary.write_text(
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )
            temporary.replace(self.path)

    def _package_entry(self, profile_id: str) -> dict[str, object]:
        entry: dict[str, object] = {"package": self._packages[profile_id]}
        experience = self._experiences.get(profile_id)
        if experience is not None:
            entry["experience"] = experience
        return entry

    def save_profile(self, profile: PlayableWorldProfile) -> None:
        with self._lock:
            super().save_profile(profile)
            self._persist()

    def save_instance(self, instance: ExperienceInstanceRecord) -> None:
        with self._lock:
            super().save_instance(instance)
            self._persist()

    def save_character(self, character: CharacterRecord) -> None:
        with self._lock:
            super().save_character(character)
            self._persist()

    def save_package(
        self,
        profile_id: str,
        package: WorldPackageDraft,
        experience: ExperiencePackage | None = None,
    ) -> None:
        with self._lock:
            super().save_package(profile_id, package, experience)
            self._persist()
