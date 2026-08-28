"""Qualify bounded emergence candidates and a no-pattern control (G101D)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime  # noqa: E402
from wanxiang_domain.hashing import semantic_sha256  # noqa: E402
from wanxiang_substrate.evolution import PatternObservationStore  # noqa: E402
from wanxiang_substrate.playable import PlayableService  # noqa: E402

from m98_burn_in_support import SOURCE_HASH, register_resolvers, write_json  # noqa: E402
from m98_emergence_support import (  # noqa: E402
    candidates,
    null_control,
    open_world,
    positive_detections,
    status_events,
)

ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "emergence_controls.json"
REPORT = ROOT / "reports" / "M98_G101D_EMERGENCE_CONTROLS.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def run() -> dict[str, Any]:
    db_path = fresh_db_path()
    build_sha = _head()
    try:
        runtime = make_world_runtime(db_path, extra_resolvers=register_resolvers)
        playable = PlayableService(runtime)
        positive_instance, positive_branch, positive_actors, positive_source = open_world(
            runtime, playable, "positive"
        )
        positive_events = status_events(
            runtime,
            playable,
            positive_instance,
            "g101d_positive_owner",
            count=9,
            prefix="watch",
            target=positive_actors["Bob"],
        )
        state_before = runtime.current_state(positive_instance, positive_branch)
        detections = positive_detections(positive_events)
        candidate_evidence = candidates(detections, positive_actors, positive_source)
        state_after = runtime.current_state(positive_instance, positive_branch)
        events_after = runtime.events(positive_instance, positive_branch)

        control_instance, control_branch, control_actors, _ = open_world(
            runtime, playable, "control"
        )
        control_events = status_events(
            runtime,
            playable,
            control_instance,
            "g101d_control_owner",
            count=3,
            prefix="burst",
            target=control_actors["Bob"],
        )
        control_evidence = null_control(control_events)
        organization_candidate = candidate_evidence["organization_candidate"]
        institution_candidate = candidate_evidence["institution_candidate"]
        ontology_candidate = candidate_evidence["ontology_candidate"]
        checks = {
            "positive_pattern_repeatable": len(detections) == 3
            and all(item.qualified for item in detections),
            "norm_candidates_eligible": all(
                item["eligible"] for item in candidate_evidence["norm_evaluations"]
            ),
            "organization_candidate_reviewed": organization_candidate["approved"] is True,
            "institution_candidate_reviewed": institution_candidate["approved"] is True,
            "ontology_candidate_reviewed": ontology_candidate["approved"] is True
            and candidate_evidence["ontology_validation"] is True,
            "control_not_qualified": control_evidence["detection"]["qualified"] is False,
            "control_norm_rejected": control_evidence["norm_candidate_rejected"] is True,
            "candidate_operations_do_not_mutate_canon": state_after.semantic_hash()
            == state_before.semantic_hash()
            and events_after == positive_events,
        }
        payload: dict[str, Any] = {
            "schema": "wanxiang.v5.5.m98.emergence-controls.v1",
            "conclusion": "PASS" if all(checks.values()) else "FAIL",
            "build_sha": build_sha,
            "seed": 10104,
            "input_hashes": {"source_sha256": SOURCE_HASH},
            "positive_world": {
                "world_ref": positive_instance.value,
                "branch_ref": positive_branch.value,
                "event_count": len(positive_events),
                "observation_window_size": 1,
                "observation_cache_hash": PatternObservationStore.rebuild(
                    positive_events, window_size=1
                ).cache_hash(),
                "candidate_evidence": candidate_evidence,
            },
            "null_control": {
                "world_ref": control_instance.value,
                "branch_ref": control_branch.value,
                "event_count": len(control_events),
                "evidence": control_evidence,
            },
            "checks": checks,
            "safety": {
                "candidate_layer_only": True,
                "ontology_law_institution_auto_commit": False,
                "canonical_state_and_history_unchanged_by_candidate_derivation": checks[
                    "candidate_operations_do_not_mutate_canon"
                ],
                "promotion_boundary_invoked": False,
            },
            "evidence_hash": semantic_sha256(
                {
                    "positive": candidate_evidence["candidate_evidence_hash"],
                    "control": control_evidence,
                    "checks": checks,
                }
            ),
            "boundaries": {
                "implemented": [
                    "repeat-pattern detector over committed event history",
                    "norm/organization/institution/ontology candidate derivation",
                    "null-control rejection and candidate-only safety check",
                ],
                "validated": ["bounded positive recurrence and false-positive control"],
                "experimental": ["emergence interpretation"],
                "not_proven": [
                    "universal emergence",
                    "scientific causality",
                    "production or live-world generalization",
                ],
                "external_blocked": [],
            },
        }
        write_json(ARTIFACT, payload)
        REPORT.write_text(
            f"""# M98 G101D Bounded Emergence Controls

**Conclusion:** `{payload["conclusion"]}`.

This run uses creator-owned synthetic input and a real migrated SQLite
WorldRuntime. The positive world produced nine committed status actions across
three one-tick windows, yielding three qualified repeated-pattern detections and
norm, organization, institution, and ontology candidates. A separate no-pattern
control produced three status actions inside one 100-tick window; its detection
was not qualified and norm creation was rejected by the existing threshold.

All candidate derivation and review operations were kept outside Canonical
Reality. No Ontology/Law/Institution promotion was invoked; the positive world
state hash and event history remained unchanged after candidate processing.
This is bounded detector calibration, not a universal-emergence, scientific,
production, or live-customer claim.

Build SHA: `{build_sha}`. Input hash: `{SOURCE_HASH}`.

Machine-readable evidence: `artifacts/v55_stable/m98/emergence_controls.json`.
""",
            encoding="utf-8",
        )
        return payload
    finally:
        cleanup_db_file(db_path)


if __name__ == "__main__":
    result = run()
    print(json.dumps({key: result[key] for key in ("conclusion", "build_sha")}, indent=2))
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
