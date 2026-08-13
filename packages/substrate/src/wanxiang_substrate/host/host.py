"""WorldHost: orchestration boundary, not a second Commit Authority (G05A).

The host holds the authoritative runtime and routes commands/queries through
it; it never mutates canonical state itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.host.errors import (
    HostNotFound,
    HostNotRunning,
    InvalidHostTransition,
)
from wanxiang_substrate.host.model import HostStatus, LifecycleMode


@dataclass(frozen=True, slots=True)
class HostHandle:
    """Opaque handle to a hosted world instance."""

    instance_id: WorldInstanceId
    root_branch_id: BranchId


class WorldHost:
    """Orchestrates one world instance; every command goes to Commit Authority."""

    def __init__(
        self,
        runtime: WorldRuntime,
        instance_id: WorldInstanceId,
        root_branch_id: BranchId,
        *,
        scheduler_enabled: bool = False,
    ) -> None:
        self._runtime = runtime
        self._status = HostStatus(
            instance_id=instance_id,
            root_branch_id=root_branch_id,
            mode="running",
            scheduler_enabled=scheduler_enabled,
        )
        self._create_result: CreateWorldResult | None = None

    @property
    def handle(self) -> HostHandle:
        return HostHandle(self._status.instance_id, self._status.root_branch_id)

    def start(self) -> HostStatus:
        self._status = self._transition("running")
        return self._status

    def pause(self) -> HostStatus:
        self._status = self._transition("paused")
        return self._status

    def stop(self) -> HostStatus:
        self._status = self._transition("stopped")
        return self._status

    def resume(self) -> HostStatus:
        self._status = self._transition("running")
        return self._status

    def status(self) -> HostStatus:
        state = self._runtime.current_state(self._status.instance_id, self._status.root_branch_id)
        return HostStatus(
            instance_id=self._status.instance_id,
            root_branch_id=self._status.root_branch_id,
            mode=self._status.mode,
            revision=state.revision.value,
            scheduler_enabled=self._status.scheduler_enabled,
        )

    def submit(self, command: CommandEnvelope) -> None:
        """Command port: validates lifecycle then routes to Commit Authority."""
        if self._status.mode == "stopped":
            raise HostNotRunning("host is stopped")
        if self._status.mode == "paused":
            raise HostNotRunning("host is paused")
        self._runtime.submit_command(command)

    def query(self, branch_id: BranchId):
        return self._runtime.current_state(self._status.instance_id, branch_id)

    def events(self, branch_id: BranchId):
        return self._runtime.events(self._status.instance_id, branch_id)

    def _transition(self, next_mode: LifecycleMode) -> HostStatus:
        if not self._status.can_transition_to(next_mode):
            raise InvalidHostTransition(f"cannot move host from {self._status.mode} to {next_mode}")
        return HostStatus(
            instance_id=self._status.instance_id,
            root_branch_id=self._status.root_branch_id,
            mode=next_mode,
            revision=self._status.revision,
            scheduler_enabled=self._status.scheduler_enabled,
        )


class HostRegistry:
    """Maps world instance ids to their hosts (single-process modular monolith)."""

    def __init__(self) -> None:
        self._hosts: dict[str, WorldHost] = {}

    def register(self, host: WorldHost) -> None:
        self._hosts[host.handle.instance_id.value] = host

    def get(self, instance_id: WorldInstanceId) -> WorldHost | None:
        return self._hosts.get(instance_id.value)

    def require(self, instance_id: WorldInstanceId) -> WorldHost:
        host = self.get(instance_id)
        if host is None:
            raise HostNotFound(f"no host for {instance_id.value!r}")
        return host

    def list_statuses(self) -> tuple[HostStatus, ...]:
        return tuple(host.status() for host in self._hosts.values())

    def shutdown(self) -> None:
        self._hosts.clear()
