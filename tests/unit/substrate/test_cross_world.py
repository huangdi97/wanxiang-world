"""G33D: cross-world distillation."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_substrate.evolution.cross_world import CrossWorldDistiller
from wanxiang_substrate.evolution.telemetry import CrossWorldDataset, TelemetryEnvelope


def _dataset() -> CrossWorldDataset:
    dataset = CrossWorldDataset()
    # Authorized aggregate/metadata across 3 worlds.
    for world in ("wld_a", "wld_b", "wld_c"):
        dataset.add(
            TelemetryEnvelope(
                envelope_id=f"t_{world}",
                world_ref=world,
                kind="aggregate",
                metric="quiet_after_curfew",
                consent=True,
                aggregate=1,
            )
        )
    return dataset


@pytest.mark.unit
def test_unauthorized_data_is_filtered_out() -> None:
    dataset = CrossWorldDataset()
    # Only 2 authorized worlds for pattern X; one world with no consent.
    for world in ("wld_a", "wld_b"):
        dataset.add(
            TelemetryEnvelope(
                envelope_id=f"x_{world}",
                world_ref=world,
                kind="metadata",
                metric="pattern_x",
                consent=True,
            )
        )
    with pytest.raises(PermissionDenied):
        dataset.add(
            TelemetryEnvelope(
                envelope_id="x_no",
                world_ref="wld_nc",
                kind="metadata",
                metric="pattern_x",
                consent=False,
            )
        )
    distiller = CrossWorldDistiller(dataset, threshold=2)
    candidates = distiller.distill()
    # Only authorized worlds contributed; the no-consent world never appears.
    assert len(candidates) == 1
    assert candidates[0].world_origins == ("wld_a", "wld_b")


@pytest.mark.unit
def test_cross_world_pattern_discovery_preserves_anonymized_origins() -> None:
    distiller = CrossWorldDistiller(_dataset(), threshold=2)
    candidates = distiller.distill()
    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.pattern == "quiet_after_curfew"
    assert candidate.meets_threshold
    # World origins preserved at world level; no actor identity in the envelope.
    assert candidate.world_origins == ("wld_a", "wld_b", "wld_c")
    assert "actor" not in str(candidate)


@pytest.mark.unit
def test_candidate_does_not_activate_directly() -> None:
    distiller = CrossWorldDistiller(_dataset(), threshold=2)
    candidate = distiller.distill()[0]
    with pytest.raises(PermissionDenied):
        distiller.activate(candidate)  # not approved
    approved = replace(candidate, approved=True)
    distiller.activate(approved, approver="reviewer")  # explicit approval works
