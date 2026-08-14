"""G16A: production topology, configuration & secret-management foundation.

- Secret scanner stays clean.
- Dev/test run offline with deterministic defaults (no secrets).
- Production profile fails fast on missing required config (no silent dev defaults).
- Production does not silently use test Fake adapters (durable SQLAlchemy path).
"""

from __future__ import annotations

import pathlib

import pytest
from scripts.architecture_check import ROOT, scan_secrets
from wanxiang_observability.config import ConfigError, load_settings


def test_secret_scanner_clean() -> None:
    assert scan_secrets(ROOT) == []


def test_dev_test_offline_deterministic_defaults() -> None:
    settings = load_settings({})
    assert settings.env == "development"
    assert settings.database_url == "sqlite:///./data/wanxiang.db"
    assert settings.is_production is False
    # Test profile also runs offline without secrets.
    test_settings = load_settings({"WANXIANG_ENV": "test"})
    assert test_settings.is_production is False


def test_production_missing_config_fails_fast() -> None:
    # Missing explicit DB URL -> ConfigError.
    with pytest.raises(ConfigError):
        load_settings({"WANXIANG_ENV": "production", "WANXIANG_SECRET_KEY": "s"})
    # Missing required secret -> ConfigError.
    with pytest.raises(ConfigError):
        load_settings(
            {
                "WANXIANG_ENV": "production",
                "WANXIANG_DATABASE_URL": "postgresql://wanxiang@localhost/wanxiang",
            }
        )


def test_production_profile_valid_and_public_surface_redacts_secrets() -> None:
    from wanxiang_observability.secrets import redact_secret_values

    settings = load_settings(
        {
            "WANXIANG_ENV": "production",
            "WANXIANG_DATABASE_URL": "postgresql://wanxiang@localhost/wanxiang",
            "WANXIANG_SECRET_KEY": "prod-secret-123",
        }
    )
    assert settings.is_production is True
    public = redact_secret_values(settings.to_public_dict())
    assert not any("prod-secret-123" in str(v) for v in public.values())


def test_production_uses_durable_persistence_not_test_fakes(
    persist_db_path: pathlib.Path,
) -> None:
    from tests.conftest import upgrade_db
    from wanxiang_api.app import build_runtime

    upgrade_db(persist_db_path)
    runtime = build_runtime(f"sqlite:///{persist_db_path.as_posix()}")
    # The runtime always wires the durable SQLAlchemy event store; in-memory
    # test Fakes are never selected by a production/default profile.
    from wanxiang_persistence.event_store import SqlAlchemyEventStore

    assert isinstance(runtime.persistence.event_store, SqlAlchemyEventStore)
