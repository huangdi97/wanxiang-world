"""Snapshot validation policy for restore (G14D).

A snapshot is usable only if its schema/rule versions match the runtime and
replaying the events up to its event_seq reproduces the snapshot state's
semantic hash. Otherwise it is rejected and restore falls back to full event
replay (events are authoritative).
"""

from __future__ import annotations

from typing import Any

from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine


def snapshot_is_valid(
    latest: Any,
    events: tuple[CommittedEvent, ...],
    *,
    rule_version: RuntimeVersion,
    schema_version: SchemaVersion,
) -> bool:
    meta = latest.metadata
    if meta.schema_version != schema_version or meta.rule_version != rule_version:
        return False
    upto = [e for e in events if e.event_seq.value <= meta.event_seq.value]
    if not upto:
        return False
    try:
        check = ReplayEngine(rule_version, schema_version).replay(upto)
    except WanxiangError:
        return False
    return check.semantic_hash() == latest.state.semantic_hash()
