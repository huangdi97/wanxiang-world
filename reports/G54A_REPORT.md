# G54A Report — Repository Truth Audit (M51)

## Status
**PASS** — v5.3-adjacent baseline audited against the CURRENT tree (not prior
claims). v5.3 M43-M50 was committed as planning material only (commit
`5e4edaa`, "not qualified"); this audit therefore certifies the real baseline
as the v5.2/M42 production baseline (tag `m42-v5.2-production`) plus the public
GitHub delivery (`v5.3.0-rc1` on CI-green `7b0674c`). M51-M70 execution starts
from this verified truth.

## Evidence (reproducible)
- `scripts/forge_truth_audit.py` — repeatable audit; writes
  `reports/forge_truth_audit.json`; exits 0 when hard invariants hold.
- `tests/architecture/test_forge_truth_audit.py` — 5 architecture tests.
- Verified live: ruff check PASS, ruff format PASS, pyright 0 errors,
  pytest 979 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED) + 3
  deselected (known Windows-sandbox `tmp_path` mode-0o700 ACL limitation;
  these run green on Linux CI), `scripts/architecture_check.py` PASS.

## Audit inventory (2026-08-16)
| Area | Count |
|---|---|
| Packages | application 7, domain 25, observability 5, persistence 10, research 12, runtime 12, substrate 257, sdk_ts (TS) |
| Apps | api 16 modules |
| Scripts | 34 |
| Test files | 225 |
| Reports | 384 .md |
| Tracked files | 1732 (923 .md, 611 .py, 26 .json) |

## Forge capability inventory (existing, real)
| Module | Files | Verdict |
|---|---|---|
| `sources/` (registry, gate, locator, identity, entity, canon, character, evidence, policy) | 13 | EXTEND |
| `compiler/` (readers text/md/json/yaml, validate, export) | 9 | EXTEND |
| `corpus/` (large-corpus pipeline) | 2 | EXTEND |
| `canon_graph/` (graphs, pipeline, timeline canon) | 4 | EXTEND |
| `semantic_world/` | 2 | EXTEND |
| `worldpack/` (assembler, package schema) | 2 | EXTEND |
| `living/` (full living runtime) | 2 | EXTEND |
| `genealogy/` (GEDCOM adapter) | 6 | EXTEND |
| `heritage/` (IIIF connector) | 6 | EXTEND |
| `studio_experience/` | 2 | EXTEND |
| `lineage/`, `release/` | 4+2 | KEEP |

## KEEP / EXTEND / MERGE / DELETE / ADD matrix
| Path | Verdict | Basis |
|---|---|---|
| packages/domain (Kernel: reality_root/commit/event/snapshot/worldline/lineage) | KEEP (frozen) | Kernel v1 freeze; kernel_guard 0 violations |
| packages/runtime (authority/replay/branch/state/invariants) | KEEP (frozen) | same |
| packages/substrate/sources (SourceRegistry/Gate/Locator/Identity/Entity/Canon) | EXTEND | Source→LivingWorld pipeline reuses these; extend to GEDCOM/CSV/DOCX/EPUB/text-PDF locators + CandidateEnvelope |
| packages/substrate/compiler | EXTEND | add EPUB/DOCX/text-PDF readers; OCR_REQUIRED honest path |
| packages/substrate/corpus | EXTEND | checkpoint/resume/idempotency for large sources |
| packages/substrate/genealogy (GEDCOM) | EXTEND | register through SourceRegistry + locators |
| packages/substrate/worldpack | EXTEND | WorldPackageDraft + preview scope |
| packages/substrate/living + rc001 | EXTEND | preview instantiate + worldness evaluator |
| packages/research (planner/ai_compiler/flags) | KEEP (EXPERIMENTAL, no API key) | Provider boundary only; never Commit |
| apps/api | EXTEND | Creation/Review/CLI use cases behind existing transport |
| migrations | EXTEND | additive tables for jobs/checkpoints (Kernel tables untouched) |
| .github/workflows/ci.yml | EXTEND | source-fixture + e2e jobs at M70 |
| reports/ + docs/ | EXTEND | per-goal reports + acceptance matrix |

## DELETE / avoid
- No duplicate registry/job/candidate/review/package abstraction introduced;
  G54D cleans duplicates found.
- No second Canonical State / Commit pipeline / Package Registry.
- Real《红楼梦》text, family private data, tokens, DBs stay out of Git (verified:
  `sources/red_chamber` = README + MANIFEST_TEMPLATE only; no forbidden tracked
  files; `data/wanxiang.db` untracked).

## Backward compatibility
- No Kernel change; no schema/migration change in this Goal; public API
  surface unchanged (17 routes).

## Local commit
- `g54a: Repository truth audit (M51)`
