# G90B — Prompt Genesis Contract

Date: 2026-08-26
Status: PASS

## Evidence

- `CreatorIntent` is a versioned creator-data channel with a stable text hash;
  it cannot be confused with a system/provider instruction channel.
- Only explicitly labelled intent constraints are extracted. Directive-like
  text is retained as input data and produces no world rule or publish action.
- Domain suggestions and generated claims carry the intent reference and are
  permanently marked E5. Existing `CompletionCandidate` invariants keep them
  out of Canon until an explicit review path exists.
- `GenesisReviewGate` requires review of E5 output, constraint acceptance, and
  an explicit preview action; accepting one action does not silently satisfy
  the others.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py`: 5 passed
- Prompt injection/data-channel separation negative test: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90C is next. Prompt output remains candidate/provenance data and has no
provider or Commit Authority path.
