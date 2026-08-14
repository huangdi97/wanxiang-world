"""G32F: Ontology/Law multi-scale evolution gated by constitution/policy."""

from __future__ import annotations

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.constitution import ROOT_CONSTITUTION, legacy_default_constitution
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.evolution.ontology_law import (
    LawCandidate,
    OntologyCandidate,
    OntologyLawEvolution,
)


@pytest.mark.unit
def test_realistic_constitution_forbids_illegal_root_rules() -> None:
    # ROOT_CONSTITUTION has NO mutable law layers -> ontology/law evolution is
    # forbidden outright (including root rules).
    with pytest.raises(PermissionDenied):
        OntologyLawEvolution.validate_ontology(
            OntologyCandidate("cand_o1", "spirit", scope="root"), ROOT_CONSTITUTION
        )
    with pytest.raises(PermissionDenied):
        OntologyLawEvolution.validate_law(LawCandidate("cand_l1", "any_rule"), ROOT_CONSTITUTION)


@pytest.mark.unit
def test_world_constitution_allows_mutable_layers_but_not_escalation() -> None:
    legacy = legacy_default_constitution()
    assert (
        OntologyLawEvolution.validate_ontology(
            OntologyCandidate("cand_o1", "spirit", scope="world"), legacy
        )
        is True
    )
    assert (
        OntologyLawEvolution.validate_law(
            LawCandidate("cand_l1", "quiet_after_curfew", permission="world"), legacy
        )
        is True
    )
    # A law candidate trying to grant platform authority is rejected.
    with pytest.raises(PermissionDenied):
        OntologyLawEvolution.validate_law(
            LawCandidate("cand_l2", "rule", permission="commit_authority"), legacy
        )
    with pytest.raises(PermissionDenied):
        OntologyLawEvolution.validate_law(LawCandidate("cand_l3", "rule", scope="platform"), legacy)


@pytest.mark.integration
def test_branch_local_ontology_law_does_not_pollute_parent() -> None:
    path = fresh_db_path()
    try:
        runtime = make_world_runtime(path)
        created = runtime.create_world()
        instance_id = created.instance_id
        root = created.root_branch_id
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_root1"),
                instance_id=instance_id,
                branch_id=root,
                expected_revision=BranchRevision(0),
                action_type="create_entity",
                payload={"entity_id": "house", "count": 1},
                world_time=WorldTime(1),
            )
        )
        parent_hash = runtime.current_state(instance_id, root).semantic_hash()
        child = runtime.create_branch(instance_id, root)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_child1"),
                instance_id=instance_id,
                branch_id=child.branch_id,
                expected_revision=BranchRevision(1),
                action_type="create_entity",
                payload={"entity_id": "branch_local_rule", "count": 1},
                world_time=WorldTime(2),
            )
        )
        # Parent state/events unchanged by the branch-local ontology/law commit.
        assert runtime.current_state(instance_id, root).semantic_hash() == parent_hash
        assert len(runtime.events(instance_id, root)) == 1
        assert len(runtime.events(instance_id, child.branch_id)) == 1
    finally:
        cleanup_db_file(path)
