# Commit Authority & Core Invariants (GOAL_01B)

Ownership: `packages/runtime` (validate/resolve/commit coordination), depending
on `packages/domain`. Persistence adapters implement the append port later.

## Authoritative mutation path

```text
Command / Intent / Observation
  -> validation (CommandValidator)
  -> resolution (Resolver -> ProposedWorldDelta)
  -> Commit Authority
       preconditions (instance/branch match, expected revision, rule version)
       -> apply_delta (pure; invariant checks; never mutates input)
       -> build CommittedEvent (event_seq from append port)
       -> append via EventAppendPort (atomic; failure exposes no new state)
       -> advance branch revision
       -> AuditRecord (trace/event identity; not part of semantic hash)
```

Only `CommitAuthority.commit` may turn a proposal into canonical state. There is
no public mutator on `InMemoryCanonicalState`; `apply_delta` returns a new
immutable state.

## Core invariants (initial registry)

- No duplicate entity create (Conflict).
- Entity must exist for update/delete (ValidationRejected).
- No duplicate relation create (Conflict).
- Relation must exist for delete (ValidationRejected).
- Relation source/target entities must exist (ValidationRejected).
- Revision monotonicity and branch/instance identity enforced by preconditions.
- Duplicate command retry handled at the event-store layer (GOAL_01C).

## Atomicity

- `apply_delta` validates first; any invariant failure raises before a new state
  exists, so the input state hash is unchanged.
- The append port is the commit point: if append raises (e.g. simulated
  persistence failure), no committed event exists and no new state is returned.
- Audit/trace metadata is emitted separately from domain state.

## Ports

- `EventAppendPort` (Protocol): append/load/last_event_seq/command_result_event.
- `InMemoryEventAppendLog`: in-memory adapter with failure injection for tests.
- Durable adapter arrives in GOAL_01C/01E behind the same port.

## Extension points

- Add invariants to `INVARIANTS` in `invariants.py` (check(state, op)).
- Register deterministic resolvers by action type in `ResolverRegistry`.
