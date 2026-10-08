"""Completion substrate (G58E/G58F)."""

from wanxiang_substrate.completion.candidates import (
    CompletionCandidate,
    CompletionClass,
    CompletionOrigin,
    class_never_upgrades,
)
from wanxiang_substrate.completion.planner import (
    CompletionPlan,
    CompletionPlanner,
    MissingRequirement,
)

__all__ = [
    "CompletionCandidate",
    "CompletionClass",
    "CompletionOrigin",
    "CompletionPlan",
    "CompletionPlanner",
    "MissingRequirement",
    "class_never_upgrades",
]
