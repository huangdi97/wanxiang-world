"""Experiment result registry (G19A).

Records experiment provenance (track, seed, code/data/model versions) and the
promote/reject decision; experiments never mutate canonical worlds directly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    track: str
    seed: int
    decision: str  # PROMOTE | KEEP_EXPERIMENTAL | REJECT
    evidence: str
    runtime_version: int = RuntimeVersion(1).value
    schema_version: int = SchemaVersion(1).value

    def __post_init__(self) -> None:
        if self.decision not in ("PROMOTE", "KEEP_EXPERIMENTAL", "REJECT"):
            raise ValueError(f"invalid research decision {self.decision!r}")
        if not self.track or not self.evidence:
            raise ValueError("experiment result requires track and evidence")

    def manifest_hash(self) -> str:
        canonical = json.dumps(
            {
                "track": self.track,
                "seed": self.seed,
                "decision": self.decision,
                "evidence": self.evidence,
                "runtime_version": self.runtime_version,
                "schema_version": self.schema_version,
            },
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode()).hexdigest()


class ExperimentRegistry:
    def __init__(self) -> None:
        self._results: list[ExperimentResult] = []

    def record(self, result: ExperimentResult) -> None:
        self._results.append(result)

    def results(self) -> tuple[ExperimentResult, ...]:
        return tuple(self._results)

    def decisions(self) -> dict[str, str]:
        return {r.track: r.decision for r in self._results}
