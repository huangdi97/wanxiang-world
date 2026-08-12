"""Body & condition substrate: constraints on action/schedule/perception (G02D)."""

from wanxiang_substrate.body.components import (
    BODY_CONDITION_COMPONENT,
    CONDITION_VISIBILITY_COMPONENT,
    MEDICATION_COMPONENT,
)
from wanxiang_substrate.body.errors import (
    BodyConstraintViolation,
    BodyError,
    InvalidConditionRange,
)
from wanxiang_substrate.body.fixture import build_condition_fixture_commands
from wanxiang_substrate.body.model import (
    BodyCondition,
    MobilityCapability,
    visible_facets,
)
from wanxiang_substrate.body.query import BodyQuery
from wanxiang_substrate.body.resolver import register_body_resolvers

__all__ = [
    "BODY_CONDITION_COMPONENT",
    "BodyCondition",
    "BodyConstraintViolation",
    "BodyError",
    "BodyQuery",
    "CONDITION_VISIBILITY_COMPONENT",
    "InvalidConditionRange",
    "MEDICATION_COMPONENT",
    "MobilityCapability",
    "build_condition_fixture_commands",
    "register_body_resolvers",
    "visible_facets",
]
