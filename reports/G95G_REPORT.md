# G95G — ValidationProfile v1

Date: 2026-08-27  
Milestone: M92  
Status: **PASS**

## Result

G95G adds an immutable, schema-versioned `ValidationProfile` covering V0–V7:
Structural, Source Fidelity, Behavioral, Mechanism, Macro, Long-Horizon,
Counterfactual, and External Calibration. The profile records an explicit
mapping to existing Worldness dimensions for traceability; it does not reuse
Worldness scoring as scientific validity.

`ValidationCheck` requires an explicit status and evidence references.
`ValidationStack` fills an omitted level with `unknown`; `ValidationReport`
aggregates conservatively and only reports `accepted=True` when every required
level is explicitly `pass`. `unknown`, `blocked`, and `fail` can never become
pass through a Worldness reference. The API/export payload contains refs,
statuses, reasons, and numeric measurements only; private source content is
not included.

## Evidence

- Unit: `tests/unit/substrate/test_g95g_validation_profile.py` — 5 passed,
  proving V0–V7 profile round-trip, unknown-by-default behavior, explicit
  all-pass acceptance, external-calibration unknown handling, and invalid
  mapping-key rejection.
- Integration: `tests/integration/test_g95g_validation_profile_product_chain.py`
  — 1 passed. A rights-approved private source traveled through the existing
  OneClickAuthoring → WorldPackage → Preview/Living Instance → SQLite runtime
  chain. The test measured manifest/entity/source-pin/action/event/replay,
  bounded seven-day trace, and isolated counterfactual branch evidence. The
  resulting report is complete but `overall_status=unknown` and
  `accepted=False` because V7 has no external calibration dataset; this is the
  required `unknown != pass` boundary. A sanitized WorldRunArtifact links the
  report statuses and verifies its content hash.
- Full quality: `1416 passed, 1 skipped, 2 warnings`; Ruff, format, Pyright,
  architecture, duplicate-abstraction, SDK compatibility, and minimality
  checks pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED
  profile.
- Current SDK/minimality evidence: 62 routes, 5 TypeScript symbols, 2011
  Python public names; 556 production files, 62426 LOC, 0 import cycles, 1
  commit path, and 0 oversized modules. Duplicate scan has no unallowed
  duplicates.

## Boundary

Gate 44 (ValidationProfile V0–V7, `unknown != pass`) is accepted as an
implementation/evidence-semantics gate. The real-chain report deliberately
remains non-accepted because external calibration is unknown; this does not
claim scientific validity. Gate 41 remains pending because G95D's real SQLite
qualification was intentionally serial. G95H–G97J and the remaining release
gates remain pending, so v5.5 remains **IN_PROGRESS / NOT_ACCEPTED** and no
v5.5 release candidate is created.
