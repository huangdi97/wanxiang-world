# M16 Research Baseline (G19A)

## Isolation
- New `wanxiang_research` package (v5.1/v6) with FeatureFlags ALL OFF by default.
- Research code never gains Commit Authority; experimental failure cannot corrupt canonical worlds.

## Flags (all OFF)
| Track | Namespace | Promote criteria |
|---|---|---|
| ai_compiler | v5.1 | benchmark parity + clean-room build |
| persona_memory | v5.1 | drift < threshold over 90d run |
| distributed_host | v6 | shard consistency + replay parity |

## Experiment registry
- `ExperimentResult` (track, seed, decision, evidence, runtime/schema versions) with manifest hash;
  decisions: PROMOTE / KEEP_EXPERIMENTAL / REJECT.

## Benchmark baseline (comparison floor)
- M12/M13 baselines: worldness 12/12, 90-day run (~36s), 44 commits/s SQLite profile.

## Regression gate
- Flags OFF == M15-equivalent behavior (stable canonical path unchanged; replay hash stable).
- Every research track must declare promote/reject criteria (enforced).

## Evidence
- `uv run pytest tests/integration/test_g19a_research_flags.py -q` -> 3 passed.
- Governance: docs/RESEARCH_GOVERNANCE.md.
