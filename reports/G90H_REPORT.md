# G90H — M87 Workshop Qualification

Date: 2026-08-26
Status: PASS

## Qualification result

The shared World Workshop now qualifies all three creation modes through the
existing product boundaries:

- From Source uses the existing OneClickAuthoring and semantic distillation
  provider, then produces a WorldPackageDraft and isolated `preview://` install.
- From Prompt uses the ProviderRouter-backed local Prompt Genesis provider,
  keeps every generated claim at E5, and blocks public publication until the
  three review actions are accepted.
- Hybrid reuses source candidates, retains source/prompt alternatives and
  provenance traces, and only blocks compilation for an unresolved
  cross-origin conflict. Same-origin source alternatives remain auditable
  rather than being silently discarded.

The API and Studio product surface is wired to the same WorkshopService and
the existing PlayableService. A publishable build may register a playable
profile; an unreviewed prompt/hybrid build does not register a public profile.
No Workshop, provider, editor, registry, or API route can mutate Canonical
World State.

## Evidence

- Source qualification: private E3 source, rights-approved package/public
  export, `local_semantic_v1`, WorldPackage, PreviewInstall, private publishing
  decision, and PlayableService observer entry.
- Prompt qualification: creator intent, local provider proposals, E5 claim
  audit, measured non-zero compiler coverage, preview, review-gated public
  publishing, and PlayableService observer entry after review.
- Hybrid qualification: source candidate plus Prompt Genesis E5 claims,
  origin/evidence traces, measured non-zero compiler coverage, preview, and
  private publishing boundary.
- API qualification: `/workshop` home, `/workshop/from-source`,
  `/workshop/from-prompt`, `/workshop/from-hybrid`, evidence/review routes,
  and `/experience` entry were exercised with FastAPI TestClient over the
  reference runtime.

## Checks

- `uv run pytest -q tests/integration/test_g90h_workshop.py tests/api/test_g90h_workshop_api.py`: 2 passed
- G90A-G90G focused regression: 17 passed
- `uv run ruff check apps/api/src/wanxiang_api tests/api/test_g90h_workshop_api.py packages/substrate/src/wanxiang_substrate/workshop`: PASS
- `uv run pyright apps/api/src/wanxiang_api tests/api/test_g90h_workshop_api.py packages/substrate/src/wanxiang_substrate/workshop`: 0 errors, 0 warnings
- `uv run python scripts/architecture_check.py`: PASS
- Production workshop/API files remain within the repository 300-line limit.

M87 is complete. v5.5 remains `IN_PROGRESS / NOT_ACCEPTED` because later M88-M94
qualification gates, final clean clone, remote SHA, Actions, and release
conditions remain pending. No model training or v5.6 work was performed.
