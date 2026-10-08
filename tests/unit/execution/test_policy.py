"""Authorization and validation rules of the execution policy."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_execution import (
    ExecutionClass,
    ExecutionPolicy,
    NetworkAccess,
    PolicyViolation,
    SecretAccess,
    SideEffectClass,
    TrustLevel,
    authorize,
)


@pytest.mark.unit
def test_default_policies_are_authorized(
    untrusted_policy: ExecutionPolicy, trusted_policy: ExecutionPolicy
) -> None:
    authorize(untrusted_policy)
    authorize(trusted_policy)


@pytest.mark.unit
def test_process_execution_class_is_authorized(untrusted_policy: ExecutionPolicy) -> None:
    authorize(replace(untrusted_policy, execution_class=ExecutionClass.PROCESS))


@pytest.mark.unit
@pytest.mark.parametrize(
    "execution_class",
    [
        ExecutionClass.FUNCTION,
        ExecutionClass.CONTAINER,
        ExecutionClass.WASM,
        ExecutionClass.MICROVM,
        ExecutionClass.VM,
        ExecutionClass.GPU,
        ExecutionClass.REMOTE,
    ],
)
def test_declared_but_unimplemented_class_is_rejected(
    untrusted_policy: ExecutionPolicy, execution_class: ExecutionClass
) -> None:
    with pytest.raises(PolicyViolation) as excinfo:
        authorize(replace(untrusted_policy, execution_class=execution_class))
    message = str(excinfo.value)
    assert "execution_class" in message
    assert execution_class.value in message


@pytest.mark.unit
@pytest.mark.parametrize(
    "trust", [TrustLevel.UNTRUSTED, TrustLevel.THIRD_PARTY, TrustLevel.GENERATED]
)
def test_network_egress_is_rejected_for_untrusted_code(
    untrusted_policy: ExecutionPolicy, trust: TrustLevel
) -> None:
    with pytest.raises(PolicyViolation) as excinfo:
        authorize(replace(untrusted_policy, trust=trust, network=NetworkAccess.EGRESS))
    message = str(excinfo.value)
    assert "network" in message
    assert "trust" in message
    assert NetworkAccess.EGRESS.value in message


@pytest.mark.unit
def test_network_egress_is_allowed_for_trusted_code(trusted_policy: ExecutionPolicy) -> None:
    authorize(replace(trusted_policy, network=NetworkAccess.EGRESS))


@pytest.mark.unit
def test_secret_grant_is_rejected_without_a_secret_broker(
    untrusted_policy: ExecutionPolicy,
) -> None:
    with pytest.raises(PolicyViolation) as excinfo:
        authorize(replace(untrusted_policy, secrets=SecretAccess.EXPLICIT_GRANT))
    message = str(excinfo.value)
    assert "secrets" in message
    assert SecretAccess.EXPLICIT_GRANT.value in message


@pytest.mark.unit
def test_irreversible_side_effects_are_rejected_by_the_fabric(
    untrusted_policy: ExecutionPolicy,
) -> None:
    with pytest.raises(PolicyViolation) as excinfo:
        authorize(replace(untrusted_policy, side_effects=SideEffectClass.IRREVERSIBLE_EXTERNAL))
    message = str(excinfo.value)
    assert "side_effects" in message
    assert "outbox" in message


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("cpu_seconds_limit", 0),
        ("cpu_seconds_limit", -5),
        ("memory_mb_limit", 0),
        ("wall_seconds_limit", -1),
        ("reproducibility", "   "),
        ("cost_class", ""),
    ],
)
def test_invalid_policy_values_are_rejected_on_construction(
    field_name: str, bad_value: object
) -> None:
    with pytest.raises(PolicyViolation) as excinfo:
        replace(ExecutionPolicy.default_untrusted(), **{field_name: bad_value})
    assert field_name in str(excinfo.value)
