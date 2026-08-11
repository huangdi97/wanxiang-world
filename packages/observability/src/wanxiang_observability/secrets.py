"""Secret-value redaction helpers for logs and audit output.

Names matching secret indicators (``SECRET``/``TOKEN``/``PASSWORD``/``KEY``)
have their values masked; arbitrary values can be redacted from text too.
"""

from __future__ import annotations

import re

_REDACTED = "***REDACTED***"

_NAME_PATTERN = re.compile(r"(SECRET|TOKEN|PASSWORD|API[_-]?KEY|PRIVATE[_-]?KEY)", re.IGNORECASE)


def is_secret_name(name: str) -> bool:
    """Return True when ``name`` looks like a secret-bearing variable."""
    return _NAME_PATTERN.search(name) is not None


def redact_secret_values(mapping: dict[str, str]) -> dict[str, str]:
    """Return a copy of ``mapping`` with secret-named values masked."""
    return {key: (_REDACTED if is_secret_name(key) else value) for key, value in mapping.items()}


def redact_values(text: str, mapping: dict[str, str]) -> str:
    """Replace known secret values appearing in ``text`` with the mask."""
    result = text
    for value in mapping.values():
        if value:
            result = result.replace(value, _REDACTED)
    return result
