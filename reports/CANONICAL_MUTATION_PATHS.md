# Canonical Mutation Paths (G13C)

The only authoritative mutation path in the implemented repository:

```text
CommandEnvelope -> resolver/adjudication -> ProposedWorldDelta -> CommitRequest
  -> CommitAuthority.commit (preconditions -> apply_delta -> atomic append -> revision advance)
  -> CommittedEvent -> canonical state projection -> audit record
```

- Authority: `wanxiang_runtime.authority.CommitAuthority.commit`
- Enforcement:
  - precondition: instance/branch match, expected revision, rule version, non-empty delta
  - apply_delta: deterministic invariant-checked pure state transition
  - append: atomic durable append through EventAppendPort (failure exposes no new state)
  - revision advance + audit record

- Entry points found (construct or call .commit): 1
  - `packages\application\src\wanxiang_application\world_runtime.py`

- Persistence write owners: apps/api, packages/persistence

No projection, simulator, Reality Bridge, Director, model provider, plugin or
SDK client holds a CommitAuthority or writes canonical events directly.
