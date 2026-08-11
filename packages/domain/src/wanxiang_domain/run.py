"""Run metadata for deterministic reproduction."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.ids import RunId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class RunMetadata:
    run_id: RunId
    instance_id: WorldInstanceId
    seed: int
    rule_version: RuntimeVersion
    schema_version: SchemaVersion
    started_world_time: WorldTime
