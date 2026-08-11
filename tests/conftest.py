"""Shared test configuration.

Registers a deterministic Hypothesis profile so property-based tests are
reproducible across runs without a fixed global seed value.
"""

from __future__ import annotations

from hypothesis import settings

settings.register_profile("wanxiang-deterministic", derandomize=True, deadline=None)
settings.load_profile("wanxiang-deterministic")
