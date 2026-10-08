"""ExperiencePackage contracts and visibility validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.models import (
    PLAYABLE_PROFILE_SCHEMA_VERSION,
    PlayableWorldProfile,
    Visibility,
)

EntryMode = Literal["observer", "character", "embodiment"]
PublishMode = Literal["preview", "publish"]


@dataclass(frozen=True, slots=True)
class EmbodimentPolicy:
    """Rules for presence and lease acquisition at the product boundary."""

    observer_allowed: bool = True
    embodiment_requires_lease: bool = True
    max_controllers_per_actor: int = 1
    resume_after_leave: bool = True

    def __post_init__(self) -> None:
        if self.max_controllers_per_actor != 1:
            raise ContractError("the stable runtime permits one primary controller per actor")

    def to_dict(self) -> dict[str, object]:
        return {
            "observer_allowed": self.observer_allowed,
            "embodiment_requires_lease": self.embodiment_requires_lease,
            "max_controllers_per_actor": self.max_controllers_per_actor,
            "resume_after_leave": self.resume_after_leave,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> EmbodimentPolicy:
        raw_max = data.get("max_controllers_per_actor", 1)
        if not isinstance(raw_max, int) or isinstance(raw_max, bool):
            raise ContractError("max_controllers_per_actor must be an integer")
        return cls(
            observer_allowed=bool(data.get("observer_allowed", True)),
            embodiment_requires_lease=bool(data.get("embodiment_requires_lease", True)),
            max_controllers_per_actor=raw_max,
            resume_after_leave=bool(data.get("resume_after_leave", True)),
        )


@dataclass(frozen=True, slots=True)
class ExperiencePackage:
    """Product-facing configuration over a WorldPackage and Scenario ref."""

    experience_id: str
    world_package_ref: str
    scenario_ref: str
    projection_profile_ref: str
    visibility: Visibility = "private"
    owner_id: str = ""
    display_name: str = ""
    version: int = 1
    entry_modes: tuple[EntryMode, ...] = ("observer", "character", "embodiment")
    controls: tuple[str, ...] = ("pause", "continue", "leave")
    ui_capabilities: tuple[str, ...] = ("hud", "free_action", "state_diff", "timeline")
    allowed_actions: tuple[str, ...] = ("set_status",)
    state_diff_fields: tuple[str, ...] = (
        "actor",
        "location",
        "relation",
        "item",
        "task",
        "knowledge",
        "organization",
    )
    embodiment_policy: EmbodimentPolicy = field(default_factory=EmbodimentPolicy)
    schema_version: int = PLAYABLE_PROFILE_SCHEMA_VERSION
    audience_ref: str = ""

    def __post_init__(self) -> None:
        self.validate()

    def validate(self, *, mode: PublishMode = "preview") -> None:
        required = {
            "experience_id": self.experience_id,
            "world_package_ref": self.world_package_ref,
            "scenario_ref": self.scenario_ref,
            "projection_profile_ref": self.projection_profile_ref,
        }
        for name, value in required.items():
            if not value.strip():
                raise ContractError(f"{name} must be a non-empty string")
        if self.visibility not in {"public", "private", "unlisted", "family-private"}:
            raise ContractError(f"unsupported visibility {self.visibility!r}")
        if self.visibility in {"private", "family-private"} and not self.owner_id.strip():
            raise ContractError("private experiences require an owner_id")
        if self.visibility == "family-private" and not self.audience_ref.strip():
            raise ContractError("family-private experiences require an audience_ref")
        if mode not in {"preview", "publish"}:
            raise ContractError(f"unsupported validation mode {mode!r}")
        self._validate_values("entry_modes", self.entry_modes)
        self._validate_values("controls", self.controls)
        self._validate_values("ui_capabilities", self.ui_capabilities)
        self._validate_values("allowed_actions", self.allowed_actions)
        self._validate_values("state_diff_fields", self.state_diff_fields)
        if (
            "embodiment" in self.entry_modes
            and not self.embodiment_policy.embodiment_requires_lease
        ):
            raise ContractError("embodiment must require a lease")
        if mode == "publish" and not self.allowed_actions:
            raise ContractError("publishable experience must expose an allowed action")

    @staticmethod
    def _validate_values(name: str, values: tuple[str, ...]) -> None:
        if not values or any(not value.strip() for value in values):
            raise ContractError(f"{name} must contain non-empty values")
        if len(set(values)) != len(values):
            raise ContractError(f"{name} must not contain duplicates")

    def can_view(self, viewer_id: str | None) -> bool:
        if self.visibility == "public":
            return True
        return bool(viewer_id) and viewer_id == self.owner_id

    def can_enter(self, viewer_id: str | None) -> bool:
        return self.can_view(viewer_id)

    def supports_entry(self, mode: EntryMode) -> bool:
        return mode in self.entry_modes

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "experience_id": self.experience_id,
            "version": self.version,
            "world_package_ref": self.world_package_ref,
            "scenario_ref": self.scenario_ref,
            "projection_profile_ref": self.projection_profile_ref,
            "visibility": self.visibility,
            "owner_id": self.owner_id,
            "display_name": self.display_name,
            "audience_ref": self.audience_ref,
            "entry_modes": list(self.entry_modes),
            "controls": list(self.controls),
            "ui_capabilities": list(self.ui_capabilities),
            "allowed_actions": list(self.allowed_actions),
            "state_diff_fields": list(self.state_diff_fields),
            "embodiment_policy": self.embodiment_policy.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExperiencePackage:
        def values(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
            raw = data.get(name, list(default))
            if not isinstance(raw, (list, tuple)):
                raise ContractError(f"{name} must be a list")
            raw_values = cast(list[object] | tuple[object, ...], raw)
            return tuple(str(item) for item in raw_values)

        def integer(name: str, default: int) -> int:
            raw = data.get(name, default)
            if not isinstance(raw, int) or isinstance(raw, bool):
                raise ContractError(f"{name} must be an integer")
            return raw

        raw_policy = data.get("embodiment_policy", {})
        if not isinstance(raw_policy, Mapping):
            raise ContractError("embodiment_policy must be an object")
        policy = cast(Mapping[str, object], raw_policy)
        return cls(
            experience_id=str(data.get("experience_id", "")),
            world_package_ref=str(data.get("world_package_ref", "")),
            scenario_ref=str(data.get("scenario_ref", "")),
            projection_profile_ref=str(data.get("projection_profile_ref", "")),
            visibility=cast(Visibility, data.get("visibility", "private")),
            owner_id=str(data.get("owner_id", "")),
            display_name=str(data.get("display_name", "")),
            version=integer("version", 1),
            entry_modes=cast(
                tuple[EntryMode, ...],
                values("entry_modes", ("observer", "character", "embodiment")),
            ),
            controls=values("controls", ("pause", "continue", "leave")),
            ui_capabilities=values(
                "ui_capabilities", ("hud", "free_action", "state_diff", "timeline")
            ),
            allowed_actions=values("allowed_actions", ("set_status",)),
            state_diff_fields=values(
                "state_diff_fields",
                ("actor", "location", "relation", "item", "task", "knowledge", "organization"),
            ),
            embodiment_policy=EmbodimentPolicy.from_dict(policy),
            schema_version=integer("schema_version", PLAYABLE_PROFILE_SCHEMA_VERSION),
            audience_ref=str(data.get("audience_ref", "")),
        )


def experience_from_profile(
    profile: PlayableWorldProfile,
    *,
    allowed_actions: tuple[str, ...] = ("set_status",),
) -> ExperiencePackage:
    """Create the default ExperiencePackage for a validated shell profile."""

    return ExperiencePackage(
        experience_id=profile.experience_package_ref,
        world_package_ref=profile.world_package_ref,
        scenario_ref=profile.scenario_ref,
        projection_profile_ref=profile.projection_profile_ref,
        visibility=profile.visibility,
        owner_id=profile.owner_id,
        display_name=profile.display_name,
        allowed_actions=allowed_actions,
    )
