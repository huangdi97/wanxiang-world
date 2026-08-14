# Goal G18F Acceptance Report — Heritage / Museum Workbench Completion

## Status
PASS

## Objective
Provide museum/heritage workflows for object semantic twins, IIIF/Linked Art/CIDOC mappings, conservation/reconstruction scenarios and rights-aware public/curator projections.

## Delivered
- `apps/api/src/wanxiang_api/heritage_workbench_service.py` — object view, curator-gated export, conservation history.
- `tests/integration/test_g18f_heritage_workbench.py` — 3 tests.
- `reports/HERITAGE_WORKBENCH_QUALIFICATION.md`, `reports/G18F_REPORT.md`.

## Findings
- Physical/digital/reconstruction states visibly distinct; reconstructions labeled (never original fact).
- Rights prevent restricted projection/export; conservation history is versioned/auditable.

## Evidence
- 3 tests passed; ruff/pyright clean.

## Remaining limitations
- Live IIIF media rendering and real museum data are EXTERNAL_BLOCKED; the rights-aware service contract is qualified.

## Final checkpoint
- commit: `g18f: heritage / museum workbench completion`
