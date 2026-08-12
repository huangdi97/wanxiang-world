"""G02E: institution value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.institution.model import DelegatedPermission, Duty, Membership, Role


@pytest.mark.unit
def test_role_grants_permission() -> None:
    role = Role(EntityId("r"), "member", ("enter.study", "read"))
    assert role.grants("enter.study") is True
    assert role.grants("write") is False
    with pytest.raises(ContractError):
        Role(EntityId("r"), "")


@pytest.mark.unit
def test_membership_time_scope() -> None:
    membership = Membership(
        EntityId("m"), EntityId("a"), EntityId("r"), EntityId("c"), start_ticks=10, end_ticks=20
    )
    assert membership.is_active_at(10) is True
    assert membership.is_active_at(20) is True
    assert membership.is_active_at(21) is False
    assert membership.is_active_at(9) is False
    open_ended = Membership(
        EntityId("m"), EntityId("a"), EntityId("r"), EntityId("c"), start_ticks=0
    )
    assert open_ended.is_active_at(999) is True
    with pytest.raises(ContractError):
        Membership(
            EntityId("m"), EntityId("a"), EntityId("r"), EntityId("c"), start_ticks=20, end_ticks=10
        )


@pytest.mark.unit
def test_delegated_permission_time_scope() -> None:
    permission = DelegatedPermission(
        EntityId("p"),
        EntityId("a"),
        "enter.study",
        "study",
        EntityId("g"),
        start_ticks=0,
        end_ticks=5,
    )
    assert permission.is_active_at(5) is True
    assert permission.is_active_at(6) is False


@pytest.mark.unit
def test_duty_validation() -> None:
    assert Duty(EntityId("d"), EntityId("a"), "rounds", 100).state == "pending"
    with pytest.raises(ContractError):
        Duty(EntityId("d"), EntityId("a"), "", 100)
