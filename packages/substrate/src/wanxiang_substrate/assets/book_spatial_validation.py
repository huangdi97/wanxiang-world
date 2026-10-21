"""File-signature and structural validation for known T3 spatial artifacts."""

# pyright: reportUnusedFunction=false

from __future__ import annotations


def _known_spatial_signature_matches(media_type: str, content: bytes) -> bool:
    """Reject masquerading bytes for formats Wanxiang can identify locally."""
    if media_type == "model/gltf-binary":
        if len(content) < 12 or content[:4] != b"glTF":
            return False
        version = int.from_bytes(content[4:8], "little")
        declared_length = int.from_bytes(content[8:12], "little")
        return version == 2 and declared_length == len(content)
    if media_type in {"application/x-ply", "model/ply"}:
        return content.startswith(b"ply\n") or content.startswith(b"ply\r\n")
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
    header = content[:65536].replace(b"\r\n", b"\n")
    lines = header.split(b"\n")
    if len(lines) < 3 or lines[0] != b"ply":
        raise ValueError("TokenHub spatial geometry has an invalid PLY header")
    format_lines = [line for line in lines[1:8] if line.startswith(b"format ")]
    if len(format_lines) != 1:
        raise ValueError("TokenHub spatial geometry has an invalid PLY format declaration")
    if format_lines[0] not in {
        b"format ascii 1.0",
        b"format binary_little_endian 1.0",
        b"format binary_big_endian 1.0",
    }:
        raise ValueError("TokenHub spatial geometry uses an unsupported PLY format")
    if b"end_header" not in lines:
        raise ValueError("TokenHub spatial geometry has no bounded PLY end_header")
