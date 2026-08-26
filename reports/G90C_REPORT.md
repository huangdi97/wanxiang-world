# G90C — Prompt Genesis Provider

Date: 2026-08-26
Status: PASS

## Evidence

- Prompt Genesis reuses the existing `ProviderRouter` and `ProviderCapability`
  boundary; no second provider registry or hidden provider call was added.
- Missing `llm` capability raises the existing typed
  `CAPABILITY_UNAVAILABLE` path. The deterministic local provider is private-
  safe, bounded, and requires no API key.
- Provider output is schema-checked for intent locator, provider identity,
  `prompt-genesis-v1`, E5 evidence class, and candidate-only output. Authority
  fields such as `commit` and `canonical_state` are rejected.
- Calls produce an auditable checkpoint with provider id, attempts, proposal
  count, and completion state. Provider results remain proposals and cannot
  mutate drafts, packages, or Canonical World State.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py tests/unit/substrate/test_g90c_prompt_genesis_provider.py`: 8 passed
- Missing-provider typed failure and malformed provenance negative tests: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90D is next. External/provider-backed output remains candidate-only; no model
training or provider-specific Commit path is introduced.
