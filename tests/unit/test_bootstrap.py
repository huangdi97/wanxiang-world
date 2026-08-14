"""M0 bootstrap smoke tests: workspace packages import cleanly."""

from __future__ import annotations

import importlib

import pytest

PACKAGES = [
    "wanxiang_application",
    "wanxiang_domain",
    "wanxiang_observability",
    "wanxiang_persistence",
    "wanxiang_runtime",
]


@pytest.mark.unit
def test_workspace_packages_importable() -> None:
    for name in PACKAGES:
        module = importlib.import_module(name)
        assert module.__version__ == "0.1.0"
