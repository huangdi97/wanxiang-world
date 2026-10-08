# G54D Report — Duplicate Abstraction Cleanup (M51)

## Status
**PASS** — Duplicate registry/job/candidate/review/package abstractions audited
against the CURRENT tree; every same-name class verified as a distinct
single-problem concern (no silent second abstraction). A guard now prevents
NEW duplicate class names.

## Delivered
1. `scripts/duplicate_abstraction_scan.py` — AST scan of production source for
   same class name across modules; allowlist documents intentional same-name
   classes with their exact modules; any unallowed duplicate fails.
2. `reports/duplicate_abstraction_scan.json` — committed scan (verdict PASS).
3. `tests/architecture/test_duplicate_abstractions.py` — 3 tests.

## Same-name classes verified as distinct (no merge — KEEP)
| Name | Modules | Distinct concern |
|---|---|---|
| CanonClaim | sources/canon.py vs canon_graph/timeline_canon.py | source-temporal canon compilation vs multi-edition canon graph (evidence refs + contradicted_by) |
| CandidateEnvelope | evolution/distillation.py (single module) | pattern-distillation envelope; M54 unified fabric must converge on this, not fork |
| RightsEnvelope | domain/rights.py vs sources/model.py | kernel allow/deny decision seam vs source rights approval (owner/usage/approved) |
| RightsDenied | domain/errors.py vs sources/errors.py | kernel error vs source-error subclass taxonomy |
| DeterministicPolicy | agency/policy.py vs population/policy.py | propose-only IntentCandidate policy port vs scheduler CommandEnvelope builder |
| Observation | observation/model.py vs research/adapters.py | perception value object vs gym-style research adapter wrapper |
| ObservationFusion | research/reality_stream.py vs substrate/reality/fusion.py | research (EXPERIMENTAL) vs production reality fusion |
| Order | agency/model.py vs cosim/campaign.py | actor order vs campaign unit order |
| AssetGenerator | research/generative_assets.py vs assets/foundry.py | research (EXPERIMENTAL) vs production asset foundry |
| ValidityEnvelope | research/sim_federation.py vs reality/experiment.py | research (EXPERIMENTAL) vs production reality experiment |
| RuntimeProfile | authoring/scenario_engine.py vs host/hypervisor.py vs playable/models.py | Forge scenario, host binding, and Playable product selection have distinct owners and lifecycles |
| ExperimentDefinition | API strategy workbench vs World Laboratory registry | legacy co-simulation request vs version-pinned world-lab definition |
| ExperimentRegistry | research result decisions vs World Laboratory run leases | experimental result history vs recoverable definition/run metadata |

## Registry/job/review/package disposition (verified with call sites)
- Registries (SourceRegistry, PackageRegistry, SkillRegistry, ActionRegistry,
  ResolverRegistry, AdjudicatorRegistry, HostRegistry, PresenceRegistry):
  all domain-local/single-problem — KEEP (consistent with G29B).
- Job/checkpoint: compiler job model, corpus pipeline cache/resume,
  recovery/checkpoint.py — distinct layers — KEEP; G54E will unify the
  Import/Authoring job on top of recovery/checkpoint.
- Review: ledger ReviewDecision, sources Identity/EntityReviewDecision/Gate,
  studio CandidateReview — distinct stages — KEEP.
- Package: PackageManifest (schema) + InMemoryPackageRegistry (registry) +
  RegistryLifecycle (lifecycle) — distinct roles — KEEP.

## Local commit
- `goal g54d: Duplicate abstraction cleanup (M51)`
