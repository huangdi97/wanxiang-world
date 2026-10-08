"""Behaviour of the persisted R7 runtime lock store (file and memory)."""

from __future__ import annotations

import json
import pathlib

import pytest
from wanxiang_reality.errors import LockImmutableError, LockStoreError, LockTamperedError
from wanxiang_reality.lock_store import (
    LOCK_STORE_SCHEMA,
    FileLockStore,
    StoredLock,
    memory_lock_store,
)
from wanxiang_reality.profiles import RuntimeLock, build_runtime_lock
from wanxiang_reality.reference_profiles import (
    reference_reality_profile,
    reference_world_profile,
)

pytestmark = pytest.mark.unit

WORLDLINE = "wl_store"

_LOCK_KEYS = {
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
    "service_contract_versions",
    "provider_versions",
    "artifact_hashes",
    "schema_versions",
    "migration_lineage",
    "runtime_config_hash",
}


def _lock() -> RuntimeLock:
    return build_runtime_lock(
        reference_reality_profile(),
        reference_world_profile(),
        world_id="world-1",
        world_instance_id="instance-1",
        worldline_id=WORLDLINE,
        composition_runtime="cordis",
        composition_runtime_version="4.0.0-rc.10",
        service_contract_versions={"wanxiang.history@1": "1"},
        provider_versions={"provider.history.memory": "1.0.0"},
        artifact_hashes={"artifact.world": "abc"},
        schema_versions={"wanxiang.schema.canonical": "1"},
        migration_lineage=("genesis",),
        runtime_config_hash="config-hash",
    )


def _stored(revision: int = 1) -> StoredLock:
    lock = _lock()
    return StoredLock(
        worldline_id=WORLDLINE,
        revision=revision,
        written_at="2026-01-01T00:00:00Z",
        lock=lock,
        lock_digest=lock.lock_digest(),
    )


def test_write_then_read_round_trips_every_bound_field_and_the_digest(
    tmp_path: pathlib.Path,
) -> None:
    store = FileLockStore(tmp_path)
    original = _stored()

    store.write(original, expected_revision=None)
    loaded = store.read(WORLDLINE)

    assert loaded == original
    assert loaded is not None
    assert loaded.lock_digest == original.lock.lock_digest()
    assert loaded.lock.world_id == "world-1"
    assert loaded.lock.world_definition_version == "1.0.0"
    assert loaded.lock.composition_runtime == "cordis"
    assert loaded.lock.provider_versions == {"provider.history.memory": "1.0.0"}
    assert loaded.lock.migration_lineage == ("genesis",)


def test_a_fresh_store_instance_from_the_same_root_reads_an_equal_record(
    tmp_path: pathlib.Path,
) -> None:
    FileLockStore(tmp_path).write(_stored(), expected_revision=None)

    assert FileLockStore(tmp_path).read(WORLDLINE) == _stored()


def test_write_over_an_existing_record_is_refused_and_leaves_the_file_untouched(
    tmp_path: pathlib.Path,
) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)
    path = store.path_for(WORLDLINE)
    before = path.read_bytes()

    with pytest.raises(LockImmutableError):
        store.write(_stored(), expected_revision=None)

    assert path.read_bytes() == before


def test_a_mismatched_expected_revision_is_refused(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)

    with pytest.raises(LockStoreError):
        store.write(_stored(revision=2), expected_revision=5)


def test_an_explicit_revision_bump_is_written(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)
    bumped = _stored(revision=2)

    store.write(bumped, expected_revision=1)

    assert store.read(WORLDLINE) == bumped


def test_a_hand_edited_field_is_reported_as_tampering(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)
    path = store.path_for(WORLDLINE)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["lock"]["provider_versions"] = {"provider.history.memory": "9.9.9"}
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(LockTamperedError):
        store.read(WORLDLINE)


def test_truncated_json_is_reported_as_tampering(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)
    store.path_for(WORLDLINE).write_text(
        '{"schema": "wanxiang.r7.runtime-lock.v1"', encoding="utf-8"
    )

    with pytest.raises(LockTamperedError):
        store.read(WORLDLINE)


def test_a_missing_file_reads_as_none(tmp_path: pathlib.Path) -> None:
    assert FileLockStore(tmp_path).read("absent") is None


def test_payload_shape_is_the_frozen_on_disk_contract(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)
    payload = json.loads(store.path_for(WORLDLINE).read_text(encoding="utf-8"))

    assert set(payload) == {"schema", "revision", "writtenAt", "lockDigest", "lock"}
    assert payload["schema"] == LOCK_STORE_SCHEMA
    assert payload["lockDigest"] == _lock().lock_digest()
    assert payload["writtenAt"].endswith("Z")
    assert set(payload["lock"]) == _LOCK_KEYS


def test_the_memory_store_has_the_same_immutability_contract() -> None:
    store = memory_lock_store()
    store.write(_stored(), expected_revision=None)

    with pytest.raises(LockImmutableError):
        store.write(_stored(), expected_revision=None)

    assert store.read(WORLDLINE) == _stored()
    assert store.worldlines() == (WORLDLINE,)


def test_the_file_store_lists_worldlines(tmp_path: pathlib.Path) -> None:
    store = FileLockStore(tmp_path)
    store.write(_stored(), expected_revision=None)

    assert store.worldlines() == (WORLDLINE,)


def test_a_stored_lock_revision_must_be_at_least_one() -> None:
    with pytest.raises(LockStoreError):
        StoredLock(
            worldline_id=WORLDLINE,
            revision=0,
            written_at="2026-01-01T00:00:00Z",
            lock=_lock(),
            lock_digest=_lock().lock_digest(),
        )


def test_a_stored_lock_digest_must_match_its_lock() -> None:
    with pytest.raises(LockStoreError):
        StoredLock(
            worldline_id=WORLDLINE,
            revision=1,
            written_at="2026-01-01T00:00:00Z",
            lock=_lock(),
            lock_digest="0" * 64,
        )
