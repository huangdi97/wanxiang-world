# G90D — Hybrid Genesis

Date: 2026-08-26
Status: PASS

## Evidence

- Hybrid fusion adapts existing source `CandidateEnvelope` records and Prompt
  Genesis E5 output into one provenance-traceable result; it does not create a
  second candidate or source registry.
- `HybridGenesisPolicy` makes source, prompt, or preserve-dissent precedence
  explicit. Precedence selects a review hint only; every conflicting
  alternative remains in the result.
- E0-E5 classes are carried on every claim. Prompt claims remain E5 and source
  claims retain their supplied source evidence class.
- Conflicts include all claim ids, selected id (when policy permits), and an
  explicit review reason. `HybridTrace` retains source refs, intent refs, and
  parent refs so generated completion can be audited back to its origin.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py tests/unit/substrate/test_g90c_prompt_genesis_provider.py tests/unit/substrate/test_g90d_hybrid_genesis.py`: 10 passed
- Source-precedence and preserve-dissent conflict tests: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90E is next. Hybrid fusion remains a candidate/review layer and never writes
source truth or Canonical World State.
