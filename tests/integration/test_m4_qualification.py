"""M4 qualification: worlds can be authored, reviewed, installed, instantiated.

End-to-end synthetic pipeline: author JSON packs -> Source Gate -> Compiler ->
Completion Ledger (canon) -> Package Registry -> Install (pinned) ->
Instantiate -> Export/re-import -> publish v2 without mutating the v1 instance.
"""

from __future__ import annotations

import json
import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    CommandId,
    ComponentId,
    EntityId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.compiler.compiler import StructuredCompiler
from wanxiang_substrate.compiler.fixture import approved_rights
from wanxiang_substrate.ledger.ledger import CompletionLedger
from wanxiang_substrate.ledger.model import ContentItem, ReviewDecision
from wanxiang_substrate.packages.install import (
    PackageInstaller,
    export_install,
    install_export_hash,
)
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import SourceRecord, payload_hash
from wanxiang_substrate.spatial.components import place_component, position_component
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_m4")
TOWN = EntityId("town")
HALL = EntityId("hall")
ALICE = EntityId("alice")
META = EntityId("instance_meta")


def _json_source(source_id: str, objects: Mapping[str, object]) -> SourceRecord:
    payload = json.dumps({"objects": objects}, sort_keys=True)
    return SourceRecord(
        source_id=source_id,
        kind="json",
        content_hash=payload_hash(payload),
        content_ref=f"ref://{source_id}.json",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance=f"fixture:{source_id}",
    )


def _town_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=TOWN,
                entity_type="spatial.place",
                components=(place_component(EntityId("region"), "town"),),
            ),
            EntityCreate(
                entity_id=HALL,
                entity_type="spatial.place",
                components=(place_component(TOWN, "hall"),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HALL),),
            ),
        )
    )


def make_m4_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("m4.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    payload = dict(command.payload)
    install_id = str(payload.get("install_id") or "unknown")
    lock_hash = str(payload.get("lock_hash") or "")
    meta = EntityCreate(
        entity_id=META,
        entity_type="instance.meta",
        components=(
            ComponentData(
                component_id=ComponentId("instance_meta_component"),
                component_type="instance.meta",
                schema_version=SchemaVersion(1),
                fields={"install_id": install_id, "lock_hash": lock_hash},
            ),
        ),
    )
    return ProposedWorldDelta(operations=_town_delta().operations + (meta,))


@pytest.fixture
def m4_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_m4_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_m4_author_review_install_instantiate_vertical(
    m4_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = m4_world

    # 1) Author + compile: JSON packs -> gated sources -> compiler candidates.
    domain_source = _json_source(
        "src_domain",
        {
            "town_domain": {
                "kind": "entity",
                "payload": {
                    "entity_id": "town_domain",
                    "entity_type": "domain.pack",
                    "name": "Town Domain",
                },
            }
        },
    )
    world_source = _json_source(
        "src_world",
        {
            "town_world": {
                "kind": "entity",
                "payload": {
                    "entity_id": "town_world",
                    "entity_type": "world.pack",
                    "name": "Town World",
                },
            }
        },
    )
    scenario_source = _json_source(
        "src_scenario",
        {
            "town_scenario": {
                "kind": "entity",
                "payload": {
                    "entity_id": "town_scenario",
                    "entity_type": "scenario.pack",
                    "name": "Town Scenario",
                },
            }
        },
    )
    gate = SourceGate()
    for source in (domain_source, world_source, scenario_source):
        assert gate.decide(source).ok is True
    compiler = StructuredCompiler()
    compiled = compiler.compile(
        "m4_job",
        {
            domain_source.source_id: domain_source,
            world_source.source_id: world_source,
            scenario_source.source_id: scenario_source,
        },
    )
    assert compiled.ok is True
    assert {c.object_id for c in compiled.candidates} >= {
        "town_domain",
        "town_world",
        "town_scenario",
    }

    # 2) Review: every compiled candidate is reviewed to canon in the ledger.
    ledger = CompletionLedger()
    for candidate in compiled.candidates:
        ledger.submit(
            ContentItem(
                item_id=candidate.object_id,
                label="source_backed",
                source_refs=candidate.source_refs,
                evidence_refs=("evid://compile",),
                rationale="compiled from approved source",
                reviewer="reviewer-m4",
                review_version=1,
                rights_usage="canonical",
                rights_approved=True,
            )
        )
        ledger.review(
            ReviewDecision(
                decision_id=f"dec_{candidate.object_id}",
                item_id=candidate.object_id,
                from_label="source_backed",
                to_label="canon",
                reviewer="reviewer-m4",
                rationale="reviewed package content",
                review_version=2,
                evidence_refs=("evid://compile",),
            )
        )
    snapshot = ledger.snapshot_labels()
    assert snapshot["town_world"] == "canon"

    # 3) Registry + install a pinned world (exact pins + lock hash).
    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="Town Domain",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-world",
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name="Town World",
            dependencies=(("town-domain", "^1.0.0"),),
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-scenario",
            kind="scenario",
            version=SemanticVersion(1, 0, 0),
            name="Town Scenario",
            dependencies=(("town-world", "^1.0.0"),),
        ).with_hash()
    )
    installer = PackageInstaller()
    record_v1 = installer.install(
        registry,
        "town-scenario",
        install_id="install_m4_v1",
        evidence_refs=tuple(sorted(snapshot)),
    )
    assert record_v1.version_for("town-world") == SemanticVersion(1, 0, 0)

    # 4) Instantiate the pinned world; pins are recorded in instance metadata.
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_m4_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="m4.instantiate",
            payload={"install_id": record_v1.install_id, "lock_hash": record_v1.lock_hash},
            world_time=WorldTime(1),
        )
    )
    state_v1 = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state_v1.entity(HALL) is not None
    meta = state_v1.entity(META)
    assert meta is not None
    meta_component = next(iter(meta.components.values()))
    assert meta_component.fields["install_id"] == record_v1.install_id

    # 5) Export / re-import roundtrip with verified hash + pins.
    exported = export_install(record_v1)
    assert install_export_hash(exported) == install_export_hash(export_install(record_v1))
    assert record_v1.version_for("town-world") == SemanticVersion(1, 0, 0)

    # 6) Publish v2; the v1-pinned record and live instance stay untouched.
    v1_hash = state_v1.semantic_hash()
    registry.register(
        PackageManifest(
            package_id="town-world",
            kind="world",
            version=SemanticVersion(2, 0, 0),
            name="Town World 2",
            dependencies=(("town-domain", "^1.0.0"),),
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-scenario",
            kind="scenario",
            version=SemanticVersion(2, 0, 0),
            name="Town Scenario 2",
            dependencies=(("town-world", "^2.0.0"),),
        ).with_hash()
    )
    record_v2 = installer.install(registry, "town-scenario", install_id="install_m4_v2")
    assert record_v2.package_version == SemanticVersion(2, 0, 0)
    assert record_v1.lock_hash != record_v2.lock_hash
    after = runtime.current_state(w.instance_id, w.root_branch_id)
    assert after.semantic_hash() == v1_hash  # v1 instance not mutated

    # 7) Replay determinism of the v1 instance.
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == v1_hash
