# Goal G20B Acceptance Report ? Clean-room Build, Install, Upgrade, Restore & Replay Certification

## Status
PASS

## Objective
Certify reproducibility from a clean environment: build artifacts, deploy private/staging profile,
migrate/restore, install external pack, instantiate reference world and replay history.

## Delivered
- `scripts/clean_room_certify.py` ? automated clean-room certification (7 steps) writing
  `reports/CLEAN_ROOM_CERTIFICATION.md`.
- `tests/integration/test_g20b_clean_room.py` ? 5 certification regression tests.
- `reports/CLEAN_ROOM_CERTIFICATION.md`, `reports/G20B_REPORT.md`.
- `.gitignore`: added `.cache/` (sandbox cache artifact guard).

## Findings (all PASS)
- Clean tree: 0 tracked modifications; no cache/scratch artifacts (93 untracked docs are the
  documented out-of-scope V5.1 pack, not developer caches).
- Release manifest: version 0.1.0, reproducible release_hash, git_sha == HEAD,
  migration head 0002_add_event_seq_index.
- Migration upgrade: 0001_initial -> 0002_add_event_seq_index on a fresh DB.
- Golden history replay: semantic hash matches the committed fixture.
- Backup/restore round-trip: 5 events backed up -> restored -> replay hash preserved.
- External sample pack: wxpack scaffold + validate with no errors.
- Reference world: synthetic_full conformance PASS, installed, instantiated (1 event).

## Decision
Clean-room certification PASS. No hidden local path dependency; all flows run from repository
artifacts and documented scripts.

## Evidence
- `uv run python scripts/clean_room_certify.py` -> exit 0, all 7 steps PASS.
- `uv run pytest tests/integration/test_g20b_clean_room.py -q` -> 5 passed.
- Full M17 gate green (628+ pytest, ruff/pyright/architecture PASS).

## Final checkpoint
- commit: `g20b: clean-room build, install, upgrade, restore & replay certification`
