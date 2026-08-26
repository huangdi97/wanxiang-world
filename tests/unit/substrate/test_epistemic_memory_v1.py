"""G89C: episodic memory refs, confidence-safe decay and reinforcement hooks."""

from __future__ import annotations

import json
from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.epistemic.components import memory_component
from wanxiang_substrate.epistemic.model import EpistemicMemory, MemoryRecord
from wanxiang_substrate.epistemic.query import memory_from_component


@pytest.mark.unit
def test_memory_v1_keeps_perception_refs_and_hooks_outside_truth() -> None:
    memory = EpistemicMemory(
        EntityId("memory_a"),
        EntityId("actor_a"),
        "observation",
        "memory://opaque-ref",
        10,
        salience=0.8,
        source_obs_ref="obs://opaque-ref",
        source_perception_refs=("perception:1",),
        decay_rate=0.1,
    )
    assert memory.perception_refs == ("obs://opaque-ref", "perception:1")
    assert memory.effective_salience(12) == 0.648
    decayed = memory.decayed(12)
    assert decayed.salience == 0.648 and memory.salience == 0.8
    reinforced = memory.reinforce(12, amount=0.1, perception_ref="perception:2")
    assert reinforced.salience == 0.9
    assert reinforced.reinforcement_count == 1
    assert reinforced.perception_refs[-1] == "perception:2"
    assert "canonical" not in repr(memory).lower()


@pytest.mark.unit
def test_memory_component_accepts_old_shape_and_serializes_new_refs() -> None:
    old = MemoryRecord(EntityId("m_old"), EntityId("a"), "observation", "ref://old", 1)
    assert old.source_perception_refs == ()
    component = memory_component(
        EntityId("m_new"),
        EntityId("a"),
        "reflection",
        "ref://reflection",
        2,
        source_perception_refs=("perception:2",),
        reinforcement_count=2,
        last_reinforced_ticks=3,
    )
    refs = json.loads(cast(str, component.fields["source_perception_refs"]))
    assert refs == ["perception:2"]
    assert component.fields["reinforcement_count"] == 2
    legacy = memory_from_component(
        {
            "memory_id": "m_legacy",
            "actor_id": "a",
            "kind": "observation",
            "content_ref": "ref://legacy",
            "at_ticks": 1,
        },
        EntityId("m_legacy"),
    )
    assert legacy is not None and legacy.decay_rate == 0.0 and legacy.source_perception_refs == ()
    with pytest.raises(ContractError):
        old.reinforce(2, amount=0.0)
