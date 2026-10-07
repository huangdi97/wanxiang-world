"""Projection profile contract for player/experience read models.

A ProjectionProfile describes how committed reality is rendered. It never owns
canonical state and can never carry write authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

PLAYABLE_PROFILE_SCHEMA_VERSION = 1


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
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
class ProjectionProfile:
    """Server-side projection policy over canonical read models; never an authority."""

    projection_id: str
    version: int = 1
    provider_ref: str = "native_web"
    capabilities: tuple[str, ...] = ("text",)
    state_source: Literal["canonical_read_model", "committed_state_diff"] = "canonical_read_model"
    write_authority: Literal["none"] = "none"
    fallback: str = "text"
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
        _text(self.provider_ref, "provider_ref")
        _texts(self.capabilities, "capabilities")
        if self.state_source not in {"canonical_read_model", "committed_state_diff"}:
            raise ContractError(f"unsupported projection state_source {self.state_source!r}")
        if self.write_authority != "none":
            raise ContractError("projection profiles can never own World write authority")
        if self.fallback not in self.capabilities:
            raise ContractError("projection fallback must be one of the declared capabilities")
        _texts(self.visible_fields, "visible_fields")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": PLAYABLE_PROFILE_SCHEMA_VERSION,
            "projection_id": self.projection_id,
            "version": self.version,
            "provider_ref": self.provider_ref,
            "capabilities": list(self.capabilities),
            "state_source": self.state_source,
            "write_authority": self.write_authority,
            "fallback": self.fallback,
            "visible_fields": list(self.visible_fields),
            "show_private_knowledge": self.show_private_knowledge,
            "show_state_diff": self.show_state_diff,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ProjectionProfile:
        return cls(
            projection_id=_text(data.get("projection_id"), "projection_id"),
            version=_version(data.get("version", 1), "version"),
            provider_ref=_text(data.get("provider_ref", "native_web"), "provider_ref"),
            capabilities=_texts(data.get("capabilities", ["text"]), "capabilities"),
            state_source=_text(data.get("state_source", "canonical_read_model"), "state_source"),  # type: ignore[arg-type]
            write_authority=_text(data.get("write_authority", "none"), "write_authority"),  # type: ignore[arg-type]
            fallback=_text(data.get("fallback", "text"), "fallback"),
            visible_fields=_texts(
                data.get(
                    "visible_fields",
                    ["location", "actors", "relations", "items", "tasks", "time"],
                ),
                "visible_fields",
            ),
            show_private_knowledge=bool(data.get("show_private_knowledge", False)),
            show_state_diff=bool(data.get("show_state_diff", True)),
        )


__all__ = ["ProjectionProfile"]
