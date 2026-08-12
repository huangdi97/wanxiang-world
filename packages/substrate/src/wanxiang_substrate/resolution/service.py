"""AdjudicationService: resolve + validate delta compatibility (no commit here)."""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ValidationRejected
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.resolution.errors import ResolverVersionError
from wanxiang_substrate.resolution.model import Adjudication, ResolverVersionPin
from wanxiang_substrate.resolution.registry import AdjudicatorRegistry


class AdjudicationService:
    """Resolves an action into an auditable Adjudication whose delta is
    validated for compatibility before Commit Authority (never commits here)."""

    def __init__(self, registry: AdjudicatorRegistry) -> None:
        self._registry = registry

    def resolve(
        self,
        command: CommandEnvelope,
        state: InMemoryCanonicalState,
        *,
        seed: int,
        pins: tuple[ResolverVersionPin, ...] = (),
    ) -> Adjudication:
        version = _pinned_version(command.action_type, pins)
        adjudicator = self._registry.get(command.action_type, version)
        if adjudicator is None:
            raise ResolverVersionError(
                f"no adjudicator for action {command.action_type!r} version {version}"
            )
        adjudication = adjudicator(command, state, seed)
        self._validate_delta(state, adjudication)
        return adjudication

    def _validate_delta(self, state: InMemoryCanonicalState, adjudication: Adjudication) -> None:
        """Dry-run the delta on a copy to prove compatibility before commit."""
        try:
            state.apply(adjudication.delta)
        except Exception as exc:
            raise ValidationRejected(
                f"adjudication delta incompatible with current state: {exc}"
            ) from exc


def _pinned_version(action_type: str, pins: tuple[ResolverVersionPin, ...]) -> int:
    for pin in pins:
        if pin.action_type == action_type:
            return pin.version
    return 1
