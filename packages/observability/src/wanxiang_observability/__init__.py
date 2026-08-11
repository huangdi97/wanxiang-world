"""Wanxiang observability foundation.

Provides environment configuration loading (secret-safe), structured logging
setup, and secret-value redaction helpers used by runtime/audit paths.
"""

from wanxiang_observability.config import WanxiangSettings, load_settings, secret_key_names
from wanxiang_observability.logging import configure_logging, get_logger
from wanxiang_observability.secrets import is_secret_name, redact_secret_values, redact_values

__version__ = "0.1.0"

__all__ = [
    "WanxiangSettings",
    "configure_logging",
    "get_logger",
    "is_secret_name",
    "load_settings",
    "redact_secret_values",
    "redact_values",
    "secret_key_names",
]
