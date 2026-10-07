"""Experimental research namespace (G19A). OFF by default; isolated from stable."""

from __future__ import annotations

from wanxiang_research.flags import DEFAULT_FLAGS, FeatureFlags, ResearchFlag
from wanxiang_research.results import ExperimentRegistry, ExperimentResult
from wanxiang_research.world_run_artifact import WorldRunArtifact

__all__ = [
    "DEFAULT_FLAGS",
    "ExperimentRegistry",
    "ExperimentResult",
    "FeatureFlags",
    "ResearchFlag",
    "WorldRunArtifact",
]
