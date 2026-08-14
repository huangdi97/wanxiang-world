# v5.1 Final Acceptance & Evidence Standard

## Evidence statuses

`PASS | FAIL | EXTERNAL_BLOCKED | NOT_APPLICABLE | EXPERIMENTAL`

Every PASS needs reproducible evidence: test name/path, command, result summary, relevant hash/version/migration id, and report path.

## Global mandatory regression axes

- canonical mutation exclusivity;
- commit atomicity/idempotency/stale revision;
- branch isolation;
- replay determinism;
- old-event interpretation under versioned semantics;
- DB/package/event migrations;
- source/evidence/rights enforcement;
- runtime provider isolation;
- runtime dispose cannot undo world history;
- LLM-independent deterministic path;
- architecture import boundaries;
- generated API/TS schema consistency;
- backward compatibility with v5.0 fixtures;
- cross-domain reference worlds;
- minimal-core metrics and dead-code inventory.

## Code-minimality pass conditions

M25 cannot PASS if any of these remain without a documented, justified exception:

- two authoritative world-state implementations;
- multiple overlapping runtime provider registries;
- a global mutable service locator used by business code;
- separate commit engines/repositories for State/Ontology/Law without irreducible justification;
- a parallel Genesis package/registry ecosystem;
- a giant Meaning/Reality/Experience God service;
- unused public interfaces or dead production paths classified P0/P1;
- duplicate backend/frontend schemas maintained manually;
- direct provider/plugin ORM write access to authoritative tables.

## Final reports

M25 must produce:

- `reports/V5_1_FINAL_TRACEABILITY.md`
- `reports/V5_1_BACKWARD_COMPATIBILITY.md`
- `reports/V5_1_MINIMAL_CORE_AUDIT.md`
- `reports/V5_1_REPLAY_MIGRATION_CERTIFICATION.md`
- `reports/V5_1_CROSS_DOMAIN_CERTIFICATION.md`
- `reports/M25_V5_1_FINAL_CERTIFICATION.md`
- `reports/V5_1_PROGRAM_COMPLETION_REPORT.md`
- `docs/V5_1_IMPLEMENTATION_STATUS.md`
- `docs/V5_1_RELEASE_READINESS.md`
