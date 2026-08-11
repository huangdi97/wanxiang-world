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


@dataclass(frozen=True, slots=True)
class WanxiangSettings:
    """Typed application settings loaded from the environment."""

    env: str
    log_level: str
    database_url: str
    log_json: bool

    def to_public_dict(self) -> dict[str, str]:
        """Serialize settings for logs/audit without any secret values."""
        return {
            "env": self.env,
            "log_level": self.log_level,
            "database_url": self.database_url,
            "log_json": "true" if self.log_json else "false",
        }


def load_settings(environ: dict[str, str] | None = None) -> WanxiangSettings:
    """Load settings from ``environ`` (defaults to ``os.environ``)."""
    env = dict(os.environ if environ is None else environ)
    return WanxiangSettings(
        env=env.get("WANXIANG_ENV", "development"),
        log_level=env.get("WANXIANG_LOG_LEVEL", "INFO").upper(),
        database_url=env.get("WANXIANG_DATABASE_URL", "sqlite:///./data/wanxiang.db"),
        log_json=env.get("WANXIANG_LOG_JSON", "false").lower() in _TRUTHY,
    )


def secret_key_names() -> frozenset[str]:
    """Names of environment variables treated as secrets (by convention)."""
    return frozenset(name for name in os.environ if is_secret_name(name))
