# V5.2 Code Minimality Ledger

> Required by `03_????????.md`: every new class/protocol/service/registry/
> manager must answer the four questions. Deletions/merges are recorded too.
> Updated continuously across G29A?G37G.

## G29A entry

### Deleted abstraction
| Item | Why | Evidence |
|---|---|---|
| `packages/evidence` stub package (5 LOC, empty `__init__`) | Empty placeholder; no consumers; evidence/rights lives in substrate (sources) ? DELETE per v5.1 G21B/G21D disposition | `rg wanxiang_evidence` -> no production consumers; quality gate green after removal |
| `packages/model_providers` stub package (5 LOC, empty `__init__`) | Empty placeholder; no consumers; provider routing stays in capability fabric ? DELETE per v5.1 G21B/G21D disposition | `rg wanxiang_model_providers` -> no production consumers; quality gate green after removal |

### New abstraction review (script/test tooling, not production Core)
| Item | 1) irreducible semantics | 2) replaces/merges | 3) why function/type/config insufficient | 4) two consumers or external boundary |
|---|---|---|---|---|
| `scripts/generate_v52_baseline_fixtures.py` | Freezes deterministic compatibility goldens (events/snapshot/branch/worldpack/api) before v5.2 work | Replaces ad-hoc fixture copying; centralizes deterministic normalization | A plain script is the right unit; no state/service needed | Consumers: `tests/architecture/test_v52_baseline_fixtures.py` + G34D backward-replay regression |
| `tests/architecture/test_v52_baseline_fixtures.py` | Reproducibility guard (reload + same semantic hash) | N/A (test) | N/A | Runs in full quality gate |

No production Core class/protocol/service/registry/manager was added in G29A.
