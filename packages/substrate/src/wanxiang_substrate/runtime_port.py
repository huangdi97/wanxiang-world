"""Narrow WorldRuntime port for substrate consumers (G29E).

Substrate (Runtime/Forge) must not depend on the application composition root.
This consumer-owned port declares only the slice of the application WorldRuntime
that substrate actually calls, keeping the dependency direction
substrate -> runtime/domain and letting the application implement it
structurally (duck typing, no import from application).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.state import InMemoryCanonicalState


@dataclass(frozen=True, slots=True)
class WorldCreateResult:
    """Substrate-local shape of a world-creation result."""

    instance_id: WorldInstanceId
    root_branch_id: BranchId


class WorldRuntimePort(Protocol):
    """The slice of the authoritative application runtime substrate may use."""

    def current_state(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> InMemoryCanonicalState: ...

    def submit_command(self, envelope: CommandEnvelope) -> object: ...

    def events(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> tuple[CommittedEvent, ...]: ...
