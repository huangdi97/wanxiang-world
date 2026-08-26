"""Free-action intent compilation into proposal-only command envelopes."""

from __future__ import annotations

import re
from collections.abc import Mapping

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.action_model import (
    ActionAffordance,
    ActionProposal,
    IntentCompileResult,
)


class IntentCompiler:
    """Deterministic adapter from UI/free text to the shared action proposal."""

    _INJECTION_MARKERS = (
        "ignore previous",
        "ignore all previous",
        "system prompt",
        "developer message",
        "commit authority",
        "write canonical",
    )

    def __init__(self, affordances: tuple[ActionAffordance, ...]) -> None:
        self._affordances = {item.action_type: item for item in affordances}
        if len(self._affordances) != len(affordances):
            raise ContractError("affordances must not duplicate action types")
        self._aliases = {
            alias.casefold(): item.action_type
            for item in affordances
            for alias in item.text_aliases
        }

    def compile_text(
        self,
        *,
        session_id: str,
        instance_id: str,
        branch_id: str,
        actor_id: str,
        text: str,
    ) -> IntentCompileResult:
        raw = text.strip()
        if not raw:
            return self._needs("empty_intent", session_id, instance_id, branch_id, actor_id, text)
        lowered = raw.casefold()
        if any(marker in lowered for marker in self._INJECTION_MARKERS):
            return self._reject(
                "unsafe_intent_text", session_id, instance_id, branch_id, actor_id, text
            )
        action_type = self._action_type_from_text(lowered)
        if action_type is None:
            return self._unsupported(
                "no_allowed_affordance", session_id, instance_id, branch_id, actor_id, text
            )
        if len([name for name in self._affordances if name.casefold() in lowered]) > 1:
            return self._needs(
                "multiple_affordances", session_id, instance_id, branch_id, actor_id, text
            )
        payload = self._payload_from_text(action_type, raw, actor_id)
        if payload is None:
            return self._needs(
                f"missing_fields:{','.join(self._affordances[action_type].required_fields)}",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                text,
            )
        return self._proposed(
            session_id, instance_id, branch_id, actor_id, action_type, payload, text
        )

    def compile_structured(
        self,
        *,
        session_id: str,
        instance_id: str,
        branch_id: str,
        actor_id: str,
        action_type: str,
        payload: Mapping[str, object],
    ) -> IntentCompileResult:
        affordance = self._affordances.get(action_type)
        if affordance is None:
            return self._unsupported(
                "unsupported_action", session_id, instance_id, branch_id, actor_id, action_type
            )
        clean = self._clean_payload(payload)
        if clean is None:
            return self._reject(
                "payload_must_be_flat_primitives",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                action_type,
            )
        missing = [field for field in affordance.required_fields if field not in clean]
        if missing:
            return self._needs(
                f"missing_fields:{','.join(missing)}",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                action_type,
            )
        if not actor_id:
            return self._reject(
                "embodied_actor_required", session_id, instance_id, branch_id, actor_id, action_type
            )
        return self._proposed(
            session_id, instance_id, branch_id, actor_id, action_type, clean, action_type
        )

    def _action_type_from_text(self, lowered: str) -> str | None:
        for alias, action_type in self._aliases.items():
            if alias in lowered:
                return action_type
        for action_type in self._affordances:
            if action_type.casefold() in lowered:
                return action_type
        return None

    def _payload_from_text(
        self, action_type: str, raw: str, actor_id: str
    ) -> dict[str, FieldValue] | None:
        affordance = self._affordances[action_type]
        payload: dict[str, FieldValue] = {}
        if "entity_id" in affordance.required_fields:
            payload["entity_id"] = actor_id
        if "status" in affordance.required_fields:
            match = re.search(r"(?:status|to)\s*(?:=|is|to)?\s*([\w-]+)\s*$", raw, re.I)
            if match is None:
                return None
            payload["status"] = match.group(1)
        if any(field not in payload for field in affordance.required_fields):
            return None
        return payload

    @staticmethod
    def _clean_payload(payload: Mapping[str, object]) -> dict[str, FieldValue] | None:
        if len(payload) > 16:
            return None
        clean: dict[str, FieldValue] = {}
        for key, value in payload.items():
            if not key or key.startswith("__"):
                return None
            if value is not None and not isinstance(value, (str, int, float, bool)):
                return None
            clean[key] = value
        return clean

    def _proposed(
        self,
        session_id: str,
        instance_id: str,
        branch_id: str,
        actor_id: str,
        action_type: str,
        payload: Mapping[str, FieldValue],
        input_text: str,
    ) -> IntentCompileResult:
        return IntentCompileResult(
            ActionProposal(
                proposal_id=f"proposal:{session_id}:{action_type}",
                session_id=session_id,
                instance_id=instance_id,
                branch_id=branch_id,
                actor_id=actor_id,
                action_type=action_type,
                payload=payload,
                status="proposed",
                input_text=input_text,
            )
        )

    @staticmethod
    def _needs(
        reason: str, session_id: str, instance_id: str, branch_id: str, actor_id: str, text: str
    ) -> IntentCompileResult:
        return IntentCompileResult(
            ActionProposal(
                f"proposal:{session_id}:clarify",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                "",
                {},
                "needs_clarification",
                input_text=text,
                clarification=reason,
            )
        )

    @staticmethod
    def _unsupported(
        reason: str, session_id: str, instance_id: str, branch_id: str, actor_id: str, text: str
    ) -> IntentCompileResult:
        return IntentCompileResult(
            ActionProposal(
                f"proposal:{session_id}:unsupported",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                "",
                {},
                "unsupported",
                input_text=text,
                rejection_reason=reason,
            )
        )

    @staticmethod
    def _reject(
        reason: str, session_id: str, instance_id: str, branch_id: str, actor_id: str, text: str
    ) -> IntentCompileResult:
        return IntentCompileResult(
            ActionProposal(
                f"proposal:{session_id}:rejected",
                session_id,
                instance_id,
                branch_id,
                actor_id,
                "",
                {},
                "rejected",
                input_text=text,
                rejection_reason=reason,
            )
        )
