# v5.2 Release Readiness (Wanxiang)

## Status
RELEASE-READY at PLATFORM-MECHANISM level (local); real RedChamber content
EXTERNAL_BLOCKED.

## Gates (all PASS, 2026-08-15)
- Full quality: 982 passed + 1 skipped (PostgreSQL EXTERNAL_BLOCKED).
- Architecture conformance: PASS; kernel change guard: 0 violations.
- SDK/package/API frozen: routes=17, ts=5, py=1176.
- Migration head 0004; golden compatibility reproducible; perf baselines
  frozen (commits ~40 ev/s, replay 1200 ev ~24ms, lineage 400 nodes ~13ms).
- Security/rights/supply-chain: prompt-injection SourceGate, malicious-source
  rejection, RBAC via institution permissions, SBOM/secret scan green.

## What is NOT release-ready
- Real《红楼梦》canon compilation, real world pack content, real 7-day/30-day/
  1-year acceptance, and real derived RedChamber world require a legal,
  traceable edition (BLOCKERS.md G35A).

## Release policy
- Local commits + tags only; no push/deploy without explicit authorization.
