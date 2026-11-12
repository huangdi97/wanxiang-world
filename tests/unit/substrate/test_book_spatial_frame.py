"""T3 projection frames stay orthonormal so renderers never receive a sheared basis."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import math

import pytest
from wanxiang_substrate.assets.book_spatial_frame import (
    _projection_frame_from_mapping,
    _projection_frame_to_dict,
)


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _norm(value: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in value))


def test_frame_normalizes_non_unit_directions() -> None:
    frame = _projection_frame_from_mapping(
        {"up": [0, 2, 0], "forward": [0, 0, -3], "center": [1, 2, 3], "scale": 0.5}
    )
    assert frame.up == (0.0, 1.0, 0.0)
    assert frame.forward == (0.0, 0.0, -1.0)
    assert frame.center == (1.0, 2.0, 3.0)
    assert frame.scale == 0.5


def test_frame_removes_shear_from_a_skewed_up_vector() -> None:
    frame = _projection_frame_from_mapping(
        {"up": [0, 1, 0], "forward": [0, 1, -1], "center": [0, 0, 0], "scale": 1}
    )

    assert math.isclose(_dot(frame.up, frame.forward), 0.0, abs_tol=1e-12)
    assert math.isclose(_norm(frame.up), 1.0, abs_tol=1e-12)
    assert math.isclose(_norm(frame.forward), 1.0, abs_tol=1e-12)
    # The provider look direction is preserved; only the up vector is corrected.
    assert frame.forward[0] == 0.0
    assert frame.forward[1] > 0
    assert frame.forward[2] < 0


def test_frame_survives_mapping_round_trip() -> None:
    frame = _projection_frame_from_mapping(
        {
            "up": [0, 3, 0],
            "forward": [0, 0, -2],
            "center": [1, -2, 0.5],
            "scale": 2,
            "convention": "provider-frame-v1",
        }
    )

    restored = _projection_frame_from_mapping(_projection_frame_to_dict(frame))

    assert restored == frame


@pytest.mark.parametrize(
    ("up", "forward"),
    [
        ([0, 0, 0], [0, 0, -1]),
        ([0, 1, 0], [0, 0, 0]),
        ([0, 1, 0], [0, 2, 0]),
        ([0, 0, -1], [0, 0, -2]),
    ],
)
def test_frame_rejects_degenerate_bases(up: list[float], forward: list[float]) -> None:
    with pytest.raises(ValueError):
        _projection_frame_from_mapping(
            {"up": up, "forward": forward, "center": [0, 0, 0], "scale": 1}
        )
