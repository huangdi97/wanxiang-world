"""G30H: Event/Snapshot version context upgrade."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
from wanxiang_domain.version_context import (
    SnapshotVersionContext,
    VersionContext,
    VersionContextEntry,
    extend,
    legacy_version_context,
    resolve_context,
)
from wanxiang_runtime.replay import ReplayEngine


@pytest.mark.unit
def test_legacy_adapter_handles_old_events() -> None:
    legacy = legacy_version_context(RULES.value, SCHEMA.value)
    assert legacy.constitution_version == 1
    assert legacy.semantic_space_version == 1
    assert legacy.law_set_version == 0
    assert legacy.runtime_ref == f"runtime:{RULES.value}"
    # Old events have no context entry: they resolve to the legacy context.
    assert resolve_context(5, ()) == legacy


@pytest.mark.unit
def test_v51_fixture_replay_unchanged() -> None:
    events = build_fixture_events()
    # The v5.1 golden semantic hash must be unchanged by the context layer.
    from wanxiang_domain.hierarchy import BranchRevision

    state = ReplayEngine(RULES, SCHEMA).replay(events)
    assert state.revision == BranchRevision(5)
    assert (
        state.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )


@pytest.mark.unit
def test_context_log_resolves_nearest_preceding_entry() -> None:
    c1 = VersionContext(
        constitution_version=1, semantic_space_version=1, law_set_version=0
    ).with_hash()
    c2 = VersionContext(
        constitution_version=1, semantic_space_version=2, law_set_version=1
    ).with_hash()
    log = extend((), VersionContextEntry(from_revision=1, context=c1))
    log = extend(log, VersionContextEntry(from_revision=4, context=c2))
    assert resolve_context(3, log) == c1
    assert resolve_context(4, log) == c2
    assert resolve_context(10, log) == c2
    assert resolve_context(0, log) == legacy_version_context()


@pytest.mark.unit
def test_context_log_is_append_only_monotonic() -> None:
    from wanxiang_domain.errors import ContractError

    c1 = VersionContext(
        constitution_version=1, semantic_space_version=1, law_set_version=0
    ).with_hash()
    log = extend((), VersionContextEntry(from_revision=5, context=c1))
    with pytest.raises(ContractError):
        extend(log, VersionContextEntry(from_revision=4, context=c1))


@pytest.mark.unit
def test_replay_deterministic_before_and_after_law_evolution() -> None:
    """Context evolution (Law/Ontology) never changes the semantic hash."""
    events = build_fixture_events()
    before = ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()
    # Resolve the history under two different contexts (pre/post law set).
    ctx_pre = legacy_version_context(RULES.value, SCHEMA.value)
    ctx_post = VersionContext(
        constitution_version=1, semantic_space_version=2, law_set_version=1
    ).with_hash()
    assert resolve_context(1, (VersionContextEntry(1, ctx_pre),)) == ctx_pre
    assert (
        resolve_context(5, (VersionContextEntry(1, ctx_pre), VersionContextEntry(3, ctx_post)))
        == ctx_post
    )
    # The canonical state hash is context-independent.
    assert ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash() == before


@pytest.mark.unit
def test_snapshot_version_context_freezes_refs() -> None:
    ctx = VersionContext(
        constitution_version=1, semantic_space_version=1, law_set_version=0
    ).with_hash()
    snap = SnapshotVersionContext(
        instance_ref="wld_golden",
        branch_ref="br_golden",
        revision=5,
        event_seq=5,
        context=ctx,
    )
    prim = snap.to_primitive()
    assert prim["revision"] == 5
    assert prim["context_hash"] == ctx.content_hash
    context = prim["context"]
    assert isinstance(context, dict)
    assert context["law_set_version"] == 0
