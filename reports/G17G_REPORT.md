# Goal G17G Acceptance Report — Black-box External Sample Pack Built Outside Core Repository Internals

## Status
PASS

## Objective
Prove the SDK/ecosystem claim by authoring a nontrivial sample package as if by a third party, using only installed public artifacts and docs.

## Delivered
- `scripts/blackbox_sample.py` — clean-room external sample authoring.
- `tests/integration/test_g17g_blackbox_sample.py` — 2 tests.
- `reports/EXTERNAL_SAMPLE_PACK_BLACKBOX.md`, `reports/G17G_REPORT.md`.

## Findings
- The sample works with no Core source-tree imports (public SDK only) and includes a custom domain action
  via the permitted resolver extension mechanism.
- Publish -> install -> instantiate -> run -> v2 publish -> explicit upgrade, with the v1 instance pinned
  and replayable.

## Evidence
- 2 tests passed; ruff/pyright clean.

## Remaining limitations
- A real hosted registry/distribution remains EXTERNAL_BLOCKED; the local black-box flow is fully qualified.

## Final checkpoint
- commit: `g17g: black-box external sample pack built outside core repository internals`
