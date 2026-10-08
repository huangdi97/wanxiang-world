"""Import/schema/locator smoke against the official GEDCOM 7 tree sample.

The sample is fetched into memory only; it is not vendored into the repo and
is not sent through the living-world product chain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from typing import Any, cast

from wanxiang_substrate.distill.passes import (
    EventTimeSpacePass,
    IdentityPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.distill.passes_knowledge import (
    CharacterKnowledgePass,
    ObjectRuleSkillPass,
)
from wanxiang_substrate.distill.protocol import DistillerDAG
from wanxiang_substrate.genealogy.gedcom import parse_gedcom
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, build_segments
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord
from wanxiang_substrate.sources.structured import StructuredAdapter

OFFICIAL_TREE1_URL = "https://gedcom.io/testfiles/gedcom70/maximal70-tree1.ged"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=OFFICIAL_TREE1_URL)
    return parser


def run(url: str = OFFICIAL_TREE1_URL) -> dict[str, Any]:
    raw = urllib.request.urlopen(url, timeout=60).read()
    text = raw.decode("utf-8-sig")
    source = SourceRecord(
        source_id="official_gedcom7_tree1_smoke",
        kind="gedcom",
        content_hash=hashlib.sha256(raw).hexdigest(),
        content_ref="https://gedcom.io/testfiles/gedcom70/maximal70-tree1.ged",
        stage="E3",
        rights=RightsEnvelope(owner="official-sample", usage="schema-smoke", approved=True),
        payload=text,
        provenance="FamilySearch GEDCOM official test file",
        access="public",
    )
    ingest = StructuredAdapter().ingest(source, raw)
    document = parse_gedcom(text)
    parsed = StructureParser().parse(
        ingest,
        source_id=source.source_id,
        version=ingest.source_version or source.version,
        content_hash=source.content_hash,
    )
    segments = build_segments(parsed, fmt=cast(LocatorFormat, "gedcom"))
    dag = DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )
    candidates = dag.run(segments, source_id=source.source_id)
    result: dict[str, Any] = {
        "url": url,
        "raw_bytes_read": len(raw),
        "schema": {
            "gedcom_version": parsed.metadata.version,
            "parsed_nodes": len(parsed.nodes) - 1,
            "individuals": len(document.individuals),
            "families": len(document.families),
            "sources": len(document.sources),
        },
        "locator": {
            "segments": len(segments),
            "gedcom_record_locators": sum(
                segment.locator.to_string().startswith(f"gedcom://{source.source_id}#record/")
                for segment in segments
            ),
            "xref_records": sum(
                "@I" in segment.text or "@F" in segment.text for segment in segments
            ),
        },
        "candidates": {
            "count": len(candidates),
            "identities": sum(candidate.kind == "identity" for candidate in candidates),
            "relations": sum(
                candidate.kind in ("relation", "membership") for candidate in candidates
            ),
            "evidence_backed": sum(
                bool(candidate.source_refs and candidate.evidence_refs) for candidate in candidates
            ),
        },
        "diagnostics": [item.message for item in parsed.diagnostics],
    }
    result["accepted"] = bool(
        result["schema"]["gedcom_version"] == "7.0"
        and result["schema"]["parsed_nodes"] > 0
        and result["locator"]["gedcom_record_locators"] == result["locator"]["segments"]
        and result["candidates"]["count"] > 0
        and not result["diagnostics"]
    )
    return result


def main() -> int:
    args = _parser().parse_args()
    print(json.dumps(run(args.url), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
