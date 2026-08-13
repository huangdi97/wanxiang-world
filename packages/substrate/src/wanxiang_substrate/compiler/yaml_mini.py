"""Minimal safe YAML-subset parser (G04C).

Deliberately restricted: plain nested mappings with scalar values only. No
anchors/aliases, tags, flow collections, multi-doc or executable constructs.
Unsupported constructs fail loudly instead of executing anything.
"""

from __future__ import annotations

import re

from wanxiang_substrate.compiler.errors import MalformedSource

_KEY_VALUE = re.compile(r"^(\S[^:]*):\s*(.*)$")
_UNSUPPORTED_PREFIXES = ("&", "*", "!<", "---", "[", "{", "|", ">")
_SCALAR_TYPES = (str, int, float, bool, type(None))


def parse_yaml_subset(text: str) -> dict[str, object]:
    """Parse a restricted YAML mapping (nested mappings + scalars)."""
    if not text.strip():
        return {}
    lines = text.splitlines()
    if any(line.strip().startswith(_UNSUPPORTED_PREFIXES) for line in lines if line.strip()):
        raise MalformedSource("YAML anchors/aliases/tags/flow collections unsupported")
    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(0, root)]
    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()
        match = _KEY_VALUE.match(stripped)
        if match is None:
            raise MalformedSource(f"YAML line {line_number}: expected key: value")
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        key = match.group(1).strip()
        value_text = match.group(2).strip()
        if value_text == "":
            child: dict[str, object] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _scalar(value_text)
    return root


def _scalar(text: str) -> object:
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    if text in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text
