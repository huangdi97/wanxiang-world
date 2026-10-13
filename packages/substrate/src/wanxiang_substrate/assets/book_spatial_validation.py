"""File-signature validation for known T3 spatial artifact formats."""

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
    return True
