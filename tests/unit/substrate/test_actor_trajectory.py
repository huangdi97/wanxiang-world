"""Actor Trajectory Ledger privacy, retention and persistence acceptance."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from wanxiang_substrate.actor_continuity.trajectory import (
    ActorTrajectoryLedger,
    ActorTrajectoryRecord,
)


def _record(*, retention_until: str = "2026-10-08T00:00:00Z") -> ActorTrajectoryRecord:
    return ActorTrajectoryRecord(
        trajectory_id="traj-1",
        actor_id="actor-1",
        world_id="world-1",
        worldline_id="wl-1",
        decision_id="decision-1",
        created_at="2026-10-07T00:00:00Z",
        observation_refs=("obs:1",),
        memory_refs=("memory:private:1",),
        memory_hashes=("sha256:memory",),
        belief_refs=("belief:1",),
        provider_id="provider.test",
        model_id="model.test",
        tool_refs=("tool:1",),
        plan_ref="plan:1",
        intent_ref="intent:1",
        adjudication_ref="adjudication:1",
        outcome_ref="outcome:1",
        world_event_refs=("event:committed:1",),
        rights_scope=("trajectory.read.private",),
        retention_until=retention_until,
    )


def test_unauthorized_read_is_filtered_and_authorized_read_returns_refs_only() -> None:
    ledger = ActorTrajectoryLedger()
    ledger.record(_record())

    assert ledger.read("actor-1", requester_scopes=("trajectory.read",)) == ()
    visible = ledger.read("actor-1", requester_scopes=("trajectory.read.private",))
    assert visible[0].memory_refs == ("memory:private:1",)
    assert not hasattr(visible[0], "prompt")
    assert not hasattr(visible[0], "memory_content")


def test_redaction_preserves_world_event_link_and_never_mutates_world_history() -> None:
    ledger = ActorTrajectoryLedger()
    ledger.record(_record())

    with pytest.raises(PermissionError):
        ledger.redact("traj-1", requester_scopes=("trajectory.read.private",))

    redacted = ledger.redact("traj-1", requester_scopes=("trajectory.admin",))
    assert redacted.redacted is True
    assert redacted.memory_refs == ()
    assert redacted.provider_id == ""
    assert redacted.world_event_refs == ("event:committed:1",)
    assert redacted.memory_hashes == ("sha256:memory",)
    assert not hasattr(ledger, "commit")


def test_retention_prunes_only_trajectory_records() -> None:
    ledger = ActorTrajectoryLedger()
    ledger.record(_record(retention_until="2026-10-07T01:00:00Z"))

    expired = ledger.prune_expired(
        datetime(2026, 10, 7, 2, tzinfo=UTC),
        requester_scopes=("trajectory.admin",),
    )
    assert expired == ("traj-1",)
    assert ledger.entries() == ()


def test_encoded_at_rest_codec_round_trips_without_plaintext(tmp_path: Path) -> None:
    path = tmp_path / "trajectory.jsonl"

    def xor(value: bytes) -> bytes:
        return bytes(byte ^ 0xA5 for byte in value)

    ledger = ActorTrajectoryLedger(path, encode=xor, decode=xor)
    ledger.record(_record())
    stored = path.read_text(encoding="ascii")
    assert "memory:private:1" not in stored
    assert "provider.test" not in stored

    restored = ActorTrajectoryLedger(path, encode=xor, decode=xor)
    assert restored.entries() == ledger.entries()
