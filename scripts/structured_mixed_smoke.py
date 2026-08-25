"""Run the synthetic M83 structured/mixed Forge smoke without private data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.sources.structured_evidence import (
    csv_cell_locator,
    json_leaf_evidence,
    json_pointer_locator,
    resolve_csv_cell,
    resolve_json_pointer,
)

ROOT = Path(__file__).resolve().parent.parent


def _record(source_id: str, kind: str, payload: str) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind=kind,
        content_hash=payload_hash(payload),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic-m83", usage="qualification", approved=True),
        payload=payload,
        provenance="synthetic:m83",
        access="public",
    )


def run() -> dict[str, object]:
    book = _record(
        "book_m83", "text", "# Chapter\nCharacter: Ada\nAda arrived in 1980 at Harbor.\n"
    )
    structured_payload = json.dumps({"people": [{"name": "Ada"}], "place": "Harbor"})
    structured = _record("json_m83", "json", structured_payload)
    csv = _record("csv_m83", "csv", "name,year,place\nAda,1980,Harbor\n")
    build = SourceToDraftPipeline().run((book, structured, csv), draft_id="wd_m83_smoke")
    one_click = OneClickAuthoring().run("job_m83_smoke", (book, structured, csv), profile="mixed")
    pointer = json_pointer_locator("json_m83", "/people/0/name")
    cell = csv_cell_locator("csv_m83", 2, 3)
    return {
        "profile": "mixed",
        "draft_id": build.draft.draft_id,
        "source_refs": list(build.draft.source_refs),
        "candidate_count": len(build.candidates),
        "fusion_alignment_count": len(build.fusion_alignments),
        "package_id": one_click.package.package_id,
        "preview_ref": one_click.preview.scoped_ref,
        "json_pointer": pointer.to_string(),
        "json_pointer_value": resolve_json_pointer(structured_payload, pointer.ref),
        "json_leaf_count": len(json_leaf_evidence("json_m83", structured_payload)),
        "csv_cell": cell.to_string(),
        "csv_cell_value": resolve_csv_cell(csv.payload, 2, 3),
        "one_world_draft": one_click.package.draft.draft_id == "wd_job_m83_smoke"
        and len(one_click.package.draft.source_refs) == 3,
    }


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    output = run()
    target = ROOT / "artifacts" / "m79_m84" / "structured_mixed_smoke.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
