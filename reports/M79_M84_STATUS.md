# M79-M84 Generalization and Stable Release Status

Date: 2026-08-25
Branch: `feature/source-to-living-world`
Scope: v5.4 continuation only; no v5.5 and no model training.

## Decision

`USER_INPUT_REQUIRED`. The M79-M84 package is not accepted and v5.4.0
stable is not authorized.

There is one remaining blocker class: `USER_INPUT_REQUIRED`, with one required
field: a private local path to a real GEDCOM file. The second-book field has
been supplied and M79 is accepted.

No private source is copied into Git or modified. No Candidate is hand-filled,
coverage is not hardcoded, compiler or Worldness gates are not disabled, and no
source-specific book logic is used.

## Goal matrix

| Milestone | Goals | Status | Boundary |
|---|---|---|---|
| M79 | G82A-G82G | `PASS` | private EPUB real E2E accepted; see `reports/M79_REAL_EPUB_QUALIFICATION.md` |
| M80 | G83A-G83H | `PASS` infrastructure only | anonymized benchmark passes; real second-book Gold Set is pending |
| M81 | G84A-G84F | `PASS` | synthetic adversarial calibration passes; real-source qualification remains pending |
| M82 | G85A-G85G | `USER_INPUT_REQUIRED` | GEDCOM path and real family validation are pending |
| M83 | G86A-G86G | `PASS` | synthetic structured/mixed path passes |
| M84 | G87A-G87H | `NOT_READY` | stable gate cannot open while M82 is pending |

## Local engineering gate

The post-implementation gate is green for the available scope:

- `uv run ruff check .`: PASS
- `uv run ruff format --check .`: PASS
- `uv run pyright`: PASS, 0 errors
- `uv run pytest -q`: 1216 passed, 1 skipped, 2 warnings
- `uv run python scripts/architecture_check.py`: PASS
- `uv run python scripts/quality.py`: PASS after the temporary pytest ACL
  directory was removed

The single skipped test is the existing live PostgreSQL profile test because
no PostgreSQL instance is available in this environment. It is not converted
into a product pass claim.

## Remote delivery gate

The implementation and evidence-only commit chain is pushed and verified
remotely:

- implementation commit `82918be493721853821562ccb66f67eaa5bf657f` — run
  `32835309602`, all six required jobs succeeded
- evidence commit `ef8a97292b6ab52ded9e2d0af69af333d75e668e` — run
  `32837328145`, all six required jobs succeeded
- alignment commit `19e3614a79a9f3e8955f11cc31bae69992291fd3` — run
  `32837871213`, all six required jobs succeeded

These are historical delivery checkpoints; the current branch tip and its
post-update Actions run must still be checked after any further report-only
commit.

The six jobs in each listed run are `python`, API/package/SDK, PostgreSQL,
release-smoke, safety, and TS.

- no stable `v5.4.0` tag or GitHub stable Release was created

This remote green result closes the historical engineering/delivery gate; the
current branch tip and its post-update Actions run still require verification.

## Independent evidence

- `reports/SEMANTIC_QUALITY_BENCHMARK.md`
- `reports/WORLDNESS_CALIBRATION.md`
- `reports/M83_STRUCTURED_MIXED_QUALIFICATION.md`
- `artifacts/m79_m84/semantic_quality_benchmark.json`
- `artifacts/m79_m84/worldness_calibration.json`
- `artifacts/m79_m84/structured_mixed_smoke.json`
- `scripts/m79_m84_checkpoint.py`
- `reports/M79_REAL_EPUB_QUALIFICATION.md`
- `artifacts/m79_m84/real_second_book_product_evidence.json`

The resumable checkpoint now validates supplied paths using metadata only:
each source must be an existing regular file outside the repository. The EPUB
source is ready; the GEDCOM field remains missing. The source contents are
never opened or copied by this checkpoint gate.

The next resumable checkpoint is `M82/G85A`. The same real product chain must
produce and verify the family WorldPackage, Preview, Worldness, Living
Instance, Commit/Replay, and the required M84 release evidence before any
stable tag or release is considered.
