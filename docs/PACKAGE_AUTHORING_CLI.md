# Package Authoring CLI (G17B)

## Commands (`python scripts/wxpack.py`)
| Command | Behavior |
|---|---|
| `scaffold <dir> <package_id> [--kind domain\|world\|scenario] [--name ...]` | generates a package directory with a public-SDK manifest module, a minimal test, and a README |
| `validate <dir> <package_id>` | loads the generated manifest and reports actionable errors (no auto-fixing) |
| `build <dir> <package_id>` | dry-run: registers the manifest and installs through the public PackageInstaller, returning the lock hash |

## Generated package
- Imports only `wanxiang_domain` / `wanxiang_substrate` (public SDK); no Wanxiang internal modules.
- Manifest: `PackageManifest(...).with_hash()` with exact pins and default-deny executable trust.
- Minimal test: registers the manifest and verifies it is resolvable.

## Conformance
- A generated package passes schema validation and the reference-world conformance harness without manual repair.
- Invalid manifests (e.g., package_id mismatch) produce actionable errors.
