"""G16D: asset/object storage, media rights & durable artifact handling.

- Blob corruption is detected on read (integrity hash).
- Asset metadata (AssetRef) is immutable/content-addressed and replayable through
  canonical commands.
- Denied rights prevent delivery.
- Canonical events refer to immutable identity/version, never a mutable path.
"""

from __future__ import annotations

import pathlib
import uuid
from collections.abc import Iterator

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.assets.errors import AssetCorrupt, AssetNotFound, AssetRightsDenied
from wanxiang_substrate.assets.storage import AssetRef, LocalObjectStore, require_delivery_rights
from wanxiang_substrate.material.resolver import register_material_resolvers

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
BLOB_ROOT = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def blob_dir() -> Iterator[pathlib.Path]:
    d = BLOB_ROOT / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


def test_blob_corruption_detected(blob_dir: pathlib.Path) -> None:
    store = LocalObjectStore(blob_dir)
    ref = store.put(b"hello world", content_type="text/plain")
    assert store.get(ref) == b"hello world"
    path = blob_dir / ref.content_hash[:2] / ref.content_hash
    path.write_bytes(b"tampered!")
    with pytest.raises(AssetCorrupt):
        store.get(ref)


def test_missing_blob_is_explicit_not_found(blob_dir: pathlib.Path) -> None:
    store = LocalObjectStore(blob_dir)
    ref = store.put(b"data", content_type="text/plain")
    store.delete(ref)
    with pytest.raises(AssetNotFound):
        store.get(ref)


def test_asset_metadata_replayable_through_canonical_commands(
    persist_db_path: pathlib.Path, blob_dir: pathlib.Path
) -> None:
    store = LocalObjectStore(blob_dir)
    ref = store.put(b"asset-bytes", content_type="image/png")
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_material_resolvers)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    # The canonical event records the immutable content-hash as the item identity.
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("asset_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="material.create_item",
            payload={"item_id": ref.content_hash, "kind": "image"},
            world_time=WorldTime(1),
        )
    )
    events = runtime.persistence.event_store.load(iid, branch)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    replayed_record = replayed.entity(EntityId(ref.content_hash))
    assert replayed_record is not None
    assert ref.asset_id.startswith("asset:")
    # Blob is retrievable by that immutable identity.
    assert store.get(ref) == b"asset-bytes"


def test_denied_rights_prevent_delivery() -> None:
    restricted = AssetRef(
        asset_id="asset:secret",
        content_hash="0" * 64,
        size=1,
        content_type="text/plain",
        rights="restricted",
    )
    with pytest.raises(AssetRightsDenied):
        require_delivery_rights(restricted, frozenset({"public"}))
    require_delivery_rights(restricted, frozenset({"restricted"}))
    public = AssetRef(
        asset_id="asset:pub",
        content_hash="1" * 64,
        size=1,
        content_type="text/plain",
        rights="public",
    )
    require_delivery_rights(public, frozenset())
