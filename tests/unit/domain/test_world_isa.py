"""G30D: World Semantic ISA minimal typed instructions."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from wanxiang_domain.delta import EntityCreate, EntityDelete, ProposedWorldDelta, RelationCreate
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_domain.world_isa import (
    ISA_INSTRUCTIONS,
    ISA_SUPPORTED_VERSIONS,
    ISA_VERSION,
    WorldIsaInstruction,
    WorldIsaOp,
    isa_op_from_primitive,
    reduce_isa_to_delta,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]


@pytest.mark.unit
def test_isa_schema_has_exactly_eight_instructions() -> None:
    assert ISA_INSTRUCTIONS == (
        "DECLARE",
        "ASSERT",
        "RETRACT",
        "PROPOSE",
        "VALIDATE",
        "COMMIT",
        "FORK",
        "PROMOTE",
    )
    assert ISA_VERSION in ISA_SUPPORTED_VERSIONS


@pytest.mark.unit
def test_schema_round_trip() -> None:
    op = WorldIsaOp(op="DECLARE", payload={"entity_id": "stone", "entity_type": "thing"})
    restored = isa_op_from_primitive(op.to_primitive())
    assert restored == op
    assert restored.payload == {"entity_id": "stone", "entity_type": "thing"}


@pytest.mark.unit
def test_unknown_isa_version_fails_explicitly() -> None:
    with pytest.raises(ContractError):
        WorldIsaOp(op="DECLARE", version=99)
    with pytest.raises(ContractError):
        isa_op_from_primitive({"op": "DECLARE", "version": 99, "payload": {}})


@pytest.mark.unit
def test_unknown_instruction_fails_explicitly() -> None:
    with pytest.raises(ContractError):
        WorldIsaOp(op=cast(WorldIsaInstruction, "TELEPORT"))
    with pytest.raises(ContractError):
        isa_op_from_primitive({"op": "TELEPORT", "version": ISA_VERSION, "payload": {}})


@pytest.mark.unit
def test_declare_reduces_to_entity_create() -> None:
    delta = reduce_isa_to_delta(
        WorldIsaOp(op="DECLARE", payload={"entity_id": "stone", "entity_type": "thing"})
    )
    assert delta is not None
    assert isinstance(delta.operations[0], EntityCreate)
    assert delta.operations[0].entity_id == EntityId("stone")


@pytest.mark.unit
def test_assert_reduces_to_relation_create() -> None:
    delta = reduce_isa_to_delta(
        WorldIsaOp(
            op="ASSERT",
            payload={
                "relation_id": "r1",
                "relation_type": "gift",
                "source_id": "alice",
                "target_id": "bob",
            },
        )
    )
    assert delta is not None
    assert isinstance(delta.operations[0], RelationCreate)
    assert delta.operations[0].target_id == EntityId("bob")


@pytest.mark.unit
def test_retract_reduces_to_delete() -> None:
    delta = reduce_isa_to_delta(WorldIsaOp(op="RETRACT", payload={"entity_id": "stone"}))
    assert delta is not None
    assert isinstance(delta.operations[0], EntityDelete)


@pytest.mark.unit
def test_control_instructions_reduce_to_none() -> None:
    for op in ("VALIDATE", "COMMIT", "FORK", "PROMOTE"):
        assert reduce_isa_to_delta(WorldIsaOp(op=op)) is None


@pytest.mark.unit
def test_isa_module_has_no_direct_db_write() -> None:
    source = (ROOT / "packages/domain/src/wanxiang_domain/world_isa.py").read_text(encoding="utf-8")
    import_lines = [ln for ln in source.splitlines() if ln.strip().startswith(("import ", "from "))]
    for forbidden in ("sqlalchemy", "persistence", "fastapi", "httpx", "requests"):
        assert not any(forbidden in ln for ln in import_lines), f"ISA must not import {forbidden!r}"


@pytest.mark.unit
def test_isa_keeps_business_actions_upper() -> None:
    # ISA reduces data ops to deltas; business actions stay at the upper layer.
    proposed = reduce_isa_to_delta(
        WorldIsaOp(
            op="PROPOSE",
            payload={
                "delta": {
                    "schema_version": 1,
                    "operations": [
                        {
                            "op": "entity_create",
                            "entity_id": "alice",
                            "entity_type": "person",
                            "components": [],
                        }
                    ],
                }
            },
        )
    )
    assert proposed is not None
    assert isinstance(proposed, ProposedWorldDelta)
