# External Sample Pack — Black-box (G17G)

## Claim
A nontrivial sample package is authored as if by a third party, using only the public SDK and docs —
no Core source-tree imports, no relative-path hacks, no Core edits.

## Sample
`scripts/blackbox_sample.py` writes a domain pack (public SDK only) with a custom domain action
(`sample.instantiate` / `sample.heal`) via the permitted resolver extension mechanism.

## Flow
1. Author sample in an external directory (public SDK only).
2. Publish + install through the registry lifecycle (lock hash).
3. Instantiate a world and run the custom actions through the public runtime.
4. Publish v2; the v1 install stays pinned; a new instance explicitly installs v2; v1 export remains stable.

## Results
| Check | Result |
|---|---|
| Sample works without Core source-tree imports | PASS |
| Old instance stays pinned/replayable after v2 publish | PASS |
| New instance can use v2 after explicit install | PASS |
| Custom domain rule/skill via permitted extension mechanism | PASS |

## Evidence
- `uv run pytest tests/integration/test_g17g_blackbox_sample.py -q` -> 2 passed.
