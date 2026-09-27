# R7 09 — Capability Foundry (Artifact2Capability)

Status: `IMPLEMENTED` / `VALIDATED` (unit level, with real subprocess execution of
verification cases through the isolated Execution Fabric).

## 1. Chain implemented

```text
Artifact (paper | repo | api | notebook | workflow)
-> CapabilityCandidate            (proposal only)
-> interface + environment declaration
-> isolated execution of golden / negative / boundary / security cases
-> VerificationReport             (K-level and C3 eligibility)
-> CapabilityPackage             (versioned, provenance-bound)
-> VerifiedCapabilityRegistry    (C3 admission, revocable)
-> invocation -> Observation / Proposal   (never canonical state)
```

## 2. Artefacts

| Module (`packages/foundry/src/wanxiang_foundry/`) | Responsibility |
|---|---|
| `errors.py` | typed foundry errors |
| `digest.py` | canonical-JSON sha256 and hex-digest check |
| `provenance.py` | `ProvenanceLayer` (SOURCE_METHOD, GENERATED_WRAPPER, VALIDATION_FIXTURE, RUNTIME_ADAPTER), `provenance_digest` |
| `levels.py` | `KnowledgeLevel` K0–K3, `PromotionLevel` C0–C5, `AUTOMATION_MAX_PROMOTION = C3` |
| `package.py` | proposal-only `OutputClass`, `Validity`, `RuntimeRequirement`, `WorldEffect`, `CapabilityPackage` with `package_digest()` |
| `candidate.py` | `ArtifactKind`, `ArtifactRef`, proposal-only `CapabilityCandidate` |
| `provider.py` | `Artifact2CapabilityProvider` seam + `ProviderRegistry` (no silent replacement) |
| `reference_provider.py` | deterministic, LLM-free reference provider (`is_reference_provider = true`) |
| `verification.py` | `CaseKind`, `FailureLayer`, `VerificationCase`, `CaseResult`, `VerificationReport`, pure `verify()` |
| `fabric_runner.py` | runs cases through the isolated Execution Fabric, returns typed outcomes |
| `registry.py` | `VerifiedCapabilityRegistry`: `admit`/`get`/`versions`/`active`/`revoke`/`promotions`/`is_invocable` |
| `invocation.py` | `CapabilityRequest` -> proposal-only `CapabilityOutcome`, `invoke()` |

## 3. Invariants (each has a test)

- A capability may observe, propose or project — never mutate canonical world
  state: `WorldEffect` has no canonical-write member and `from_output_class`
  refuses any such string. The package's AST+call guard asserts the package never
  imports `wanxiang_runtime`/`wanxiang_domain`/`wanxiang_substrate`/
  `wanxiang_application`/`wanxiang_persistence` or any commit/authority module.
- Verification is honest: `verify()` returns K3 only when all GOLDEN, BOUNDARY and
  NEGATIVE cases pass, and C3 eligibility only when all four kinds pass. A declared
  case with no result fails and is reported — unknown is not pass.
- `admit()` refuses a package whose report does not grant C3 or whose
  `verification_digest` does not match the report's evidence digest, and refuses a
  second admission of the same id+version: versions coexist, nothing is overwritten
  or deleted, revocation is recorded.
- Automation stops at C3: `is_automation_grantable` is false for C4/C5, which are
  human/organisation decisions.
- Execution is real and isolated: cases run as a child process through
  `wanxiang_execution.LocalProcessProvider` with the fabric's policy check first;
  stdout digest and exit status decide the outcome, and a policy denial or a
  non-starting command becomes a typed failed `CaseResult` (`ENVIRONMENT`), never
  an unhandled exception.
- Provenance is tamper-evident: the package digest folds the sorted provenance
  records.

## 4. Evidence

```text
uv run pytest -q tests/unit/foundry                 -> 59 passed
uv run pytest -q tests/unit                         -> 914 passed
uv run pytest -q tests/architecture tests/unit/foundry -> 146 passed
uv run ruff check . / ruff format --check .         -> clean
uv run pyright                                      -> 0 errors (repo-wide)
uv run python scripts/architecture_check.py         -> PASS
uv run python scripts/duplicate_abstraction_scan.py -> verdict PASS (0 unallowed)
uv run python scripts/v52_minimality_budget.py      -> registries 20, ports 49, cycles 0, commit_paths 1
```

## 5. Not claimed

- No Paper2Agent implementation, binary or model is used or claimed: the bundled
  provider is a documented reference and reports `officialDsh`-style honesty for
  its own identity (`provider_id = foundry-rule-based-reference`).
- No capability was produced from a real external paper/repo in this slice; the
  pipeline is validated on declared artifacts and real local executions.
- Container/microVM isolation is not claimed: isolation is the execution fabric's
  process-level isolation.
- No automation above C3, and no level implies world truth.
