"""Report resumable M79/M82 user-input gates without reading private files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _source_status(path: Path | None) -> dict[str, str]:
    """Validate only source-path metadata; never open or copy the source."""
    if path is None:
        return {"status": "missing", "reason": "path_not_provided"}
    try:
        resolved = path.expanduser().resolve(strict=False)
        if not resolved.is_file():
            return {"status": "invalid", "reason": "not_a_file"}
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            return {"status": "ready", "reason": "external_regular_file"}
        return {"status": "invalid", "reason": "inside_repository"}
    except OSError:
        return {"status": "invalid", "reason": "path_metadata_unreadable"}


def _resume_checkpoint(goal: str, status: str) -> str:
    if status == "ready":
        return f"{goal}_SOURCE_GATE_READY"
    if status == "invalid":
        return f"{goal}_SOURCE_GATE_INVALID"
    return goal


def checkpoint(second_book: Path | None = None, gedcom: Path | None = None) -> dict[str, object]:
    sources = {
        "second_book": _source_status(second_book),
        "gedcom": _source_status(gedcom),
    }
    missing: list[str] = []
    invalid: list[str] = []
    for key, input_name in (
        ("second_book", "second_real_book_path"),
        ("gedcom", "gedcom_path"),
    ):
        status = sources[key]["status"]
        if status == "missing":
            missing.append(input_name)
        elif status == "invalid":
            invalid.append(input_name)
    needs_input = bool(missing or invalid)
    return {
        "package": "M79-M84",
        "status": "USER_INPUT_REQUIRED" if needs_input else "READY_TO_RESUME",
        "missing_inputs": missing,
        "invalid_inputs": invalid,
        "source_validation": sources,
        "private_local_sources": {
            "second_book": sources["second_book"]["status"] == "ready",
            "gedcom": sources["gedcom"]["status"] == "ready",
            "copied_to_git": False,
            "modified": False,
        },
        "resume": {
            "M79": _resume_checkpoint("G82A", sources["second_book"]["status"]),
            "M82": _resume_checkpoint("G85A", sources["gedcom"]["status"]),
            "completed_independent_work": ("M80", "M81", "M83"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--second-book", type=Path)
    parser.add_argument("--gedcom", type=Path)
    args = parser.parse_args()
    print(json.dumps(checkpoint(args.second_book, args.gedcom), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
