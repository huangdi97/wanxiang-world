# M79-M84 Generalization and Stable Release Status

Date: 2026-08-25
Branch: `feature/source-to-living-world`
Scope: v5.4 continuation only; no v5.5 and no model training.

## Decision

`M82 PASS / M84 ACTIVE`. M79, M80, M81, M82, and M83 are accepted within their
documented evidence boundaries. v5.4.0 stable remains unauthorized until the
M84 clean-clone, full-regression, source-safety, final-branch, tag, and
post-release gates pass.

The GEDCOM field has now been supplied and qualified. M82 uses a public
historical genealogy fixture for real product-chain evidence; it is not a
private living-family user-validation claim.

No private source is copied into Git or modified. No Candidate is hand-filled,
coverage is not hardcoded, compiler or Worldness gates are not disabled, and no
source-specific book logic is used.

## Goal matrix

| Milestone | Goals | Status | Boundary |
|---|---|---|---|
| M79 | G82A-G82G | `PASS` | private EPUB real E2E accepted; see `reports/M79_REAL_EPUB_QUALIFICATION.md` |
| M80 | G83A-G83H | `PASS` infrastructure only | anonymized benchmark passes; real second-book Gold Set is pending |
| M81 | G84A-G84F | `PASS` | synthetic adversarial calibration passes; real-source qualification remains pending |
| M82 | G85A-G85G | `PASS` | real GEDCOM product chain accepted; privacy/user-validation boundary explicit |
| M83 | G86A-G86G | `PASS` | synthetic structured/mixed path passes |
| M84 | G87A-G87H | `ACTIVE` | clean clone, full regression, source safety, delivery, stable tag, and post-release gates remain |

## Local engineering gate

The post-implementation gate is green for the available scope:

- `uv run ruff check .`: PASS
- `uv run ruff format --check .`: PASS
- `uv run pyright`: PASS, 0 errors
- `uv run pytest -q`: 1219 passed, 1 skipped, 2 warnings
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
- current remote tip `d9d136176b2df2b0bb4acaf30bb3ea876389ee9e` — run
  `32864182259`, all six required jobs succeeded

The current remote tip is verified green. The local implementation commit
`da8c21b3ae1811a14cfe132fd697c6089ed35526` and the remote tip have identical
trees; the remote Git Database commit uses the same parent, message, author,
and content with its timestamp normalized to UTC.

The six jobs in each listed run are `python`, API/package/SDK, PostgreSQL,
release-smoke, safety, and TS.

- no stable `v5.4.0` tag or GitHub stable Release was created

This remote green result closes the current engineering/delivery gate. The
M79-M84 package remains `USER_INPUT_REQUIRED` only because M82 still lacks a
private GEDCOM path; no stable tag or v5.5 work is authorized.

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

M82/G85A-G85G is now qualified in `reports/M82_GEDCOM_QUALIFICATION.md` with
the sanitized product evidence in `artifacts/m79_m84/real_gedcom_product_evidence.json`.
The same real product chain produced and verified the family WorldPackage,
Preview, Worldness, Living Instance, Commit/Replay, and branch-isolation
evidence. The next active checkpoint is M84/G87A.

The existing `v5.4.0-rc2` history is preserved. No stable tag has been
created by M82; v5.5 and model training remain out of scope.

## M82 checkpoint gate (2026-08-26)

The post-fix local gate is green: `uv run python scripts/quality.py` completed
Ruff check, format check, Pyright (`0 errors`), `1219 passed`, one existing
PostgreSQL-profile skip, two warnings, and the architecture guard. The
PostgreSQL skip is an external environment boundary, not a GEDCOM product
success claim.

## M84 final current truth (2026-08-26)
M84 G87A-G87E engineering evidence is PASS on the GitHub feature branch: the
final clean clone installed, migrated, bootstrapped, ran clean-room,
CLI/API/Studio, Python, and TypeScript gates; the required Actions run
`32879104870` is green across all six jobs. The cross-platform fixture repair
is committed and pushed.

G87F/G87G are **HELD**. The first real Chinese book remains `NOT_ACCEPTED` in
`reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md` with zero candidates
and zero coverage even in the rights-approved diagnostic. M79's accepted
second EPUB and M82's accepted public historical GEDCOM do not replace that
first-source acceptance. No stable tag or stable GitHub Release is authorized.
See `reports/M84_STABLE_BLOCKER.md`.
