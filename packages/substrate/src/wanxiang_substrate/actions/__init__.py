"""Action, affordance & validator substrate (G03D)."""

from wanxiang_substrate.actions.affordance import Affordance, compute_affordances
from wanxiang_substrate.actions.model import (
    ActionDefinition,
    ParameterSpec,
    ValidationIssue,
    ValidationResult,
)
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.actions.validator import ActionValidator

__all__ = [
    "ActionDefinition",
    "Affordance",
    "ActionRegistry",
    "ActionValidator",
    "ParameterSpec",
    "ValidationIssue",
    "ValidationResult",
    "compute_affordances",
    "register_reference_actions",
]
