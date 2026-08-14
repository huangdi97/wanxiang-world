"""G20D: black-box external author + reference world final acceptance.

Runs the three external persona flows (author, operator, end user) plus the
product-surface audit through the public SDK/API only; no internal imports or
DB edits. The authoritative execution is scripts/blackbox_final_acceptance.py.
"""

from __future__ import annotations

import reference_worlds.synthetic_full.synthetic_full as sf
from scripts.blackbox_final_acceptance import (
    author_flow,
    end_user_flow,
    operator_flow,
    surfaces_flow,
)
from tests.conftest import fresh_db_path, make_world_runtime


def test_author_persona_publishes_and_installs_without_core_modification() -> None:
    result = author_flow()
    assert result["ok"] is True
    assert result["published_and_installed"] is True
    assert result["custom_action_ran"] is True
    assert result["no_core_modification"] is True


def test_operator_persona_deploys_backs_up_restores_and_replays() -> None:
    result = operator_flow()
    assert result["ok"] is True
    assert result["replay_ok"] is True
    assert result["restored_hash_matches"] is True


def test_end_user_persona_enters_rejoins_branches_and_replays() -> None:
    result = end_user_flow()
    assert result["ok"] is True
    assert result["session_independent"] is True
    assert result["branch_isolated"] is True
    assert result["replay_ok"] is True


def test_surfaces_smoke_branch_aware_projection_and_write_contract() -> None:
    runtime = make_world_runtime(fresh_db_path(), extra_resolvers=vars(sf)["register_resolvers"])
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    result = surfaces_flow(runtime.current_state(sf.INSTANCE, w.root_branch_id), w.root_branch_id)
    assert result["ok"] is True
    assert result["routes"] >= 5
    assert result["write_api_violations"] == []
    assert result["projection_items"] >= 1
