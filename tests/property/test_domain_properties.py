"""GOAL_01A: property-based tests for identifiers and revisions."""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.serialization import command_to_primitive


@given(st.text(min_size=1, max_size=128))
def test_valid_ids_are_self_describing(value: str) -> None:
    # only safe identifier chars pass; others raise ContractError
    try:
        ident = CommandId(value)
    except ContractError:
        return
    assert CommandId(ident.value) == ident


@given(st.integers(min_value=0, max_value=10**9))
def test_revisions_and_seqs_accept_non_negative_ints(value: int) -> None:
    assert BranchRevision(value).value == value
    assert EventSeq(value).value == value


@given(st.integers(max_value=-1))
def test_revisions_reject_negative_ints(value: int) -> None:
    try:
        BranchRevision(value)
    except ContractError:
        return
    raise AssertionError(f"expected ContractError for {value}")


@given(
    st.from_regex(r"[a-z][a-z0-9_]{0,31}", fullmatch=True),
    st.integers(min_value=0, max_value=100),
)
def test_command_serialization_round_trip(action: str, revision: int) -> None:
    command = CommandEnvelope(
        command_id=CommandId("cmd_p"),
        instance_id=WorldInstanceId("wld_p"),
        branch_id=BranchId("br_p"),
        expected_revision=BranchRevision(revision),
        action_type=action,
    )
    assert command_to_primitive(command)["action_type"] == action
