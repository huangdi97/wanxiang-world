"""Structured logging bootstrap built on the standard library.

Two formatters are available: JSON lines (machine-readable) and a compact
key=value formatter. Both are suitable for deterministic local test output.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from wanxiang_observability.config import WanxiangSettings

_LOG_RECORD_ATTRS = frozenset(
    {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "taskName",
        "message",
    }
)


class JsonFormatter(logging.Formatter):
    """Emit one JSON object per record; extra fields are flattened."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _LOG_RECORD_ATTRS and not key.startswith("_"):
                payload[key] = value
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


class KeyValueFormatter(logging.Formatter):
    """Emit ``key=value`` pairs suitable for local development logs."""

    def format(self, record: logging.LogRecord) -> str:
        parts = [
            f"level={record.levelname}",
            f"logger={record.name}",
            f"message={record.getMessage()}",
        ]
        for key, value in record.__dict__.items():
            if key not in _LOG_RECORD_ATTRS and not key.startswith("_"):
                parts.append(f"{key}={value}")
        return " ".join(parts)


def configure_logging(settings: WanxiangSettings) -> None:
    """Configure the root logger with a structured handler."""
    formatter: logging.Formatter = JsonFormatter() if settings.log_json else KeyValueFormatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(settings.log_level)


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger for a module."""
    return logging.getLogger(name)
