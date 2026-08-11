"""GOAL_01A: version and time semantics."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import PackageVersion, RuntimeVersion, SchemaVersion


@pytest.mark.unit
def test_schema_version_validation() -> None:
    assert SchemaVersion(0).value == 0
    assert SchemaVersion(7).value == 7
    for bad in (-1, "1", 1.5, True):
        with pytest.raises(ContractError):
            SchemaVersion(bad)  # type: ignore[arg-type]


@pytest.mark.unit
def test_runtime_and_package_versions() -> None:
    assert RuntimeVersion(3).value == 3
    assert PackageVersion(2).value == 2


@pytest.mark.unit
def test_world_time_is_monotonic_counter() -> None:
    t0 = WorldTime(0)
    t1 = WorldTime(10)
    assert t1.ticks > t0.ticks
    with pytest.raises(ContractError):
        WorldTime(-1)


@pytest.mark.unit
def test_commit_timestamp_is_timezone_aware() -> None:
    ts = CommitTimestamp(datetime(2026, 1, 1, 12, 0, 0))
    assert ts.utc.tzinfo == UTC
    parsed = CommitTimestamp.from_isoformat("2026-01-01T12:00:00+00:00")
    assert parsed.utc == ts.utc
