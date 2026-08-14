"""G20B: clean-room build/install/upgrade/restore/replay certification.

The certification script (scripts/clean_room_certify.py) is exercised through its
deterministic steps: release manifest reproducibility, previous-revision migration
upgrade, golden history replay, external sample pack validation and reference world
instantiation. Backup/restore round-trip and conformance are additionally covered by
test_g16g/test_g16h/test_g15a/test_g15b.
"""

from __future__ import annotations

from scripts.clean_room_certify import (
    external_sample_pack,
    golden_replay,
    migration_upgrade,
    reference_world,
    release_manifest,
)


def test_release_manifest_reproducible_and_matches_head() -> None:
    result = release_manifest()
    assert result["ok"] is True
    assert result["version"] == "0.1.0"
    assert result["migration_head"] == "0002_add_event_seq_index"
    assert result["reproducible"] is True
    assert result["git_matches_head"] is True


def test_previous_revision_upgrade_to_head() -> None:
    result = migration_upgrade()
    assert result["ok"] is True
    assert result["previous_revision"] == "0001_initial"
    assert result["head_revision"] == "0002_add_event_seq_index"


def test_golden_history_replay_hash_matches() -> None:
    result = golden_replay()
    assert result["ok"] is True
    assert result["events"] >= 1
    assert result["expected_hash"] == result["actual_hash"]


def test_external_sample_pack_scaffold_and_validate() -> None:
    result = external_sample_pack()
    assert result["ok"] is True
    assert result["validation_errors"] == []


def test_reference_world_install_and_instantiate_smoke() -> None:
    result = reference_world()
    assert result["ok"] is True
    assert result["conformance_ok"] is True
    assert result["installed"] is True
    assert result["instantiate_events"] >= 1
