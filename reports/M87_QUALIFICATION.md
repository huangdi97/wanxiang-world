# M87 — World Workshop Qualification

Date: 2026-08-26
Status: PASS

## Scope

M87 G90A-G90H delivers one Source/Prompt/Hybrid Workshop information
architecture over the existing v5.4 authoring, compiler, package, preview,
provider, rights, registry, and PlayableService boundaries. It does not add a
second candidate store, package registry, runtime, branch store, or commit
authority.

## Goal evidence

| Goal | Result | Evidence |
|---|---|---|
| G90A | PASS | Shared home and immutable optimistic WorkshopDraftStore |
| G90B | PASS | CreatorIntent, explicit constraints, E5 review contract |
| G90C | PASS | ProviderRouter, local private-safe provider, checkpoint/schema gate |
| G90D | PASS | Source/prompt fusion, preserved dissent, E0-E5 typed traces |
| G90E | PASS | Scenario/Experience editor and hashed read-only preview |
| G90F | PASS | Rights/visibility/publishing/safety profile gates |
| G90G | PASS | Existing package registry/install/trust adapter |
| G90H | PASS | Source/Prompt/Hybrid → WorldPackage → Preview → Playable/API E2E |

## Acceptance gates

- From Source regression is accepted by a real private source through the
  shared semantic-provider path, compiler/package assembly, PreviewInstall and
  PlayableService entry.
- From Prompt is accepted as a candidate-only E5 path. The initial public
  request is not publishable; `review_e5`, `accept_constraints`, and `preview`
  are required before a public profile is registered.
- Hybrid is accepted with source and prompt provenance retained separately;
  prompt traces are E5 and source claims retain their source evidence class.
  Cross-origin conflicts remain explicit and block compilation until review.
- Private visibility is owner-bound and not Plaza-visible. Public visibility
  requires public-export rights and completed content review. Rights-blocked
  builds fail closed.

## Verification

- G90H direct and API tests: 2 passed; G90A-G90G regression: 17 passed.
- Ruff, Pyright, architecture guard, and production-file size checks passed.
- The source payloads used by qualification are test fixtures only; no private
  book, source bytes, model, or training artifact was added to Git.

The M87 milestone is complete; the v5.5 release is not accepted until the
remaining M88-M94 gates and final release evidence pass.
