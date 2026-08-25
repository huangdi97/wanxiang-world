"""Report resumable M79/M82 user-input gates without reading private files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def checkpoint(second_book: Path | None = None, gedcom: Path | None = None) -> dict[str, object]:
    missing: list[str] = []
    if second_book is None:
        missing.append("second_real_book_path")
    if gedcom is None:
        missing.append("gedcom_path")
    return {
        "package": "M79-M84",
        "status": "USER_INPUT_REQUIRED" if missing else "READY_TO_RESUME",
        "missing_inputs": missing,
        "private_local_sources": {
            "second_book": second_book is not None,
            "gedcom": gedcom is not None,
            "copied_to_git": False,
            "modified": False,
        },
        "resume": {
            "M79": "G82A" if second_book is None else "G82A_SOURCE_GATE_READY",
            "M82": "G85A" if gedcom is None else "G85A_SOURCE_GATE_READY",
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
