"""Event/Snapshot version context (G30H).

History must stay interpretable and replayable after Constitution, Sigma
(ontology space) and Gamma (law set) evolve. This module adds a minimized
version context:

- `VersionContext` records constitution_version, semantic_space_version,
  law_set_version and optional domain/runtime refs (one record, not per-event
  duplication).
- `legacy_version_context()` adapts old v5.0/v5.1 events (no context) so they
  still replay deterministically.
- `VersionContextLog` is an immutable append-only log mapping revisions to the
  context active at that revision; `resolve(revision)` picks the nearest
  preceding entry, else the legacy context.
- `SnapshotVersionContext` freezes the context a snapshot was created under.

The context is metadata: it is never part of the canonical semantic hash, so
replay determinism is unaffected by context evolution.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

VERSION_CONTEXT_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class VersionContext:
    """Versioned semantic interpretation context for history."""

    constitution_version: int
    semantic_space_version: int
    law_set_version: int
    domain_ref: str | None = None
    runtime_ref: str | None = None
    schema_version: int = VERSION_CONTEXT_SCHEMA_VERSION
    content_hash: str = ""

    def __post_init__(self) -> None:
        for name, value in (
            ("constitution_version", self.constitution_version),
            ("semantic_space_version", self.semantic_space_version),
            ("law_set_version", self.law_set_version),
        ):
            if isinstance(value, bool) or value < 0:
                raise ContractError(f"{name} must be a non-negative integer")

    def canonical(self) -> dict[str, object]:
        return {
            "constitution_version": self.constitution_version,
            "semantic_space_version": self.semantic_space_version,
            "law_set_version": self.law_set_version,
            "domain_ref": self.domain_ref,
            "runtime_ref": self.runtime_ref,
            "schema_version": self.schema_version,
        }

    def compute_hash(self) -> str:
        payload = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> VersionContext:
        return VersionContext(
            constitution_version=self.constitution_version,
            semantic_space_version=self.semantic_space_version,
            law_set_version=self.law_set_version,
            domain_ref=self.domain_ref,
            runtime_ref=self.runtime_ref,
            schema_version=self.schema_version,
            content_hash=self.compute_hash(),
        )


def legacy_version_context(rule_version: int = 1, schema_version: int = 1) -> VersionContext:
    """Adapter context for old v5.0/v5.1 events (no explicit context)."""
    return VersionContext(
        constitution_version=1,
        semantic_space_version=1,
        law_set_version=0,
        domain_ref=None,
        runtime_ref=f"runtime:{rule_version}",
        schema_version=schema_version,
    ).with_hash()


@dataclass(frozen=True, slots=True)
class VersionContextEntry:
    """Context active from a given revision onward."""

    from_revision: int
    context: VersionContext


def extend(
    log: tuple[VersionContextEntry, ...], entry: VersionContextEntry
) -> tuple[VersionContextEntry, ...]:
    """Append a context entry (immutable log; must be monotonic by revision)."""
    if log and entry.from_revision <= log[-1].from_revision:
        raise ContractError("version context log must be append-only with increasing revisions")
    return log + (entry,)


def resolve_context(revision: int, log: tuple[VersionContextEntry, ...]) -> VersionContext:
    """Resolve the context active at a revision (nearest preceding entry)."""
    active: VersionContext | None = None
    for entry in log:
        if entry.from_revision <= revision:
            active = entry.context
        else:
            break
    return active if active is not None else legacy_version_context()


@dataclass(frozen=True, slots=True)
class SnapshotVersionContext:
    """The version context frozen under a snapshot was created."""

    instance_ref: str
    branch_ref: str
    revision: int
    event_seq: int
    context: VersionContext

    def to_primitive(self) -> dict[str, object]:
        return {
            "instance_ref": self.instance_ref,
            "branch_ref": self.branch_ref,
            "revision": self.revision,
            "event_seq": self.event_seq,
            "context": self.context.canonical(),
            "context_hash": self.context.content_hash,
        }
