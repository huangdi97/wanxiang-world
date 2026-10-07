# R7 09 — Capability Foundry (Artifact2Capability)

Status: `IMPLEMENTED / VALIDATED` for the tracked reference-artifact path.

```text
Artifact
 -> CapabilityCandidate
 -> interface/environment
 -> Execution Fabric verification
 -> VerificationReport
 -> CapabilityPackage
 -> C3 registry admission
 -> proposal-only invocation
```

Artifact kinds cover paper, repo, API, manual, standard, notebook, workflow,
dataset and simulation.

A CapabilityPackage binds source URI/digest/rights basis, primary artifact,
declared interface + recomputed digest, exact verification case ids, four
provenance layers, validity/limitations, execution policy/environment, K/C
levels and verification evidence. Registry admission requires the full
GOLDEN/NEGATIVE/BOUNDARY/SECURITY C3 report and exact evidence/case binding.
Versions coexist and revocation remains recorded. Automation does not promote
above C3.

The science reference slice uses the tracked
`reference_worlds/r7/science/double_capability.py` artifact. It runs all four
verification kinds through Execution Fabric, admits the package, invokes it,
proves World history did not change, then separately sends a reviewed action
through normal World authority.

The deterministic provider is not Paper2Agent. No live Paper2Agent model run and
no externally fetched paper/repository capability are claimed here.
