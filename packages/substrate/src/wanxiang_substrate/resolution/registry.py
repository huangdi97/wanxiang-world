"""Adjudicator registry keyed by action + version."""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.resolution.model import Adjudication

Adjudicator = Callable[[CommandEnvelope, InMemoryCanonicalState, int], Adjudication]


class AdjudicatorRegistry:
    """Maps (action_type, version) -> adjudicator (propose-only)."""

    def __init__(self) -> None:
        self._adjudicators: dict[tuple[str, int], Adjudicator] = {}

    def register(self, action_type: str, version: int, adjudicator: Adjudicator) -> None:
        self._adjudicators[(action_type, version)] = adjudicator

    def get(self, action_type: str, version: int) -> Adjudicator | None:
        return self._adjudicators.get((action_type, version))

    def has(self, action_type: str, version: int) -> bool:
        return (action_type, version) in self._adjudicators
