# Package Certification Harness (G17D)

## Command
`python scripts/wxpack.py certify <dir> <package_id>` -> machine-readable JSON report (and human-readable).

## Checks
| Check | Behavior |
|---|---|
| static_validation | manifest structure/schema; actionable errors |
| forbidden_imports | only `wanxiang_domain`/`wanxiang_substrate` (public SDK); internal modules rejected |
| runtime_install | dry-run install through the public PackageInstaller (lock hash) |

## Report fields
`package_id`, `runtime_version`, `schema_version`, `platform`, `checks[]`, `ok` — includes
runtime/SDK/package versions for reproducibility.

## Qualification results
| Check | Result |
|---|---|
| Reference external package passes certification | PASS |
| Known-bad fixture (forbidden import) fails for the expected reason | PASS |
| Output includes runtime/SDK/package versions | PASS |

## Evidence
- `uv run pytest tests/integration/test_g17d_certification.py -q` -> 2 passed.
- Conformance harness is a release gate for bundled examples (runs in the authoring workflow).
