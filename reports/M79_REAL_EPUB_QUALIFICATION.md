# M79 G82A-G82G — Second Real Book Qualification

Date: 2026-08-25
Branch: `feature/source-to-living-world`
Scope: private second real book only; no v5.5 and no model training.

## Decision

**ACCEPTED for M79.** The second private local source completed the same
Source → Candidate → WorldDraft → WorldPackage → Preview → Worldness → Living
Instance chain through the product CLI and API/Studio surfaces. The original
2026-08-25 `NOT_ACCEPTED` report remains unchanged as historical evidence of
the first source's pre-repair zero-candidate failure.

The source path, raw fingerprint, and source text are intentionally absent
from this public report and from Git. Sanitized evidence is in
`artifacts/m79_m84/real_second_book_product_evidence.json`.

## G82A — Source Gate and rights boundary

- Input format: EPUB; raw bytes read locally: `2,919,697`.
- The source is an external regular private file. It was not edited, copied to
  the repository, uploaded to an external model, or used for training.
- The run used `stage=E3` with package inclusion approved for this local
  qualification. Private analysis was allowed; external model processing,
  public export, and training were false.
- The configured provider was the bounded private-safe local semantic
  provider. Provider output remained Candidate-only; it had no Commit
  Authority.

## G82B — EPUB structure and locator generalization

The generic EPUB adapter handled the package container, OPF manifest/spine,
both namespaced and unnamespaced EPUB 2/3 XML, and XHTML text extraction. The
real run observed 472 spine itemrefs and produced 28,510 parsed nodes/segments:

| Structure/evidence | Result |
|---|---:|
| Chapter segments | 475 |
| Section segments | 0 |
| Paragraph segments | 28,035 |
| Segments carrying spine/href locator data | 28,510 |
| Candidate source refs non-empty | 25,315 |
| Candidate evidence refs non-empty | 24,664 |

The locator path is generic `epub://…#…/spine=…;href=…`, with line detail
for extracted paragraph nodes. No title, author, or cultivation-domain logic
was added.

## G82C — Semantic distillation

The existing `SemanticDistillationService` ran 1,188 bounded batches of 24
segments. All 1,188 calls completed, with zero retries and zero stage errors.
The fused result contained 25,315 provenance-bound candidates:

| Kind | Count |
|---|---:|
| identity | 8,605 |
| character | 8,605 |
| event | 3,968 |
| time | 1,217 |
| place | 1,158 |
| relation | 1,182 |
| rule | 572 |
| organization | 8 |

The provider IDs recorded by the product path were `deterministic` and
`local_semantic_v1`; every candidate retained source and evidence locators.
Coverage was measured as `0.8333333333333334`, not injected or hardcoded.

## G82D — Cross-chapter identity evidence

The run recorded 4,785 identity keys with locator provenance, including 789
keys observed across more than one EPUB spine. Fusion retained source-backed
candidate evidence and did not write an automatic identity merge into Canon.
Cross-chapter alignment therefore remains a reversible Forge suggestion. No
human-labeled alias precision number is claimed here; that belongs to the
separate M80 Gold Set protocol and is not replaced by candidate count.

## G82E — Event, time, place, relation, organization, and object boundary

Events, time uncertainty, places, relations, and organizations were all
observed in the semantic result. Unknown dates remained unknown rather than
being fabricated, and event candidates retained their source locators; source
traversal order was not promoted as chronological truth. The object channel
produced zero candidates for this source, so no object was invented. Worldness
measured `object_persistence=1.0` with `required=false`, preserving that
missingness honestly.

## G82F — Product and runtime evidence

The same private raw bytes were used for the formal CLI and for an API request
through `POST /studio/one-click` with binary `content_base64` transport. The
route-level Studio UI returned HTTP 200 and exposed binary upload, Worldness,
and Enter-Living-World controls.

| Gate | Result |
|---|---|
| CLI WorldPackage | present |
| CLI Preview | present |
| CLI publish | accepted |
| API one-click/build/preview/publish | accepted |
| Worldness | passed; overall `0.9733333333333333`; all gates true |
| Living Instance / perception | accepted; 4,786 entities and 1,182 relations |
| Commit Authority action | committed and proposal-validated |
| Replay | equal |
| Branch isolation | true |
| Bounded repair | converged; zero repair candidates |

The full sanitized CLI/API/Studio evidence is stored in
`artifacts/m79_m84/real_second_book_product_evidence.json`; it contains no
private path, raw digest, or source excerpt.

## G82G — Qualification boundary

M79 is accepted. M82 still has no user-supplied private GEDCOM, so the overall
M79–M84 package remains `USER_INPUT_REQUIRED`; no stable `v5.4.0` tag or
release is authorized. The only remaining user-input blocker is the real
GEDCOM path at `M82/G85A`. Existing `v5.4.0-rc2` history is preserved; no new
release tag is created by this qualification.
