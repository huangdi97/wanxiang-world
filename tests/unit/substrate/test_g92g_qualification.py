"""G92G horizon evidence ledger tests."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.long_horizon import HorizonLabel, HorizonQualification, HorizonSample


def _sample(label: str, tick: int, events: int, storage: int) -> HorizonSample:
    return HorizonSample(
        cast(HorizonLabel, label),
        tick,
        tick,
        ("alice", "bob"),
        events,
        tick // 10,
        storage,
        f"h{tick}",
        f"h{tick}",
    )


def test_24h_and_7d_reference_samples_qualify_when_replay_and_storage_are_monotonic() -> None:
    qualification = HorizonQualification("run-g92g")
    qualification.record(_sample("24h", 100, 10, 1000))
    qualification.record(_sample("7d", 700, 70, 3000))
    report = qualification.finish()
    assert report.qualified is True
    assert report.replay_recovery_equal is True
    assert report.storage_bytes_growth == 2000


def test_horizon_rejects_regression_and_missing_replay_equality() -> None:
    qualification = HorizonQualification("run-g92g-fail")
    qualification.record(_sample("24h", 100, 10, 1000))
    with pytest.raises(ContractError):
        qualification.record(_sample("7d", 90, 9, 900))
    failed = HorizonSample("7d", 700, 700, ("alice", "bob"), 70, 7, 3000, "before", "after")
    qualification.record(failed)
    assert qualification.finish().qualified is False
