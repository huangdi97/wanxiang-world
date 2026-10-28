"""Round-trip tests for durable world package serialization."""

from __future__ import annotations

import json

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.experience import experience_from_profile
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\n"
        "relationship: Alice -> Bob\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="package_roundtrip_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://package_roundtrip_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:package-roundtrip",
        access="private",
    )


def _package() -> WorldPackageDraft:
    authored = OneClickAuthoring().run("job_package_roundtrip", (_source(),), profile="book")
    return authored.package


def test_world_package_round_trips_through_json() -> None:
    package = _package()
    profile = profile_from_world_package(package, owner_id="alice", visibility="public")
    experience = experience_from_profile(profile)

    payload = json.loads(json.dumps(package.to_dict(), ensure_ascii=False))
    restored = WorldPackageDraft.from_dict(payload)

    assert restored == package
    assert restored.manifest.content_hash == package.manifest.content_hash
    assert restored.draft == package.draft
    restored_profile = profile_from_world_package(
        restored,
        owner_id="alice",
        visibility="public",
    )
    assert experience_from_profile(restored_profile) == experience


def test_world_package_serialization_rejects_tampered_hash() -> None:
    payload = json.loads(json.dumps(_package().to_dict(), ensure_ascii=False))
    payload["manifest"]["content_hash"] = "0" * 64
    with pytest.raises(ContractError):
        WorldPackageDraft.from_dict(payload)


def test_world_package_serialization_rejects_bad_draft_status() -> None:
    payload = json.loads(json.dumps(_package().to_dict(), ensure_ascii=False))
    payload["draft"]["status"] = "NOT_A_STATUS"
    with pytest.raises(ContractError):
        WorldPackageDraft.from_dict(payload)


def test_world_package_serialization_rejects_unknown_version() -> None:
    payload = json.loads(json.dumps(_package().to_dict(), ensure_ascii=False))
    payload["serialization_version"] = 99
    with pytest.raises(ContractError):
        WorldPackageDraft.from_dict(payload)
