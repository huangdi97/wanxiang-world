"""Persistent lifecycle substrate (G06A)."""

from wanxiang_substrate.lifecycle.errors import (
    InvalidLifecycleTransition,
    LifecycleError,
)
from wanxiang_substrate.lifecycle.model import (
    LIFECYCLE_MODES,
    LifecycleMode,
    LifecycleState,
    advances_time,
    can_transition,
)
from wanxiang_substrate.lifecycle.resolver import (
    ACTION_SET_MODE,
    LIFECYCLE_ENTITY,
    register_lifecycle_resolvers,
)
from wanxiang_substrate.lifecycle.service import LifecycleService

__all__ = [
    "ACTION_SET_MODE",
    "InvalidLifecycleTransition",
    "LIFECYCLE_ENTITY",
    "LIFECYCLE_MODES",
    "LifecycleError",
    "LifecycleMode",
    "LifecycleService",
    "LifecycleState",
    "advances_time",
    "can_transition",
    "register_lifecycle_resolvers",
]
