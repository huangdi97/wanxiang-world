"""Sanitized, hash-verifiable evidence for one world run (G95A)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from math import isfinite
from typing import cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

ARTIFACT_SCHEMA_VERSION = 1
_FORBIDDEN_KEYS = frozenset(
    {"content", "payload", "source_text", "source_bytes", "secret", "token", "api_key"}
)


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        raise ContractError(f"{name} must be a non-empty opaque reference")
    return value


def _version(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ContractError(f"{name} must be a non-empty version")
    return value


def _ref_tuple(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(_text(value, f"{name} item") for value in values)
    if len(set(result)) != len(result):
        raise ContractError(f"{name} must not contain duplicates")
    return tuple(sorted(result))


def _pairs(values: Sequence[object], name: str) -> tuple[tuple[str, str], ...]:
    result: list[tuple[str, str]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((_text(pair[0], f"{name} key"), _version(pair[1], f"{name} value")))
    if len({key for key, _value in result}) != len(result):
        raise ContractError(f"{name} keys must be unique")
    return tuple(sorted(result))


def _metrics(values: Sequence[object]) -> tuple[tuple[str, float], ...]:
    result: list[tuple[str, float]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError("metrics items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError("metrics items must be pairs")
        key = _text(pair[0], "metric key")
        value = pair[1]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ContractError("metric values must be finite numbers")
        result.append((key, float(value)))
    if len({key for key, _value in result}) != len(result):
        raise ContractError("metric keys must be unique")
    return tuple(sorted(result))


def _reject_forbidden_keys(value: object) -> None:
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        for key, item in mapping.items():
            normalized = str(key).casefold().replace("-", "_")
            if normalized in _FORBIDDEN_KEYS:
                raise ContractError(f"artifact contains forbidden private field {key!r}")
            _reject_forbidden_keys(item)
    elif isinstance(value, (list, tuple)):
        items = cast(list[object] | tuple[object, ...], value)
        for item in items:
            _reject_forbidden_keys(item)


def sanitize_metadata(
    metadata: Mapping[str, object],
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    """Keep only short opaque metadata and report fields intentionally redacted."""
    kept: list[tuple[str, str]] = []
    redacted: list[str] = []
    for raw_key in sorted(metadata, key=str):
        key = _text(str(raw_key), "metadata key")
        normalized = key.casefold().replace("-", "_")
        value = metadata[raw_key]
        if normalized in _FORBIDDEN_KEYS or normalized.endswith(("_text", "_bytes", "_payload")):
            redacted.append(key)
            continue
        if not isinstance(value, str) or not value.strip() or len(value) > 256:
            redacted.append(key)
            continue
        if any(char in value for char in "\r\n"):
            redacted.append(key)
            continue
        kept.append((key, value))
    return tuple(kept), tuple(sorted(set(redacted)))


@dataclass(frozen=True, slots=True)
class WorldRunArtifact:
    """One sanitized, immutable and re-verifiable world-run evidence record."""

    artifact_id: str
    world_package_ref: str
    world_package_version: str
    scenario_ref: str
    scenario_version: str
    constitution_version: str
    runtime_profile_ref: str
    provider_versions: tuple[tuple[str, str], ...]
    seed: int
    control_ledger_refs: tuple[str, ...] = ()
    commit_refs: tuple[str, ...] = ()
    snapshot_refs: tuple[str, ...] = ()
    branch_refs: tuple[str, ...] = ()
    actor_trajectory_refs: tuple[tuple[str, str], ...] = ()
    intervention_refs: tuple[str, ...] = ()
    validation_results: tuple[tuple[str, str], ...] = ()
    metrics: tuple[tuple[str, float], ...] = ()
    privacy_metadata: tuple[tuple[str, str], ...] = ()
    redacted_fields: tuple[str, ...] = ()
    sanitized: bool = True
    schema_version: int = ARTIFACT_SCHEMA_VERSION
    content_hash: str = ""

    def __post_init__(self) -> None:
        _text(self.artifact_id, "artifact_id")
        for name in (
            "world_package_ref",
            "scenario_ref",
            "runtime_profile_ref",
        ):
            _text(getattr(self, name), name)
        for name in ("world_package_version", "scenario_version", "constitution_version"):
            _version(getattr(self, name), name)
        if type(self.seed) is not int:
            raise ContractError("seed must be an integer")
        if self.schema_version != ARTIFACT_SCHEMA_VERSION:
            raise ContractError(f"unsupported WorldRunArtifact schema {self.schema_version!r}")
        if not self.sanitized:
            raise ContractError("WorldRunArtifact must be sanitized before export")
        object.__setattr__(
            self, "provider_versions", _pairs(self.provider_versions, "provider_versions")
        )
        for name in (
            "control_ledger_refs",
            "commit_refs",
            "snapshot_refs",
            "branch_refs",
            "intervention_refs",
        ):
            object.__setattr__(self, name, _ref_tuple(getattr(self, name), name))
        object.__setattr__(
            self,
            "actor_trajectory_refs",
            _pairs(self.actor_trajectory_refs, "actor_trajectory_refs"),
        )
        object.__setattr__(
            self,
            "validation_results",
            _pairs(self.validation_results, "validation_results"),
        )
        object.__setattr__(self, "metrics", _metrics(self.metrics))
        privacy = _pairs(self.privacy_metadata, "privacy_metadata")
        if any(key.casefold() in _FORBIDDEN_KEYS for key, _value in privacy):
            raise ContractError("privacy metadata contains a forbidden field")
        object.__setattr__(self, "privacy_metadata", privacy)
        object.__setattr__(
            self, "redacted_fields", _ref_tuple(self.redacted_fields, "redacted_fields")
        )
        if self.content_hash and (
            len(self.content_hash) != 64
            or any(c not in "0123456789abcdef" for c in self.content_hash)
        ):
            raise ContractError("content_hash must be a lowercase SHA-256 hex digest")

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "artifact_id": self.artifact_id,
            "world_package_ref": self.world_package_ref,
            "world_package_version": self.world_package_version,
            "scenario_ref": self.scenario_ref,
            "scenario_version": self.scenario_version,
            "constitution_version": self.constitution_version,
            "runtime_profile_ref": self.runtime_profile_ref,
            "provider_versions": [list(item) for item in self.provider_versions],
            "seed": self.seed,
            "control_ledger_refs": list(self.control_ledger_refs),
            "commit_refs": list(self.commit_refs),
            "snapshot_refs": list(self.snapshot_refs),
            "branch_refs": list(self.branch_refs),
            "actor_trajectory_refs": [list(item) for item in self.actor_trajectory_refs],
            "intervention_refs": list(self.intervention_refs),
            "validation_results": [list(item) for item in self.validation_results],
            "metrics": [list(item) for item in self.metrics],
            "privacy_metadata": [list(item) for item in self.privacy_metadata],
            "redacted_fields": list(self.redacted_fields),
            "sanitized": self.sanitized,
        }

    def compute_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def with_hash(self) -> WorldRunArtifact:
        return replace(self, content_hash=self.compute_hash())

    def verify_hash(self) -> bool:
        return bool(self.content_hash) and self.content_hash == self.compute_hash()

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["content_hash"] = self.content_hash
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> WorldRunArtifact:
        _reject_forbidden_keys(data)
        raw = dict(data)
        artifact = cls(
            artifact_id=_text(raw.get("artifact_id"), "artifact_id"),
            world_package_ref=_text(raw.get("world_package_ref"), "world_package_ref"),
            world_package_version=_version(
                raw.get("world_package_version"), "world_package_version"
            ),
            scenario_ref=_text(raw.get("scenario_ref"), "scenario_ref"),
            scenario_version=_version(raw.get("scenario_version"), "scenario_version"),
            constitution_version=_version(raw.get("constitution_version"), "constitution_version"),
            runtime_profile_ref=_text(raw.get("runtime_profile_ref"), "runtime_profile_ref"),
            provider_versions=_pair_strings(raw.get("provider_versions", ()), "provider_versions"),
            seed=_integer(raw.get("seed"), "seed"),
            control_ledger_refs=_strings(raw.get("control_ledger_refs", ()), "control_ledger_refs"),
            commit_refs=_strings(raw.get("commit_refs", ()), "commit_refs"),
            snapshot_refs=_strings(raw.get("snapshot_refs", ()), "snapshot_refs"),
            branch_refs=_strings(raw.get("branch_refs", ()), "branch_refs"),
            actor_trajectory_refs=_pair_strings(
                raw.get("actor_trajectory_refs", ()), "actor_trajectory_refs"
            ),
            intervention_refs=_strings(raw.get("intervention_refs", ()), "intervention_refs"),
            validation_results=_pair_strings(
                raw.get("validation_results", ()), "validation_results"
            ),
            metrics=_metric_pairs(raw.get("metrics", ()), "metrics"),
            privacy_metadata=_pair_strings(raw.get("privacy_metadata", ()), "privacy_metadata"),
            redacted_fields=_strings(raw.get("redacted_fields", ()), "redacted_fields"),
            sanitized=_boolean(raw.get("sanitized", True), "sanitized"),
            schema_version=_integer(raw.get("schema_version"), "schema_version"),
            content_hash=_text(raw.get("content_hash"), "content_hash"),
        )
        if not artifact.verify_hash():
            raise ContractError("WorldRunArtifact content hash does not verify")
        return artifact


def _sequence(value: object, name: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractError(f"{name} must be a list")
    return tuple(cast(list[object] | tuple[object, ...], value))


def _strings(value: object, name: str) -> tuple[str, ...]:
    values = _sequence(value, name)
    return tuple(_text(item, f"{name} item") for item in values)


def _integer(value: object, name: str) -> int:
    if type(value) is not int:
        raise ContractError(f"{name} must be an integer")
    return value


def _boolean(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise ContractError(f"{name} must be boolean")
    return value


def _pair_strings(value: object, name: str) -> tuple[tuple[str, str], ...]:
    return _pairs(_sequence(value, name), name)


def _metric_pairs(value: object, name: str) -> tuple[tuple[str, float], ...]:
    return _metrics(_sequence(value, name))


__all__ = ["ARTIFACT_SCHEMA_VERSION", "WorldRunArtifact", "sanitize_metadata"]
