"""G96F: external engine discovery records unavailable state honestly."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import (
    BlockedExternalEngineAdapter,
    ExternalEngineAdapter,
    ExternalEngineCapability,
)


def test_blocked_discovery_round_trip_never_claims_engine_success() -> None:
    adapter = BlockedExternalEngineAdapter(
        engine_id="godot",
        engine_kind="renderer",
        reason="Godot runtime is not installed in the CI environment",
    )
    capability = adapter.discover()

    assert isinstance(adapter, ExternalEngineAdapter)
    assert capability.external_blocked is True
    assert capability.available is False
    assert capability.deterministic is False
    assert capability.version == ""
    assert ExternalEngineCapability.from_dict(capability.to_dict()) == capability
    assert not hasattr(adapter, "commit")
    assert not hasattr(adapter, "apply")


def test_capability_rejects_mismatched_available_status() -> None:
    with pytest.raises(ContractError, match="does not match"):
        ExternalEngineCapability(
            engine_id="phaser",
            engine_kind="renderer",
            availability="external_blocked",
            available=True,
            reason="runtime unavailable",
        )
