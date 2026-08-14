# Registry Lifecycle Qualification (G17F)

## Results
| Check | Result |
|---|---|
| Publishing a new version does not change an existing pinned install | PASS |
| Upgrade requires explicit action (upgrade_candidate + new install); no auto-upgrade | PASS |
| Dependency conflict produces actionable failure (DependencyConflict) | PASS |
| Deprecated/yanked packages remain identifiable; old world history reproducible | PASS |
| Explicit root-version pin honored by the resolver (fixed in this Goal) | PASS |

## Fix (P1)
The package resolver accepted `root_version` but selected the latest version for the root and only
validated afterwards; an explicit root pin was therefore a no-op that errored. The resolver now seeds
the root pin before traversal, so `install(root, version)` honors the requested version.

## Semantics
- Running instances are pinned; a new publish never silently changes a running world.
- Yank blocks NEW installs but preserves metadata for replay/reproducibility.

## Evidence
- `uv run pytest tests/integration/test_g17f_registry_lifecycle.py -q` -> 4 passed.
- Package registry/install regression (20 tests) PASS.
