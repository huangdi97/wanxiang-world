"""G03B: epistemic value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.epistemic.model import BeliefAssertion, MemoryRecord


@pytest.mark.unit
def test_memory_record_validation() -> None:
    memory = MemoryRecord(EntityId("m"), EntityId("a"), "observation", "ref://x", 10, 0.6)
    assert memory.kind == "observation"
    with pytest.raises(ContractError):
        MemoryRecord(EntityId("m"), EntityId("a"), "observation", "", 10)
    with pytest.raises(ContractError):
        MemoryRecord(EntityId("m"), EntityId("a"), "chat", "ref://x", 10)  # type: ignore[arg-type]
    with pytest.raises(ContractError):
        MemoryRecord(EntityId("m"), EntityId("a"), "observation", "ref://x", 10, salience=1.5)


@pytest.mark.unit
def test_belief_assertion_validation() -> None:
    belief = BeliefAssertion(EntityId("b"), EntityId("a"), "it rains", 0.8, 5)
    assert belief.status == "active"
    with pytest.raises(ContractError):
        BeliefAssertion(EntityId("b"), EntityId("a"), "", 0.8, 5)
    with pytest.raises(ContractError):
        BeliefAssertion(EntityId("b"), EntityId("a"), "it rains", 1.2, 5)
    with pytest.raises(ContractError):
        BeliefAssertion(EntityId("b"), EntityId("a"), "it rains", 0.8, 5, status="bogus")  # type: ignore[arg-type]
