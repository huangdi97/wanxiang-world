# v5.5 Real-Book Evidence Lineage

Date: 2026-08-27

This lineage reconciles two records for the same private local source without
rewriting either record.

## Qualification lineage selector

The source qualification records are ordered by their qualification date. The
latest authoritative qualification is the newest accepted qualification, not
the oldest protected report:

| Qualification id | Date | Status | Authority role |
|---|---|---|---|
| `historical_pre_repair` | 2026-08-25 | `NOT_ACCEPTED` | historical protected record |
| `current_first_book_qualification` | 2026-08-26 | `ACCEPTED` | latest authoritative qualification |

The later v5.4.0 stable release is a release event based on
`current_first_book_qualification`; it is not a replacement source
qualification. The machine selector is recorded in
`reports/G97I_FINAL_EVIDENCE.json` under `qualification_lineage`.
The selected `latest_authoritative_qualification` is
`current_first_book_qualification`; selection is by the greatest
`qualified_at` value among source qualifications.

| Record | Source identity | Result | Role |
|---|---|---|---|
| 2026-08-25 acceptance report | 937,500 bytes; 323,815 UTF-8 characters; private local text | `NOT_ACCEPTED`; rights diagnostic produced 0 candidates and coverage 0 | Historical pre-repair evidence, preserved unchanged |
| M84 first-book requalification | Same 937,500-byte / 323,815-character source; local read only | `ACCEPTED`; 3,918 parsed nodes/segments, 11,549 candidates, measured coverage 0.8333333333333334, Worldness 0.9733333333333333 | Current Source → Living World product-chain evidence |

The current record used the real CLI and API/Studio chains, producing a
WorldPackage, Preview, published package, Worldness result, Living Instance,
Commit/Replay and branch-isolation evidence. The private source was not
modified, copied to a public export, uploaded to an external model, or used
for training.

Machine evidence:

- `reports/M84_FIRST_BOOK_REQUALIFICATION.md`
- `artifacts/m79_m84/real_book_reacceptance_product_evidence.json`
- `artifacts/m79_m84/m84_post_release_verification.json`

Historical immutability checksums:

- `reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md`:
  `8E976B210E96EA1369A05E3D5EA6410DBEB6F39F8E55A4460197365818FA7B73`
- `reports/M84_FIRST_BOOK_REQUALIFICATION.md`:
  `A94E3339FB180A9E93EAD9284B2951B23856057B59E1A1FC128564F27444C22C`
- `artifacts/m79_m84/real_book_reacceptance_product_evidence.json`:
  `C166E69967D8B419DF6E141E184EB9227BB9AAF126BFAC1CD48EF47BDAE6930A`
