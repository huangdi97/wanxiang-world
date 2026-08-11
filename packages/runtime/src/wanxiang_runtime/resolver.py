"""Deterministic resolution seam.

A resolver turns a validated command into a ProposedWorldDelta. Resolvers may
read the current canonical state (never mutate it) to apply deterministic
policies such as resource conservation. Domain-specific resolvers register
against action types; core never hard-codes a specific world.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected

from wanxiang_runtime.state import InMemoryCanonicalState

Resolver = Callable[[CommandEnvelope, InMemoryCanonicalState | None], ProposedWorldDelta]


class CommandValidator(Protocol):
    """Validates a command before resolution."""

    def validate(self, command: CommandEnvelope) -> None: ...


class ResolverRegistry:
    """Maps action types to deterministic, state-aware resolvers."""

    def __init__(self) -> None:
        self._resolvers: dict[str, Resolver] = {}

    def register(self, action_type: str, resolver: Resolver) -> None:
        self._resolvers[action_type] = resolver

    def action_types(self) -> tuple[str, ...]:
        return tuple(sorted(self._resolvers))

    def resolve(
        self,
        command: CommandEnvelope,
        state: InMemoryCanonicalState | None = None,
    ) -> ProposedWorldDelta:
        resolver = self._resolvers.get(command.action_type)
        if resolver is None:
            raise ValidationRejected(f"no resolver registered for action {command.action_type!r}")
        return resolver(command, state)
