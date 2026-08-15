# Known Failures ? Wanxiang Engineering Program

| Date | Goal | Failure | Root cause | Fix / status |
|---|---|---|---|---|
| 2026-08-14 | G29A | `ruff format --check` crashed (panic) on tests/architecture/test_v51_forensics.py | File stored with UTF-8 BOM; ruff annotation-range bug | Stripped BOM; fixed (pre-existing defect D1) |
| 2026-08-14 | G29A | `scripts/v51_metrics.py` failed pyright strict (18 errors) | v5.1 script lacked strict type annotations; v5.1 "pyright PASS" did not cover it | Added TypedDict + strict annotations (D2) |
| 2026-08-14 | G29A | Uncommitted v5.2 prep edit corrupted scripts/architecture_check.py + architecture_forensics.py (syntax error, lost observability/substrate guard entries, em-dash mojibake) | Over-wide deletion during stub-package removal | Rebuilt FORBIDDEN dicts = HEAD minus stub entries; em-dash restored (D3/D4) |
| 2026-08-14 | G29A | 140 tracked `.md` docs/reports carry UTF-8 BOM | Files written by earlier batches with BOM | Cosmetic; left untouched to avoid noise diff; py files normalized |
| 2026-08-14 | G29A | v5.1 stash@{0} (foreign V5.1 tracked artifacts pre-M16 cleanup) left in repo | v5.1 session stashed PACK_MANIFEST/baselines/typing tweaks | Reviewed, not restored; tree is intended v5.2 start state |
| 2026-08-15 | G38A | v5.2 M30-M34 not executed (M34 not complete) | Program state gap from prior v5.2 batch (stopped at G33A) | Completing G33B-G37G + M30-M34 gates before M35 freeze |
