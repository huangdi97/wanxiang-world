# M36 Full Corpus Qualification

## Status
PASS (mechanism) — full-corpus -> canon-graph pipeline qualified on synthetic
corpora; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
- `canon_graph` package: SceneCandidate/detect_scenes, CharacterGraph,
  SourceGraph, TimelineGraph, CanonGraph (editions + contradictions),
  CoverageReport, FullCorpusPipeline (resume/retry).
- Tests: `uv run pytest tests/unit/substrate/test_canon_graph.py -q` -> 8 passed.
- M36 gate: full quality 946 passed + 1 skipped; architecture PASS after
  canon_graph size split; SDK baseline py=1118.

## Coverage evidence
- Source segments -> scenes -> character/source/timeline/canon graphs,
  deterministic; contradictory claims preserved; edition views isolated.
- Coverage report: source->claim traceability + resume/retry counts.

## Boundary
Real-corpus coverage requires a legal, traceable edition (BLOCKERS.md G35A).
