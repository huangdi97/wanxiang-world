# GOAL 00A — Repository & Toolchain Foundation

## Objective

Create a reproducible monorepo engineering base for Wanxiang with Python/TypeScript tooling, CI-ready quality commands, ledgers, documentation structure, deterministic test configuration and local developer startup. This Goal establishes no fake business functionality.

## Scope

- repository/workspace structure;
- Python 3.12 toolchain using `uv` unless an equivalent mature setup already exists;
- TypeScript/pnpm workspace foundation for future web/sdk code, without building product UI;
- pytest, Hypothesis, Ruff, Pyright;
- ESLint/TypeScript strict/Vitest baseline where TS workspace is initialized;
- Docker Compose baseline if compatible with environment, but local tests must not require Docker;
- configuration and `.env.example`;
- structured logging foundation;
- project ledgers and ADR structure;
- common scripts/Makefile/task runner equivalents for quality commands;
- Git hygiene and secret exclusions.

## Non-goals

- no world domain model beyond minimal smoke-test placeholder package importability;
- no FastAPI business endpoints;
- no database schema beyond tooling bootstrap if absolutely necessary;
- no React/Phaser UI;
- no LLM integration;
- no real world packs;
- no microservices/distributed messaging.

## Required reading

- v5 master spec: engineering architecture, recommended tech stack, code quality, immutable principles;
- `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`;
- `02_ENGINEERING_STANDARDS.md`;
- `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`;
- current git/repository state.

## Architecture constraints

- modular monolith;
- future `domain` must be framework-independent;
- local deterministic test loop must not require API keys or Docker;
- tooling/config should work from repository root;
- no production source file should be created merely as an empty placeholder to make a directory exist.

## Deliverables

Expected or equivalent structure:

```text
AGENTS.md
README.md
PLAN.md
STATUS.md
DECISIONS.md
BLOCKERS.md
KNOWN_FAILURES.md
CHANGELOG.md
pyproject.toml
pnpm-workspace.yaml
.env.example
apps/
packages/
docs/spec/
docs/architecture/
docs/decisions/
docs/runbook/
tests/
reports/
scripts/
```

Add `docs/runbook/DEVELOPMENT.md` with exact bootstrap and quality commands.

## Implementation tasks

1. Inventory repository and preserve useful existing setup.
2. Establish workspace/package names that align with Program Architecture.
3. Configure Python package discovery without circular editable-install hacks.
4. Configure Ruff and Pyright with meaningful strictness.
5. Configure pytest and Hypothesis profiles suitable for deterministic CI.
6. Configure TS strict baseline and root commands if TS is initialized.
7. Add repository-root quality command(s) that can run all applicable checks.
8. Add `.gitignore`, `.env.example`, and secret-safe configuration loading convention.
9. Add structured logging setup location and tests for configuration redaction if implemented now.
10. Create ledgers with initial program status; do not fill them with speculative tasks beyond current program.
11. Add ADR template.
12. Add acceptance report template.
13. Ensure source/test package naming is unambiguous and importable from clean environment.
14. Add CI workflow if repository policy permits; otherwise add CI-ready scripts and document why workflow is deferred.
15. Verify fresh environment bootstrap from documented commands as far as current environment permits.

## Tests

- test package imports;
- test root configuration loads with no secrets;
- test deterministic test seed/profile behavior where configured;
- run Ruff/Pyright/pytest;
- run TS lint/typecheck/test baseline if TS initialized;
- optional CI config validation.

## Acceptance criteria

PASS only if:
- documented root bootstrap works;
- Python quality checks pass;
- TS baseline checks pass if included;
- no API key needed;
- repository contains required ledgers/docs;
- no business placeholder is being counted as implemented functionality;
- quality commands have stable names used by later Goal files;
- `reports/goal_00A_report.md` contains commands and results.

## Failure / blocker handling

Fix internal setup failures. Do not mark missing optional external services as blockers. If Docker is unavailable locally, deterministic non-Docker tests must still pass and Docker validation may be documented separately.

## Documentation updates

- README getting started;
- development runbook;
- PLAN/STATUS/CHANGELOG;
- DECISIONS for tool substitutions.

## Git / checkpoint requirements

Create final local commit only after acceptance:

`goal 00A: establish reproducible engineering foundation`
