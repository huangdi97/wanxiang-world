"""SDK public-API baseline generator (G17A).

Snapshots the stable extension surface: FastAPI routes (from the OpenAPI
contract), the TypeScript SDK surface, and public (non-underscore) names of the
stable Python packages. Used by the compatibility test to detect breaking
changes.
"""

from __future__ import annotations

import ast
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

STABLE_PY_PACKAGES = (
    "wanxiang_domain",
    "wanxiang_application",
    "wanxiang_runtime",
    "wanxiang_substrate",
    "wanxiang_persistence",
    "wanxiang_observability",
)


def api_routes() -> list[str]:
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    return sorted(
        f"{method.upper()} {path}"
        for path in contract["paths"]
        for method in contract["paths"][path]
    )


def ts_surface() -> list[str]:
    names: set[str] = set()
    for py in (ROOT / "packages/sdk_ts/src").glob("*.ts"):
        if py.name.endswith(".test.ts"):
            continue
        text = py.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("export "):
                names.add(line.split(" ")[1].split("<")[0].split("(")[0])
    return sorted(names)


def python_surface() -> list[str]:
    names: set[str] = set()
    for pkg in STABLE_PY_PACKAGES:
        for py in (ROOT / "packages").rglob("*.py"):
            if f"/{pkg}/" not in str(py).replace("\\", "/"):
                continue
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except (SyntaxError, OSError):
                continue
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not node.name.startswith("_"):
                        names.add(f"{pkg}.{node.name}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith("_"):
                            names.add(f"{pkg}.{target.id}")
    return sorted(names)


def build() -> dict[str, Any]:
    return {
        "api_routes": api_routes(),
        "ts_surface": ts_surface(),
        "python_surface": python_surface(),
    }


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    data = build()
    (REPORTS / "sdk_api_baseline.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    lines = [
        "# SDK API Baseline (G17A)",
        "",
        f"- API routes: {len(data['api_routes'])}",
        f"- TypeScript surface symbols: {len(data['ts_surface'])}",
        f"- Python public names (stable packages): {len(data['python_surface'])}",
        "",
        "## API routes",
        "",
    ]
    for r in data["api_routes"]:
        lines.append(f"- `{r}`")
    lines += ["", "## Python public names (stable)", ""]
    for n in data["python_surface"][:300]:
        lines.append(f"- `{n}`")
    lines += ["", "Machine-readable: reports/sdk_api_baseline.json.", ""]
    (REPORTS / "SDK_API_BASELINE.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"routes={len(data['api_routes'])} ts={len(data['ts_surface'])} py={len(data['python_surface'])}"  # noqa: E501
    )
