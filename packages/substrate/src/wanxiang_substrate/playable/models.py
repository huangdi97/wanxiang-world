"""Versioned, transport-neutral contracts for the Playable World entry shell."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

PLAYABLE_PROFILE_SCHEMA_VERSION = 1
Visibility = Literal["public", "private", "unlisted", "family-private"]


def _text(value: object, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ContractError(f"{name} must be a non-empty string")
    return value


def _texts(values: object, name: str) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise ContractError(f"{name} must be a list")
    raw = cast(list[object] | tuple[object, ...], values)
    result = tuple(_text(item, f"{name} item") for item in raw)
    if len(set(result)) != len(result):
        raise ContractError(f"{name} must not contain duplicates")
    return result


def _version(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ContractError(f"{name} must be a positive integer")
    return value


@dataclass(frozen=True, slots=True)
class ScenarioProfile:
    """A selectable scenario reference; it never contains canonical state."""

    scenario_id: str
    world_package_ref: str
    name: str = "Default scenario"
    version: int = 1
    starting_location_ref: str = ""
    default_actor_ref: str = ""

    def __post_init__(self) -> None:
        _text(self.scenario_id, "scenario_id")
        _text(self.world_package_ref, "world_package_ref")
        _text(self.name, "name")
        _version(self.version, "version")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": PLAYABLE_PROFILE_SCHEMA_VERSION,
            "scenario_id": self.scenario_id,
            "world_package_ref": self.world_package_ref,
            "name": self.name,
            "version": self.version,
            "starting_location_ref": self.starting_location_ref,
            "default_actor_ref": self.default_actor_ref,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ScenarioProfile:
        return cls(
            scenario_id=_text(data.get("scenario_id"), "scenario_id"),
            world_package_ref=_text(data.get("world_package_ref"), "world_package_ref"),
            name=_text(data.get("name", "Default scenario"), "name"),
            version=_version(data.get("version", 1), "version"),
            starting_location_ref=_text(
                data.get("starting_location_ref", ""),
                "starting_location_ref",
                allow_empty=True,
            ),
            default_actor_ref=_text(
                data.get("default_actor_ref", ""), "default_actor_ref", allow_empty=True
            ),
        )


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    """Runtime selection and budgets, kept outside the Kernel."""

    runtime_id: str
    version: int = 1
    time_scale: int = 1
    simulation_lod: str = "L0"
    seed: int = 0
    provider_versions: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        _text(self.runtime_id, "runtime_id")
        _version(self.version, "version")
        if self.time_scale < 1:
            raise ContractError("time_scale must be positive")
        if self.simulation_lod not in {"L0", "L1", "L2", "L3", "L4"}:
            raise ContractError("simulation_lod must be one of L0..L4")
        for provider, provider_version in self.provider_versions:
            _text(provider, "provider id")
            _text(provider_version, "provider version")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": PLAYABLE_PROFILE_SCHEMA_VERSION,
            "runtime_id": self.runtime_id,
            "version": self.version,
            "time_scale": self.time_scale,
            "simulation_lod": self.simulation_lod,
            "seed": self.seed,
            "provider_versions": [list(item) for item in self.provider_versions],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> RuntimeProfile:
        raw_providers = data.get("provider_versions", [])
        if not isinstance(raw_providers, (list, tuple)):
            raise ContractError("provider_versions must be a list")
        provider_items = cast(list[object] | tuple[object, ...], raw_providers)
        providers: list[tuple[str, str]] = []
        for item in provider_items:
            if not isinstance(item, (list, tuple)):
                raise ContractError("provider_versions items must be pairs")
            pair = cast(list[object] | tuple[object, ...], item)
            if len(pair) != 2:
                raise ContractError("provider_versions items must be pairs")
            providers.append((_text(pair[0], "provider id"), _text(pair[1], "provider version")))
        raw_seed = data.get("seed", 0)
        seed = raw_seed if isinstance(raw_seed, int) and not isinstance(raw_seed, bool) else 0
        return cls(
            runtime_id=_text(data.get("runtime_id"), "runtime_id"),
            version=_version(data.get("version", 1), "version"),
            time_scale=_version(data.get("time_scale", 1), "time_scale"),
            simulation_lod=_text(data.get("simulation_lod", "L0"), "simulation_lod"),
            seed=seed,
            provider_versions=tuple(providers),
        )


@dataclass(frozen=True, slots=True)
class ProjectionProfile:
    """A server-side visibility profile for UI projections."""

    projection_id: str
    version: int = 1
    visible_fields: tuple[str, ...] = (
        "location",
        "actors",
        "relations",
        "items",
        "tasks",
        "time",
    )
    show_private_knowledge: bool = False
    show_state_diff: bool = True

    def __post_init__(self) -> None:
        _text(self.projection_id, "projection_id")
        _version(self.version, "version")
        _texts(self.visible_fields, "visible_fields")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": PLAYABLE_PROFILE_SCHEMA_VERSION,
            "projection_id": self.projection_id,
            "version": self.version,
            "visible_fields": list(self.visible_fields),
            "show_private_knowledge": self.show_private_knowledge,
            "show_state_diff": self.show_state_diff,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ProjectionProfile:
        return cls(
            projection_id=_text(data.get("projection_id"), "projection_id"),
            version=_version(data.get("version", 1), "version"),
            visible_fields=_texts(
                data.get(
                    "visible_fields", ["location", "actors", "relations", "items", "tasks", "time"]
                ),
                "visible_fields",
            ),
            show_private_knowledge=bool(data.get("show_private_knowledge", False)),
            show_state_diff=bool(data.get("show_state_diff", True)),
        )


@dataclass(frozen=True, slots=True)
class PlayableWorldProfile:
    """The immutable product entry descriptor for one world experience."""

    profile_id: str
    world_package_ref: str
    scenario_ref: str
    runtime_profile_ref: str
    experience_package_ref: str
    projection_profile_ref: str
    visibility: Visibility = "private"
    owner_id: str = ""
    display_name: str = ""
    schema_version: int = PLAYABLE_PROFILE_SCHEMA_VERSION
    version: int = 1
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        for name in (
            "profile_id",
            "world_package_ref",
            "scenario_ref",
            "runtime_profile_ref",
            "experience_package_ref",
            "projection_profile_ref",
        ):
            _text(getattr(self, name), name)
        if self.visibility not in {"public", "private", "unlisted", "family-private"}:
            raise ContractError(f"unsupported visibility {self.visibility!r}")
        _text(self.owner_id, "owner_id", allow_empty=True)
        _text(self.display_name, "display_name", allow_empty=True)
        if self.schema_version != PLAYABLE_PROFILE_SCHEMA_VERSION:
            raise ContractError(f"unsupported playable profile schema {self.schema_version}")
        _version(self.version, "version")
        _texts(self.tags, "tags")

    def visible_to(self, viewer_id: str | None) -> bool:
        if self.visibility == "public":
            return True
        return bool(viewer_id) and viewer_id == self.owner_id

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "version": self.version,
            "world_package_ref": self.world_package_ref,
            "scenario_ref": self.scenario_ref,
            "runtime_profile_ref": self.runtime_profile_ref,
            "experience_package_ref": self.experience_package_ref,
            "projection_profile_ref": self.projection_profile_ref,
            "visibility": self.visibility,
            "owner_id": self.owner_id,
            "display_name": self.display_name,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PlayableWorldProfile:
        raw_schema = data.get("schema_version", 0)
        if raw_schema not in (0, PLAYABLE_PROFILE_SCHEMA_VERSION):
            raise ContractError(f"unsupported playable profile schema {raw_schema!r}")
        # v0 used the shorter package/scenario/runtime names.  Reading it is
        # deliberately one-way; writes always emit the current schema.
        return cls(
            profile_id=_text(data.get("profile_id"), "profile_id"),
            world_package_ref=_text(
                data.get("world_package_ref", data.get("package_id")), "world_package_ref"
            ),
            scenario_ref=_text(
                data.get("scenario_ref", data.get("scenario_id", "default")), "scenario_ref"
            ),
            runtime_profile_ref=_text(
                data.get("runtime_profile_ref", data.get("runtime_id", "reference")),
                "runtime_profile_ref",
            ),
            experience_package_ref=_text(
                data.get("experience_package_ref", data.get("profile_id")),
                "experience_package_ref",
            ),
            projection_profile_ref=_text(
                data.get("projection_profile_ref", "default"), "projection_profile_ref"
            ),
            visibility=data.get("visibility", "private"),  # type: ignore[arg-type]
            owner_id=_text(data.get("owner_id", ""), "owner_id", allow_empty=True),
            display_name=_text(data.get("display_name", ""), "display_name", allow_empty=True),
            schema_version=PLAYABLE_PROFILE_SCHEMA_VERSION,
            version=_version(data.get("version", 1), "version"),
            tags=_texts(data.get("tags", []), "tags"),
        )
