# Provider SDK Guide

Providers are replaceable proposal ports. They may analyze a source and return
`ProviderProposal` records, but they do not own a registry, job, package,
preview, Commit Authority, or Canonical World State.

## Minimal provider

Implement the existing `Provider` protocol: expose a
`ProviderCapability` and a `propose` method.

```python
from wanxiang_substrate.authoring.providers import (
    ProviderCapability,
    ProviderProposal,
    ProviderRouter,
)


class LinkingProvider:
    capability = ProviderCapability(
        provider_id="demo-linker",
        kind="linking",
        version="1",
        deterministic=True,
        private_safe=False,
        cost_units=1,
    )

    def propose(self, source_refs, payload):
        return (
            ProviderProposal(
                proposal_id="demo-link-1",
                kind="candidate",
                provider_id=self.capability.provider_id,
                source_refs=source_refs,
                payload=(("observed_length", str(len(payload))),),
                confidence=0.5,
            ),
        )


router = ProviderRouter((LinkingProvider(),))
proposals = router.propose("linking", ("source://demo",), "source data")
```

The proposal is evidence-bearing Forge input. A provider must not call a
runtime write API or manufacture a canonical fact. A custom provider should
have deterministic tests for its capability metadata, proposal provenance,
failure behavior, and privacy policy.

## Routing policy

`ProviderRouter.select` can require availability, private-source safety,
determinism, and a maximum cost. Keep those constraints at the shared router:

```python
capability = router.select(
    "linking",
    private_source=False,
    require_deterministic=True,
    max_cost_units=2,
    source_refs=("source://demo",),
)
```

LLM, Agent, OCR, ASR, vision, embedding, and linking implementations are all
providers under this rule. No API key is needed for the reference provider or
core tests.

## Missing capability is a typed result

Do not substitute an empty success for a missing provider. In particular,
scanned PDF authoring without OCR raises `OcrRequired` with the stable
`OCR_REQUIRED` marker. Other absent capabilities raise
`CAPABILITY_UNAVAILABLE`. The caller can display the requirement or resume
after installing a provider; neither path creates Canon.
