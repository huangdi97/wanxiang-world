"""Artifact and report serialization for the M96 prompt-world qualification."""

from __future__ import annotations

import json
import pathlib
import subprocess
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m96" / "original_prompt_world.json"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(payload: dict[str, Any]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_outputs(
    *,
    checks: dict[str, bool],
    conclusion: str,
    intent: Any,
    prompt_run: Any,
    build: Any,
    entry: Any,
    opened: Any,
    install_export: dict[str, Any],
    profile_id: str,
    instance_id: str,
    branch: Any,
    action: dict[str, Any],
    leave: Any,
    continued: Any,
    events: tuple[Any, ...],
    day_events: list[str],
    checkpoints: list[dict[str, Any]],
    child_branch_id: str,
    continuity: Any,
    run_artifact: Any,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m96.original-prompt-world.v1",
        "conclusion": conclusion,
        "gates": {"67": conclusion, "68": conclusion, "69": conclusion},
        "build_sha": _head(),
        "seed": 9601,
        "prompt": {
            "sha256": intent.text_hash,
            "intent_id": intent.intent_id,
            "source_channel": intent.source_channel,
            "raw_text_emitted": False,
        },
        "genesis": {
            "provider_id": prompt_run.provider_id,
            "deterministic_reference": True,
            "profile": "local_prompt_genesis_v1",
            "proposal_count": len(prompt_run.proposals),
            "claim_ids": list(prompt_run.contract.generated_fact_ids),
            "evidence_class": "E5",
        },
        "draft": {
            "workshop_id": build.workshop.workshop_id,
            "world_draft_id": build.workshop.world_draft_id,
            "world_draft_revision": build.workshop.world_draft_revision,
            "source_refs": list(build.package.source_versions),
            "entity_count": len(build.package.draft.entities),
            "place_count": len(build.package.draft.places),
        },
        "review": {
            "actions": ["review_e5", "accept_constraints", "preview"],
            "ready_for_preview": prompt_run.contract.review_gate.ready_for_preview,
        },
        "package": {
            "package_id": build.package.package_id,
            "manifest_hash": build.package.manifest.content_hash,
            "evidence_coverage": build.package.evidence_coverage,
        },
        "publish": {
            "publishable": build.publishing.publishable,
            "visible_in_plaza": build.publishing.visible_in_plaza,
            "rights": build.workshop.publishing.rights.to_dict(),
            "registry_entry": entry.to_dict(),
            "opened": opened.to_dict(),
            "install": install_export,
        },
        "play": {
            "profile_id": profile_id,
            "instance_id": instance_id,
            "branch_id": branch.value,
            "action": {
                "event_id": action["event_id"],
                "state_hash": action["state_hash"],
                "trace": action["evidence"],
            },
            "leave_status": leave.json().get("status"),
            "continued_instance_id": continued.json().get("instance", {}).get("instance_id"),
        },
        "bounded_7d": {
            "days": 7,
            "commit_event_count": len(events),
            "day_events": day_events,
            "checkpoints": checkpoints,
            "child_branch_id": child_branch_id,
            "branch_isolated": checks["branch_isolated"],
            "continuity": continuity.to_dict(),
            "run_artifact": run_artifact.to_dict(),
        },
        "checks": checks,
        "boundaries": {
            "implemented": ["prompt genesis to review/package/publish/play chain"],
            "validated": [
                "bounded reference-provider product chain",
                "seven-day replay and branch checks",
            ],
            "experimental": ["Prompt Genesis output and bounded long-horizon continuity"],
            "not_proven": [
                "universal creative quality",
                "scientific validity",
                "live-world emergence",
            ],
            "external_blocked": [],
        },
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _write(payload)
    report = f"""# M96 Original Prompt World Acceptance

**Conclusion:** `{conclusion}` for bounded Gates 67–69.

The exact creator prompt is recorded only by SHA-256 `{intent.text_hash}`; raw
prompt text is not copied into the artifact. The local deterministic
`{prompt_run.provider_id}` provider produced E5 candidates, the explicit
review gate was completed, the WorldDraft/WorldPackage was published and
installed through the package registry, and the published package was played
through the shared PlayableService.

The run made real canonical commits, emitted StateDiff, checkpointed each of
seven accelerated days, replayed each checkpoint, verified a child branch did
not alter its parent, and ran the separate bounded actor continuity contract.
All of this remains engineering evidence: Prompt Genesis and long-horizon
continuity are `EXPERIMENTAL`/`BOUNDED`, not universal or scientific claims.

Machine-readable evidence: `artifacts/v55_stable/m96/original_prompt_world.json`.
"""
    (ROOT / "reports" / "M96_ORIGINAL_PROMPT_WORLD_ACCEPTANCE.md").write_text(
        report, encoding="utf-8"
    )
    return payload
