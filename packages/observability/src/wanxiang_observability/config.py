"""Environment-based configuration loading with secret-safe defaults.

Local deterministic tests never require secrets; all settings carry defaults.
Secret-bearing environment variables are never exposed through the public
settings surface.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from wanxiang_observability.secrets import is_secret_name

_TRUTHY = frozenset({"1", "true", "yes", "on"})


class ConfigError(ValueError):
    """Raised when required production configuration is missing/invalid."""


@dataclass(frozen=True, slots=True)
class WanxiangSettings:
    """Typed application settings loaded from the environment."""

    env: str
    log_level: str
    database_url: str
    log_json: bool

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    def to_public_dict(self) -> dict[str, str]:
        """Serialize settings for logs/audit without any secret values."""
        return {
            "env": self.env,
            "log_level": self.log_level,
            "database_url": self.database_url,
            "log_json": "true" if self.log_json else "false",
        }


_DEV_DEFAULT_DATABASE_URL = "sqlite:///./data/wanxiang.db"
_REQUIRED_PRODUCTION_SECRETS = ("WANXIANG_SECRET_KEY",)


def load_settings(environ: dict[str, str] | None = None) -> WanxiangSettings:
    """Load settings from ``environ`` (defaults to ``os.environ``).

    The production profile fails fast (ConfigError) when required configuration
    is missing, so a broken production deploy is rejected at startup rather than
    silently running with dev/test defaults. Development/test keep deterministic
    offline defaults and never require secrets.
    """
    raw = dict(os.environ if environ is None else environ)
    env_name = raw.get("WANXIANG_ENV", "development")
    database_url = raw.get("WANXIANG_DATABASE_URL", _DEV_DEFAULT_DATABASE_URL)
    if env_name == "production":
        if database_url == _DEV_DEFAULT_DATABASE_URL:
            raise ConfigError(
                "WANXIANG_DATABASE_URL must be set explicitly in production "
                "(the development sqlite default is rejected)"
            )
        missing = [name for name in _REQUIRED_PRODUCTION_SECRETS if not raw.get(name)]
        if missing:
            raise ConfigError("missing required production secrets: " + ", ".join(missing))
    return WanxiangSettings(
        env=env_name,
        log_level=raw.get("WANXIANG_LOG_LEVEL", "INFO").upper(),
        database_url=database_url,
        log_json=raw.get("WANXIANG_LOG_JSON", "false").lower() in _TRUTHY,
    )


def secret_key_names() -> frozenset[str]:
    """Names of environment variables treated as secrets (by convention)."""
    return frozenset(name for name in os.environ if is_secret_name(name))
