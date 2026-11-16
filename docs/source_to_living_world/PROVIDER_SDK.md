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


## Visual and spatial provider boundary

Source-analysis providers above are proposal providers. Visual providers are a
separate derived-asset boundary:

- T1 implements `SceneImageProvider` and returns verified raster bytes.
- T2 panorama providers use the governed panorama materialization path.
- T3 implements `SpatialGenerationProvider`: submit once, persist the provider
  task reference, poll to a terminal provider state, locally verify returned
  artifacts, then attach only derived `AssetRef` values to the Player.

None of these providers may write Canon, Worldline or History. A successful
generation only changes available projection assets.

### T3 provider requirements

A production T3 adapter must declare provider id/version, network/private-source
policy, cost units, allowed media types and whether submission is actually
idempotent. It must also:

1. compile only the bounded scene brief; never send the full book by default;
2. persist a submission identity before a potentially billable request;
3. use the same idempotency key for safe retries only when the provider contract
   supports it;
4. treat an uncertain non-idempotent submit as `submission_ambiguous` rather
   than automatically paying for a second job;
5. download only from explicit artifact hosts and verify size, digest and known
   media signatures before ObjectStore write;
6. preserve provider usage/billing evidence separately from canonical state;
7. continue to revalidate current source rights when a persisted asset is
   restored or attached after restart.

The repository has two supported integration shapes today: the direct Tencent
TokenHub Hy-World adapter and the normalized HTTP gateway. Do not pass a raw
vendor endpoint into the normalized gateway unless a bridge translates that
vendor's request, operation and artifact schema into the Wanxiang contract.

### World Labs / Marble integration note

Current World Labs guidance requires integrations to follow the live Marble 2
Developer API schemas, persist operation IDs, reuse one `Idempotency-Key` for
transport retries of the same logical submission, and poll the operation until
its `done` terminal signal. The current API reference exposes task-specific
operations such as `atlasTextToImage`, `atlasGenerate`, `atlasChisel` and
`splats2Mesh`; task availability is account-dependent. World Labs also warns
that older World API / Marble examples are not interchangeable contracts with
the live Marble 2 beta API.

Therefore this repository does **not** pretend that the existing generic T3
gateway is a raw Marble endpoint or invent a direct Marble adapter from older
examples. A future direct adapter should be added only against the exact enabled
task schema and real authorized operation/artifact evidence.

Official references:

- https://atlas-beta.worldlabs.ai/docs/operations
- https://atlas-beta.worldlabs.ai/docs/errors
- https://atlas-beta.worldlabs.ai/docs/api-reference
- https://atlas-beta.worldlabs.ai/docs/best-practices

## Missing capability is a typed result

Do not substitute an empty success for a missing provider. In particular,
scanned PDF authoring without OCR raises `OcrRequired` with the stable
`OCR_REQUIRED` marker. Other absent capabilities raise
`CAPABILITY_UNAVAILABLE`. The caller can display the requirement or resume
after installing a provider; neither path creates Canon.
