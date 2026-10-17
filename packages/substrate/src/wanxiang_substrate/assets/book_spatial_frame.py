"""Validated provider coordinate frames for non-canonical T3 projection."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import cast

from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame


def _vector3(value: object, *, label: str) -> tuple[float, float, float]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"spatial projection frame {label} must contain three numbers")
    parts = cast(list[object] | tuple[object, ...], value)
    if len(parts) != 3:
        raise ValueError(f"spatial projection frame {label} must contain three numbers")
    result: list[float] = []
    for raw in parts:
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError(f"spatial projection frame {label} must contain finite numbers")
        number = float(raw)
        if not math.isfinite(number):
            raise ValueError(f"spatial projection frame {label} must contain finite numbers")
        result.append(number)
    return (result[0], result[1], result[2])


def _norm(value: tuple[float, float, float]) -> float:
    return math.hypot(*value)


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _unit(value: tuple[float, float, float]) -> tuple[float, float, float]:
    length = _norm(value)
    return (value[0] / length, value[1] / length, value[2] / length)


def _orthonormal_basis(
    up: tuple[float, float, float],
    forward: tuple[float, float, float],
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Keep the provider look direction and remove any shear from the up vector.

    Renderers treat the frame as an orthonormal camera basis. Providers may send
    unnormalized or slightly skewed vectors, which would shear the projection, so
    normalize forward and Gram-Schmidt the up vector against it.
    """

    unit_forward = _unit(forward)
    orthogonal_up = (
        up[0] - _dot(up, unit_forward) * unit_forward[0],
        up[1] - _dot(up, unit_forward) * unit_forward[1],
        up[2] - _dot(up, unit_forward) * unit_forward[2],
    )
    if _norm(orthogonal_up) < 1e-9:
        raise ValueError("spatial projection frame up and forward must not be parallel")
    return _unit(orthogonal_up), unit_forward


def _projection_frame_from_mapping(
    value: object,
    *,
    convention: str = "",
) -> _SpatialProjectionFrame:
    """Normalize provider orientation without promoting it to canonical geometry."""
    if not isinstance(value, Mapping):
        raise ValueError("spatial projection frame must be an object")
    row = cast(Mapping[object, object], value)
    raw_convention = convention or row.get("convention", "")
    if not isinstance(raw_convention, str):
        raise ValueError("spatial projection frame convention must be text")
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
    unit_up, unit_forward = _orthonormal_basis(up, forward)
    return _SpatialProjectionFrame(
        unit_up,
        unit_forward,
        center,
        scale,
        raw_convention.strip()[:80],
    )


def _projection_frame_to_dict(frame: _SpatialProjectionFrame) -> dict[str, object]:
    return {
        "up": list(frame.up),
        "forward": list(frame.forward),
        "center": list(frame.center),
        "scale": frame.scale,
        "convention": frame.convention,
    }
