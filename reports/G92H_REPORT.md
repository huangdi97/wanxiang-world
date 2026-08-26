# G92H — 30d Qualification

Date: 2026-08-26  
Status: PASS

## Real source-created product chain

`tests/integration/test_g92h_30d_literary_runtime.py` starts from a private,
rights-approved synthetic literary `SourceRecord`, runs the existing
`OneClickAuthoring` source path, registers the resulting `WorldPackage` in
`PlayableService`, enters an embodied Alice character, and commits the first
action through the existing Commit Authority. The resulting SQLite runtime
instance is `prv_playable_1` and the package ref is
`world:wd_job_g92h_literary`. The source payload is used only in the local
qualification; it is not uploaded or copied into public evidence.

The detached run uses the existing `RuntimeProfile`-bound
`BackgroundSimulation` and `RecurringScheduler`. Scheduler occurrences are
proposal-side only; clock, actor status, and actor-local observation commands
are submitted through the existing `WorldRuntime`/Commit Authority path. The
run also exercises the leave/Continue boundary at day 15 while retaining the
same instance and branch.

## Measured 30d evidence

| Measure | Result |
|---|---:|
| accelerated world horizon | 30 days / 3,000 world ticks |
| source actors | 2 (`ent_alice`, `ent_bob`) |
| committed event count | 155 |
| successful run checkpoints | 30 |
| actor-local memories | 30 per actor / 60 total |
| memory summary refs after compaction | 12 |
| serialized state storage | 1,832 → 31,968 bytes |
| world budget calls / storage charged | 150 / 30,136 bytes |
| observed LOD levels | L0, L3, L4 |
| replay vs restart recovery | equal |

Every day reaches its exact target tick, both source actors are available, and
the event stream remains contiguous. `HorizonQualification` records 24h, 7d,
and 30d samples; all samples have equal replay and recovery hashes. A fresh
SQLite runtime restores the final state to the same semantic hash. The
reference-only compaction manifest retains recent event sequence refs and
memory summary refs without deleting or rewriting the authoritative EventStore.

The injected checkpoint publication crash leaves no latest checkpoint, while
the successful run store retains all 30 prior publications. This is the
required no-P0/P1 logical-corruption evidence for this accelerated run:
canonical state is only changed by the existing Commit Authority, and the
scheduler, background policy, LOD, budget ledger, and compaction service do
not own a second canonical state or event store.

## Quality evidence

- `tests/integration/test_g92h_30d_literary_runtime.py`: 1 passed; one
  existing Hypothesis collection warning.
- Ruff format/check: PASS.
- Pyright on the changed long-horizon implementation and G92H integration:
  0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G92H is PASS. M89's 30d literary run and Gates 23, 25, 26, 27, and 28 are
accepted by this evidence. Gate 24 (90d selected-world run) and M90-M94 remain
pending; v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No model training, private
source upload, or v5.6 work was performed.
