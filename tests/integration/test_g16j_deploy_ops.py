"""G16J: private/staging deployment, operator runbooks & M13 production qualification.

- A new environment can be brought up from repository artifacts + docs.
- The reference world survives restart/upgrade.
- The operator can diagnose a seeded failure using the runbook diagnostics.
- The security baseline is enabled (production profile + rate limits).
"""

from __future__ import annotations

import pytest
from scripts.ops_deploy import PrerequisiteError, check_prerequisites, deploy
from tests.conftest import fresh_db_path


def test_fresh_environment_brings_up_from_artifacts() -> None:
    db = fresh_db_path()
    result = deploy(f"sqlite:///{db.as_posix()}")
    assert result["replay_ok"] is True
    revision = result["revision"]
    assert isinstance(revision, int) and revision >= 1
    assert result["instance"] == "wld_sf"
    # The world survives a restart (fresh runtime over the same DB).
    from tests.conftest import make_world_runtime

    runtime = make_world_runtime(db)
    from wanxiang_domain.ids import WorldInstanceId

    branches = runtime.persistence.branches.list(WorldInstanceId("wld_sf"))
    assert branches
    state = runtime.current_state(WorldInstanceId("wld_sf"), branches[0].branch_id)
    assert state.semantic_hash() == result["final_hash"]


def test_reference_world_survives_restart_upgrade() -> None:
    db = fresh_db_path()
    result = deploy(f"sqlite:///{db.as_posix()}")
    # Upgrade = re-run migrations (idempotent) and re-instantiate a fresh runtime.
    from tests.conftest import upgrade_db

    upgrade_db(db)
    from tests.conftest import make_world_runtime

    runtime = make_world_runtime(db)
    from wanxiang_domain.ids import WorldInstanceId

    branches = runtime.persistence.branches.list(WorldInstanceId("wld_sf"))
    assert branches
    state = runtime.current_state(WorldInstanceId("wld_sf"), branches[0].branch_id)
    assert state.semantic_hash() == result["final_hash"]


def test_operator_diagnoses_seeded_failure() -> None:
    from wanxiang_observability.config import ConfigError, load_settings

    # Seeded failure: production config missing -> clear diagnostic (ConfigError).
    with pytest.raises(ConfigError):
        load_settings({"WANXIANG_ENV": "production"})
    # Seeded failure: missing prerequisite -> clear diagnostic (PrerequisiteError).
    with pytest.raises(PrerequisiteError):
        check_prerequisites("")
    with pytest.raises(PrerequisiteError):
        check_prerequisites("sqlite:///./data/wanxiang.db")


def test_security_baseline_enabled() -> None:
    # Production profile requires secrets; API rate limiting is active.
    from wanxiang_observability.config import load_settings

    settings = load_settings(
        {
            "WANXIANG_ENV": "production",
            "WANXIANG_DATABASE_URL": "postgresql://wanxiang@localhost/wanxiang",
            "WANXIANG_SECRET_KEY": "s",
        }
    )
    assert settings.is_production is True
    from wanxiang_api.limits import RateLimiter

    limiter = RateLimiter(limit=2, window_seconds=60.0)
    assert limiter.allow("k") and limiter.allow("k")
    assert limiter.allow("k") is False
