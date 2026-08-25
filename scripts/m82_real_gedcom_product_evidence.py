"""Sanitized real GEDCOM -> WorldPackage -> Living evidence.

The source is read from the caller's private local path and submitted through
the public Studio/API routes. The report contains counts and gate evidence,
never the path, source text, or content digest.
"""

from __future__ import annotations

import argparse
import base64
import json
from collections import Counter
from pathlib import Path
from typing import Any, cast

from fastapi.testclient import TestClient
from wanxiang_api.app import create_app

from reference_runtime import build_reference_runtime


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--job-id", default="m82_real_gedcom_api")
    return parser


def _request(client: Any, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    response: Any = client.request(method, path, **kwargs)
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"{method} {path} returned HTTP {response.status_code}: {response.text}")
    value: Any = response.json()
    if not isinstance(value, dict):
        raise RuntimeError(f"{method} {path} did not return an object")
    return cast(dict[str, Any], value)


def _draft_evidence(value: dict[str, Any]) -> dict[str, Any]:
    draft = cast(dict[str, Any], value.get("draft") or {})
    candidates = cast(list[dict[str, Any]], value.get("candidates") or [])
    fields = [cast(dict[str, str], item.get("payload") or {}) for item in candidates]
    event_types = sorted({item.get("event_type", "") for item in fields if item.get("event_type")})
    relation_types = sorted(
        {item.get("relation_type", "") for item in fields if item.get("relation_type")}
    )
    precisions = Counter(
        item.get("date_precision", "") for item in fields if item.get("date_precision")
    )
    family_candidates = sum(
        item.get("kind") == "organization"
        and item.get("payload", {}).get("entity_type") == "family"
        for item in candidates
    )
    xref_identities = sum(
        item.get("kind") == "identity" and bool(item.get("payload", {}).get("xref"))
        for item in candidates
    )
    absent_fact_kinds = {"residence", "migration", "education", "occupation"}
    absent_fact_candidates = sorted(absent_fact_kinds.intersection(event_types))
    return {
        "status": draft.get("status"),
        "coverage": draft.get("coverage"),
        "uncertainty": draft.get("uncertainty"),
        "selected_domains": draft.get("selected_domains", []),
        "completion_items": draft.get("completion_items", []),
        "counts": {
            "entities": len(draft.get("entities", [])),
            "relations": len(draft.get("relations", [])),
            "places": len(draft.get("places", [])),
            "events": len(draft.get("events", [])),
            "candidates": len(candidates),
            "claims": sum(item.get("kind") == "claim" for item in candidates),
            "family_candidates": family_candidates,
            "xref_identities": xref_identities,
        },
        "candidate_kind_counts": dict(
            sorted(Counter(item.get("kind", "") for item in candidates).items())
        ),
        "event_types": event_types,
        "relation_types": relation_types,
        "date_precision_counts": dict(sorted(precisions.items())),
        "uncertain_date_candidate_count": sum(item.get("uncertain") == "true" for item in fields),
        "exact_date_candidate_count": sum(item.get("uncertain") == "false" for item in fields),
        "stable_xref_candidate_count": xref_identities,
        "evidence_refs": sum(bool(item.get("evidence_refs")) for item in candidates),
        "source_refs": sum(bool(item.get("source_refs")) for item in candidates),
        "absent_fact_candidates": absent_fact_candidates,
    }


def run(source: Path, *, job_id: str) -> dict[str, Any]:
    raw = source.read_bytes()
    app = create_app(build_reference_runtime())
    client: Any = TestClient(app)
    source_input = {
        "source_id": "m82_real_gedcom_source",
        "kind": "gedcom",
        "content_base64": base64.b64encode(raw).decode("ascii"),
        "version": "1",
        "stage": "E3",
        "owner": "public-historical-fixture",
        "usage": "public historical genealogy test",
        "rights_approved": True,
        "access": "private",
        "provenance": "D-Jeffrey/gedcom-samples — bronte.ged",
        "private_analysis_allowed": True,
        "external_model_processing_allowed": False,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
    }
    one_click = _request(
        client,
        "POST",
        "/studio/one-click",
        json={
            "job_id": job_id,
            "profile": "family",
            "semantic_provider": "local",
            "sources": [source_input],
        },
    )
    draft = _request(client, "GET", f"/studio/jobs/{job_id}/draft")
    built = _request(client, "POST", f"/studio/jobs/{job_id}/build")
    preview = _request(client, "POST", f"/studio/jobs/{job_id}/preview")
    published = _request(client, "POST", f"/studio/jobs/{job_id}/publish")
    worldness = cast(
        dict[str, Any],
        _request(client, "POST", f"/studio/jobs/{job_id}/worldness").get("worldness") or {},
    )
    entered = _request(client, "POST", f"/studio/jobs/{job_id}/enter")
    living = _request(client, "GET", f"/studio/jobs/{job_id}/living")
    status = _request(client, "GET", f"/studio/jobs/{job_id}")
    ui: Any = client.get("/studio/ui")
    action = cast(dict[str, Any], worldness.get("living", {}).get("action") or {})
    branch = cast(dict[str, Any], worldness.get("branch_proof") or {})
    return {
        "source": {
            "kind": "gedcom",
            "private_local_input": True,
            "raw_bytes_read": len(raw),
            "rights": {
                "stage": "E3",
                "approved": True,
                "private_analysis": True,
                "external_model_processing": False,
                "package_inclusion": True,
                "public_export": False,
                "training": False,
            },
            "provenance_label": "public historical genealogy fixture; not authoritative research",
        },
        "api_studio": {
            "one_click": bool(one_click.get("package_id") and one_click.get("preview_id")),
            "build": bool(built.get("package_id")),
            "preview": bool(preview.get("preview_id")),
            "publish": bool(published.get("publishable")),
            "studio_ui": {
                "http_status": ui.status_code,
                "binary_upload": "content_base64" in ui.text,
                "worldness_control": "runWorldness" in ui.text,
                "living_control": "enterWorld" in ui.text,
            },
        },
        "product_refs": {
            "package_id": built.get("package_id"),
            "preview_id": preview.get("preview_id"),
            "manifest_hash_present": bool(built.get("manifest_hash")),
            "draft_id": built.get("draft_id"),
        },
        "job_status": status,
        "draft": _draft_evidence(draft),
        "diagnostics": status.get("diagnostics", []),
        "worldness": {
            "passed": worldness.get("passed"),
            "overall": worldness.get("overall"),
            "gates": worldness.get("gates", {}),
            "commit": {
                "committed": action.get("committed"),
                "proposal_validated": action.get("proposal_validated"),
                "replay_equal": action.get("replay_equal"),
            },
            "branch_isolated": branch.get("isolated"),
            "event_head": action.get("event_seq"),
        },
        "living": {
            "record_present": bool(living.get("living")),
            "perception_entities": len(entered.get("perception", {}).get("entities", [])),
            "perception_relations": len(entered.get("perception", {}).get("relations", [])),
        },
        "source_path_or_digest_emitted": False,
    }


def main() -> int:
    args = _parser().parse_args()
    print(json.dumps(run(args.file, job_id=args.job_id), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
