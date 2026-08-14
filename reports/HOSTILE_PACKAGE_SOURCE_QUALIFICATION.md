# Hostile Package, Plugin & Source Input Qualification (G14F)

## Trust model (matches implementation)
- Package/source metadata is parsed but NEVER executed during inspection or install.
- Executable extensions are **default deny** (`ExecutableExtensionPolicy`): only explicitly trusted
  packages may use the known extension set (.py/.pyc/.js/.wasm/.dll/.so/.exe); untrusted is always denied.
- No OS-level sandboxing is claimed; the boundary is "trusted/signed executable plugins or none" (limitation stated).

## Scenarios
| Hostile input | Behavior | Result |
|---|---|---|
| Path-traversal-like package id (`../../evil`) | treated as an opaque identifier; install is pure metadata, no filesystem write | PASS |
| Malformed content hash | rejected at registry boundary (InvalidManifest) before any install state | PASS |
| Untrusted executable | rejected (UntrustedExecutable); registry unchanged | PASS |
| Conflicting dependency constraints | rejected (DependencyConflict); both versions remain registered | PASS |
| Prompt-injection in source payload | remains data inside candidates; compiler behavior/hash unchanged | PASS |
| Oversized / unsupported (pdf/ocr) sources | rejected with error diagnostics (never silently extracted) | PASS |
| Deeply nested YAML (schema bomb) | bounded by MAX_PAYLOAD_BYTES (64KB); parsed as data or rejected, never corrupted | PASS |

## Evidence
- `uv run pytest tests/integration/test_g14f_hostile_input.py -q` -> 6 passed.
- Strong sandboxing limitation stated: executable plugin code is not executed by the platform at all.
