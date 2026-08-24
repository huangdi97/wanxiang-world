"""M69 one-click book/family/structured/mixed and living-instance contracts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
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
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.preview import PreviewWorld, register_preview_resolvers
from wanxiang_substrate.sources.errors import OcrRequired
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


class _MemoryInstances:
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
            instances=_MemoryInstances(),
        ),
        RuntimeVersion(1),
        resolvers=registry,
    )


def _record(source_id: str, kind: str, content: str, *, access: str = "private") -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind=kind,
        content_hash=payload_hash(content),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=content,
        provenance=f"synthetic:m69:{source_id}",
        access=access,  # type: ignore[arg-type]
    )


def _book() -> SourceRecord:
    return _record(
        "book_m69",
        "text",
        "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
        "Alice arrived in Beijing in 1985.\n"
        "Bob visited Beijing.\nrelationship: Alice -> Bob\nrule: visitors register\n",
    )


def _family() -> SourceRecord:
    return _record(
        "family_m69",
        "gedcom",
        "0 HEAD\n1 SOUR TEST\n"
        "0 @I1@ INDI\n1 NAME Alice /Doe/\n1 BIRT\n2 DATE 1980\n2 PLAC Beijing\n"
        "0 @I2@ INDI\n1 NAME Bob /Doe/\n1 BIRT\n2 DATE 1982\n2 PLAC Beijing\n"
        "1 NOTE rule: visitors register\n"
        "0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@\n0 TRLR\n",
    )


def _structured() -> SourceRecord:
    content = {
        "people": [{"name": "Alice"}, {"name": "Bob"}],
        "text": "Alice arrived in Beijing in 1985. relationship: Alice -> Bob\n"
        "rule: visitors register",
        "rule": "visitors register",
    }
    return _record("json_m69", "json", json.dumps(content))


def _image() -> SourceRecord:
    return _record("image_m69", "image", "\x89PNG\r\nsynthetic-image")


@pytest.mark.integration
def test_all_four_one_click_profiles_build_preview_packages() -> None:
    flows = {
        "book": (_book(),),
        "family": (_family(),),
        "structured": (_structured(),),
        "mixed": (_book(), _image(), _structured()),
    }
    for profile, sources in flows.items():
        authoring = OneClickAuthoring()
        result = authoring.run(f"job_{profile}_m69", sources, profile=profile)
        assert result.source_profile == profile
        assert result.package.manifest.content_hash
        assert result.preview.scoped_ref.startswith("preview://")
        assert result.orchestration is not None
        assert result.orchestration.stages[-1] == "evaluate"
        assert authoring.service.package_validation(result.job_id).publish_ok is True
        assert authoring.publish(result).publish_ok is True


@pytest.mark.integration
def test_one_click_enters_living_instance_through_existing_runtime_authority() -> None:
    result = OneClickAuthoring().run("job_living_m69", (_family(),), profile="family")
    runtime = _runtime()
    living = OneClickAuthoring().enter_living_instance(result, runtime)
    observed = living.observe()
    assert isinstance(observed["entities"], list)
    before = living.replay_hash()
    living.step("set_status", {"entity_id": "ent_alice_doe", "status": "awake"})
    after = living.replay_hash()
    assert after != before
    assert living.replay_hash() == after
    child = runtime.create_branch(living.instance_id, living.branch_id)
    child_world = PreviewWorld(
        living.install, runtime, living.host, living.instance_id, child.branch_id
    )
    child_world.step("set_status", {"entity_id": "ent_bob_doe", "status": "away"})
    parent: Any = living.observe()
    child_state: Any = child_world.observe()
    assert any(
        component["fields"].get("value") == "away"
        for entity in child_state["entities"]
        for component in entity["components"]
        if component["type"] == "status"
    )
    assert all(
        component["fields"].get("value") != "away"
        for entity in parent["entities"]
        for component in entity["components"]
        if component["type"] == "status"
    )


@pytest.mark.integration
def test_csv_structured_profile_enters_living_preview() -> None:
    csv_source = _record(
        "csv_m69",
        "csv",
        "name,year,place\nAlice,1985,Beijing\nBob,1986,Beijing\n",
    )
    authoring = OneClickAuthoring()
    result = authoring.run("job_csv_m69", (csv_source,), profile="structured")
    assert len(result.package.draft.entities) == 2
    living = authoring.enter_living_instance(result, _runtime())
    observed: Any = living.observe()
    assert len(observed["entities"]) == 2


@pytest.mark.integration
def test_scanned_pdf_without_provider_stays_ocr_required() -> None:
    scanned = _record("scan_m69", "pdf", "%PDF-1.7\n/image-only")
    with pytest.raises(OcrRequired, match="OCR"):
        OneClickAuthoring().run("job_scan_m69", (scanned,), profile="book")


@pytest.mark.integration
def test_studio_one_click_and_cli_reference_use_the_same_flow() -> None:
    client: Any = TestClient(create_app())
    api = client.post(
        "/studio/one-click",
        json={
            "job_id": "job_m69_api",
            "profile": "family",
            "sources": [
                {
                    "source_id": "api_book_m69",
                    "kind": "gedcom",
                    "content": (
                        "0 HEAD\n1 SOUR TEST\n"
                        "0 @I1@ INDI\n1 NAME Alice /Doe/\n1 BIRT\n"
                        "2 DATE 1980\n2 PLAC Beijing\n"
                        "0 @I2@ INDI\n1 NAME Bob /Doe/\n1 BIRT\n"
                        "2 DATE 1982\n2 PLAC Beijing\n1 NOTE rule: visitors register\n"
                        "0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@\n0 TRLR\n"
                    ),
                    "stage": "E3",
                    "rights_approved": True,
                    "access": "public",
                }
            ],
        },
    )
    assert api.status_code == 201
    assert api.json()["preview_ref"].startswith("preview://")
    assert api.json()["publishable"] is True
    inbox = client.get("/studio/jobs/job_m69_api/review-inbox")
    assert inbox.status_code == 200
    assert inbox.json()["items"]
    published = client.post("/studio/jobs/job_m69_api/publish")
    assert published.status_code == 200
    assert published.json()["publishable"] is True
    assert published.json()["status"]["stage"] == "published"

    completed = subprocess.run(
        [
            sys.executable,
            str(Path("scripts/wxworld.py")),
            "reference",
            "--profile",
            "book",
            "--publish",
            "--job-id",
            "job_m69_cli",
            "--content",
            "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
            "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
            "relationship: Alice -> Bob\nrule: visitors register\n",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["profile"] == "book"
    assert result["preview_ref"].startswith("preview://")
    assert result["published"] is True
