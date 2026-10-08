# Wanxiang R7 reference slices

These are **qualification slices**, not four new product implementations.

The R7 architecture must prove that one composition model can support materially
different worlds without creating a second canonical-state path. The executable
qualification lives in `tests/integration/test_r7_reference_worlds.py` and covers:

- **Original / Fiction** — Player action -> Commit, legal rejection, branch isolation,
  and a read-only Observer Experience sharing the same canonical runtime.
- **Heritage** — rights/evidence gating, source-backed canon promotion, and a
  reconstruction that remains explicitly non-canonical until reviewed.
- **Agent World** — the real cross-process reference harness observes, proposes,
  receives committed/rejected consequences, and never holds commit authority.
  It is intentionally labelled non-official; official DeepSeek Harness remains a
  separately qualified external provider.
- **Science / Capability** — this directory's tracked
  `science/double_capability.py` is hashed as a real ArtifactRef, verified across
  golden/negative/boundary/security cases through the Execution Fabric, admitted
  at C3, invoked proposal-only, then independently considered by World authority.

The slices reuse the existing WorldRuntime, Capability Foundry, Execution Fabric,
source/evidence ledger and harness bridge. They do not fork those mechanisms.

## Evidence boundary

Passing these slices establishes R7 reference architecture behavior. It does **not**
claim a production museum corpus, a production-scale scientific package, official
DSH model credentials, or a hardened container/microVM sandbox.
