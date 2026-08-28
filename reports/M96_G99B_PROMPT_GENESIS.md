# M96 G99B — Prompt Genesis Candidate Chain

**Conclusion:** `PASS` for the bounded G99B contract.

The reproducible run in `artifacts/v55_stable/m96/original_prompt_world.json`
uses seed `9601`, creator-intent hash
`f4f45e60dc9ae8fa3839b1a8e6b32dd0cd5a51024e7aa4b729a5ed2e029354c1`, and
`local_prompt_genesis_v1`. The provider emitted one proposal and the artifact
records every generated claim as `E5`; no generated claim is promoted to E0/E1.

Command:

```powershell
$env:UV_CACHE_DIR='E:\\AI\\wanxiang\\.uv-cache'
uv run python scripts/m96_prompt_world.py
```

The resulting WorldDraft keeps the prompt as a creator-intent provenance
reference. Raw prompt text is not emitted into the artifact. This is bounded
reference-provider engineering evidence; Prompt Genesis remains
`EXPERIMENTAL`/`BOUNDED` and does not establish creative or scientific truth.
