"""File-signature and structural validation for known T3 spatial artifacts."""

# pyright: reportUnusedFunction=false

from __future__ import annotations


_PLY_FORMATS = frozenset(
    {
        b"format ascii 1.0",
        b"format binary_little_endian 1.0",
        b"format binary_big_endian 1.0",
    }
)


def _ply_format(content: bytes) -> bytes | None:
    """Return a bounded PLY 1.0 format declaration for a structurally valid header."""
    if not content.startswith((b"ply\n", b"ply\r\n")):
        return None
    lines = content[:65536].replace(b"\r\n", b"\n").split(b"\n")
    try:
        end_index = lines.index(b"end_header")
    except ValueError:
        return None
    header_lines = lines[: end_index + 1]
    if len(header_lines) < 3 or header_lines[0] != b"ply":
        return None
    format_lines = [line for line in header_lines[1:] if line.startswith(b"format ")]
    if len(format_lines) != 1 or format_lines[0] not in _PLY_FORMATS:
        return None
    return format_lines[0]


def _known_spatial_signature_matches(media_type: str, content: bytes) -> bool:
    """Reject masquerading bytes for formats Wanxiang can identify locally."""
    if media_type == "model/gltf-binary":
        if len(content) < 12 or content[:4] != b"glTF":
            return False
        version = int.from_bytes(content[4:8], "little")
        declared_length = int.from_bytes(content[8:12], "little")
        return version == 2 and declared_length == len(content)
    if media_type in {"application/x-ply", "model/ply"}:
        return _ply_format(content) is not None
    if media_type == "image/png":
        return content.startswith(bytes.fromhex("89504e470d0a1a0a"))
    if media_type == "image/jpeg":
        return content.startswith(bytes.fromhex("ffd8ff"))
    if media_type == "image/webp":
        return content.startswith(b"RIFF") and content[8:12] == b"WEBP"
    return False


def _image_media_type(content: bytes) -> str:
    for media_type in ("image/png", "image/jpeg", "image/webp"):
        if _known_spatial_signature_matches(media_type, content):
            return media_type
    raise ValueError("TokenHub spatial preview is not PNG, JPEG or WebP")


def _require_ply_artifact(content: bytes) -> None:
    """Require a bounded, structurally recognizable PLY header before storage."""
    if not _known_spatial_signature_matches("model/ply", content):
        raise ValueError("TokenHub spatial geometry is not a PLY artifact")
    ply_format = _ply_format(content)
    if ply_format is None:
        raise ValueError("TokenHub spatial geometry has an invalid bounded PLY header")
    if ply_format not in {
        b"format ascii 1.0",
        b"format binary_little_endian 1.0",
    }:
        raise ValueError("TokenHub spatial geometry uses an unsupported PLY format")
