"""M57 Draft -> Package -> isolated Preview qualification."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.branch import InMemoryBranchRepository
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.snapshot import InMemorySnapshotStore
from wanxiang_substrate.compile import (
    CompilerBoundary,
    CompilerInput,
    PackageAssembler,
    PackageValidator,
)
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.preview import (
    PreviewRegistry,
    instantiate_preview,
    register_preview_resolvers,
)


class MemoryInstanceStore:
    def __init__(self) -> None:
        self._rows: dict[str, tuple[SchemaVersion, RuntimeVersion, WorldTime]] = {}

    def create(
        self,
        instance_id: WorldInstanceId,
        schema_version: SchemaVersion,
        rule_version: RuntimeVersion,
        created_world_time: WorldTime,
    ) -> None:
        self._rows[instance_id.value] = (schema_version, rule_version, created_world_time)

    def get(self, instance_id: WorldInstanceId) -> tuple[SchemaVersion, RuntimeVersion, WorldTime]:
        return self._rows[instance_id.value]


def _runtime() -> WorldRuntime:
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    register_preview_resolvers(registry)
    return WorldRuntime(
        PersistenceBundle(
            event_store=InMemoryEventStore(),
            snapshot_store=InMemorySnapshotStore(),
            branches=InMemoryBranchRepository(),
            instances=MemoryInstanceStore(),
        ),
        RuntimeVersion(1),
        resolvers=registry,
    )


def _draft(*, status: str = "READY_TO_COMPILE", gaps: tuple[str, ...] = ()) -> WorldDraft:
    return WorldDraft(
        draft_id="draft_preview",
        revision=3,
        status=status,  # type: ignore[arg-type]
        source_refs=("book_a",),
        source_versions=(("book_a", "v1"),),
        constitution_ref="constitution_reference",
        selected_domains=("narrative",),
        entities=(("alice", "Alice"), ("bob", "Bob")),
        relations=(("alice", "bob", "knows"),),
        places=("harbor",),
        events=(("arrival", "1900-01-01"),),
        rules=("keep promises",),
        completion_items=gaps,
        scenario_candidates=("scenario_1",),
        genesis_candidates=("genesis_1",),
        coverage=0.9,
        uncertainty=0.1,
        quality=0.9,
    )


@pytest.mark.unit
def test_m57_compiles_pins_and_instantiates_through_host() -> None:
    draft = _draft()
    compiler = CompilerBoundary()
    outcome = compiler.check(
        CompilerInput(
            draft=draft,
            draft_revision=3,
            source_versions=(("book_a", "v1"),),
            domain_versions=(("narrative", "1.0.0"),),
        )
    )
    assert outcome.ok is True
    package = PackageAssembler().assemble(
        draft,
        compile_outcome=outcome,
        domain_versions=(("narrative", "1.0.0"),),
        evidence_coverage=0.9,
        for_preview=True,
    )
    assert PackageValidator().validate(package).preview_ok is True
    registry = PreviewRegistry()
    install = registry.install(package)
    assert registry.install(package) == install
    preview = instantiate_preview(_runtime(), package, install)
    observed = preview.observe()
    entities = observed["entities"]
    relations = observed["relations"]
    assert isinstance(entities, list)
    assert isinstance(relations, list)
    assert len(cast(list[object], entities)) == 2
    assert len(cast(list[object], relations)) == 1
    assert len(preview.runtime.events(preview.instance_id, preview.branch_id)) == 3
    before = preview.replay_hash()
    preview.step("set_status", {"entity_id": "ent_alice", "status": "awake"})
    assert preview.replay_hash() != before


@pytest.mark.unit
def test_m57_publish_keeps_completion_gap_out_of_canon() -> None:
    draft = _draft(gaps=("object continuity",))
    outcome = CompilerBoundary().check(
        CompilerInput(
            draft=draft,
            draft_revision=draft.revision,
            source_versions=draft.source_versions,
            domain_versions=(("narrative", "1.0.0"),),
        )
    )
    package = PackageAssembler().assemble(
        draft,
        compile_outcome=outcome,
        domain_versions=(("narrative", "1.0.0"),),
        evidence_coverage=0.9,
        for_preview=True,
    )
    result = PackageValidator().validate(package)
    assert result.preview_ok is True
    assert result.publish_ok is False
    assert "object continuity" in package.unresolved_gaps


@pytest.mark.unit
def test_m57_rejects_changed_source_pin() -> None:
    draft = _draft()
    outcome = CompilerBoundary().check(
        CompilerInput(
            draft=draft,
            draft_revision=draft.revision,
            source_versions=(("book_a", "v2"),),
            domain_versions=(("narrative", "1.0.0"),),
        )
    )
    assert outcome.ok is False
    assert any("version changed" in reason for reason in outcome.reasons)
