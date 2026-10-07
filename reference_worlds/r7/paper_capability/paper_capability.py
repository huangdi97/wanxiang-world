#!/usr/bin/env python3
"""Bounded executable wrapper over the pinned paper repository implementation."""

from __future__ import annotations

import json
import os
import sys
from importlib import util
from pathlib import Path


UPSTREAM = Path(__file__).parent / "upstream" / "optimality_search.py"


def _load_upstream() -> object:
    spec = util.spec_from_file_location("r7_pointcounts_optimality", UPSTREAM)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned upstream optimality_search.py")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--security"]:
        if os.environ.get("WANXIANG_SECRET"):
            print("unsafe")
            return 3
        print("safe")
        return 0
    if len(args) != 1:
        return 2
    try:
        q = int(args[0])
    except ValueError:
        return 2
    if q < 2 or q > 3:
        return 2

    module = _load_upstream()
    study = getattr(module, "study", None)
    if not callable(study):
        raise RuntimeError("pinned upstream module has no callable study")
    n_weil, n_images, collisions = study(q, 2)
    result = {
        "collisions": len(collisions),
        "images": n_images,
        "injective": n_weil == n_images,
        "q": q,
        "weil": n_weil,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
