"""G95A: WorldRunArtifact round-trip, privacy and tamper evidence."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import WorldRunArtifact, sanitize_metadata


def _artifact() -> WorldRunArtifact:
    return WorldRunArtifact(
        artifact_id="artifact:g95a:unit",
        world_package_ref="world:g95a:package",
        world_package_version="1.0.0",
        scenario_ref="scenario:g95a",
        scenario_version="1",
        constitution_version="1",
        runtime_profile_ref="runtime:g95a",
        provider_versions=(("policy", "1"),),
        seed=17,
        control_ledger_refs=("control:g95a",),
        commit_refs=("event:2", "event:1"),
        snapshot_refs=("snapshot:g95a",),
        branch_refs=("branch:g95a",),
        actor_trajectory_refs=(("actor:alice", "sha256:trajectory"),),
        intervention_refs=("intervention:none",),
        validation_results=(("V0", "pass"), ("V7", "unknown")),
        metrics=(("event_count", 2), ("latency_ms", 1.5)),
        privacy_metadata=(("visibility", "private"),),
        redacted_fields=("source_text",),
    ).with_hash()


def test_artifact_round_trip_preserves_verified_hash() -> None:
    artifact = _artifact()

    restored = WorldRunArtifact.from_dict(artifact.to_dict())

    assert restored == artifact
    assert restored.verify_hash() is True


def test_artifact_rejects_tampered_payload_and_raw_private_fields() -> None:
    artifact = _artifact()
    tampered = artifact.to_dict()
    tampered["metrics"] = [["event_count", 999]]

    with pytest.raises(ContractError, match="hash"):
        WorldRunArtifact.from_dict(tampered)
    with pytest.raises(ContractError, match="private field"):
        WorldRunArtifact.from_dict({**artifact.to_dict(), "source_text": "private book"})


def test_sanitization_keeps_opaque_metadata_and_reports_redactions() -> None:
    kept, redacted = sanitize_metadata(
        {
            "owner": "qualification",
            "source_text": "private book bytes",
            "api_key": "do-not-export",
            "too_long": "x" * 257,
        }
    )

    assert kept == (("owner", "qualification"),)
    assert redacted == ("api_key", "source_text", "too_long")
