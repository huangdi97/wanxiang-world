"""G101A versioned M98 matrix contracts."""

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import BurnInMatrix, stable_m98_matrix


def test_stable_matrix_covers_complete_30d_and_90d_rows() -> None:
    matrix = stable_m98_matrix()
    assert matrix.verify_hash()
    assert len(matrix.rows) == 18
    assert sum(row.horizon == "30d" for row in matrix.rows) == 12
    assert sum(row.horizon == "90d" for row in matrix.rows) == 6
    assert BurnInMatrix.from_dict(matrix.to_dict()) == matrix


def test_matrix_rejects_partial_shape() -> None:
    matrix = stable_m98_matrix()
    with pytest.raises(ContractError, match="12 30d"):
        BurnInMatrix(
            matrix_id=matrix.matrix_id,
            world_package_ref=matrix.world_package_ref,
            scenario_ref=matrix.scenario_ref,
            rows=matrix.rows[:-1],
        )


def test_ninety_day_rows_use_baseline_policy() -> None:
    matrix = stable_m98_matrix()
    assert all(row.policy_profile == "baseline" for row in matrix.rows if row.horizon == "90d")
