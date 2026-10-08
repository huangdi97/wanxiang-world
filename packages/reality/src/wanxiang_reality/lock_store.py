"""Frozen on-disk format for persisted R7 runtime locks (``wanxiang.r7.runtime-lock.v1``).

Holds ``revision``, ``writtenAt`` (ISO-8601 UTC/``Z``), ``lockDigest`` (sha256 hex)
and ``lock`` (snake_case RuntimeLock projection). A stored lock is immutable and a
``lockDigest`` mismatch is tampering, never a lock to be repaired in place.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Protocol, cast

from wanxiang_reality.errors import (
    LockImmutableError,
    LockMissingError,
    LockStoreError,
    LockTamperedError,
    RuntimeLockError,
)
from wanxiang_reality.profiles import RuntimeLock, lock_projection

LOCK_STORE_SCHEMA = "wanxiang.r7.runtime-lock.v1"

_TEXT_FIELDS = (
    "world_id",
    "world_definition_version",
    "world_instance_id",
    "worldline_id",
    "reality_profile_ref",
    "reality_profile_hash",
    "world_profile_ref",
    "world_profile_hash",
    "composition_runtime",
    "composition_runtime_version",
    "runtime_config_hash",
)

_MAP_FIELDS = (
    "service_contract_versions",
    "provider_versions",
    "artifact_hashes",
    "schema_versions",
)

_LOCK_KEYS = frozenset((*_TEXT_FIELDS, *_MAP_FIELDS, "migration_lineage"))
_STORE_KEYS = frozenset(("schema", "revision", "writtenAt", "lockDigest", "lock"))


@dataclass(frozen=True, slots=True)
class StoredLock:
    """One persisted runtime lock with its explicit revision and write time."""

    worldline_id: str
    revision: int
    written_at: str
    lock: RuntimeLock
    lock_digest: str

    def __post_init__(self) -> None:
        if self.revision < 1:
            raise LockStoreError("stored lock revision must be >= 1")
        if not self.written_at.strip():
            raise LockStoreError("stored lock written_at must not be empty")
        if self.worldline_id != self.lock.worldline_id:
            raise LockStoreError(
                f"stored lock worldline_id {self.worldline_id!r} does not match "
                f"lock worldline_id {self.lock.worldline_id!r}"
            )
        actual = self.lock.lock_digest()
        if self.lock_digest != actual:
            raise LockStoreError(
                f"stored lock digest {self.lock_digest!r} does not match lock digest {actual!r}"
            )

    def to_payload(self) -> dict[str, object]:
        """Return the frozen JSON payload written to disk."""
        return {
            "schema": LOCK_STORE_SCHEMA,
            "revision": self.revision,
            "writtenAt": self.written_at,
            "lockDigest": self.lock_digest,
            "lock": lock_projection(self.lock),
        }

    @classmethod
    def from_payload(cls, payload: object) -> StoredLock:
        """Parse a payload, raising LockTamperedError on any deviation."""
        data = _require_object(payload, "stored lock")
        _require_exact_keys(data, _STORE_KEYS, "stored lock")
        if data["schema"] != LOCK_STORE_SCHEMA:
            raise LockTamperedError(f"unexpected lock store schema: {data['schema']!r}")
        revision = data["revision"]
        if isinstance(revision, bool) or not isinstance(revision, int):
            raise LockTamperedError("stored lock revision must be an integer")
        lock = _lock_from_projection(data["lock"])
        try:
            return cls(
                worldline_id=lock.worldline_id,
                revision=revision,
                written_at=_require_text(data["writtenAt"], "writtenAt"),
                lock=lock,
                lock_digest=_require_text(data["lockDigest"], "lockDigest"),
            )
        except LockStoreError as exc:
            raise LockTamperedError(str(exc)) from exc


def _lock_from_projection(payload: object) -> RuntimeLock:
    data = _require_object(payload, "runtime lock")
    _require_exact_keys(data, _LOCK_KEYS, "runtime lock")
    text = {name: _require_text(data[name], name) for name in _TEXT_FIELDS}
    maps = {name: _require_str_map(data[name], name) for name in _MAP_FIELDS}
    try:
        lock = RuntimeLock(
            world_id=text["world_id"],
            world_definition_version=text["world_definition_version"],
            world_instance_id=text["world_instance_id"],
            worldline_id=text["worldline_id"],
            reality_profile_ref=text["reality_profile_ref"],
            reality_profile_hash=text["reality_profile_hash"],
            world_profile_ref=text["world_profile_ref"],
            world_profile_hash=text["world_profile_hash"],
            composition_runtime=text["composition_runtime"],
            composition_runtime_version=text["composition_runtime_version"],
            service_contract_versions=maps["service_contract_versions"],
            provider_versions=maps["provider_versions"],
            artifact_hashes=maps["artifact_hashes"],
            schema_versions=maps["schema_versions"],
            migration_lineage=_require_text_tuple(data["migration_lineage"], "migration_lineage"),
            runtime_config_hash=text["runtime_config_hash"],
        )
        lock.validate()
    except RuntimeLockError as exc:
        raise LockTamperedError(f"runtime lock is invalid: {exc}") from exc
    return lock


def _require_object(value: object, what: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise LockTamperedError(f"{what} must be a JSON object")
    return cast("dict[str, object]", value)


def _require_exact_keys(data: dict[str, object], expected: frozenset[str], what: str) -> None:
    actual = frozenset(data)
    if actual != expected:
        diff = f"missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}"
        raise LockTamperedError(f"{what} has wrong keys: {diff}")


def _require_text(value: object, what: str) -> str:
    if not isinstance(value, str):
        raise LockTamperedError(f"{what} must be a string")
    return value


def _require_text_tuple(value: object, what: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise LockTamperedError(f"{what} must be a list of strings")
    items = cast("list[object]", value)
    result: list[str] = []
    for item in items:
        if not isinstance(item, str):
            raise LockTamperedError(f"{what} must be a list of strings")
        result.append(item)
    return tuple(result)


def _require_str_map(value: object, what: str) -> dict[str, str]:
    fields = _require_object(value, what)
    result: dict[str, str] = {}
    for key, item in fields.items():
        if not isinstance(item, str):
            raise LockTamperedError(f"{what}[{key!r}] must be a string")
        result[key] = item
    return result


class LockStore(Protocol):
    """Read/write access to persisted runtime locks, keyed by worldline id."""

    def read(self, worldline_id: str) -> StoredLock | None:
        """Return the stored lock, or ``None`` when the worldline has no record."""
        ...

    def write(self, stored: StoredLock, *, expected_revision: int | None) -> None:
        """Persist ``stored`` under the revision contract in the module docs."""
        ...


def _check_write(
    current: StoredLock | None, stored: StoredLock, expected_revision: int | None
) -> None:
    """Enforce create-only / exact-revision writes shared by every store."""
    if expected_revision is None:
        if current is not None:
            raise LockImmutableError(
                f"worldline {stored.worldline_id} already has a lock at revision "
                f"{current.revision}; an existing runtime lock is immutable"
            )
        if stored.revision != 1:
            raise LockStoreError("a new runtime lock must be written at revision 1")
        return
    if current is None:
        raise LockMissingError(f"worldline {stored.worldline_id} has no lock to update")
    if current.revision != expected_revision:
        raise LockStoreError(
            f"worldline {stored.worldline_id} is at revision {current.revision}, "
            f"expected {expected_revision}"
        )
    if stored.revision <= expected_revision:
        raise LockStoreError(
            f"updated lock revision {stored.revision} must be greater than {expected_revision}"
        )


class FileLockStore:
    """One JSON file per worldline under ``<root>/<worldline_id>.json``."""

    def __init__(self, root: pathlib.Path) -> None:
        self._root = root

    def path_for(self, worldline_id: str) -> pathlib.Path:
        """Return the file this store uses for ``worldline_id``."""
        return self._root / f"{worldline_id}.json"

    def read(self, worldline_id: str) -> StoredLock | None:
        """Read and validate a record; fail closed on anything ill-shaped."""
        path = self.path_for(worldline_id)
        if not path.is_file():
            return None
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise LockTamperedError(f"cannot read lock file {path}: {exc}") from exc
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LockTamperedError(f"lock file {path} is not valid JSON: {exc}") from exc
        stored = StoredLock.from_payload(payload)
        if stored.worldline_id != worldline_id:
            raise LockTamperedError(
                f"lock file {path} pins worldline {stored.worldline_id!r}, "
                f"expected {worldline_id!r}"
            )
        return stored

    def write(self, stored: StoredLock, *, expected_revision: int | None) -> None:
        """Write a record, refusing any implicit overwrite or re-digest."""
        current = self.read(stored.worldline_id)
        _check_write(current, stored, expected_revision)
        self._root.mkdir(parents=True, exist_ok=True)
        self.path_for(stored.worldline_id).write_text(
            json.dumps(stored.to_payload(), sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def worldlines(self) -> tuple[str, ...]:
        """Return the worldline ids that have a file in this store, sorted."""
        if not self._root.is_dir():
            return ()
        return tuple(sorted(path.stem for path in self._root.glob("*.json")))


class MemoryLockStore:
    """In-memory :class:`LockStore` with the same immutability contract."""

    def __init__(self) -> None:
        self._records: dict[str, StoredLock] = {}

    def read(self, worldline_id: str) -> StoredLock | None:
        return self._records.get(worldline_id)

    def write(self, stored: StoredLock, *, expected_revision: int | None) -> None:
        _check_write(self._records.get(stored.worldline_id), stored, expected_revision)
        self._records[stored.worldline_id] = stored

    def worldlines(self) -> tuple[str, ...]:
        return tuple(sorted(self._records))


def memory_lock_store() -> MemoryLockStore:
    """Return a fresh empty in-memory lock store."""
    return MemoryLockStore()


__all__ = [
    "LOCK_STORE_SCHEMA",
    "FileLockStore",
    "LockStore",
    "MemoryLockStore",
    "StoredLock",
    "lock_projection",
    "memory_lock_store",
]
