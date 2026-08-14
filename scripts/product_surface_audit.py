"""Product surface contract audit (G18A)."""

from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent


def api_route_ownership() -> list[dict[str, str]]:
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    rows: list[dict[str, str]] = []
    for path, item in contract["paths"].items():
        for method, op in item.items():
            rows.append(
                {"method": method.upper(), "path": path, "operation_id": op.get("operationId", "")}
            )
    return rows


def surface_write_api() -> dict[str, list[str]]:
    """Surface write-method audit.

    `submit(...)` is the sanctioned command path (surfaces write only through
    the command API). Any other write-like method is a violation.
    """
    forbidden = {"append", "save", "record", "commit", "write", "mutate", "update"}
    violations: list[str] = []
    submit_sites: list[str] = []
    for py in (ROOT / "packages/sdk_ts/src").glob("*.ts"):
        if py.name.endswith(".test.ts") or py.name == "openapi.ts":
            continue
        text = py.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if "submit(" in stripped:
                submit_sites.append(f"{py.name}: {stripped}")
            elif any(f"{w}(" in stripped for w in forbidden):
                violations.append(f"{py.name}: {stripped}")
    return {"violations": violations, "submit_command_path": submit_sites}


def audit() -> dict[str, Any]:
    return {
        "routes": api_route_ownership(),
        "surface_write_api_candidates": surface_write_api(),
    }
