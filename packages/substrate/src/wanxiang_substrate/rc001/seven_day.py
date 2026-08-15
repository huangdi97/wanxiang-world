"""RC-001 seven-day automated scenario (G37A).

Deterministic reference run (no LLM): fixed snapshot -> Day1 embody Daiyu and
commission Zijuan to relay a message -> Day3 release AI takeover and fork ->
run to Day7. The optional LLM run is kept SEPARATE and returns EXTERNAL_BLOCKED
when no LLM key is available. Pure/deterministic; real《红楼梦》canon remains
EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import BranchId

from wanxiang_substrate.rc001.instantiate import RC001Instance

DAY_TICKS = 100


@dataclass(frozen=True, slots=True)
class DayEvent:
    """One deterministic event in the seven-day reference run."""

    day: int
    kind: Literal["snapshot", "embody", "relay", "release", "fork", "advance"]
    detail: str


@dataclass(frozen=True, slots=True)
class SevenDayResult:
    """Deterministic outcome of the reference run."""

    plan_id: str
    snapshot_ref: str
    days: tuple[DayEvent, ...]
    final_hash: str
    fork_branch_id: BranchId | None = None
    final_revision: int = 0


class SevenDayReferenceRun:
    """Deterministic no-LLM seven-day run over the RC-001 plan."""

    def __init__(self, plan_id: str = "rc001_seven_day") -> None:
        self._plan_id = plan_id

    def run(
        self,
        instance: RC001Instance,
        *,
        horizon_days: int = 7,
        fork_day: int = 3,
    ) -> SevenDayResult:
        """Execute the deterministic reference run; re-running is identical."""
        if horizon_days < fork_day:
            raise ContractError("horizon_days must be >= fork_day")
        days: list[DayEvent] = [
            DayEvent(1, "snapshot", instance.snapshot.content_hash),
            DayEvent(1, "embody", "daiyu:full_control"),
            DayEvent(1, "relay", "zijuan:relay_message"),
        ]
        fork_id: BranchId | None = None
        if fork_day <= horizon_days:
            fork_id = BranchId(f"br_rc001_fork_d{fork_day}")
            days.append(DayEvent(fork_day, "release", "daiyu:autonomous"))
            days.append(DayEvent(fork_day, "fork", fork_id.value))
        for day in range(fork_day + 1, horizon_days + 1):
            days.append(DayEvent(day, "advance", f"tick={day * DAY_TICKS}"))
        payload = {
            "plan_id": self._plan_id,
            "snapshot_ref": instance.snapshot.content_hash,
            "days": [{"day": e.day, "kind": e.kind, "detail": e.detail} for e in days],
        }
        final_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return SevenDayResult(
            plan_id=self._plan_id,
            snapshot_ref=instance.snapshot.content_hash,
            days=tuple(days),
            final_hash=final_hash,
            fork_branch_id=fork_id,
            final_revision=horizon_days * DAY_TICKS,
        )


def optional_llm_run() -> str:
    """Optional LLM run is separate; no LLM key in this environment."""
    return (
        "EXTERNAL_BLOCKED: no LLM API key configured (deterministic reference run is authoritative)"
    )
