"""G14D: history corruption diagnostics.

`diagnose_stream` scans an ordered committed-event stream and reports precise
corruption findings (sequence gaps, instance/branch mismatch, revision jumps,
unsupported versions). It is read-only: it never mutates history. Replay
continues to be the authoritative consumer; this tool identifies the affected
event for operators.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


def diagnose_stream(
    events: Sequence[CommittedEvent],
    *,
    rule_version: RuntimeVersion,
    schema_version: SchemaVersion,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not events:
        return findings
    instance_id = events[0].instance_id
    branch_id = events[0].branch_id
    expected_seq = 1
    expected_revision = 1
    for index, event in enumerate(events):
        where = {"event_index": index, "event_id": event.event_id.value}
        if event.instance_id != instance_id or event.branch_id != branch_id:
            findings.append({**where, "kind": "instance_branch_mismatch"})
        if event.event_seq.value != expected_seq:
            findings.append(
                {
                    **where,
                    "kind": "sequence_gap_or_reorder",
                    "expected_seq": expected_seq,
                    "actual_seq": event.event_seq.value,
                }
            )
        if event.revision.value != expected_revision:
            findings.append(
                {
                    **where,
                    "kind": "revision_jump",
                    "expected_revision": expected_revision,
                    "actual_revision": event.revision.value,
                }
            )
        if event.schema_version != schema_version:
            findings.append(
                {
                    **where,
                    "kind": "unsupported_schema_version",
                    "actual": event.schema_version.value,
                    "supported": schema_version.value,
                }
            )
        if event.rule_version != rule_version:
            findings.append(
                {
                    **where,
                    "kind": "unsupported_rule_version",
                    "actual": event.rule_version.value,
                    "supported": rule_version.value,
                }
            )
        expected_seq += 1
        expected_revision += 1
    return findings
