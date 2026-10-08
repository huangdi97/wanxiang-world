# G60A Report — World Compiler Boundary

## Status

**PASS** — Compiler input is a reviewed `WorldDraft` with an explicit draft
revision, exact source pins, and selected-domain version pins.

## Evidence

- `CompilerBoundary` rejects non-compilable lifecycle states, unresolved
  conflicts/rights, zero coverage, changed source versions, missing pins, and
  source-reference mismatches.
- `CompilerInput` rejects duplicate pins and revision mismatch.
- `tests/unit/substrate/test_compile_preview.py::test_m57_rejects_changed_source_pin`
  passes.

