# G90G — World Registry / Marketplace Baseline

Date: 2026-08-26
Status: PASS

## Evidence

- `WorldRegistryCatalog` is an index/search/open adapter over the existing
  `InMemoryPackageRegistry` and `PackageInstaller`; it does not create a
  second package store or dependency resolver.
- Entries carry official/community labels, categories, tags, semantic version,
  compatibility, manifest hash, trust class, and explicit package provenance.
- Search filters by query, label, category, tag, runtime compatibility, and
  viewer visibility. Private/unlisted entries are not publicly discoverable;
  public entries use the PublishingPolicy Plaza listing decision.
- Open is data-only and reports `executable_loaded=False`. Data-only install is
  allowed, while existing executable trust enforcement rejects extensions for
  untrusted packages.
- Rights-blocked publishing is rejected before package registration, so a
  blocked world cannot enter the Registry.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py tests/unit/substrate/test_g90b_prompt_genesis_contract.py tests/unit/substrate/test_g90c_prompt_genesis_provider.py tests/unit/substrate/test_g90d_hybrid_genesis.py tests/unit/substrate/test_g90e_workshop_editor.py tests/unit/substrate/test_g90f_publishing_profiles.py tests/unit/substrate/test_g90g_world_registry.py`: 17 passed
- Search/open/install and untrusted-executable negative tests: PASS
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90H is next. The Registry remains a package metadata/trust boundary and does
not implement commercial transactions or runtime authority.
