"""G03D: action validator preconditions."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.actions.validator import ActionValidator


def _empty_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("wld_v"),
        branch_id=BranchId("br_v"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


def _registry() -> ActionRegistry:
    registry = ActionRegistry()
    register_reference_actions(registry)
    return registry


def _command(
    action: str, payload: Mapping[str, FieldValue], actor: str | None = "a"
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(f"cmd_{action.replace('.', '_')}"),
        instance_id=WorldInstanceId("wld_v"),
        branch_id=BranchId("br_v"),
        expected_revision=BranchRevision(0),
        action_type=action,
        payload=payload,
        actor_id=ActorId(actor) if actor else None,
    )


@pytest.mark.unit
def test_unknown_action_rejected_explicitly() -> None:
    validator = ActionValidator(_registry())
    result = validator.validate(_command("bogus.action", {}), _empty_state())
    assert result.ok is False
    assert result.issues[0].code == "unknown_action"


@pytest.mark.unit
def test_missing_parameter_rejected() -> None:
    validator = ActionValidator(_registry())
    result = validator.validate(_command("spatial.move", {}), _empty_state())
    assert any(i.code == "missing_parameter" for i in result.issues)


@pytest.mark.unit
def test_wrong_parameter_type_rejected() -> None:
    validator = ActionValidator(_registry())
    result = validator.validate(
        _command("body.rest", {"actor_id": "a", "ticks": "not_an_int"}), _empty_state()
    )
    assert any(i.code == "parameter_type" for i in result.issues)


@pytest.mark.unit
def test_missing_actor_rejected() -> None:
    validator = ActionValidator(_registry())
    result = validator.validate(
        _command("spatial.move", {"entity_id": "e", "target_place_id": "p"}, actor="ghost"),
        _empty_state(),
    )
    assert any(i.code == "actor_missing" for i in result.issues)


@pytest.mark.unit
def test_validation_is_side_effect_free() -> None:
    state = _empty_state()
    before = state.semantic_hash()
    validator = ActionValidator(_registry())
    validator.validate(_command("bogus.action", {}), state)
    validator.validate(_command("spatial.move", {}), state)
    assert state.semantic_hash() == before
    assert len(state.entities()) == 0
