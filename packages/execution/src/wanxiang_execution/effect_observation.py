"""Proposal-only observation produced during external-effect reconciliation.

SECURITY INVARIANT:
    An ``EffectObservation`` is NOT world history. It can never be appended to
    canonical history, holds no path to a state writer and confers no authority.
    It is a proposal the reconciliation step offers, and only a Commit Authority
    may decide whether anything derived from it becomes canonical.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from wanxiang_execution.errors import OutboxError
from wanxiang_execution.outbox_records import (
    STATUS_AMBIGUOUS,
    ExternalEffectIntent,
    ExternalEffectResult,
)


@dataclass(frozen=True, slots=True)
class EffectObservation:
    """What one external-effect attempt proposes the authority consider.

    INVARIANT: this object is evidence, never canonical state. See the module
    docstring for the security invariant.

    Attributes:
        intent_id: Intent the observation belongs to.
        worldline_id: Worldline the effect was requested for.
        status: Result status the observation was derived from.
        external_ref: External reference, when the service reported one.
        requires_manual_reconciliation: True when the effect may have happened
            and a human/authority must resolve it before retrying.
        detail: Human-readable detail; never contains secret payloads.
    """

    intent_id: str
    worldline_id: str
    status: str
    external_ref: str | None
    requires_manual_reconciliation: bool
    detail: str

    def digest(self) -> str:
        """Return sha256 over the canonical JSON form of every field.

        Returns:
            Lowercase hex sha256 digest, stable for equal field values.
        """
        payload = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def observe_effect(intent: ExternalEffectIntent, result: ExternalEffectResult) -> EffectObservation:
    """Build the proposal-only observation for one handler result.

    Args:
        intent: Intent the result belongs to, supplying the worldline.
        result: Handler result; must reference the same intent id.

    Returns:
        An observation; ``requires_manual_reconciliation`` is True exactly when
        the result status is STATUS_AMBIGUOUS, because the effect may have
        happened and must not be retried automatically.

    Raises:
        OutboxError: If the result does not belong to the intent.
    """
    if result.intent_id != intent.intent_id or result.idempotency_key != intent.idempotency_key:
        raise OutboxError(
            "external effect result does not belong to the intent: "
            f"intent_id={result.intent_id!r}/{intent.intent_id!r}, "
            f"idempotency_key={result.idempotency_key!r}/{intent.idempotency_key!r}"
        )
    return EffectObservation(
        intent_id=intent.intent_id,
        worldline_id=intent.worldline_id,
        status=result.status,
        external_ref=result.external_ref,
        requires_manual_reconciliation=result.status == STATUS_AMBIGUOUS,
        detail=result.detail,
    )
