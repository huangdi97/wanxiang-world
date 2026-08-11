"""M0 tests: settings load without secrets and redaction works."""

from __future__ import annotations

import logging

import pytest
from wanxiang_observability.config import load_settings
from wanxiang_observability.logging import KeyValueFormatter
from wanxiang_observability.secrets import is_secret_name, redact_secret_values


@pytest.mark.unit
def test_public_settings_never_include_secret_values() -> None:
    env = {"WANXIANG_SECRET_PLACEHOLDER": "super-secret-value", "WANXIANG_ENV": "test"}
    settings = load_settings(env)
    public = settings.to_public_dict()
    assert "super-secret-value" not in " ".join(public.values())


@pytest.mark.unit
def test_redact_secret_values_masks_secret_named_keys() -> None:
    env = {"API_KEY": "abc", "WANXIANG_TOKEN": "def", "NAME": "visible"}
    redacted = redact_secret_values(env)
    assert redacted["API_KEY"] == "***REDACTED***"
    assert redacted["WANXIANG_TOKEN"] == "***REDACTED***"
    assert redacted["NAME"] == "visible"


@pytest.mark.unit
def test_is_secret_name_detects_common_secret_suffixes() -> None:
    assert is_secret_name("DATABASE_URL_PASSWORD")
    assert is_secret_name("OPENAI_API_KEY")
    assert is_secret_name("PRIVATE_KEY")
    assert not is_secret_name("WANXIANG_ENV")
    assert not is_secret_name("DATABASE_URL")


@pytest.mark.unit
def test_log_formatter_redacts_secret_values() -> None:
    env = {"WANXIANG_TOKEN": "tok-1234-secret"}
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="connect with tok-1234-secret",
        args=(),
        exc_info=None,
    )
    record.secret_hint = "tok-1234-secret"
    formatter = KeyValueFormatter()
    rendered = formatter.format(record)
    assert "tok-1234-secret" in rendered  # formatter itself does not redact; caller must

    from wanxiang_observability.secrets import redact_values

    safe = redact_values(rendered, env)
    assert "tok-1234-secret" not in safe
    assert "***REDACTED***" in safe
