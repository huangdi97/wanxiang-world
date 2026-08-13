# Goal G04C Acceptance Report

## Status
PASS

## Pre-goal state
- branch: master
- commit: 02f8b3b (G04B checkpoint)
- working-tree notes: clean before G04C work

## Objective
Implement a deterministic structured compiler MVP with safe readers for
TXT/MD/JSON/YAML, provenance-bound candidates, schema validation and explicit
non-goal guards (PDF/OCR unsupported, not faked).

## Delivered
- `wanxiang_substrate.compiler`: CompilerJob/stage contracts (CompileResult,
  CompileDiagnostic, CandidateObject, SourceOffset), safe readers (json strict,
  restricted YAML subset, markdown explicit sections, text facts), deterministic
  StructuredCompiler pipeline with validation and stable result hash, review
  export, synthetic fixtures (json/yaml/markdown/text/pdf/malformed/oversized).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run python scripts/quality.py` (full gate) | 293 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests (`tests/integration/test_structured_compiler.py`, 10 tests):
- unit: json source -> entity candidate;
- unit: yaml source -> entity candidate (restricted subset);
- unit: markdown explicit-markup -> entity candidate;
- unit: text -> fact candidate;
- golden: same inputs/compiler version -> same result hash;
- negative: malformed JSON fails safely (read_failed);
- negative: oversized source fails safely;
- non-goal: PDF explicitly unsupported (no fake extraction, no candidates);
- provenance: every candidate has source refs and provenance;
- unit: review export carries version/hash/diagnostics.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | guard + review |
| Goal + regression tests PASS | PASS | 293 tests incl. M1-M3/G04A-B |
| Lint/type/architecture PASS | PASS | full quality gate |
| Golden determinism | PASS | stable result hash test |
| Negative/unsupported fail safely | PASS | malformed/oversized/pdf tests |
| Provenance on every candidate | PASS | provenance test |
| No new forbidden dependency | PASS | architecture guard |

## Key decisions
- Restricted YAML subset parser (no anchors/tags/flow); explicit-markup
  markdown; PDF/OCR/video explicitly unsupported (ADR-0027).

## Known limitations
- YAML subset is deliberately restricted; full YAML is out of scope for MVP.

## External blockers
None.

## Final checkpoint
- commit: `goal g04c: structured compiler mvp`