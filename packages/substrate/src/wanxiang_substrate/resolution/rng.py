"""Seeded deterministic RNG with explicit ownership (no globals)."""

from __future__ import annotations

import hashlib


class SeededRng:
    """A deterministic RNG derived from (seed, stream, counter).

    The adjudicator owns the RNG instance; the same seed + stream + call order
    always produces the same draws.
    """

    def __init__(self, seed: int, stream: str = "adjudication", counter: int = 0) -> None:
        self._seed = seed
        self._stream = stream
        self._counter = counter

    def draw(self) -> float:
        """Deterministic draw in [0, 1) derived from seed+stream+counter."""
        digest = hashlib.sha256(f"{self._seed}:{self._stream}:{self._counter}".encode()).hexdigest()
        self._counter += 1
        return int(digest[:12], 16) / (16**12)

    def chance(self, probability: float) -> bool:
        return self.draw() < probability
