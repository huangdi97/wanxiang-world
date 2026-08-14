"""Strong identifiers for the authoritative world kernel.

Identifiers are validated, immutable value objects. Distinct identifier types
are distinct classes so callers cannot silently mix e.g. a CommandId with an
EventId. Extension: add a subclass with a distinct ``_prefix``.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import ClassVar, Self

from wanxiang_domain.errors import ContractError

_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,127}$")


def validate_id(value: object, kind: str) -> None:
    if not isinstance(value, str) or _ID_PATTERN.match(value) is None:
        raise ContractError(f"invalid {kind}: {value!r} must match {_ID_PATTERN.pattern}")


@dataclass(frozen=True, slots=True)
class WanxiangId:
    """Base validated identifier."""

    value: str
    _prefix: ClassVar[str] = "id"

    def __post_init__(self) -> None:
        validate_id(self.value, type(self).__name__)

    def __str__(self) -> str:
        return self.value

    @classmethod
    def generate(cls) -> Self:
        return cls(f"{cls._prefix}_{uuid.uuid4().hex}")


class WorldInstanceId(WanxiangId):
    _prefix = "wld"


class ConstitutionId(WanxiangId):
    _prefix = "con"


class BranchId(WanxiangId):
    _prefix = "br"


class SessionId(WanxiangId):
    _prefix = "ses"


class ProjectionId(WanxiangId):
    _prefix = "proj"


class CommandId(WanxiangId):
    _prefix = "cmd"


class EventId(WanxiangId):
    _prefix = "evt"


class EntityId(WanxiangId):
    _prefix = "ent"


class ComponentId(WanxiangId):
    _prefix = "cmp"


class RelationId(WanxiangId):
    _prefix = "rel"


class SnapshotId(WanxiangId):
    _prefix = "snap"


class RunId(WanxiangId):
    _prefix = "run"


class ActorId(WanxiangId):
    _prefix = "act"


class ClaimId(WanxiangId):
    _prefix = "claim"


class EvidenceId(WanxiangId):
    _prefix = "evid"


class CorrelationId(WanxiangId):
    _prefix = "corr"


class TraceId(WanxiangId):
    _prefix = "trace"
