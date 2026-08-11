# Core Semantic Contracts (GOAL_01A)

Ownership: `packages/domain` (pure, framework-independent). No FastAPI,
SQLAlchemy, Alembic, LLM or Pydantic imports (architecturally enforced).

## Module map

| Module | Responsibility |
|---|---|
| ids.py | validated immutable ID value objects (WanxiangId subclasses) |
| versions.py | SchemaVersion / RuntimeVersion / PackageVersion (non-negative ints) |
| time.py | WorldTime (deterministic ticks) vs CommitTimestamp (wall clock, non-semantic) |
| errors.py | structured error taxonomy (WanxiangError -> typed subclasses) |
| hierarchy.py | BranchRevision / EventSeq / BranchAncestry / BranchMetadata |
| entity.py | EntityState / RelationState / ComponentData (typed identity + flexible fields) |
| command.py | CommandEnvelope (proposal, idempotency/causation/correlation) |
| delta.py | ProposedWorldDelta + typed operations (EntityCreate/Update/Delete, RelationCreate/Delete) |
| event.py | CommittedEvent (append-only replayable record) |
| hashing.py | canonical_json + semantic_sha256 (excludes non-semantic fields) |
| state.py | CanonicalState read-model boundary (Protocol) |
| snapshot.py | SnapshotMetadata |
| run.py | RunMetadata (seed/version for deterministic runs) |
| evidence.py | ClaimRef / EvidenceRef (source is not automatically a fact) |
| rights.py | RightsEnvelope decision seam |
| serialization.py | versioned serialization for command/delta contracts |
| serialization_history.py | versioned serialization for event/snapshot/run/ancestry |

## Key semantics

- **Proposal vs Commit are distinct**: `CommandEnvelope` + `ProposedWorldDelta`
  are proposals; `CommittedEvent` is the durable committed record carrying the
  applied delta. Only Commit Authority turns a proposal into a committed event.
- **World time vs wall clock**: `WorldTime` (monotonic ticks) determines
  canonical ordering; `CommitTimestamp` is audit-only and excluded from
  semantic hashing (`NON_SEMANTIC_KEYS`).
- **Branch semantics**: `BranchRevision` starts at 0 (empty/initial state) and
  advances per committed event; `EventSeq` is the per-branch append position
  (1-based; 0 = empty stream). `BranchAncestry` carries parent/fork metadata.
- **Versioning**: every serialized contract embeds `schema_version`; unknown or
  newer versions raise `IncompatibleVersion` on deserialize.
- **No universal dict events**: deltas are typed operations; component payload
  fields are flexible but identity/version/order metadata stays typed.
- **Claims/evidence/rights**: first-class references exist now to avoid schema
  breakage in P4; full policies are later.

## Extension points

- New ID kinds: subclass `WanxiangId` with a distinct `_prefix`.
- New delta operations: add a typed dataclass to `delta.py`, wire it into
  `delta_to_primitive`/`delta_from_primitive`, add round-trip tests.
- New serialized contracts: use `expect_version` and `encode_id`/`decode_id`.
