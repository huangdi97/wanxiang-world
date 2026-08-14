# Goal G17C Acceptance Report — External Author Documentation & Reference Templates

## Status
PASS

## Objective
Create documentation that allows a developer unfamiliar with Core internals to build a correct package from public contracts.

## Delivered
- `docs/sdk/EXTERNAL_AUTHOR_GUIDE.md` — quickstart, hierarchy, state/action boundaries, source/rights, testing, versioning, debugging, anti-patterns.
- `tests/integration/test_g17c_author_docs.py` — 2 tests.

## Findings
- A clean-room authoring exercise (scaffold -> validate -> build) follows the guide and uses only the public SDK.
- Docs distinguish definition content (packs/manifests) from runtime instance state.
- Examples avoid Core internals and anti-patterns (no ORM/Commit internals, no inference-as-fact, no UI-only authz).

## Evidence
- 2 tests passed; ruff/pyright clean.

## Remaining limitations
- Publishing/packaging to a live registry is covered by later M14 goals; the authoring workflow is fully local.

## Final checkpoint
- commit: `g17c: external author documentation & reference templates`
