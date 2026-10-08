# G89H — M86 Character Continuity Qualification

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Real qualification chain

The integration qualification used a book-profile `OneClickAuthoring` run to
create a source-derived WorldPackage, registered that package through the
shared `PlayableService`, entered two owned characters, and exercised actual
leave/Continue on Alice's runtime instance. The package contained at least two
runtime entities and the instance refs were the generated `prv_*` preview
instances; no hand-filled world candidate or canonical state was supplied.

The accelerated actor qualification then ran seven days at 24 ticks/day over
the real package ref and both runtime instance refs. Each day produced an
actor-local observation memory, a Belief revision, a bounded Goal revision,
an Action/why-reference record, and a Relationship revision. The checkpoint
was replayed from the same seed and rebuilt across the leave/re-enter boundary.

Derived evidence counts are 7 days, 2 actors, 14 memories, 14 belief
revisions, 16 goal revisions (creation plus daily reprioritization), and 7
relationship revisions. Replay digest equality and leave/re-enter digest
equality are computed from the checkpoint payload, not asserted as constants.

## Gates

| Gate | Result |
|---|---|
| Source-created literary WorldPackage | PASS |
| Multiple actor entry | PASS; Alice and Bob |
| Actual PlayableService leave/Continue | PASS; same Alice instance |
| Seven-day accelerated actor continuity | PASS; 7 × 24 ticks |
| Goal / Memory / Belief / Relationship persistence | PASS; derived counts above |
| Replay equality | PASS; computed digest equality |
| Leave/re-enter equality | PASS; computed checkpoint digest equality |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| G89H integration qualification | PASS; 1 passed, 1 expected Hypothesis warning |

M86 Gate 11 (`7-day actor continuity`) is **ACCEPTED** in
`reports/V55_ACCEPTANCE_MATRIX.md`. M86 is complete. v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**; execution continues at M87 / G90A.
