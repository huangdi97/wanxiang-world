# M7 Acceptance ? Multiple Unrelated Domains Prove Core Generality

## Verdict
PASS

## Scope
P7 (G08A?G10D) delivered on top of verified M1-M6. Three unrelated domain
families (mansion/literature, family genealogy/archive, heritage/museum) run
on the same authoritative core.

## Mandatory scenario
1. Mansion (G08A): a synthetic mansion Domain/World/Scenario runs seven
   in-world days with no-user periods, human takeover/resume, a day-3 alternate
   branch (parent never mutated) and letter custody/read/knowledge propagation
   (`tests/integration/test_m7_mansion.py`).
2. Red Chamber (G08B): Source Gate positive/negative fixture behavior; real
   literary data EXTERNAL_BLOCKED with manifest template only
   (`tests/integration/test_m7_qualification.py` + `sources/red_chamber/`).
3. Family (G09A-C): GEDCOM round-trip profile with source retention and
   extension preservation, conflicting claims as evidence-backed candidates,
   living-person privacy/consent/revocation and persona mode labeling.
4. Heritage (G10A-D): IIIF manifest ingest, Linked Art/CIDOC mapping profile,
   distinct physical/digital/twin/reconstruction identities, replayable
   conservation history, museum biography truth labels + curator gate.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| Mansion 7-day persistence/control/knowledge/material/branch | PASS | mansion test |
| Family GEDCOM round-trip + sources + conflicts + living privacy | PASS | genealogy tests + qualification |
| Persona modes distinguish evidence/reconstructed/creative; revocation enforced | PASS | privacy tests |
| Heritage IIIF refs + Linked Art/CIDOC profile | PASS | heritage tests |
| Physical/surrogate/twin/reconstruction distinct | PASS | twin distinctness test |
| Object biography replayable; rights/cultural protocols enforced | PASS | conservation + curator tests |
| Domain rules are plugins/packages above Core | PASS | all domains on existing substrate |
| Real-source slices EXTERNAL_BLOCKED; Source Gate fixtures PASS | PASS | red chamber section |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1-M6 milestone gates | PASS | full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | full suite |
| Rights/projection leakage | PASS | full suite |
| No-LLM deterministic profile | PASS | full suite |
| Lint/typecheck | PASS | ruff + pyright clean |
| TODO/placeholder + secret scan | PASS | architecture guard |

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed (366 tests).
- Checkpoint commit: `m7: qualify milestone`
- Milestone tag: `m7-domain-generality`