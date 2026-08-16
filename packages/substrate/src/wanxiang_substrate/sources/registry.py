"""Immutable source registry with audited review transitions (G04B)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.sources.errors import (
    DuplicateSource,
    InvalidTransition,
    SourceNotFound,
)
from wanxiang_substrate.sources.model import (
    ReviewStage,
    SourceRecord,
    canonical_json,
)


@dataclass(frozen=True, slots=True)
class AuditEntry:
    """Immutable decision history for a source."""

    source_id: str
    from_stage: str
    to_stage: str
    reviewer: str
    policy_version: int
    provenance: str


class SourceRegistry:
    """In-memory registry; source identity is immutable by content hash."""

    def __init__(self) -> None:
        self._records: dict[str, SourceRecord] = {}
        self._audit: dict[str, tuple[AuditEntry, ...]] = {}
        self._by_fingerprint: dict[str, str] = {}

    def register(self, record: SourceRecord) -> SourceRecord:
        # Identity = kind + content hash + version (G55A): a changed source
        # version is a new registration, never a silent overwrite.
        existing_id = self._by_fingerprint.get(record.fingerprint())
        if existing_id is not None and existing_id != record.source_id:
            raise DuplicateSource(
                f"content {record.content_hash[:12]} version {record.version!r} "
                f"already registered as {existing_id}"
            )
        if record.source_id in self._records:
            raise DuplicateSource(f"source {record.source_id!r} already registered")
        self._records[record.source_id] = record
        self._by_fingerprint[record.fingerprint()] = record.source_id
        self._audit[record.source_id] = (
            AuditEntry(record.source_id, "none", record.stage, "system", 1, record.provenance),
        )
        return record

    def get(self, source_id: str) -> SourceRecord | None:
        return self._records.get(source_id)

    def require(self, source_id: str) -> SourceRecord:
        record = self.get(source_id)
        if record is None:
            raise SourceNotFound(f"source {source_id!r} not found")
        return record

    def transition(
        self,
        source_id: str,
        next_stage: ReviewStage,
        reviewer: str,
        policy_version: int,
    ) -> SourceRecord:
        record = self.require(source_id)
        if not record.can_transition_to(next_stage):
            raise InvalidTransition(
                f"source {source_id!r} cannot move from {record.stage} to {next_stage}"
            )
        updated = SourceRecord(
            source_id=record.source_id,
            kind=record.kind,
            content_hash=record.content_hash,
            content_ref=record.content_ref,
            stage=next_stage,
            rights=record.rights,
            payload=record.payload,
            provenance=record.provenance,
            version=record.version,
            access=record.access,
            reliability=record.reliability,
            schema_version=record.schema_version,
        )
        self._records[source_id] = updated
        history = self._audit[source_id]
        self._audit[source_id] = history + (
            AuditEntry(
                source_id, record.stage, next_stage, reviewer, policy_version, record.provenance
            ),
        )
        return updated

    def audit_history(self, source_id: str) -> tuple[AuditEntry, ...]:
        self.require(source_id)
        return self._audit.get(source_id, ())

    def canonical_snapshot(self, source_id: str) -> str:
        return canonical_json(self.require(source_id))
