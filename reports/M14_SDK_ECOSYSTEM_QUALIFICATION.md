# M14 SDK & Ecosystem Qualification (G17H)

## Coverage
| Goal | Focus | Tests | Verdict |
|---|---|---|---|
| G17A | SDK contract + semver/compat policy | 3 | PASS |
| G17B | Authoring CLI + schema validation | 3 | PASS |
| G17C | External author docs + templates | 2 | PASS |
| G17D | Third-party conformance/certification harness | 2 | PASS |
| G17E | Plugin trust/signing/capabilities | 4 | PASS |
| G17F | Registry publish/upgrade/deprecation | 4 | PASS (resolver pin fixed) |
| G17G | Black-box external sample pack | 2 | PASS |
| G17H | Ecosystem qualification | 2 | PASS |

## Consolidated evidence
- A third-party developer adds a world without modifying Core (public SDK + registry + runtime).
- Stable public APIs have compatibility snapshots (sdk_api_baseline.json; breaking changes detected).
- Trust policy (data-only never executes; signed+capability-gated trusted) and registry policy (pin/yank/
  deprecation preserving history) enforced.
- Black-box sample: author -> publish -> install -> instantiate -> run -> v2 explicit upgrade, v1 pinned.

## Evidence
- M14 suites: 22 passed.
- Full gate: 554 passed + 1 EXTERNAL_BLOCKED skip, ruff/pyright/architecture PASS.
