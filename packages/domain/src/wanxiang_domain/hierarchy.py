"""Branch hierarchy primitives: revisions, event sequences, ancestry.

BranchRevision and EventSeq are validated non-negative integers with explicit
semantics:
- EventSeq is the per-branch append position (1-based; 0 means empty stream).
- BranchRevision is the canonical-state revision produced by committed events
  (starts at 0 for the empty/initial state).
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


def _validate_count(value: object, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContractError(f"{name} must be a non-negative integer, got {value!r}")


@dataclass(frozen=True, slots=True)
class EventSeq:
    value: int

    def __post_init__(self) -> None:
        _validate_count(self.value, "EventSeq")

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class BranchRevision:
    value: int

    def __post_init__(self) -> None:
        _validate_count(self.value, "BranchRevision")

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class BranchAncestry:
    """Explicit ancestry metadata for a branch (Program Architecture 9.6)."""

    parent_branch_id: BranchId | None = None
    fork_revision: BranchRevision | None = None
    fork_event_seq: EventSeq | None = None
    fork_snapshot_ref: str | None = None

    def __post_init__(self) -> None:
        has_parent = self.parent_branch_id is not None
        has_fork_rev = self.fork_revision is not None
        has_fork_seq = self.fork_event_seq is not None
        if has_parent != has_fork_rev or has_parent != has_fork_seq:
            raise ContractError(
                "BranchAncestry requires parent_branch_id, fork_revision and"
                " fork_event_seq together"
            )


@dataclass(frozen=True, slots=True)
class BranchMetadata:
    """Immutable branch identity + ancestry + pinned versions."""

    branch_id: BranchId
    instance_id: WorldInstanceId
    ancestry: BranchAncestry
    schema_version: SchemaVersion
    rule_version: RuntimeVersion
    snapshot_ref: str | None = None
