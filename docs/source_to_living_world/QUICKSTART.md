# Source -> Living World Quickstart

This is the no-API reference workflow for creating a world from a synthetic
source. The same backend is used by the CLI and Studio API:

`Source Registry -> Parse/Segment/Locator -> Distill -> Candidate/Evidence/Rights -> Fusion -> Domain Composition -> WorldDraft -> Completion/Consistency -> Scenario/Genesis -> WorldPackageDraft -> Preview -> Worldness -> Publish checkpoint -> Living World preview`

## Install

```powershell
uv sync --all-groups --all-packages
```

The examples below use synthetic text. Do not put a copyrighted book,
family-private GEDCOM, token, database, or model cache in the repository.

## CLI reference path

Run a deterministic book profile:

```powershell
uv run python scripts/wxworld.py reference `
  --profile book --kind text --source-id demo-book --job-id demo-book-job `
  --content "# Chapter One`nCharacter: Alice`nCharacter: Bob`nAlice arrived in Beijing in 1985.`nBob visited Beijing.`nrelationship: Alice -> Bob`nrule: visitors register`n"
```

The JSON result contains the job status, package id, manifest hash, and an
isolated `preview_ref`. `--publish` requests the explicit Forge package
checkpoint after validation; it does not write Canonical World State:

```powershell
uv run python scripts/wxworld.py reference --profile book --kind text `
  --content "# Reference`nCharacter: Alice`nCharacter: Bob`nAlice arrived in Beijing in 1985.`nBob visited Beijing.`nrelationship: Alice -> Bob`nrule: visitors register`n" `
  --publish
```

`publishable: false` is an honest result when Completion, rights, or other
package gaps remain. Previewability is not publication eligibility.

Use the matching source kind for structured and family inputs. A family
profile requires `--kind gedcom`; a structured profile accepts `json`, `csv`,
or `yaml`. The mixed profile requires at least two source records and is most
convenient through the Python service or API, where `sources` is a list.

## Studio API

Start the API using the repository's normal application command, then submit a
synthetic, rights-approved source:

```powershell
curl -X POST http://127.0.0.1:8000/studio/one-click `
  -H "Content-Type: application/json" `
  -d '{"job_id":"api-demo","profile":"book","sources":[{"source_id":"api-book","kind":"text","content":"# Chapter\nCharacter: Alice\nCharacter: Bob\nAlice arrived in Beijing in 1985.\nBob visited Beijing.\nrelationship: Alice -> Bob\nrule: visitors register\n","stage":"E3","owner":"demo","usage":"package","rights_approved":true,"access":"public"}]}'
```

The response exposes `package_id`, `manifest_hash`, `preview_id`,
`publishable`, `publish_reasons`, and job status. If it is publishable, request
the separate checkpoint endpoint:

```powershell
curl -X POST http://127.0.0.1:8000/studio/jobs/api-demo/publish
```

Both routes call the shared `AuthoringService`; transport code owns no job,
candidate, package, preview, or Canonical World State.


## Visual world ladder

The current product path is one Player world with progressively richer derived
renderers, not four separate applications:

`Source -> Evidence -> WorldPackage -> T0/T1/T2/T3 assets -> Player Stage -> Intent -> Commit Authority -> History`

- **T0** is deterministic/offline and is the safe default. It produces the
  source-grounded narrative atlas and procedural scene pixels.
- **T1** is an optional governed still-image provider. Remote processing is
  disabled unless source rights, network policy and the configured budget all
  allow it.
- **T2** upgrades selected scenes to panorama projection. It remains derived
  presentation and never becomes canonical geometry.
- **T3** is an asynchronous spatial-asset job for selected anchor places. The
  repository includes durable submit/poll/verify/attach, restart recovery,
  cost reservation, a direct TokenHub adapter, a vendor-neutral HTTP gateway,
  and a dependency-free PLY Player renderer.

Use `WANXIANG_VISUAL_CACHE_DIR` for restart-safe local blobs, visual metadata,
budgets and spatial jobs. Leaving all remote-provider settings unset keeps the
reference product entirely offline.

### T3 backend selection

Choose exactly one T3 deployment backend:

1. direct Tencent TokenHub Hy-World using
   `WANXIANG_SPATIAL_TOKENHUB_SUBMIT_ENDPOINT`,
   `WANXIANG_SPATIAL_TOKENHUB_TASKS_ENDPOINT`,
   `WANXIANG_SPATIAL_TOKENHUB_API_KEY` and an explicit
   `WANXIANG_SPATIAL_TOKENHUB_ARTIFACT_HOSTS` allowlist; or
2. the normalized Wanxiang HTTP gateway using
   `WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT` and
   `WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT`.

Set `WANXIANG_SPATIAL_ALLOW_NETWORK=true` only with a configured backend and
set `WANXIANG_SPATIAL_MAX_COST_UNITS` explicitly. Configuring TokenHub and the
generic HTTP gateway together is rejected at application startup; paid-provider
selection is never implicit.

Real T1/T3 execution still requires authorized credentials and rights-safe
source material. Local tests prove the contracts and safety boundaries, not
provider billing, latency or visual quality.

## Boundaries to keep visible

- Sources and evidence retain stable locators and provenance.
- Candidates and Completion E1-E5 remain Forge data; they are not E0 Canon.
- Providers and agents return proposals only.
- Only Commit Authority can mutate a living instance.
- A scanned PDF without an OCR provider returns `OCR_REQUIRED`; it is never
  silently treated as extracted text.
