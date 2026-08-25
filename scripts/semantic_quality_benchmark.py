"""Run the anonymized M80 semantic Gold Set benchmark."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.quality.semantic_benchmark import sample_candidates
from wanxiang_substrate.quality.semantic_metrics import evaluate_gold_set
from wanxiang_substrate.quality.semantic_models import GoldAssertion, GoldSet

ROOT = Path(__file__).resolve().parent.parent


def _candidate(
    candidate_id: str, kind: str, payload: dict[str, str], ref: str
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m80_anonymized_fixture",
        payload=tuple(sorted(payload.items())),
        confidence=0.9,
        source_refs=(ref,),
        distiller_version=1,
    )


def build_anonymized_fixture() -> tuple[tuple[CandidateEnvelope, ...], GoldSet]:
    rows = (
        ("id_ada", "identity", {"key": "ada", "display_name": "Ada"}, "book#p/1"),
        ("alias_ada", "alias", {"identity_key": "ada", "alias": "A"}, "book#p/2"),
        (
            "event_departure",
            "event",
            {"event_type": "departure", "date": "1980", "participants": "ada"},
            "book#p/3",
        ),
        (
            "event_return",
            "event",
            {"event_type": "return", "date": "1990", "participants": "ada"},
            "book#p/4",
        ),
        (
            "event_unknown",
            "event",
            {
                "event_type": "meeting",
                "date": "unknown",
                "uncertain": "true",
                "participants": "ada",
            },
            "book#p/5",
        ),
        (
            "relation_ada_bob",
            "relation",
            {"source_key": "ada", "target_key": "bob", "relation_type": "friend"},
            "book#p/6",
        ),
        ("place_harbor", "place", {"name": "Harbor"}, "book#p/7"),
        ("org_guild", "organization", {"name": "Guild"}, "book#p/8"),
        (
            "boundary_ada",
            "knowledge_boundary",
            {"subject_key": "ada", "boundary": "observed_only"},
            "book#p/9",
        ),
    )
    candidates = tuple(_candidate(*row) for row in rows)
    sampled, manifest = sample_candidates(candidates, sample_size=12, seed=83)
    assertions = tuple(
        GoldAssertion(
            candidate.candidate_id,
            candidate.kind,
            True,
            tuple(candidate.payload),
            candidate.source_refs,
            expected_uncertain=(candidate.fields.get("uncertain") == "true")
            if candidate.kind == "event"
            else None,
            expected_order=(1 if candidate.candidate_id == "event_departure" else 2)
            if candidate.candidate_id in {"event_departure", "event_return"}
            else None,
            expected_merge_target="ada" if candidate.kind == "alias" else "",
        )
        for candidate in sampled
    )
    return candidates, GoldSet("m80-v1", assertions, manifest)


def run() -> dict[str, object]:
    candidates, gold = build_anonymized_fixture()
    report = evaluate_gold_set(candidates, gold)
    return {"sampling": gold.sampling.to_dict(), "report": report.to_dict()}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    output = run()
    target = ROOT / "artifacts" / "m79_m84" / "semantic_quality_benchmark.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
