"""Versioned fork provenance and intervention-run evidence models (G95C)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.reality.intervention import InterventionBranch, InterventionTrigger

FORK_SCHEMA_VERSION = 1
LedgerStatus = Literal["forked", "resumed"]
_LEDGER_STATUSES = frozenset({"forked", "resumed"})


def ref(value: object, name: str, *, allow_empty: bool = False) -> str:
    if (
        not isinstance(value, str)
        or (not allow_empty and not value.strip())
        or any(char.isspace() for char in value)
    ):
        raise ContractError(f"{name} must be a non-empty opaque reference")
    return value


def count(value: object, name: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ContractError(f"{name} must be an integer >= {minimum}")
    return value


def digest(value: object, name: str, *, allow_empty: bool = False) -> str:
    result = ref(value, name, allow_empty=allow_empty)
    if result and (len(result) != 64 or any(char not in "0123456789abcdef" for char in result)):
        raise ContractError(f"{name} must be a lowercase SHA-256 digest")
    return result


@dataclass(frozen=True, slots=True)
class ForkProvenance:
    """Immutable proof of the parent point and the child branch ancestry."""

    provenance_id: str
    instance_ref: str
    parent_branch_ref: str
    parent_head_revision: int
    parent_head_event_seq: int
    parent_head_hash: str
    fork_revision: int
    fork_event_seq: int
    fork_snapshot_ref: str
    child_branch_ref: str
    intervention_id: str
    artifact_ref: str
    trigger: InterventionTrigger
    schema_version: int = FORK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "provenance_id",
            "instance_ref",
            "parent_branch_ref",
            "fork_snapshot_ref",
            "child_branch_ref",
            "intervention_id",
            "artifact_ref",
        ):
            ref(getattr(self, name), name)
        if self.parent_branch_ref == self.child_branch_ref:
            raise ContractError("fork child branch must differ from parent branch")
        count(self.parent_head_revision, "parent_head_revision")
        count(self.parent_head_event_seq, "parent_head_event_seq")
        count(self.fork_revision, "fork_revision")
        count(self.fork_event_seq, "fork_event_seq")
        if self.fork_revision > self.parent_head_revision:
            raise ContractError("fork revision cannot exceed parent head")
        if self.fork_event_seq > self.parent_head_event_seq:
            raise ContractError("fork event seq cannot exceed parent head")
        digest(self.parent_head_hash, "parent_head_hash")
        if self.schema_version != FORK_SCHEMA_VERSION:
            raise ContractError("unsupported fork provenance schema")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "provenance_id": self.provenance_id,
            "instance_ref": self.instance_ref,
            "parent_branch_ref": self.parent_branch_ref,
            "parent_head_revision": self.parent_head_revision,
            "parent_head_event_seq": self.parent_head_event_seq,
            "parent_head_hash": self.parent_head_hash,
            "fork_revision": self.fork_revision,
            "fork_event_seq": self.fork_event_seq,
            "fork_snapshot_ref": self.fork_snapshot_ref,
            "child_branch_ref": self.child_branch_ref,
            "intervention_id": self.intervention_id,
            "artifact_ref": self.artifact_ref,
            "trigger": self.trigger.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class InterventionLedgerEntry:
    """One append-only fork or resume fact; it never represents canon."""

    entry_id: str
    run_id: str
    provenance_id: str
    branch_ref: str
    intervention_id: str
    status: LedgerStatus
    cursor_revision: int
    replay_hash: str = ""
    sequence: int = 0
    schema_version: int = FORK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ("entry_id", "run_id", "provenance_id", "branch_ref", "intervention_id"):
            ref(getattr(self, name), name)
        if self.status not in _LEDGER_STATUSES:
            raise ContractError(f"unsupported intervention ledger status {self.status!r}")
        count(self.cursor_revision, "cursor_revision")
        count(self.sequence, "sequence")
        digest(self.replay_hash, "replay_hash", allow_empty=True)
        if self.schema_version != FORK_SCHEMA_VERSION:
            raise ContractError("unsupported intervention ledger schema")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "entry_id": self.entry_id,
            "run_id": self.run_id,
            "provenance_id": self.provenance_id,
            "branch_ref": self.branch_ref,
            "intervention_id": self.intervention_id,
            "status": self.status,
            "cursor_revision": self.cursor_revision,
            "replay_hash": self.replay_hash,
            "sequence": self.sequence,
        }


@dataclass(frozen=True, slots=True)
class ForkedInterventionRun:
    """Resumable branch handle carrying provenance and replay evidence."""

    run_id: str
    branch: InterventionBranch
    provenance: ForkProvenance
    resume_cursor: int
    resume_count: int = 0
    status: Literal["forked", "resumed"] = "forked"
    replay_hash: str = ""

    def __post_init__(self) -> None:
        ref(self.run_id, "run_id")
        count(self.resume_cursor, "resume_cursor")
        count(self.resume_count, "resume_count")
        if self.status not in {"forked", "resumed"}:
            raise ContractError("unsupported forked run status")
        digest(self.replay_hash, "replay_hash", allow_empty=True)
        if self.branch.branch_ref != self.provenance.child_branch_ref:
            raise ContractError("run branch does not match fork provenance")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": FORK_SCHEMA_VERSION,
            "run_id": self.run_id,
            "branch": self.branch.to_dict(),
            "provenance": self.provenance.to_dict(),
            "resume_cursor": self.resume_cursor,
            "resume_count": self.resume_count,
            "status": self.status,
            "replay_hash": self.replay_hash,
        }


InterventionRun = ForkedInterventionRun
ForkRun = ForkedInterventionRun


__all__ = [
    "FORK_SCHEMA_VERSION",
    "ForkProvenance",
    "ForkRun",
    "ForkedInterventionRun",
    "InterventionLedgerEntry",
    "InterventionRun",
    "LedgerStatus",
    "count",
    "digest",
    "ref",
]
