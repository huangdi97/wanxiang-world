"""Observation & perspective isolation substrate (G03A)."""

from wanxiang_substrate.observation.components import (
    OBSERVATION_VISIBILITY_COMPONENT,
)
from wanxiang_substrate.observation.errors import (
    InvalidVisibility,
    ObservationError,
)
from wanxiang_substrate.observation.fixture import build_confidential_fixture_commands
from wanxiang_substrate.observation.model import (
    Observation,
    ObservationFact,
    VisibilityLevel,
    channel_confidence,
)
from wanxiang_substrate.observation.query import PerspectiveService
from wanxiang_substrate.observation.resolver import register_observation_resolvers

__all__ = [
    "InvalidVisibility",
    "OBSERVATION_VISIBILITY_COMPONENT",
    "Observation",
    "ObservationError",
    "ObservationFact",
    "PerspectiveService",
    "VisibilityLevel",
    "build_confidential_fixture_commands",
    "channel_confidence",
    "register_observation_resolvers",
]
