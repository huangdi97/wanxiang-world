# G95F — Worldline Comparator

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

`WorldlineMeasurement` records sanitized numeric trajectory points linked to an
existing WorldRunArtifact. `WorldlineComparator` aligns by one shared input
reference and the complete `(category, metric, tick)` key. It covers Actor,
Relation, Institution, Macro, and Cost planes together; missing or extra keys
are reported and make the comparison unqualified. All aligned candidate
values, including zero deltas, are retained in the report, so no conclusion
can be selected from one metric. The read-only API/visual report contains
worldline/artifact refs and numeric series only.

The comparator consumes evidence and has no runtime, event-store, branch, or
Commit Authority dependency. It cannot mutate canonical state.

## Evidence

- Unit: `tests/unit/substrate/test_g95f_worldline_comparator.py` — 4 passed,
  proving five-plane alignment, complete difference summaries, missing-metric
  non-qualification, schema round-trip, API report generation, and alignment
  mismatch rejection.
- Integration: `tests/integration/test_g95f_worldline_comparator_product_chain.py`
  — 1 passed. The same private rights-approved source produced one
  WorldPackage and a real SQLite playable runtime; a baseline child branch and
  a normal Playable Commit Authority candidate branch retained separate
  snapshots, artifacts, event streams, and replay equality. Seven aligned
  Actor/Relation/Institution/Macro/Cost points were compared.
- Full quality: 1410 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  architecture, duplicate-abstraction, SDK compatibility, and minimality
  checks pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED
  profile.

## Boundary

Gate 43 (worldline trajectory/cost comparator) is accepted. Gate 41 remains
pending because the G95D real SQLite qualification was intentionally serial;
G95G-G97J and the remaining M92-M94 gates remain pending, so v5.5 remains
NOT_ACCEPTED.
