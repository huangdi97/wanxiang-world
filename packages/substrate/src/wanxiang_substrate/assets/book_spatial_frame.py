"""Validated provider coordinate frames for non-canonical T3 projection."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import cast

from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame


def _vector3(value: object, *, label: str) -> tuple[float, float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"spatial projection frame {label} must contain three numbers")
    result: list[float] = []
    for raw in cast(list[object] | tuple[object, ...], value):
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError(
                f"spatial projection frame {label} must contain finite numbers"
            )
        number = float(raw)
        if not math.isfinite(number):
            raise ValueError(
                f"spatial projection frame {label} must contain finite numbers"
            )
        result.append(number)
    return (result[0], result[1], result[2])


def _norm(value: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in value))


def _projection_frame_from_mapping(
    value: object,
    *,
    convention: str = "",
) -> _SpatialProjectionFrame:
    """Normalize provider orientation without promoting it to canonical geometry."""
    if not isinstance(value, Mapping):
        raise ValueError("spatial projection frame must be an object")
    row = cast(Mapping[object, object], value)
    up = _vector3(row.get("up", row.get("up_direction")), label="up")
    forward = _vector3(row.get("forward", row.get("facing_direction")), label="forward")
    center = _vector3(row.get("center", row.get("center_point")), label="center")
    raw_scale = row.get("scale")
    if isinstance(raw_scale, bool) or not isinstance(raw_scale, (int, float)):
        raise ValueError("spatial projection frame scale must be a finite positive number")
    scale = float(raw_scale)
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("spatial projection frame scale must be a finite positive number")
    if _norm(up) < 1e-9 or _norm(forward) < 1e-9:
        raise ValueError("spatial projection frame directions must be non-zero")
    cross = (
        up[1] * forward[2] - up[2] * forward[1],
        up[2] * forward[0] - up[0] * forward[2],
        up[0] * forward[1] - up[1] * forward[0],
    )
    if _norm(cross) < 1e-9:
        raise ValueError("spatial projection frame up and forward must not be parallel")
    return _SpatialProjectionFrame(
        up,
        forward,
        center,
        scale,
        convention.strip()[:80],
    )


def _projection_frame_to_dict(frame: _SpatialProjectionFrame) -> dict[str, object]:
    return {
        "up": list(frame.up),
        "forward": list(frame.forward),
        "center": list(frame.center),
        "scale": frame.scale,
        "convention": frame.convention,
    }
