"""Generate a software-bill-of-materials inventory (G16F).

Parses uv.lock (Python) and pnpm-lock.yaml (JS) into a reproducible SBOM
inventory. Vulnerability scanning tooling is not available offline
(EXTERNAL_BLOCKED); the inventory enables manual/advisory review.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"


def python_packages() -> list[dict[str, str]]:
    text = (ROOT / "uv.lock").read_text(encoding="utf-8")
    data = tomllib.loads(text)
    out = []
    for pkg in data.get("package", []):
        out.append({"name": pkg.get("name", ""), "version": pkg.get("version", "")})
    return sorted(out, key=lambda p: (p["name"], p["version"]))


def js_packages() -> list[dict[str, str]]:
    import re

    text = (ROOT / "pnpm-lock.yaml").read_text(encoding="utf-8")
    out = []
    for line in text.splitlines():
        m = re.match(r"^  (?:@[^/]+/)?([^/]+)@(\d+\.\d+\.\d+):", line)
        if m:
            out.append({"name": m.group(1), "version": m.group(2)})
    # dedupe
    seen = set()
    unique = []
    for p in out:
        key = (p["name"], p["version"])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def main() -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    py = python_packages()
    js = js_packages()
    payload = {
        "python": py,
        "javascript": js,
        "note": "vulnerability scanning tool unavailable offline (EXTERNAL_BLOCKED)",
    }
    (ARTIFACTS / "sbom.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# SBOM Info (G16F)",
        "",
        f"- Python packages (uv.lock): {len(py)}",
        f"- JavaScript packages (pnpm-lock.yaml): {len(js)}",
        "",
        "## Python",
        "",
        "| Package | Version |",
        "|---|---|",
    ]
    for p in py[:200]:
        lines.append(f"| {p['name']} | {p['version']} |")
    lines += ["", "## JavaScript (deduped)", "", "| Package | Version |", "|---|---|"]
    for p in js[:200]:
        lines.append(f"| {p['name']} | {p['version']} |")
    lines += [
        "",
        "Machine-readable: artifacts/sbom.json.",
        "Vulnerability scanning (e.g., OSV/advisory) requires an offline tool or network: EXTERNAL_BLOCKED;",  # noqa: E501
        "the inventory supports manual advisory review.",
        "",
    ]
    (ARTIFACTS / "SBOM_INFO.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"SBOM: python={len(py)} js={len(js)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
