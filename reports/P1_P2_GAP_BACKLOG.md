# P1/P2 Gap Backlog (G13I)

## P1 gaps (required for a trustworthy stable platform)
| ID | Title | Status | Closure evidence |
|---|---|---|---|
| P1-1 | OpenAPI/SDK vocabulary drift (documented ops did not exist on the server) | CLOSED (G13D) | server exports canonical contract; drift test regenerates + compares; TS SDK consumes the contract |
| P1-2 | Placeholder-guard blind spot (FIXME/NotImplemented/... unchecked) | CLOSED (G13D, upgraded to P0 during audit) | guard scans all markers; regression test covers every marker |
| P1-3 | Child-branch cold replay corruption | CLOSED (G13E, upgraded to P0 during audit) | replay seq/revision fix; cold cache + restore produce identical hash |

**P1 open count (required by stable platform): 0**

## P2 items (tracked, not required for M11-M17, do not invalidate design acceptance)
| ID | Item | Rationale | Owner | Review trigger |
|---|---|---|---|---|
| P2-1 | genealogy/gedcom.py complexity hotspot (max 25) | data-heavy parser; within size limit; fully tested | substrate genealogy | refactor when adding new GEDCOM features |
| P2-2 | spatial/resolver.py complexity hotspot (max 21) | many spatial action branches; within size limit; tested | substrate spatial | refactor on next spatial feature |
| P2-3 | heritage/iiif.py complexity hotspot (max 19) | external-format parser; tested; real IIIF EXTERNAL_BLOCKED | substrate heritage | refactor with real IIIF integration |
| P2-4 | material/query.py complexity hotspot (max 19) | query builder branches; tested | substrate material | refactor with custody feature growth |
| P2-5 | institution/query.py complexity hotspot (max 16) | permission/norm query branches; tested | substrate institution | refactor with rights features |
| P2-6 | 9 public `Any`-typed params in serialization/DB boundary | intentional boundary typing (JSON decode / SQLAlchemy conn); not domain escape hatches | domain/persistence | revisit if a typed schema-codec is introduced |
| P2-7 | best-effort `population.record_run` marker suppress | documented; run result returned regardless | population | revisit if record_run must be guaranteed |
