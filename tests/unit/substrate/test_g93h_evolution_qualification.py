"""G93H: baseline/evolved comparison rejects false long-run qualification."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.evolution.qualification import (
    EvolutionProjectionSnapshot,
    compare_evolution,
)


def _baseline() -> EvolutionProjectionSnapshot:
    return EvolutionProjectionSnapshot(
        run_id="run:g93h",
        elapsed_days=0,
        world_ticks=0,
        source_ref="memory://g93h_source",
        source_content_hash="source-hash-0",
        package_ref="package:g93h",
        canonical_hash="canonical-hash-0",
        replay_hash="replay-hash-0",
        canonical_revision=1,
        canonical_event_refs=("event:g93h:entry",),
        actor_fingerprints=(("actor:alice", "persona-0"),),
        relationship_fingerprints=(("relationship:alice:bob", "trust-0"),),
        organization_fingerprints=(("organization:g93h", "members-0"),),
        evidence_refs=("memory://g93h_source",),
        validated_delta_ids=(),
    )


def test_comparison_requires_30d_nonzero_three_plane_change_and_append_only_history() -> None:
    baseline = _baseline()
    evolved = replace(
        baseline,
        elapsed_days=30,
        world_ticks=3000,
        canonical_hash="canonical-hash-30",
        replay_hash="canonical-hash-30",
        canonical_revision=2,
        canonical_event_refs=("event:g93h:entry", "event:g93h:day-30"),
        actor_fingerprints=(("actor:alice", "persona-1"),),
        relationship_fingerprints=(("relationship:alice:bob", "trust-1"),),
        organization_fingerprints=(("organization:g93h", "members-1"),),
        evidence_refs=("memory://g93h_source", "event:g93h:day-30"),
        validated_delta_ids=("persona_g93h", "relationship_g93h", "organization_g93h"),
    )
    comparison = compare_evolution(baseline, evolved)
    assert comparison.qualified is True
    assert comparison.source_unchanged is True
    assert comparison.package_unchanged is True
    assert comparison.canonical_history_preserved is True
    assert comparison.replay_equal is True
    assert comparison.changed_actor_refs == ("actor:alice",)
    assert comparison.changed_relationship_refs == ("relationship:alice:bob",)
    assert comparison.changed_organization_refs == ("organization:g93h",)


def test_source_mutation_or_replay_drift_is_not_qualified() -> None:
    baseline = _baseline()
    evolved = replace(
        baseline,
        elapsed_days=30,
        world_ticks=3000,
        canonical_hash="canonical-hash-30",
        replay_hash="different-replay-hash",
        canonical_revision=2,
        canonical_event_refs=("event:g93h:entry", "event:g93h:day-30"),
        actor_fingerprints=(("actor:alice", "persona-1"),),
        relationship_fingerprints=(("relationship:alice:bob", "trust-1"),),
        organization_fingerprints=(("organization:g93h", "members-1"),),
        evidence_refs=("event:g93h:day-30",),
        validated_delta_ids=("delta:g93h",),
        source_content_hash="source-hash-mutated",
    )
    comparison = compare_evolution(baseline, evolved)
    assert comparison.source_unchanged is False
    assert comparison.replay_equal is False
    assert comparison.qualified is False
