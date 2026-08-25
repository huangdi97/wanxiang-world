# M82 G85A-G85G — Real GEDCOM Family World Qualification

Date: 2026-08-26
Branch: `feature/source-to-living-world`
Scope: supplied local GEDCOM product qualification only; no v5.5 and no model
training.

## Decision

**ACCEPTED for M82.** The supplied local GEDCOM completed the same real
Source -> Candidate -> WorldDraft -> WorldPackage -> Preview -> Worldness ->
Living Instance chain through the product CLI and the API/Studio routes. The
original 2026-08-25 Real Book `NOT_ACCEPTED` report remains unchanged as
historical evidence of the earlier Chinese-book zero-candidate failure; this
qualification does not alter that source or its evidence.

The source path, content digest, and raw GEDCOM are absent from this report,
the artifacts, and Git. The source was read from the caller's private local
file, was not edited or copied into the repository, was not sent to an
external model, and was not used for training. The supplied file is a public
historical genealogy fixture and is not an authoritative Bronte research or
private living-family validation source.

Sanitized product evidence is recorded in
`artifacts/m79_m84/real_gedcom_product_evidence.json`.

## G85A — Private GEDCOM source gate

The metadata-only checkpoint reports `READY_TO_RESUME`: the GEDCOM is an
external regular file, outside the repository, and unchanged. The product
request used `stage=E3`, approved private analysis and package inclusion, and
explicitly disabled external model processing, public export, and training.
The checkpoint contains no path, digest, or source bytes.

The real product run read 2,897 bytes locally. The source gate and rights
metadata were passed through the normal SourceRegistry/AuthoringService path;
no internal authoring helper replaced the CLI/API product path.

## G85B — Generic GEDCOM to family candidates

The normalized GEDCOM parser observed version `5.5`, 14 individuals, 4
families, and zero embedded `SOUR` records. The semantic provider was the
bounded local `local_semantic_v1` provider, and its output remained
Candidate-only. The run produced 326 candidates from 19 parsed nodes and one
bounded batch:

| Product measure | Result |
|---|---:|
| Candidate count | 326 |
| Draft entities / relations | 19 / 79 |
| Draft events / places | 55 / 7 |
| Family organization candidates | 8 |
| XREF-scoped identity candidates | 28 |
| Claim candidates | 42 |
| Birth / marriage / death event candidates | present |
| Parent / spouse relation candidates | present |
| Candidates with source refs | 326 |
| Candidates with evidence refs | 326 |
| Uninvented residence/migration/education/occupation candidates | 0 |

Birth, marriage, and death facts, family membership, kinship, places, date
precision, and claims were extracted generically. Residence, migration, and
embedded source records are absent from this fixture; the pipeline preserved
that absence instead of inventing facts. Same-name people remain distinct by
source-scoped GEDCOM XREF, not by display name.

Date precision was retained (`day=93`, `year=23`, `approximate=4`,
`text=4`), with 31 uncertain and 93 exact-date candidates in the sanitized
candidate-level audit. No date was promoted from traversal order.

The official GEDCOM 7 regression smoke also passed against the official
`maximal70-tree1.ged` sample fetched in memory: schema `7.0`, 4 individuals,
2 families, 2 sources, 9 record locators, and 46 evidence-backed candidates.
Its sanitized result is in `artifacts/m79_m84/gedcom7_official_smoke.json`.

## G85C — Claim and conflict preservation

The real fixture produced `conflict_count=0`; no conflict was fabricated. The
generic candidate path retains source/evidence provenance and does not
last-write-wins merge claims. The existing conflict, provenance, and family
portal regression contracts passed together with the new GEDCOM semantics:
`26 passed`, including conflicting-claim preservation, source-rights gates,
family privacy, and creative-legacy restrictions.

Any future conflicting life-event claims therefore remain reviewable
Candidate/evidence material until the existing review and Commit Authority
boundaries are satisfied; they do not become Canon merely because they came
from GEDCOM input.

## G85D — Consent, privacy, and legacy boundary

The real run carried private access, approved analysis, package inclusion,
`public_export=false`, `training=false`, and no external model processing.
Living-person consent, viewer-specific projection, revocation, posthumous
policy, and biometric/voice-likeness restrictions remain enforced by the
existing genealogy privacy contracts and passed in the regression set.

This historical fixture does not constitute private living-person consent or
user validation. No such claim is made, and no living-person likeness asset
was generated.

## G85E — Family WorldDraft, Package, and Preview

The normal family profile selected `family` and `spatial` domains. The
WorldDraft was `READY_TO_COMPILE`, measured coverage was `1.0`, uncertainty
was `0.05`, and `completion_items` was empty. The normal compiler produced a
WorldPackage with a manifest hash and a Preview; the publish gate accepted the
package.

| Product artifact/gate | Evidence |
|---|---|
| API/Studio one-click | accepted |
| WorldDraft | `READY_TO_COMPILE`, 326 candidates |
| WorldPackage | `world:wd_m82_real_gedcom_api_final` |
| Preview | `preview_1` |
| Publish | accepted |
| Studio route surface | HTTP 200; upload, Worldness, and living controls present |

The CLI was also run against the same local GEDCOM with the family profile,
local semantic provider, publish, instantiate, and Worldness flags; it
returned success with the same package/preview/living gate results.

## G85F — Family Living World

Worldness passed with overall score `0.99`; `previewable`, `publishable`, and
`living_ready` were all true. The living record exposed 19 entities and 79
relations. The Commit Authority proof recorded a committed action, validated
proposal, replay equality, event head `99`, and isolated branch state.

This demonstrates the timeline/person/place/life-event/evidence path for the
facts present in the fixture. Since the fixture contains no migration facts,
no migration event is claimed. The branch proof confirms that the runtime
branch did not mutate the source/evidence history.

## G85G — M82 qualification

M82 is accepted. The same Kernel, Forge, compiler, package/preview boundary,
Commit Authority, replay engine, and Living Runtime handled the real GEDCOM
input. No LLM key or external model was required, and no provider was granted
canonical mutation authority.

The complete local engineering gate then passed with Ruff, format, Pyright,
architecture, and `1219 passed` tests; one existing live PostgreSQL profile
was skipped because no PostgreSQL instance was available, and two non-product
warnings were emitted.

## Reproducibility and evidence commands

The qualification runner is `scripts/m82_real_gedcom_product_evidence.py`.
It submits the source through the public `/studio` routes, then calls build,
preview, publish, Worldness, enter-living, and living-status routes. The
official-schema smoke runner is `scripts/gedcom7_official_smoke.py`; it fetches
the official sample into memory only and does not vendor it or run it through
the living-world chain.

The original failure report remains the source-of-truth record for the
earlier real-book failure:
`reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md`.
