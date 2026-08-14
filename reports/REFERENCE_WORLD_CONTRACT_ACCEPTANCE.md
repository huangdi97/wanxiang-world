# Reference World Contract Acceptance (G15A)

## Contract
`docs/REFERENCE_WORLD_CONTRACT.md` defines the black-box World Pack contract:
- package composition (id/kind/version/dependencies/content_hash/executable_trust);
- rights/evidence/eval metadata requirements;
- worldness scenarios (12 required continuities);
- version pinning and reproducible install (lock hash);
- acceptance through public package/runtime contracts only (Core never imports reference content).

## Conformance harness
`scripts/reference_world_conformance.py::conformance_report(registry, root_id, rights_refs=..., ...)`:
- validates manifest metadata;
- catches missing rights/evidence/eval metadata;
- proves install through the public PackageInstaller (no Core modification).

## Evidence
| Check | Result |
|---|---|
| Tiny external synthetic pack builds + installs without Core changes | PASS |
| Conformance catches missing rights/evidence/eval metadata | PASS |
| Conformance reports install failures (missing dependency) | PASS |
| `uv run pytest tests/integration/test_g15a_reference_world_contract.py -q` | 3 passed |
