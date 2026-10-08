# G90F — Publishing Profiles

Date: 2026-08-26
Status: PASS

## Evidence

- `PublishingProfile` carries explicit public/private/unlisted/family-private
  visibility, owner/audience refs, package metadata, rights summary, and safety
  extension refs.
- `RightsSummary.from_sources()` preserves source, package, public-export,
  blocked, and review refs separately. Creator-intent-only profiles use an
  explicit intent ref rather than pretending to have source rights.
- `PublishingPolicy` blocks missing package rights, blocked source refs, and
  public export without public-export approval. It does not register a package
  or mutate Canonical World State.
- Private and family-private profiles are publishable only within their
  boundary and never become Plaza listings; the decision exposes this as
  `visible_in_plaza=False`.
- Package metadata and safety extension points are schema-versioned data and
  references, not executable moderation or Commit Authority paths.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py tests/unit/substrate/test_g90c_prompt_genesis_provider.py tests/unit/substrate/test_g90d_hybrid_genesis.py tests/unit/substrate/test_g90e_workshop_editor.py tests/unit/substrate/test_g90f_publishing_profiles.py`: 14 passed
- Private-not-in-Plaza and blocked-rights negative tests: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90G is next. Registry/search/install remains metadata and trust-boundary work,
not a commercial transaction system.
