"""Completion review CLI (G35H): batch review of completion records.

Usage:
  uv run python scripts/completion_review.py manifest.json report.json

manifest.json:
  {"records": [{"completion_id": "...", "description": "...", "support_refs": [...],
   "confidence": 0.8}], "decisions": [{"decision_id": "...", "completion_id": "...",
   "decision": "approve|reject", "reviewer": "human", "rationale": "...",
   "evidence_refs": [...]}]}

All records are submitted first (never overwriting), then decisions are applied
in order under E0-E5 stage semantics. The report JSON records final statuses,
can_enter_canon, conflicts and a stage summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from wanxiang_substrate.ledger.completion import (
    CompletionDecision,
    CompletionRecord,
    CompletionReviewLedger,
    CompletionStudio,
    apply_batch_review,
)


def _record(data: dict[str, Any]) -> CompletionRecord:
    return CompletionRecord(
        completion_id=str(data["completion_id"]),
        description=str(data["description"]),
        support_refs=tuple(str(x) for x in data.get("support_refs", [])),
        confidence=float(data.get("confidence", 0.5)),
    )


def _decision(data: dict[str, Any]) -> CompletionDecision:
    return CompletionDecision(
        decision_id=str(data["decision_id"]),
        completion_id=str(data["completion_id"]),
        decision=str(data["decision"]),  # type: ignore[arg-type]
        reviewer=str(data["reviewer"]),
        rationale=str(data["rationale"]),
        evidence_refs=tuple(str(x) for x in data.get("evidence_refs", [])),
    )


def run_batch(
    manifest: dict[str, Any],
) -> tuple[CompletionReviewLedger, CompletionStudio, dict[str, Any]]:
    """Submit records, apply decisions, and produce the report payload."""
    ledger = CompletionReviewLedger()
    for raw in manifest.get("records", []):
        ledger.submit(_record(raw))
    decisions = tuple(_decision(raw) for raw in manifest.get("decisions", []))
    updated = apply_batch_review(ledger, decisions)
    studio = CompletionStudio(ledger)
    report = {
        "reviewed": [record.completion_id for record in updated],
        "can_enter_canon": [record.completion_id for record in studio.canon_candidates()],
        "conflicts": [list(pair) for pair in studio.conflicts()],
        "stage_summary": studio.stage_summary(),
    }
    return ledger, studio, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Batch completion review")
    parser.add_argument("manifest", type=Path, help="input manifest JSON")
    parser.add_argument("report", type=Path, nargs="?", help="output report JSON")
    args = parser.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    _ledger, _studio, report = run_batch(manifest)
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.report is not None:
        args.report.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
