# G97F — Security / Safety / Cost / Storage

Date: 2026-08-27  
Status: PASS

## Scope

G97F audits the security boundary for long-horizon and untrusted UGC inputs:
prompt/data injection, package trust, resource exhaustion, private-source
privacy, secret scanning, and bounded cost/storage accounting. The original
2026-08-25 323,815-character private book remains the preserved
`NOT_ACCEPTED` source-of-truth boundary; it was not uploaded, edited, or used
as a test fixture in this Goal.

## Delivered and verified

- The existing Source→Draft ingestion path continues to treat source text as
  data, applies the SourceGate, validates bytes and archive safety, and keeps
  semantic/provider output proposal-only.
- Configured archive decompression-ratio limits are now actually applied by
  `IngestSecurityGate`; a strict configured ratio is covered by a regression
  test.
- `BudgetTracker` rejects negative command/tick/model-call consumption before
  accounting, preventing resource-budget underflow.
- A real migrated SQLite API application passed a private UGC source through
  Workshop → private Plaza → Character → embodiment → action/StateDiff →
  Leave → Continue. Owner/guest access was server-enforced and the private
  source marker was absent from every serialized response collected across the
  chain.
- The same public Studio API rejected a prompt-injection source with typed
  `malicious_source` and no package/preview; an untrusted registry package
  remained data-only and executable installation was rejected.
- API payload limits returned 413 and the abusive action burst returned 429.
  `CostBudgetLedger` preserved atomic usage when the next request degraded at
  the lower LOD boundary.

## Evidence

| Check | Result |
|---|---:|
| G97F product/security integration | 3 passed |
| Existing security, hostile-input, privacy, resource, package and budget regression | 17 passed, 2 warnings |
| Independent G20C curated security/chaos rerun | 65 passed, 0 failed, 0 skipped |
| `scripts/security_forensics.py` | secret findings=0, gate probes=4, threats=8, rights=6 |
| `uv run python scripts/architecture_check.py` | PASS |
| `uv run python scripts/quality.py` | 1455 passed, 1 skipped, 2 warnings in 371.58s |

The focused warnings are the known Hypothesis collection notice and the
Starlette/httpx deprecation notice; neither is a security finding. External
vulnerability scanning and live PostgreSQL remain explicitly
`EXTERNAL_BLOCKED` where the environment does not provide them.

## Boundary and decision

No P0/P1 security, privacy, package-trust, or budget bypass was found in the
scoped repository evidence. No source bytes entered Git, no secret was added,
no Canonical World State path was granted to a provider/UI/package, and no
compiler or Worldness gate was weakened. This accepts Gate 52 only; it does
not change the original real-book acceptance, scientific-validity boundary,
or the locked v5.5 rc1 release condition.

G97F is PASS and the Goal checkpoint is ready for commit. G97G remains the
next Goal for clean-clone and remote CI evidence.
