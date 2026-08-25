"""Sanitized API/Studio evidence runner for one private real source.

The source is read locally and sent only to the in-process product routes. The
JSON result contains counts, gate outcomes, and replay evidence, never a path,
digest, or source text.
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
    parser.add_argument("--kind", default="epub")
    parser.add_argument("--job-id", default="m79_real_source_api")
    return parser


def _request(client: TestClient, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    client_any: Any = client
    response: Any = client_any.request(method, path, **kwargs)
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"{method} {path} returned HTTP {response.status_code}: {response.text}")
    value: Any = response.json()
    if not isinstance(value, dict):
        raise RuntimeError(f"{method} {path} did not return an object")
    return cast(dict[str, Any], value)


def _source_payload(raw: bytes, *, kind: str) -> dict[str, Any]:
    if kind in {"epub", "docx", "pdf"}:
        return {"content": "", "content_base64": base64.b64encode(raw).decode("ascii")}
    return {"content": raw.decode("utf-8")}


def _sanitize_draft(value: dict[str, Any], *, kind: str) -> dict[str, Any]:
    draft = cast(dict[str, Any], value.get("draft") or {})
    candidates = cast(list[dict[str, Any]], value.get("candidates") or [])
    refs = [
        ref
        for candidate in candidates
        for ref in candidate.get("source_refs", [])
        if isinstance(ref, str)
    ]
    return {
        "status": draft.get("status"),
        "coverage": draft.get("coverage"),
        "uncertainty": draft.get("uncertainty"),
        "selected_domains": draft.get("selected_domains", []),
        "counts": {
            field: len(draft.get(field, []))
            for field in ("entities", "relations", "places", "events", "completion_items")
        },
        "candidate_count": len(candidates),
        "candidate_kind_counts": dict(
            sorted(Counter(item.get("kind", "") for item in candidates).items())
        ),
        "provider_ids": sorted({item.get("provider", "") for item in candidates}),
        "evidence_locator_count": sum(bool(item.get("evidence_refs")) for item in candidates),
        "nonempty_locator_count": len(refs),
        "format_locator_count": sum(ref.startswith(f"{kind}://") for ref in refs),
        "structured_locator_count": sum("href=" in ref or "spine=" in ref for ref in refs),
    }


def _spine_ref(value: str) -> str:
    marker = "spine="
    return value.partition(marker)[2].split(";", 1)[0] if marker in value else ""


def run(source: Path, *, kind: str, job_id: str) -> dict[str, Any]:
    raw = source.read_bytes()
    app = create_app(build_reference_runtime())
    client = TestClient(app)
    source_input = {
        "source_id": "m79_real_source_api",
        "kind": kind,
        **_source_payload(raw, kind=kind),
        "stage": "E3",
        "rights_approved": True,
        "access": "private",
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
            "profile": "book",
            "semantic_provider": "local",
            "sources": [source_input],
        },
    )
    draft = _request(client, "GET", f"/studio/jobs/{job_id}/draft")
    build_state = app.state.authoring.build(job_id)
    state_candidates = build_state.candidates if build_state is not None else ()
    identity_spines: dict[str, set[str]] = {}
    for candidate in state_candidates:
        if candidate.kind not in {"identity", "character"}:
            continue
        fields = candidate.fields
        key = fields.get("key") or fields.get("subject_key")
        if not key:
            continue
        identity_spines.setdefault(key, set()).update(
            spine for spine in (_spine_ref(ref) for ref in candidate.source_refs) if spine
        )
    cross_chapter_identity_keys = sum(len(spines) > 1 for spines in identity_spines.values())
    built = _request(client, "POST", f"/studio/jobs/{job_id}/build")
    preview = _request(client, "POST", f"/studio/jobs/{job_id}/preview")
    published = _request(client, "POST", f"/studio/jobs/{job_id}/publish")
    worldness = cast(
        dict[str, Any],
        _request(client, "POST", f"/studio/jobs/{job_id}/worldness").get("worldness") or {},
    )
    entered = _request(client, "POST", f"/studio/jobs/{job_id}/enter")
    living = _request(client, "GET", f"/studio/jobs/{job_id}/living")
    client_any: Any = client
    ui: Any = client_any.get("/studio/ui")
    action = cast(dict[str, Any], worldness.get("living", {}).get("action") or {})
    branch = cast(dict[str, Any], worldness.get("branch_proof") or {})
    dimensions = cast(list[dict[str, Any]], worldness.get("evidence") or [])
    return {
        "source": {
            "kind": kind,
            "private_local_only": True,
            "raw_bytes_read": len(raw),
            "rights": {
                "private_analysis": True,
                "external_model_processing": False,
                "package_inclusion": True,
                "public_export": False,
                "training": False,
            },
        },
        "api": {
            "one_click": "accepted",
            "build": "accepted" if built.get("package_id") else "missing",
            "preview": "accepted" if preview.get("preview_id") else "missing",
            "publish": bool(published.get("publishable")),
            "worldness": "accepted" if worldness.get("passed") else "failed",
            "enter": "accepted" if entered.get("perception") else "missing",
            "living_record": bool(living.get("living")),
            "studio_ui": {
                "http_status": ui.status_code,
                "binary_upload": "content_base64" in ui.text,
                "worldness_control": "runWorldness" in ui.text,
                "living_control": "enterWorld" in ui.text,
            },
        },
        "job_status": _request(client, "GET", f"/studio/jobs/{job_id}").get("status", {}),
        "draft": _sanitize_draft(draft, kind=kind),
        "structure": {
            "segment_kind_counts": dict(
                sorted(
                    Counter(
                        segment.kind for segment in (build_state.segments if build_state else ())
                    ).items()
                )
            ),
            "spine_locator_count": sum(
                bool(_spine_ref(segment.locator.ref))
                for segment in (build_state.segments if build_state else ())
            ),
            "cross_chapter_identity_key_count": cross_chapter_identity_keys,
            "identity_keys_with_locator_provenance": len(identity_spines),
        },
        "worldness": {
            "passed": worldness.get("passed"),
            "overall": worldness.get("overall"),
            "gates": worldness.get("gates", {}),
            "dimensions": [
                {"name": item.get("name"), "score": item.get("score")} for item in dimensions
            ],
            "commit": {
                "committed": action.get("committed"),
                "proposal_validated": action.get("proposal_validated"),
                "replay_equal": action.get("replay_equal"),
            },
            "branch_isolated": branch.get("isolated"),
            "repair": {
                "converged": worldness.get("repair", {}).get("converged"),
                "rounds": worldness.get("repair", {}).get("rounds"),
                "candidate_count": worldness.get("repair", {}).get("candidate_count"),
            },
        },
        "perception": {
            "entity_count": len(entered.get("perception", {}).get("entities", [])),
            "relation_count": len(entered.get("perception", {}).get("relations", [])),
        },
        "source_path_or_digest_emitted": False,
        "one_click_status_fields": sorted(one_click.get("status", {}).keys()),
    }


def main() -> int:
    args = _parser().parse_args()
    print(
        json.dumps(
            run(args.file, kind=args.kind, job_id=args.job_id),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
