"""G55G: Ingestion security — zip bomb / traversal / size / encoding / encrypted / corrupt."""

from __future__ import annotations

import io
import zipfile

import pytest
from wanxiang_substrate.sources.security import (
    CorruptSource,
    EncryptedSource,
    IngestSecurityGate,
    PathTraversal,
    SourceSizeExceeded,
    UndecodableSource,
    ZipBomb,
    check_archive,
)


@pytest.fixture()
def gate() -> IngestSecurityGate:
    return IngestSecurityGate(max_bytes=1024 * 1024)


def _zip(members: list[tuple[str, bytes]], *, deflate: bool = False) -> bytes:
    buf = io.BytesIO()
    compression = zipfile.ZIP_DEFLATED if deflate else zipfile.ZIP_STORED
    with zipfile.ZipFile(buf, "w", compression=compression) as z:
        for name, data in members:
            z.writestr(name, data)
    return buf.getvalue()


@pytest.mark.unit
def test_clean_zip_passes(gate: IngestSecurityGate) -> None:
    blob = _zip([("OEBPS/chap.xhtml", b"<html><body><p>hello</p></body></html>")])
    checks = gate.check_blob(blob, kind="epub")
    assert all(check.ok for check in checks)


@pytest.mark.unit
def test_size_limit_enforced(gate: IngestSecurityGate) -> None:
    with pytest.raises(SourceSizeExceeded):
        gate.check_blob(b"x" * (1024 * 1024 + 1), kind="text")


@pytest.mark.unit
def test_undecodable_text_rejected(gate: IngestSecurityGate) -> None:
    with pytest.raises(UndecodableSource):
        gate.check_blob(b"\xff\xfe\x00\x01\x02", kind="text")


@pytest.mark.unit
def test_binary_kind_skips_encoding(gate: IngestSecurityGate) -> None:
    gate.check_blob(b"\x89PNG\r\n\x1a\n", kind="image")  # arbitrary binary -> ok


@pytest.mark.unit
def test_zip_bomb_rejected(gate: IngestSecurityGate) -> None:
    blob = _zip([("bomb.txt", b"0" * 400000)], deflate=True)  # highly compressible
    with pytest.raises(ZipBomb):
        gate.check_blob(blob, kind="docx")


@pytest.mark.unit
def test_path_traversal_rejected(gate: IngestSecurityGate) -> None:
    blob = _zip([("../evil.txt", b"x")])
    with pytest.raises(PathTraversal):
        gate.check_blob(blob, kind="epub")


@pytest.mark.unit
def test_encrypted_member_rejected(gate: IngestSecurityGate) -> None:
    blob = _zip([("doc.txt", b"secret")])
    archive = zipfile.ZipFile(io.BytesIO(blob))
    archive.filelist[0].flag_bits |= 0x1
    with pytest.raises(EncryptedSource):
        gate.check_archive(archive)


@pytest.mark.unit
def test_corrupt_zip_rejected(gate: IngestSecurityGate) -> None:
    payload = b"hello world"
    blob = bytearray(_zip([("doc.txt", payload)]))
    index = blob.find(payload)
    assert index >= 0
    blob[index] ^= 0xFF  # corrupt the stored payload -> CRC mismatch
    with pytest.raises(CorruptSource):
        gate.check_blob(bytes(blob), kind="docx")


@pytest.mark.unit
def test_non_zip_for_zip_kind_rejected(gate: IngestSecurityGate) -> None:
    with pytest.raises(CorruptSource):
        gate.check_blob(b"not a zip at all", kind="epub")


@pytest.mark.unit
def test_check_archive_reports_all_failures() -> None:
    blob = _zip([("../x.txt", b"y")])
    archive = zipfile.ZipFile(io.BytesIO(blob))
    archive.filelist[0].flag_bits |= 0x1
    checks = {check.name: check.ok for check in check_archive(archive)}
    assert checks["path_traversal"] is False
    assert checks["encrypted"] is False
