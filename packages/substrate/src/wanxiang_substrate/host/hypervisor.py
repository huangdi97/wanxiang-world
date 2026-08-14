"""World Hypervisor ? multi-instance isolation over the existing WorldHost
(G31D).

This is NOT a second host: it composes the existing WorldHost/HostRegistry and
adds explicit instance/worldline routing, per-instance resource budgets and
runtime-profile binding. Every command carries its instance/worldline
(CommandEnvelope.instance_id + branch_id) and is verified against the route
target before submission.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import WorldInstanceId

from wanxiang_substrate.host.host import HostRegistry, WorldHost
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    """A runtime profile bound to an instance (budget + evolution policy)."""

    name: str
    budget: ResourceBudget = ResourceBudget()
    evolution_policy: str = "canonical_replay"


class WorldHypervisor:
    """Routes commands to per-instance WorldHosts with budgets and profiles."""

    def __init__(self) -> None:
        self._registry = HostRegistry()
        self._profiles: dict[str, RuntimeProfile] = {}
        self._trackers: dict[str, BudgetTracker] = {}

    def bind(self, host: WorldHost, *, profile: RuntimeProfile | None = None) -> WorldHost:
        instance = host.handle.instance_id.value
        self._registry.register(host)
        self._profiles[instance] = profile or RuntimeProfile(name="default")
        self._trackers[instance] = BudgetTracker(self._profiles[instance].budget)
        return host

    def profile(self, instance_id: WorldInstanceId) -> RuntimeProfile:
        profile = self._profiles.get(instance_id.value)
        if profile is None:
            raise ContractError(f"no runtime profile bound for {instance_id.value!r}")
        return profile

    def host(self, instance_id: WorldInstanceId) -> WorldHost:
        return self._registry.require(instance_id)

    def submit(self, instance_id: WorldInstanceId, command: CommandEnvelope) -> None:
        """Route a command with explicit instance/worldline to its host."""
        if command.instance_id != instance_id:
            raise ContractError(
                f"command targets {command.instance_id.value!r} but route is {instance_id.value!r}"
            )
        tracker = self._trackers.get(instance_id.value)
        if tracker is None:
            raise ContractError(f"instance {instance_id.value!r} is not bound")
        tracker.consume(commands=1)
        self._registry.require(instance_id).submit(command)

    def statuses(self) -> tuple[object, ...]:
        return self._registry.list_statuses()

    def shutdown(self) -> None:
        self._registry.shutdown()
        self._profiles.clear()
        self._trackers.clear()
