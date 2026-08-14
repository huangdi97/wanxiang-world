"""Export the canonical OpenAPI contract consumed by the TS SDK (G13D).

The FastAPI app is the single source of truth for the public API vocabulary.
This script writes packages/sdk_ts/src/openapi-contract.json; the Python drift
test regenerates and compares, so a manually edited client is detected.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "packages" / "sdk_ts" / "src" / "openapi-contract.json"


def build_contract(app: Any) -> dict[str, Any]:
    spec = app.openapi()
    paths: dict[str, Any] = {}
    for path in sorted(spec.get("paths", {})):
        item = spec["paths"][path]
        paths[path] = {
            method: {"operationId": op.get("operationId", "")} for method, op in item.items()
        }
    return {
        "openapi": spec.get("openapi", "3.1.0"),
        "info": {"title": spec["info"]["title"], "version": spec["info"]["version"]},
        "paths": paths,
    }


def main() -> int:
    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    from wanxiang_api.app import create_app

    contract = build_contract(create_app())
    CONTRACT.write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")
    ops = sum(len(item) for item in contract["paths"].values())
    print(
        f"exported {len(contract['paths'])} paths / {ops} operations to {CONTRACT.relative_to(ROOT)}"  # noqa: E501
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
