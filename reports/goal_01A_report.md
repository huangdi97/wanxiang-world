# Goal 01A Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 3410300 (goal 00B checkpoint; M0 tag m0-engineering-base)
- working-tree notes: clean

## Objective
Define a minimal, durable, framework-independent set of typed semantic
contracts required by the authoritative world kernel: identity, versioning,
commands, events, deltas, snapshots, branches, claims/evidence/rights
foundations and structured errors.

## Delivered
- `packages/domain` modules: ids, versions, time, errors, hierarchy, entity,
  command, delta, event, hashing, state, snapshot, run, evidence, rights.
- Versioned serialization: `serialization.py` (command/delta),
  `serialization_history.py` (event/snapshot/run/ancestry) with schema-version
  rejection on unknown versions.
- Semantic hashing utility (canonical sorted JSON + SHA-256) excluding
  wall-clock/audit fields.
- `docs/architecture/CORE_CONTRACTS.md` documenting ownership/semantics/extension.
- Contract/property tests (unit + Hypothesis).

## Key architecture decisions
- Strong IDs as validated immutable value objects (distinct classes per ID kind).
- BranchRevision (state revision, 0-based) vs EventSeq (append position, 1-based).
- WorldTime ticks are canonical ordering; CommitTimestamp is non-semantic.
- Proposal (Command/Delta) and Commit (CommittedEvent) are distinct types.
- Manual dataclass serialization (no Pydantic in domain per architecture rules).

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS | |
| Pyright strict | `uv run pyright` | PASS (0 errors) | |
| Pytest | `uv run pytest -q` | 48 passed | tests/unit/domain, tests/property |
| Architecture | `uv run python scripts/architecture_check.py` | PASS | |
| Full gate | `uv run python scripts/quality.py` | PASS | |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Later Commit/EventStore implementable without changing names/ownership | PASS | contracts stable; CORE_CONTRACTS.md |
| No SQLAlchemy/FastAPI in domain | PASS | architecture guard negative tests |
| Proposal and Commit records distinct | PASS | command/delta vs event tests |
| Branch/event sequence semantics documented | PASS | CORE_CONTRACTS.md |
| Rights/evidence foundations exist | PASS | evidence.py, rights.py |
| Tests pass without external services | PASS | full suite green |

## Migrations / compatibility
- Serialized contracts carry `schema_version`; unknown versions rejected.
- No persisted DB schema in this Goal (SQLite tables arrive in GOAL_01E).

## Security / rights impact
- RightsEnvelope decision seam; no boolean is_allowed scattering.
- Claims carry status; source is not automatically a fact.

## Known limitations
- Component payload fields are a typed primitive mapping; richer payload
  schemas are deferred to later substrate goals.
- Claim/Evidence are reference contracts only (full Source Registry is P4).

## External blockers
None.

## Final checkpoint
- commit: `goal 01A: define authoritative world core contracts`
