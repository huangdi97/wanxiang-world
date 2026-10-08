# G97B — Literary 30d/90d Certification

Date: 2026-08-27  
Status: PASS

## Scope and boundary

G97B certifies a selected, source-created literary qualification world over
the existing v5.4 product/runtime path. The source is private,
rights-approved, package-eligible, and training-disabled. It is a bounded
qualification fixture, not the original 2026-08-25 323,815-character private
book. The original real-book report remains `NOT_ACCEPTED` and is not replaced
by this run.

No source text from the original book was added to the repository. No second
canonical state, event store, branch system, package/source registry, or
Commit Authority was introduced. Long-horizon services emit scheduler,
checkpoint, LOD, budget, and compaction evidence; canonical clock, actor, and
memory effects still use the existing `WorldRuntime` Commit Authority path.

## Reproducible product chain

`tests/integration/test_g97b_literary_90d_certification.py` runs:

`SourceRecord → OneClickAuthoring → WorldPackage → Preview →
PlayableService → Living Instance → SQLite WorldRuntime → Commit Authority`.

The run uses the selected accelerated profile `g97b-selected-90d` with
`time_scale=100`, `seed=9702`, and 100 world ticks per simulated day. The
qualification ledger explicitly requires `24h`, `7d`, `30d`, and `90d`; a
unit regression proves that a 30d sample alone cannot satisfy that requirement.

## Measured evidence

| Measure | Result |
|---|---:|
| Horizon samples | 24h / 7d / 30d / 90d |
| Selected horizon | 90 simulated days / 9,000 world ticks |
| Source actors | 2 (`ent_alice`, `ent_bob`) |
| Main-branch committed events | 455 |
| Runtime/run checkpoints | 90 |
| Actor-local memories | 90 per actor / 180 total |
| Serialized state storage | 1,832 → 92,088 bytes |
| World budget calls / charged storage | 450 / 90,256 bytes |
| Observed LOD levels | L0, L3, L4 |
| Reference compaction summaries | 18 |
| Replay vs SQLite restart recovery | equal |
| Relationship projection revisions | 4 (baseline + 3 reviewed changes) |
| Relationship trust after reviewed drift | 0.6 |
| Actor persona projection | changed, bounded by policy |

All four horizon samples reached their exact target tick and had equal replay
and recovery semantic hashes. The 90 daily checkpoints retain a monotonic
scheduler cursor ending at tick 9,000 and the final main-branch event head.
The injected crash before checkpoint publication left no latest checkpoint.
A fresh SQLite runtime restored the final state hash. Reference-only
compaction retained event and memory-summary refs without deleting or
rewriting the authoritative event stream.

At day 45, a child branch accepted a branch-only status command while the
parent hash and event tuple stayed unchanged. Child restore/replay matched its
child state. This is branch evidence, not a replacement for parallel
worldline Gate 41.

## Actor / Relationship drift boundary

Three committed Alice status-event refs at days 30, 60, and 90 formed the
multi-event evidence window for a reviewed, bounded `PersonaDelta`. The same
event refs drove three reviewed `RelationshipDelta` proposals through the
existing immutable `RelationshipGraph`; the graph replayed exactly. Applying
these projections changed the Actor persona fingerprint and relationship
trust while leaving the canonical SQLite state hash and event history
unchanged. Projection drift is therefore evidence-backed and explainable; it
does not silently rewrite world truth.

## Quality and architecture evidence

- Focused G97B and long-horizon/evolution regression:
  `7 passed, 1 warning` in 29.93s.
- Full quality: `1447 passed, 1 skipped, 2 warnings` in 371.44s (6:11).
- The one skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile because
  `WANXIANG_POSTGRES_TEST_URL` is not configured.
- Ruff check and format check: PASS; full Pyright: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G97B is PASS and Gate 24 is `ACCEPTED`. The wider v5.5 matrix remains
`IN_PROGRESS / NOT_ACCEPTED`: later M94 goals, clean-clone/remote/Actions
evidence, and the original real-book acceptance boundary remain separate
requirements. No v5.5 rc1, v5.6 work, model training, or private-source
upload was performed.
