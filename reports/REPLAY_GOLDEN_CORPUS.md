# Replay Golden Corpus (G13E)

Stable semantic hashes replayed from clean event state (no chat memory).

## Golden fixture (tests/fixtures/golden_replay_v1.json)

- Events: 5, final revision: 5
- Replayed semantic hash: `7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00`
- Fixture expected hash: `7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00`
- Match: True

## Synthetic micro-world history (M1-style, via WorldRuntime + SQLite)

- Events: 3, final revision: 3
- Replayed semantic hash: `0964e48a7d03fe52bc227395d8332b24a18798e3c0c1a293f63231d88941aed5`
- Hash at commit time: `0964e48a7d03fe52bc227395d8332b24a18798e3c0c1a293f63231d88941aed5`
- Stable across clean replay: True

Replay command: `ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)`
