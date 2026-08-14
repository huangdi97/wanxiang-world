# Red Chamber Reference Qualification (G15H)

## Status
Generic capability PASS; real-data slice **EXTERNAL_BLOCKED** (no approved literary sources in the repository).

## Scope (mother-spec minimal slice, not the whole novel)
Source-gated literary slice: character/world packages, schedules, etiquette/duties, objects/messages,
takeover, branch comparison and a seven-day scenario — using ONLY approved source material with explicit
canon/completion/model provenance.

## Source-gate audit
| Check | Result |
|---|---|
| Approved synthetic fixture compiles as canonical (provenance fixture:approved) | PASS |
| Rights-denied source cannot compile as canonical (RightsDenied) | PASS |
| Unapproved-stage source cannot compile as canonical (SourceNotApproved) | PASS |
| Canon / source_backed / model_inference labels remain distinct in the ledger | PASS |
| Promotion requires review + evidence; provenance (source_refs) retained through canon | PASS |

## EXTERNAL_BLOCKED (exact missing needs)
- Approved public-domain Red Chamber source text with a documented rights grant (owner + usage + approval),
  registered as versioned literary SourceRecords with content hashes and provenance.
- Without that corpus, no canon is fabricated from model memory; the generic compiler/source-gate/ledger
  capability is complete and tested with synthetic provenance.

## Evidence
- `uv run pytest tests/integration/test_g15h_red_chamber.py -q` -> 3 passed.
