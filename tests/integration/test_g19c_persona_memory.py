"""G19C: long-horizon persona, memory metabolism & drift evaluation research.

- No private/unknown facts leak through memory retrieval.
- Compaction preserves required provenance and key events.
- Persona drift metric is reported.
"""

from __future__ import annotations

from wanxiang_research.persona_memory import Memory, MemoryStore, PersonaDecision, PersonaDrift


def test_no_private_facts_leak_through_retrieval() -> None:
    store = MemoryStore()
    store.add(Memory("m1", "alice", "likes tea", "ref://a", privacy="public"))
    store.add(Memory("m2", "alice", "secret plan", "ref://b", privacy="private"))
    retrieved = store.retrieve("alice", "plan")
    assert retrieved == ()
    # Public facts are retrievable.
    assert len(store.retrieve("alice", "tea")) == 1
    # Another actor cannot retrieve alice's memories.
    assert store.retrieve("bob", "tea") == ()


def test_compaction_preserves_provenance_and_key_events() -> None:
    store = MemoryStore()
    store.add(Memory("m1", "alice", "met bob", "ref://a", key_event=True))
    store.add(Memory("m2", "alice", "met bob", "ref://a"))  # duplicate non-key
    store.add(Memory("m3", "alice", "likes tea", "ref://c"))
    compacted = store.compact()
    facts = {m.fact for m in compacted}
    assert "met bob" in facts  # key event preserved
    # Provenance is retained for every kept memory.
    assert all(m.provenance for m in compacted)
    assert len(compacted) == 2  # duplicate deduped, key event kept


def test_persona_drift_metric_reported() -> None:
    earlier = (
        PersonaDecision("alice", "gift", "give"),
        PersonaDecision("alice", "insult", "ignore"),
    )
    later = (
        PersonaDecision("alice", "gift", "give"),
        PersonaDecision("alice", "insult", "confront"),
    )
    drift = PersonaDrift.drift(earlier, later)
    assert drift == 0.5  # one of two shared scenarios changed
    assert 0.0 <= drift <= 1.0
