# M84 — First Real Chinese Book Requalification

Date: 2026-08-26  
Branch: `feature/source-to-living-world`  
Scope: requalification of the same private local Chinese TXT after the
semantic-distillation data-flow repair; no v5.5 and no model training.

## Decision

**ACCEPTED for the first-book Source → Living World product chain.**

The exact original private local source metadata matches the preserved
2026-08-25 report (`937,500` bytes and `323,815` UTF-8 characters). It was
read locally through the real product CLI and API/Studio routes, was not
edited, was not copied into Git, was not sent to an external model, and was
not used for training. The old
`reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md` remains unchanged as
the historical pre-repair `NOT_ACCEPTED` record.

Sanitized evidence is in
`artifacts/m79_m84/real_book_reacceptance_product_evidence.json`.

## Real CLI evidence

The public `scripts/wxworld.py reference` path used the same source file with
the book profile, local semantic provider, publish, instantiate, and
Worldness flags. It produced:

| Measure | Result |
|---|---:|
| Parsed nodes / segments | 3,918 / 3,918 |
| Bounded semantic batches / calls | 164 / 164 |
| Retries / stage errors | 0 / 0 |
| Candidate count | 11,549 |
| Measured coverage | 0.8333333333333334 |
| WorldPackage | `world:wd_m84_original_book_cli_rerun` |
| Preview | `preview://preview_1` |
| Publish | accepted |
| Worldness | passed, overall `0.9733333333333333` |
| Commit / Replay / Branch | committed / equal / isolated |

Coverage is measured by the normal draft/compiler path. No Candidate was
hand-filled and no coverage value was injected or hardcoded.

## Real API/Studio evidence

The same raw bytes were submitted through the normal `/studio/one-click`
route and then through the public lifecycle routes:

`one-click → build → preview → publish → worldness → enter → living`.

Every step was accepted. The resulting draft was `READY_TO_COMPILE` with
11,549 candidates, 0.8333333333333334 measured coverage, uncertainty 0.05,
2,764 entities, 1,091 relations, 405 places, and 27 draft events. All 11,549
candidates retained evidence locators. The Studio UI returned HTTP 200 and
exposed binary upload, Worldness, and Enter-Living controls.

Worldness gates were all true: previewable, publishable, and living-ready.
The Commit Authority record was committed and proposal-validated; replay was
equal and the branch probe was isolated.

## Boundaries

This clears the first-book product-chain blocker only. It does not claim
arbitrary Source inputs are 100% semantically correct. Provider output remains
Candidate/evidence material, review and uncertainty boundaries remain active,
and providers remain replaceable and optional. No canonical mutation authority
was granted to the local semantic provider.

The public historical GEDCOM qualification remains separate: it is real Family
product validation, not private living-family user validation. The explicit
privacy statement remains:

`PUBLIC HISTORICAL FAMILY E2E = REAL PRODUCT VALIDATION`  
`PRIVATE LIVING FAMILY USER VALIDATION = NOT PERFORMED`

