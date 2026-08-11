"""Generate the committed golden replay fixture.

Writes tests/fixtures/golden_replay_v1.json containing the serialized fixture
events and the expected final semantic hash. Run from the repository root:

    uv run python scripts/generate_golden_fixture.py

The committed fixture is the golden value: replay regression tests compare
against it, and a legitimate semantic change updates it with documented
rationale in the changelog.
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tests.helpers.replay_fixture import INSTANCE, build_fixture_events  # noqa: E402
from wanxiang_domain.serialization_history import event_to_primitive  # noqa: E402
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion  # noqa: E402
from wanxiang_runtime.replay import ReplayEngine  # noqa: E402


def main() -> int:
    events = build_fixture_events()
    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    final_state = engine.replay(events)
    payload = {
        "schema_version": 1,
        "instance_id": INSTANCE.value,
        "expected_semantic_hash": final_state.semantic_hash(),
        "events": [event_to_primitive(e) for e in events],
    }
    target = ROOT / "tests/fixtures/golden_replay_v1.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {target}")
    print(f"expected_semantic_hash={payload['expected_semantic_hash']}")
    print(f"events={len(events)} final_revision={final_state.revision.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
