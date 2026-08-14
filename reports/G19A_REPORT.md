# Goal G19A Acceptance Report — Research Namespace, Feature Flags, Benchmarks & Promotion Rules

## Status
PASS

## Objective
Create a safe experimental architecture for v5.1/v6 research so new AI/world-model/distributed ideas can be tested without destabilizing the release-qualified core.

## Delivered
- `packages/research/` — `wanxiang_research` experimental namespace (flags.py, results.py) OFF by default.
- `docs/RESEARCH_GOVERNANCE.md` — isolation, promote/reject criteria, reproducibility, ADR requirement.
- `tests/integration/test_g19a_research_flags.py` — 3 tests.
- `reports/M16_RESEARCH_BASELINE.md`, `reports/G19A_REPORT.md`.

## Findings
- Flags OFF == M15-equivalent behavior; experimental failure cannot corrupt canonical worlds.
- Every research track has promote/reject criteria (enforced); results are reproducible via manifest hash.

## Evidence
- 3 tests passed; ruff/pyright clean; architecture guard PASS.

## Remaining limitations
- Research tracks are experiments only; no promotion decisions made yet (each later G19 track decides).

## Final checkpoint
- commit: `g19a: research namespace, feature flags, benchmarks & promotion rules`
