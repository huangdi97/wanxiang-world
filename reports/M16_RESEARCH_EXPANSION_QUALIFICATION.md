# M16 Research Expansion Qualification

## Scope
Ten research tracks (G19A-G19J) executed behind OFF-by-default feature flags in the isolated
`wanxiang_research` namespace; no research code ever gains Commit Authority.

## Track decisions
| Track | Goal | Module / evidence | Decision |
|---|---|---|---|
| Research namespace/flags/benchmarks | G19A | flags.py, results.py, M16_RESEARCH_BASELINE.md | KEEP_EXPERIMENTAL (infrastructure) |
| AI-assisted world compiler extraction | G19B | ai_compiler.py | KEEP_EXPERIMENTAL (real LLM EXTERNAL_BLOCKED) |
| Long-horizon persona memory & drift | G19C | persona_memory.py | KEEP_EXPERIMENTAL |
| Cognitive LOD / population scheduling | G19D | cognitive_lod.py | KEEP_EXPERIMENTAL |
| World-model / planner proposals | G19E | planner.py | KEEP_EXPERIMENTAL (learned provider EXTERNAL_BLOCKED) |
| Generative asset/scene pipeline | G19F | generative_assets.py | KEEP_EXPERIMENTAL (real generators/renderers EXTERNAL_BLOCKED) |
| Digital human / XR presence | G19G | digital_human.py | KEEP_EXPERIMENTAL (real avatar/XR EXTERNAL_BLOCKED) |
| Multi-simulator federation | G19H | sim_federation.py | KEEP_EXPERIMENTAL (real FMI simulators EXTERNAL_BLOCKED) |
| Reality/digital-twin streaming | G19I | reality_stream.py | KEEP_EXPERIMENTAL (real feeds EXTERNAL_BLOCKED) |
| Distributed world host / sharding | G19J | distributed_host.py | **REJECT promotion** (2.2x overhead, no correctness gain); seam stays behind flag |

## Promotion evidence summary
- No track met its promote criteria in this cycle; every track documented criteria and evidence.
- Distributed hosting is explicitly REJECTED for stable defaults (modular monolith retained per
  engineering rules); it is the only track with a negative decision.
- Real external providers/feeds/renderers/hardware remain EXTERNAL_BLOCKED; deterministic synthetic
  substitutes are the reproducible baseline everywhere.

## Stable regression
- Flags all OFF: stable canonical path unchanged (replay hash stable; G19A test).
- Full gate: `uv run python scripts/quality.py` -> 628 passed + 1 EXTERNAL_BLOCKED skip (live
  PostgreSQL), ruff/pyright/architecture PASS.
