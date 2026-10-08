"""Ingestion security gate (G55G).

Pre-ingest safety checks: size limit, encoding validity, zip-bomb ratio,
archive path traversal, encrypted members, and corruption (CRC). All failures
are typed and explicit; no risky source proceeds silently. Rights checks stay
in the existing SourceGate (G04B) and are re-asserted here for the adapter path.
"""

from __future__ import annotations

import zipfile
from dataclasses import dataclass

from wanxiang_substrate.sources.errors import SourceError

DEFAULT_MAX_BYTES = 256 * 1024 * 1024  # 256 MiB
DEFAULT_MAX_UNCOMPRESSED_RATIO = 200  # uncompressed <= 200x compressed
TEXT_ENCODINGS = ("utf-8", "utf-16", "utf-16-le", "gb18030")


class IngestSecurityError(SourceError):
    code = "ingest_security_error"


class SourceSizeExceeded(IngestSecurityError):
    code = "source_size_exceeded"


class ZipBomb(IngestSecurityError):
    code = "zip_bomb"


class PathTraversal(IngestSecurityError):
    code = "archive_path_traversal"


class EncryptedSource(IngestSecurityError):
    code = "encrypted_source"


class CorruptSource(IngestSecurityError):
    code = "corrupt_source"


class UndecodableSource(IngestSecurityError):
    code = "undecodable_source"


@dataclass(frozen=True, slots=True)
class SecurityCheck:
    """Result of one ingestion security check."""

    name: str
    ok: bool
    detail: str


def _is_path_traversal(member: str) -> bool:
    normalized = member.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return True
    if normalized.startswith("/") or len(member) >= 2 and member[1] == ":":
        return True
    return any(part in ("..", "") for part in parts)


def check_archive(
    archive: zipfile.ZipFile, *, max_uncompressed_ratio: int = DEFAULT_MAX_UNCOMPRESSED_RATIO
) -> tuple[SecurityCheck, ...]:
    if max_uncompressed_ratio < 0:
        raise ValueError("max_uncompressed_ratio must be non-negative")
    checks: list[SecurityCheck] = []
    members = archive.infolist()
    compressed = sum(info.compress_size for info in members)
    uncompressed = sum(info.file_size for info in members)
    ratio = (uncompressed / compressed) if compressed else 0.0
    checks.append(
        SecurityCheck(
            "zip_bomb_ratio",
            ratio <= max_uncompressed_ratio,
            f"uncompressed/compressed ratio {ratio:.1f} (limit {max_uncompressed_ratio})",
        )
    )
    traversal = [info.filename for info in members if _is_path_traversal(info.filename)]
    checks.append(SecurityCheck("path_traversal", not traversal, f"members={traversal!r}"))
    encrypted = [info.filename for info in members if info.flag_bits & 0x1]
    checks.append(SecurityCheck("encrypted", not encrypted, f"encrypted={encrypted!r}"))
    try:
        bad = archive.testzip()
    except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
        bad = str(exc)
    checks.append(SecurityCheck("corrupt_crc", bad is None, f"bad_member={bad!r}"))
    return tuple(checks)


def _decodable(blob: bytes) -> bool:
    for encoding in TEXT_ENCODINGS:
        try:
            blob.decode(encoding)
            return True
        except (UnicodeDecodeError, LookupError):
            continue
    return False


class IngestSecurityGate:
    """Runs all ingestion security checks before an adapter ingests a source."""

    def __init__(
        self,
        *,
        max_bytes: int = DEFAULT_MAX_BYTES,
        max_uncompressed_ratio: int = DEFAULT_MAX_UNCOMPRESSED_RATIO,
    ) -> None:
        self._max_bytes = max_bytes
        self._max_uncompressed_ratio = max_uncompressed_ratio
        self._checks: list[SecurityCheck] = []

    def check_blob(
        self,
        blob: bytes,
        *,
        kind: str,
        filename: str = "",
    ) -> tuple[SecurityCheck, ...]:
        self._checks = []
        if len(blob) > self._max_bytes:
            raise SourceSizeExceeded(
                f"source {filename or kind!r} is {len(blob)} bytes; limit {self._max_bytes}"
            )
        binary_kinds = ("image", "audio", "video", "asset", "generic_asset", "pdf", "epub", "docx")
        if kind not in binary_kinds and not _decodable(blob):
            raise UndecodableSource(f"source {filename or kind!r} is not decodable as text")
        if kind in ("epub", "docx"):
            try:
                archive = zipfile.ZipFile(__import__("io").BytesIO(blob))
            except (zipfile.BadZipFile, OSError) as exc:
                raise CorruptSource(
                    f"source {filename or kind!r} is not a valid zip: {exc}"
                ) from exc
            try:
                self.check_archive(archive, source_label=filename or kind)
            except IngestSecurityError:
                raise
            except (zipfile.BadZipFile, OSError) as exc:
                raise CorruptSource(
                    f"source {filename or kind!r} failed archive validation: {exc}"
                ) from exc
        return tuple(self._checks)

    def check_archive(
        self, archive: zipfile.ZipFile, *, source_label: str = "archive"
    ) -> tuple[SecurityCheck, ...]:
        """Validate an already-open archive and raise typed failures."""
        checks = check_archive(archive, max_uncompressed_ratio=self._max_uncompressed_ratio)
        self._checks = list(checks)
        failed = {check.name for check in checks if not check.ok}
        if "zip_bomb_ratio" in failed:
            raise ZipBomb(f"source {source_label!r} exceeds zip-bomb ratio")
        if "path_traversal" in failed:
            raise PathTraversal(f"source {source_label!r} contains traversal members")
        if "encrypted" in failed:
            raise EncryptedSource(f"source {source_label!r} has encrypted members")
        if "corrupt_crc" in failed:
            raise CorruptSource(f"source {source_label!r} failed CRC validation")
        return tuple(checks)

    @property
    def last_checks(self) -> tuple[SecurityCheck, ...]:
        return tuple(self._checks)
