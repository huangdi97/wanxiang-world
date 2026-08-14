"""G32G: evolution telemetry & privacy rights."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_substrate.evolution.telemetry import (
    CrossWorldDataset,
    TelemetryEnvelope,
)


@pytest.mark.unit
def test_unauthorized_world_data_does_not_enter_cross_world_dataset() -> None:
    dataset = CrossWorldDataset()
    no_consent = TelemetryEnvelope(
        envelope_id="t1", world_ref="wld_a", kind="metadata", metric="ticks", consent=False
    )
    with pytest.raises(PermissionDenied):
        dataset.add(no_consent)
    # Sensitive trajectory without rights/retention is rejected too.
    sensitive = TelemetryEnvelope(
        envelope_id="t2",
        world_ref="wld_a",
        kind="trajectory",
        metric="actor_lin",
        consent=True,
        rights_ref="platform-default",
    )
    with pytest.raises(PermissionDenied):
        dataset.add(sensitive)
    assert dataset.count() == 0  # nothing unauthorized entered


@pytest.mark.unit
def test_authorized_aggregate_and_hash_enter() -> None:
    dataset = CrossWorldDataset()
    agg = TelemetryEnvelope(
        envelope_id="t3",
        world_ref="wld_a",
        kind="aggregate",
        metric="population",
        consent=True,
        aggregate=120,
    )
    dataset.add(agg)
    assert dataset.count() == 1


@pytest.mark.unit
def test_deletion_revocation_policy() -> None:
    dataset = CrossWorldDataset()
    dataset.add(
        TelemetryEnvelope(
            envelope_id="t4", world_ref="wld_a", kind="metadata", metric="ticks", consent=True
        )
    )
    dataset.add(
        TelemetryEnvelope(
            envelope_id="t5",
            world_ref="wld_b",
            kind="trajectory",
            metric="actor_x",
            consent=True,
            rights_ref="rights:cc0",
            retention_days=30,
        )
    )
    assert dataset.count() == 2
    removed = dataset.revoke_world("wld_a")
    assert removed == 1
    assert dataset.get("t4") is None
    assert dataset.get("t5") is not None
    assert dataset.count() == 1
