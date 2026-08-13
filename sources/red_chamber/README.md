# Red Chamber Source-gated Reference Slice (G08B)

## Status
EXTERNAL_BLOCKED for real literary data: no approved/rights-cleared Red Chamber
source corpus is present in this environment. Per the Goal, this directory
contains only manifests, templates and tests; real-pack acceptance is
EXTERNAL_BLOCKED and must never fabricate literary facts.

## What is implemented locally (PASS)
- Source Gate positive/negative fixture behavior (approved synthetic source
  compiles; rights-denied text cannot enter canonical compilation).
- Bounded slice manifest/template below.
- Tests: `tests/integration/test_m7_qualification.py` (red chamber section).

## When real data arrives
1. Place rights-cleared sources under `sources/` with provenance.
2. Run through Source Gate + Completion Ledger (canon/completion labels).
3. Compile a bounded character/location/event slice; never invent missing facts.