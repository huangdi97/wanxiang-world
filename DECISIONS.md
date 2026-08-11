# Decisions ? Wanxiang Engineering Program

ADRs live in `docs/decisions/` (`NNNN-slug.md`); this file is the index.

| ADR | Title | Status |
|---|---|---|
| 0001 | Toolchain and workspace layout (M0) | accepted |

## Decision log (inline quick notes)

- 2026-08-11: Repository begins as a fresh `git init` on `main`; the batch control
  documents shipped in the workspace are committed as the initial baseline, then
  Goal checkpoints follow the `goal <id>: ...` convention.
