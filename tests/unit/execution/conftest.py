"""Shared fixtures for execution fabric and outbox tests."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from wanxiang_execution import ExecutionPolicy


@pytest.fixture
def untrusted_policy() -> ExecutionPolicy:
    """Baseline untrusted policy: PROCESS, no network, no secrets, scratch writes."""
    return ExecutionPolicy.default_untrusted()


@pytest.fixture
def trusted_policy() -> ExecutionPolicy:
    """Baseline trusted policy: PROCESS, loopback, no secrets, read-only filesystem."""
    return ExecutionPolicy.default_trusted()


@pytest.fixture
def write_script(tmp_path: Path) -> Callable[[str, str], Path]:
    """Return a writer that drops a Python script into the test tmp dir."""

    def _write(name: str, body: str) -> Path:
        path = tmp_path / name
        path.write_text(body, encoding="utf-8")
        return path

    return _write
