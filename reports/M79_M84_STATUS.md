# M79-M84 Generalization and Stable Release Status

Date: 2026-08-25
Branch: `feature/source-to-living-world`
Scope: v5.4 continuation only; no v5.5 and no model training.

## Decision

`USER_INPUT_REQUIRED`. The M79-M84 package is not accepted and v5.4.0
stable is not authorized.

There is one blocker class: `USER_INPUT_REQUIRED`, with two required fields:

1. a private local path to an independent second real book;
2. a private local path to a real GEDCOM file.

No private source is copied into Git or modified. No Candidate is hand-filled,
coverage is not hardcoded, compiler or Worldness gates are not disabled, and no
source-specific book logic is used.

## Goal matrix

| Milestone | Goals | Status | Boundary |
|---|---|---|---|
| M79 | G82A-G82G | `USER_INPUT_REQUIRED` | second real-book path and real E2E are pending |
| M80 | G83A-G83H | `PASS` infrastructure only | anonymized benchmark passes; real second-book Gold Set is pending |
| M81 | G84A-G84F | `PASS` | synthetic adversarial calibration passes; real-source qualification remains pending |
| M82 | G85A-G85G | `USER_INPUT_REQUIRED` | GEDCOM path and real family validation are pending |
| M83 | G86A-G86G | `PASS` | synthetic structured/mixed path passes |
| M84 | G87A-G87H | `NOT_READY` | stable gate cannot open while M79/M82 are pending |

## Local engineering gate

The post-implementation gate is green for the available scope:

- `uv run ruff check .`: PASS
- `uv run ruff format --check .`: PASS
- `uv run pyright`: PASS, 0 errors
- `uv run pytest -q`: 1211 passed, 1 skipped, 2 warnings
- `uv run python scripts/architecture_check.py`: PASS
- `uv run python scripts/quality.py`: PASS

The single skipped test is the existing live PostgreSQL profile test because
no PostgreSQL instance is available in this environment. It is not converted
into a product pass claim.

## Remote delivery gate

The evidence-only feature commit is pushed and verified remotely:

- local HEAD and `origin/feature/source-to-living-world`: `82918be493721853821562ccb66f67eaa5bf657f`
- GitHub Actions run `32835309602`: all six required jobs succeeded
  (`python`, API/package/SDK, PostgreSQL, release-smoke, safety, and TS)
- no stable `v5.4.0` tag or GitHub stable Release was created

This remote green result closes the available engineering/delivery gate; it
does not turn the missing real-source inputs into M79/M82 acceptance.

## Independent evidence

- `reports/SEMANTIC_QUALITY_BENCHMARK.md`
- `reports/WORLDNESS_CALIBRATION.md`
- `reports/M83_STRUCTURED_MIXED_QUALIFICATION.md`
- `artifacts/m79_m84/semantic_quality_benchmark.json`
- `artifacts/m79_m84/worldness_calibration.json`
- `artifacts/m79_m84/structured_mixed_smoke.json`
- `scripts/m79_m84_checkpoint.py`

The next resumable checkpoints are `M79/G82A` and `M82/G85A`. Once the two
private paths are supplied, the same real product chain must produce and
verify WorldPackage, Preview, semantic quality, Worldness, Living Instance,
Commit/Replay, and the required M84 release evidence before any stable tag or
release is considered.
