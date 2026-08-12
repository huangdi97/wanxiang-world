"""Policy ports: propose-only output, never direct mutation."""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.agency.model import IntentCandidate


class PolicyContext(Protocol):
    """Authorized information a policy may use to propose (read-only)."""

    actor_id: EntityId
    observations: tuple[object, ...]
    beliefs: tuple[object, ...]


class Policy(Protocol):
    """A controller policy: turns authorized context into a propose-only candidate."""

    def propose(self, context: PolicyContext) -> IntentCandidate | None: ...

    def policy_ref(self) -> str: ...


class DeterministicPolicy:
    """Produces a fixed deterministic candidate (no LLM)."""

    def __init__(
        self,
        action_type: str,
        payload: dict[str, FieldValue] | None = None,
        ref: str = "deterministic",
    ) -> None:
        self._action_type = action_type
        self._payload = {str(k): v for k, v in (payload or {}).items()}
        self._ref = ref

    def propose(self, context: PolicyContext) -> IntentCandidate | None:
        return IntentCandidate(
            actor_id=context.actor_id,
            action_type=self._action_type,
            payload=self._payload,
            policy_ref=self._ref,
        )

    def policy_ref(self) -> str:
        return self._ref


class RulePolicy:
    """Rule-based policy: proposes when a rule predicate holds."""

    def __init__(self, action_type: str, rule: str, ref: str = "rule") -> None:
        self._action_type = action_type
        self._rule = rule
        self._ref = ref

    def propose(self, context: PolicyContext) -> IntentCandidate | None:
        # Deterministic example rule: propose only when the actor has at least
        # one observation to act on.
        if not context.observations:
            return None
        return IntentCandidate(
            actor_id=context.actor_id,
            action_type=self._action_type,
            payload={"rule": self._rule},
            policy_ref=self._ref,
        )

    def policy_ref(self) -> str:
        return self._ref


class HumanPolicy:
    """Seam for a human-supplied candidate (returns a queued input or None)."""

    def __init__(self, ref: str = "human") -> None:
        self._ref = ref
        self._pending: list[IntentCandidate] = []

    def queue(self, candidate: IntentCandidate) -> None:
        self._pending.append(candidate)

    def propose(self, context: PolicyContext) -> IntentCandidate | None:
        return self._pending.pop(0) if self._pending else None

    def policy_ref(self) -> str:
        return self._ref
