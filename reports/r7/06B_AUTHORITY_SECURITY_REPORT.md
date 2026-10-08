# R7 06B — Authority & Security Closure

Status: `IMPLEMENTED / VALIDATED` for the R7 architecture/security scope.

## Canonical write surface

R7 now has one auditable canonical-write path rather than a convention-based
"please do not write" rule.

- Python event stores require a branded `CanonicalWriteLease`.
- Look-alike/hand-built leases are rejected.
- A lease is bound to one world instance + branch/worldline.
- The minting surface is frozen by
  `tests/architecture/test_r7_write_surface_guard.py`.
- Persistence imports, `CommitAuthority` references and minter references are
  exact-golden sets: unexpected expansion fails CI.
- Foundry, Execution, Reality, Substrate, Application, Observability, Research
  and agent-harness modules are guarded from persistence/minter access.

Runtime denial evidence lives in `tests/security/test_r7_write_denials.py` and
covers unleased append, forged credential, cross-worldline credential use,
SQLAlchemy adapter denial, ordinary actor denial and RPC authority denial.

## Cordis-side authority

`packages/cordis_host/src/authority.ts` keeps capability minting inside the
explicit Authority bootstrap. Policy resolution is monotonic:

- cross-worldline write -> hard deny;
- rights denied -> hard deny;
- required evidence missing -> hard deny;
- external effect that bypasses the outbox -> hard deny;
- unversioned overwrite -> deny;
- a later ALLOW cannot reverse an earlier HARD_DENY.

`grantAuditView()` exposes operator-safe mint audit metadata without exposing
the capability itself.

## Boundary

This report proves the repository's defined write surface and negative/security
tests. It does not claim hostile-code security for trusted in-process Cordis
plugins; generated/untrusted execution remains an Execution Fabric concern.
