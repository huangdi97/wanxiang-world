"""Visual generation budget units are discrete non-negative integers."""

# pyright: reportPrivateUsage=false

import pytest
from wanxiang_substrate.assets.book_generation_budget import _require_nonnegative_int


@pytest.mark.parametrize("value", [True, False, 1.5, "3", None, -1])
def test_generation_budget_rejects_ambiguous_numeric_values(value: object) -> None:
    with pytest.raises(ValueError, match="non-negative integer"):
        _require_nonnegative_int(value, label="visual budget")


@pytest.mark.parametrize("value", [0, 1, 17])
def test_generation_budget_accepts_discrete_nonnegative_units(value: int) -> None:
    assert _require_nonnegative_int(value, label="visual budget") == value
