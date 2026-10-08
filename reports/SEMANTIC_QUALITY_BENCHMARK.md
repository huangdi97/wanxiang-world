# M80 / G83 Semantic Quality Benchmark

Date: 2026-08-25
Scope: M79-M84 generalization; no model training; no private source content.

## Decision

`PASS` for the benchmark infrastructure and anonymized regression fixture.
The second private real-book path is now supplied and its product-chain
qualification is recorded in `reports/M79_REAL_EPUB_QUALIFICATION.md`. This
report still does not invent a human-labeled Gold Set or claim precision from
candidate count alone; the real run's structural/provenance evidence is
reported separately.

## Evidence

The benchmark uses a deterministic, stratified Gold Set sampler with seed 83
and explicit `random`, `high_impact`, `low_confidence`, `conflict_merge`, and
`fill` strata. The fixture contains no private book text and is independent of
the extractor implementation.

Artifact: `artifacts/m79_m84/semantic_quality_benchmark.json`

The current anonymized sample selected 9 labeled assertions. The measured
metrics all pass:

- identity precision: 1.0
- alias merge precision: 1.0
- false merge rate: 0.0
- duplicate rate: 0.0
- missing evidence rate: 0.0
- event precision: 1.0
- participant correctness: 1.0
- temporal ordering: 1.0
- uncertainty honesty: 1.0
- relation/place/org precision: 1.0
- knowledge boundary safety: 1.0
- evidence traceability: 1.0

The benchmark also checks source-reference matching, so an assertion cannot
pass traceability merely because its semantic value matches.

## Gates

The new integration test and the existing source-matrix/candidate regression
tests pass locally. The real source remains unmodified and outside Git. Any
future labeled Gold Set must be derived from that source without
source-specific logic or hand-filled candidates; the current M79 acceptance
does not substitute candidate count for that precision protocol.
