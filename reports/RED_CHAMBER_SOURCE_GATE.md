# Red Chamber Full Source Gate (G35A)

## Status
**EXTERNAL_BLOCKED** — real《红楼梦》full-text source acquisition

## What was checked (evidence)
1. Workspace scan for an existing legal/traceable text: `sources/red_chamber/`
   contains only `README.md` + `MANIFEST_TEMPLATE.yaml` (templates); no
   full-text corpus is present anywhere in the repository.
2. Environment: sandbox is read-only and network-restricted; no capability to
   fetch and legally verify a public-domain edition (rights/edition/checksum
   cannot be certified).
3. Prior M15 record (`reports/RED_CHAMBER_REFERENCE_QUALIFICATION.md`) already
   documented the same EXTERNAL_BLOCKED: no approved/rights-cleared Red Chamber
   source corpus in this environment.

## Missing needs (exact, not fabricated)
- An approved public-domain (or rights-cleared) full-text edition of《红楼梦》
  with: source URI/file, sha256 checksum, edition/version note, rights grant
  (owner + usage + approval), review status.
- That corpus registered as versioned literary SourceRecords with provenance.

## What IS implemented and verified locally (PASS — mechanism only)
- Source registration mechanism: deterministic sha256 checksum, RightsEnvelope
  (owner/usage/approved/reviewer), ReviewStage E0-E5, canonical eligibility,
  SourceRecord immutability.
- Tests `tests/unit/substrate/test_red_chamber_source_registration.py` (3):
  checksum reproducible; rights/review_status non-empty for registration;
  no model-memory canon fabricated (sources dir holds templates only).
- No real《红楼梦》canon was created from model memory; Completion/Generated
  content is never promoted to E0/Canon without evidence.

## How to unblock
1. Place a rights-cleared full text under `sources/red_chamber/` with
   provenance (URI, checksum, edition, rights note).
2. Register it as SourceRecords (E0 -> E1 rights -> E2 review -> E3 approved).
3. Run through the Source Gate + Completion Ledger; then compile the full
   corpus (M36) and semantic world (M37).
