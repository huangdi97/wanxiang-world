# G73C Report — Performance/recovery qualification

**PASS (2026-08-25)**

The existing bounded-source, job-checkpoint, runtime, backup and replay paths
were requalified without introducing a second cache, runtime, or authority.

| Gate | Result | Evidence |
|---|---|---|
| Commit throughput / replay benchmark | PASS | 200 commits: 45.68 events/s; 1200-event replay: 0.0161s |
| Lineage query benchmark | PASS | 400 nodes; ancestor/descendant query: 0.0091s |
| Concurrency/idempotency/lost update | PASS | G14A regression included in 14 passed |
| Backup/restore/disaster recovery | PASS | G16G regression included in 14 passed |
| Large-source chunk/cache/hash/restart | PASS | M59 hardening regression included in 14 passed |
| Orchestrator checkpoint/resume | PASS | M67 regression included in 14 passed |
| One-click long-path smoke | PASS | M69 regression included in 14 passed |
| Architecture conformance | PASS | 1 commit path, no new runtime authority |

Machine evidence: `reports/performance_benchmarks.json`. The benchmark profile
is the existing deterministic `small_ci` SQLite profile; it is capacity
evidence, not a claim about production multi-node throughput or real-book
latency. Live PostgreSQL/PITR remains the documented external boundary.
