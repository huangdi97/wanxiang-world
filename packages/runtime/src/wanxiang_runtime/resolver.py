"""Deterministic resolution seam.

A resolver turns a validated command into a ProposedWorldDelta. Domain-specific
resolvers (later goals/domain packs) register against action types; core never
hard-codes a specific world. A simple registry keeps the seam deterministic and
testable without an LLM.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected

Resolver = Callable[[CommandEnvelope], ProposedWorldDelta]


class CommandValidator(Protocol):
    """Validates a command before resolution."""

    def validate(self, command: CommandEnvelope) -> None: ...


class ResolverRegistry:
    """Maps action types to deterministic resolvers."""

    def __init__(self) -> None:
        self._resolvers: dict[str, Resolver] = {}

    def register(self, action_type: str, resolver: Resolver) -> None:
        self._resolvers[action_type] = resolver

    def resolve(self, command: CommandEnvelope) -> ProposedWorldDelta:
        resolver = self._resolvers.get(command.action_type)
        if resolver is None:
            raise ValidationRejected(f"no resolver registered for action {command.action_type!r}")
        return resolver(command)
