# GOAL 00B — Architecture Guards & Engineering Constitution

## Objective

Convert Wanxiang architectural rules into automated repository constraints so future Goals cannot silently create framework leakage, authority bypass or maintainability decay.

## Scope

- import/dependency conformance tests;
- code-structure quality checks;
- prohibited dependency rules;
- file-size reporting/guard policy;
- generic dumping-ground detection policy/review script where practical;
- test taxonomy folders/markers;
- acceptance matrix bootstrap;
- contribution/AGENTS instructions for Codex.

## Non-goals

- do not implement canonical world behavior;
- do not invent a complex custom static-analysis framework;
- do not enforce arbitrary complexity numbers that create busywork;
- no microservice boundaries.

## Required reading

Program Architecture and Engineering Standards in full.

## Architecture constraints

The guard mechanism itself must be simple, local and maintainable. Prefer existing import-linter rules or small tests/scripts over a bespoke compiler.

## Deliverables

1. automated checks preventing critical forbidden imports;
2. documented dependency diagram;
3. `docs/architecture/MODULE_BOUNDARIES.md`;
4. `reports/ACCEPTANCE_MATRIX.md` initialized with M0/M1 requirements;
5. `AGENTS.md` updated with non-negotiable coding/authority rules;
6. normal quality command includes architecture conformance.

## Implementation tasks

1. Define current physical packages and legal dependency direction.
2. Add tests/rules that fail if `domain` imports FastAPI/SQLAlchemy/Alembic/app modules.
3. Add rules preventing runtime/core from importing transport apps.
4. Add future-facing guards/comments for plugins/model providers not accessing persistence internals directly.
5. Implement a simple production file-size report. Default target <=300 lines; report/explain exceptions rather than blindly failing generated files.
6. Add import-cycle detection through tooling or test.
7. Add repository search/check preventing committed secrets and clearly dangerous placeholder markers in required production paths, while not banning legitimate words in docs/tests.
8. Define test markers/folders: unit, property, contract, integration, architecture, migration, e2e.
9. Add acceptance evidence schema/template validation if practical.
10. Add a deliberate small test fixture proving the architecture guard actually fails on a forbidden dependency, or test the rule implementation directly.

## Tests

- architecture rule positive tests;
- architecture rule deliberate negative fixture;
- import cycle check;
- file-size report execution;
- full quality suite.

## Acceptance criteria

- critical layer violations are machine-detectable;
- quality command fails on a controlled forbidden-import fixture/test case;
- architecture docs match actual package tree;
- no large custom framework was added merely for policy enforcement;
- M0 acceptance matrix entries have evidence;
- M0 can be declared PASS after 00A+00B.

## Failure / blocker handling

Architecture conflicts in existing code are internal issues: refactor or document an explicit ADR only when the master architecture permits it.

## Documentation updates

- AGENTS;
- MODULE_BOUNDARIES;
- DECISIONS;
- acceptance matrix;
- M0 acceptance report.

## Git / checkpoint requirements

`goal 00B: enforce architecture and quality boundaries`
