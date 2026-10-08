# G90E — Scenario / Experience Editor

Date: 2026-08-26
Status: PASS

## Evidence

- Scenario and Experience edits now use the same `WorkshopDraftStore` and
  increment the shared draft revision; no parallel editor state is introduced.
- Existing versioned `ScenarioProfile` and `ExperiencePackage` contracts are
  reused. Package refs are checked against the workshop world draft when one is
  already attached, and ExperiencePackage validation is run before save.
- Preview validation checks both references and product configuration. The
  read-only `WorkshopPreview` is content-hashed and explicitly reports
  `published=False`; it performs no package publication or runtime mutation.
- Stale editor revisions are rejected before an edit can be saved.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py tests/unit/substrate/test_g90c_prompt_genesis_provider.py tests/unit/substrate/test_g90d_hybrid_genesis.py tests/unit/substrate/test_g90e_workshop_editor.py`: 12 passed
- Revision/concurrency and preview-without-publish tests: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90F is next. Publishing visibility and rights policy remains a separate gate.
