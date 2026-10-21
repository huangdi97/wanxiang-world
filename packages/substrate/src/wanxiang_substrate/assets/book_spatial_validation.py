"""File-signature and Player-compatible structural validation for T3 artifacts."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

_PLAYER_MAX_PLY_BYTES = 64 * 1024 * 1024
_PLAYER_MAX_VERTICES = 5_000_000
_PLAYER_MAX_HEADER_BYTES = 64 * 1024
_PLY_FORMATS = frozenset(
    {
        b"format ascii 1.0",
        b"format binary_little_endian 1.0",
        b"format binary_big_endian 1.0",
    }
)
_PLY_SCALAR_BYTES = {
    "char": 1,
    "int8": 1,
    "uchar": 1,
    "uint8": 1,
    "short": 2,
    "int16": 2,
    "ushort": 2,
    "uint16": 2,
    "int": 4,
    "int32": 4,
    "uint": 4,
    "uint32": 4,
    "float": 4,
    "float32": 4,
    "double": 8,
    "float64": 8,
}


def _ply_header(content: bytes) -> tuple[list[bytes], int] | None:
    """Return normalized PLY header lines plus exact payload offset."""
    if not content.startswith((b"ply\n", b"ply\r\n")):
        return None
    prefix = content[:_PLAYER_MAX_HEADER_BYTES]
    for marker in (b"end_header\r\n", b"end_header\n"):
        marker_at = prefix.find(marker)
        if marker_at < 0:
            continue
        end = marker_at + len(marker)
        header = content[:end].replace(b"\r\n", b"\n")
        lines = header.split(b"\n")
        if len(lines) < 3 or lines[0] != b"ply":
            return None
        return lines, end
    return None


def _ply_format(content: bytes) -> bytes | None:
    """Return the unique bounded PLY 1.0 format declaration."""
    parsed = _ply_header(content)
    if parsed is None:
        return None
    lines, _ = parsed
    format_lines = [line for line in lines[1:] if line.startswith(b"format ")]
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
    """Accept only the PLY subset the dependency-free Player can actually render."""
    if not _known_spatial_signature_matches("model/ply", content):
        raise ValueError("TokenHub spatial geometry is not a PLY artifact")
    if len(content) > _PLAYER_MAX_PLY_BYTES:
        raise ValueError("TokenHub spatial geometry exceeds built-in Player PLY size limit")

    parsed = _ply_header(content)
    if parsed is None:
        raise ValueError("TokenHub spatial geometry has an invalid bounded PLY header")
    lines, payload_offset = parsed
    ply_format = _ply_format(content)
    if ply_format not in {b"format ascii 1.0", b"format binary_little_endian 1.0"}:
        raise ValueError("TokenHub spatial geometry uses an unsupported PLY format")

    vertex_count = -1
    in_vertex = False
    data_element_seen = False
    vertex_properties: list[tuple[str, str]] = []
    for raw_line in lines[1:]:
        parts = raw_line.strip().split()
        if not parts:
            continue
        if parts[0] == b"element":
            if len(parts) != 3:
                raise ValueError("TokenHub spatial geometry has an invalid PLY element")
            try:
                count = int(parts[2])
            except ValueError as exc:
                raise ValueError(
                    "TokenHub spatial geometry has an invalid PLY element count"
                ) from exc
            if count < 0:
                raise ValueError("TokenHub spatial geometry has an invalid PLY element count")
            if parts[1] == b"vertex":
                if data_element_seen:
                    raise ValueError("TokenHub spatial PLY vertex data must be first")
                vertex_count = count
                in_vertex = True
            else:
                if count > 0 and vertex_count < 0:
                    data_element_seen = True
                in_vertex = False
        elif parts[0] == b"property" and in_vertex:
            if len(parts) >= 2 and parts[1] == b"list":
                raise ValueError("TokenHub spatial PLY vertex list properties are unsupported")
            if len(parts) != 3:
                raise ValueError("TokenHub spatial geometry has an invalid PLY vertex property")
            scalar_type = parts[1].decode("ascii", errors="ignore")
            if scalar_type not in _PLY_SCALAR_BYTES:
                raise ValueError("TokenHub spatial PLY vertex property type is unsupported")
            name = parts[2].decode("ascii", errors="ignore")
            vertex_properties.append((name, scalar_type))

    if not 0 < vertex_count <= _PLAYER_MAX_VERTICES:
        raise ValueError("TokenHub spatial PLY vertex count is outside Player limits")
    if not {"x", "y", "z"}.issubset({name for name, _ in vertex_properties}):
        raise ValueError("TokenHub spatial PLY requires x/y/z vertex properties")

    if ply_format == b"format binary_little_endian 1.0":
        stride = sum(_PLY_SCALAR_BYTES[scalar_type] for _, scalar_type in vertex_properties)
        if payload_offset + stride * vertex_count > len(content):
            raise ValueError("TokenHub spatial binary PLY vertex payload is truncated")
    elif not content[payload_offset:].strip():
        raise ValueError("TokenHub spatial ASCII PLY has no vertex payload")
