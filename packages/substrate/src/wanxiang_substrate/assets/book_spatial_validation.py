"""Local structural validation for external T3 spatial artifacts.

Provider field names and MIME labels are not trusted as proof of file type.
These checks validate only transport structure; spatial geometry remains a
derived projection and never becomes Canon or History.
"""

from __future__ import annotations


def _image_media_type(content: bytes) -> str:
    if content.startswith(bytes.fromhex("89504e470d0a1a0a")):
        return "image/png"
    if content.startswith(bytes.fromhex("ffd8ff")):
        return "image/jpeg"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("TokenHub spatial preview is not PNG, JPEG or WebP")


def _require_ply_artifact(content: bytes) -> None:
    """Require a bounded, structurally recognizable PLY header before storage."""
    if not content.startswith((b"ply\n", b"ply\r\n")):
        raise ValueError("TokenHub spatial geometry is not a PLY artifact")
    header = content[:65536]
    normalized = header.replace(b"\r\n", b"\n")
    lines = normalized.split(b"\n")
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
