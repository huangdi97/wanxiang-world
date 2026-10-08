"""Provider-neutral Execution Fabric router.

Callers declare an ExecutionPolicy; they do not select Docker/process by reaching
into provider implementations. The router selects the registered provider for
the requested execution class, while each provider remains responsible for
honestly enforcing the rest of the policy.

The router is orchestration only and imports no World state or commit surface.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from wanxiang_execution.errors import PolicyViolation
from wanxiang_execution.fabric import ExecutionRequest, ExecutionResult
from wanxiang_execution.policy import ExecutionClass, ExecutionPolicy


class ExecutionProvider(Protocol):
    """One execution provider behind the Runtime Router seam."""

    provider_id: str
    provider_version: str
    execution_class: ExecutionClass

    def run(self, request: ExecutionRequest, workspace_dir: Path) -> ExecutionResult:
        """Run one already-declared execution request."""


class ExecutionRouter:
    """Resolve execution requirements to exactly one registered provider."""

    def __init__(self, providers: Iterable[ExecutionProvider] = ()) -> None:
        self._providers: dict[ExecutionClass, ExecutionProvider] = {}
        for provider in providers:
            self.register(provider)

    def register(self, provider: ExecutionProvider) -> None:
        execution_class = provider.execution_class
        if execution_class in self._providers:
            existing = self._providers[execution_class]
            raise PolicyViolation(
                "execution provider already registered for "
                f"{execution_class.value!r}: {existing.provider_id!r}"
            )
        self._providers[execution_class] = provider

    def resolve(self, policy: ExecutionPolicy) -> ExecutionProvider:
        provider = self._providers.get(policy.execution_class)
        if provider is None:
            available = ", ".join(sorted(item.value for item in self._providers))
            raise PolicyViolation(
                f"no execution provider for {policy.execution_class.value!r}; "
                f"available=[{available}]"
            )
        return provider

    def run(self, request: ExecutionRequest, workspace_dir: Path) -> ExecutionResult:
        return self.resolve(request.policy).run(request, workspace_dir)

    def provider_ids(self) -> tuple[str, ...]:
        return tuple(
            self._providers[key].provider_id
            for key in sorted(self._providers, key=lambda item: item.value)
        )


__all__ = ["ExecutionProvider", "ExecutionRouter"]
