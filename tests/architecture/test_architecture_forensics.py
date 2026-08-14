"""G13C: architecture forensics + canonical-mutation-bypass tests.

Static detectors run over the real repository and must be clean; the same
detectors are exercised against adversarial fixtures (workspace-local temp,
because the sandbox cannot write the OS temp dir) to prove they catch
violations. A behavioral test proves canonical state only mutates through
CommitAuthority: projections/readers expose no write API, and the event store
rejects duplicate-command retries (idempotency).
"""

from __future__ import annotations  # noqa: I001

import inspect
import pathlib
import uuid
import contextlib
from collections.abc import Iterator

import pytest
from scripts.architecture_forensics import (
    commit_authority_callsites,
    detect_cycles,
    direct_append_calls,
    forbidden_violations,
    import_edges,
    persistence_leakage,
)
from wanxiang_application.state_reader import StateReader
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_substrate.projection.service import ProjectionService

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ARCH_TMP = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def arch_tmp() -> Iterator[pathlib.Path]:
    ARCH_TMP.mkdir(parents=True, exist_ok=True)
    d = ARCH_TMP / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            with contextlib.suppress(OSError):
                p.unlink()
    with contextlib.suppress(OSError):
        d.rmdir()


def _write(root: pathlib.Path, rel: str, content: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_repository_has_no_forbidden_imports() -> None:
    assert forbidden_violations(ROOT) == []


def test_repository_has_no_persistence_leakage() -> None:
    assert persistence_leakage(ROOT) == []


def test_repository_has_no_direct_persistence_writes() -> None:
    assert direct_append_calls(ROOT) == []


def test_repository_has_no_import_cycles() -> None:
    edges = import_edges(ROOT)
    assert detect_cycles(edges) == []


def test_single_commit_authority_entry_point() -> None:
    sites = commit_authority_callsites(ROOT)
    constructors = [s for s in sites if s["constructs_authority"]]
    assert len(constructors) == 1, (
        f"expected exactly one CommitAuthority constructor, got {constructors}"
    )
    assert any("world_runtime.py" in str(s.get("file", "")) for s in constructors)


def test_detector_catches_forbidden_import(arch_tmp: pathlib.Path) -> None:
    _write(
        arch_tmp,
        "packages/domain/src/wanxiang_domain/evil.py",
        "import sqlalchemy\n",
    )
    findings = forbidden_violations(arch_tmp)
    assert any("sqlalchemy" in str(f.get("import", "")) for f in findings)


def test_detector_catches_persistence_write_outside_owners(arch_tmp: pathlib.Path) -> None:
    _write(
        arch_tmp,
        "packages/substrate/src/wanxiang_substrate/evil.py",
        "def boom(event_store):\n    event_store.append('x')\n",
    )
    findings = direct_append_calls(arch_tmp)
    assert len(findings) == 1 and findings[0]["lines"]


def test_detector_catches_import_cycle(arch_tmp: pathlib.Path) -> None:
    _write(arch_tmp, "packages/a/src/wanxiang_a/mod.py", "import wanxiang_b\n")
    _write(arch_tmp, "packages/b/src/wanxiang_b/mod.py", "import wanxiang_a\n")
    edges = import_edges(arch_tmp)
    assert detect_cycles(edges)


def test_projection_service_has_no_write_api() -> None:
    write_names = {"append", "save", "record", "commit", "write", "mutate", "update", "submit"}
    members = {name for name, _ in inspect.getmembers(ProjectionService, inspect.isfunction)}
    assert not (members & write_names), (
        f"projection must not expose write API: {members & write_names}"
    )


def test_state_reader_has_no_write_api() -> None:
    # update/invalidate only manage the discardable read cache; they never
    # append/save/commit canonical state or touch persistence.
    write_names = {"append", "save", "record", "commit", "submit"}
    members = {name for name, _ in inspect.getmembers(StateReader, inspect.isfunction)}
    assert not (members & write_names)


def test_canonical_mutation_only_through_commit_authority(
    persist_db_path: pathlib.Path, world_runtime: WorldRuntime
) -> None:
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.errors import DuplicateCommandConflict
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    created = world_runtime.create_world()
    instance_id = created.instance_id
    branch_id = created.root_branch_id

    cmd = CommandEnvelope(
        command_id=CommandId("cmd_g13c_1"),
        instance_id=instance_id,
        branch_id=branch_id,
        expected_revision=BranchRevision(0),
        action_type="create_entity",
        payload={"entity_id": "ent_g13c", "count": 3},
        world_time=WorldTime(1),
    )
    result = world_runtime.submit_command(cmd)
    assert result.event is not None
    events = world_runtime.persistence.event_store.load(instance_id, branch_id)
    assert len(events) == 1

    # Duplicate command retry routed around CommitAuthority must never duplicate
    # world effects: the store rejects a second append for the same command id.
    store = world_runtime.persistence.event_store
    assert store.has_command(cmd.command_id)

    from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
    from wanxiang_domain.entity import ComponentData
    from wanxiang_domain.event import CommittedEvent
    from wanxiang_domain.hierarchy import EventSeq
    from wanxiang_domain.ids import ComponentId, EntityId, EventId, TraceId
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

    rogue_event = CommittedEvent(
        event_id=EventId("evt_g13c_rogue"),
        instance_id=instance_id,
        branch_id=branch_id,
        event_seq=EventSeq(2),
        revision=BranchRevision(2),
        schema_version=SchemaVersion(1),
        command_id=cmd.command_id,  # duplicate of the committed command
        delta=ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId("ent_rogue"),
                    entity_type="person",
                    components=(
                        ComponentData(
                            component_id=ComponentId("res_rogue"),
                            component_type="resource",
                            schema_version=SchemaVersion(1),
                            fields={"count": 1},
                        ),
                    ),
                ),
            )
        ),
        world_time=WorldTime(2),
        rule_version=RuntimeVersion(1),
        trace_id=TraceId("trace_g13c_rogue"),
    )
    with pytest.raises(DuplicateCommandConflict):
        store.append(rogue_event)
    events_after = world_runtime.persistence.event_store.load(instance_id, branch_id)
    assert len(events_after) == 1
