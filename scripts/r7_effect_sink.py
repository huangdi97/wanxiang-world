"""Reference HTTP effect sink for the R7 external-effect outbox.

This is a **reference** service that lives inside this repository. It is NOT a
third-party SaaS: it holds no credentials, reaches no external network and
stores nothing except a local JSONL journal. It exists so the outbox path can be
exercised against a real, out-of-process effect provider.

Endpoints::

    POST /effect            apply once per Idempotency-Key
    POST /effect/ambiguous  apply, then close the connection without answering
    POST /effect/slow       apply nothing, sleep, then answer applied
    POST /effect/fail       answer 503 without applying
    POST /effect/crash      apply, then os._exit(1) without answering
    GET  /journal           the journal rows as JSON
    GET  /health            {"ok": true, "applied": <count>}

Run it::

    uv run python scripts/r7_effect_sink.py --port 0 --journal <path>

On start it prints exactly one JSON line ``{"port": N, "journal": "..."}`` to
stdout, then serves until killed.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import socket
import threading
import time
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast
from urllib.parse import urlsplit

DEFAULT_SLOW_DELAY_MS = 3000
_JSON_CONTENT_TYPE = "application/json"


class _EffectState:
    """Thread-safe journal plus idempotency-key set for the reference sink."""

    def __init__(self, journal_path: Path) -> None:
        self.journal_path = journal_path
        self._lock = threading.Lock()
        self._applied_keys: set[str] = set()
        self._applied_count = 0
        self._rehydrate()

    def _rehydrate(self) -> None:
        for row in self.rows():
            key = row.get("key")
            if isinstance(key, str):
                self._applied_keys.add(key)
                self._applied_count += 1

    def rows(self) -> list[dict[str, object]]:
        """Read every journal row in append order; a missing file reads empty."""
        if not self.journal_path.is_file():
            return []
        rows: list[dict[str, object]] = []
        for line in self.journal_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = _as_object(json.loads(line))
            if row is not None:
                rows.append(row)
        return rows

    def applied_count(self) -> int:
        """Return how many distinct effects were applied so far."""
        with self._lock:
            return self._applied_count

    def apply(self, key: str, intent_id: str, operation: str) -> bool:
        """Apply once per idempotency key.

        SAFETY: the journal line is fsynced before this returns, so the durable
        fact of the effect precedes any response.

        Returns:
            True when this call applied the effect, False on a repeat.
        """
        with self._lock:
            if key in self._applied_keys:
                return False
            row: dict[str, object] = {
                "status": "applied",
                "key": key,
                "intentId": intent_id,
                "operation": operation,
                "at": datetime.now(UTC).isoformat(),
            }
            self._append_row(row)
            self._applied_keys.add(key)
            self._applied_count += 1
            return True

    def _append_row(self, row: Mapping[str, object]) -> None:
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(row), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        with self.journal_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())


class _EffectSinkServer(ThreadingHTTPServer):
    """Threading HTTP server that carries the shared effect state."""

    state: _EffectState

    def handle_error(self, request: object, client_address: object) -> None:
        """Suppress per-connection tracebacks; a broken pipe is expected here."""


class _EffectRequestHandler(BaseHTTPRequestHandler):
    """Serve the reference effect endpoints."""

    server_version = "wanxiang-r7-effect-sink/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: object) -> None:
        """Silence the default request log; stdout must carry one JSON line."""

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/journal":
            self._respond_json(200, {"rows": self._state().rows()})
        elif path == "/health":
            self._respond_json(200, {"ok": True, "applied": self._state().applied_count()})
        else:
            self._respond_json(404, {"status": "not_found"})

    def do_POST(self) -> None:
        route = urlsplit(self.path).path
        handlers: dict[str, Callable[[], None]] = {
            "/effect": self._handle_effect,
            "/effect/ambiguous": self._handle_ambiguous,
            "/effect/slow": self._handle_slow,
            "/effect/fail": self._handle_fail,
            "/effect/crash": self._handle_crash,
        }
        handler = handlers.get(route)
        if handler is None:
            self._respond_json(404, {"status": "not_found"})
        else:
            handler()

    def _handle_effect(self) -> None:
        key = self._idempotency_key()
        if not key:
            self._respond_json(400, {"status": "missing_idempotency_key"})
            return
        body = self._read_body()
        newly_applied = self._state().apply(
            key, _str_field(body, "intentId"), _str_field(body, "operation")
        )
        if newly_applied:
            self._respond_json(200, {"status": "applied", "externalRef": f"effect:{key}"})
        else:
            self._respond_json(200, {"status": "duplicate"})

    def _handle_ambiguous(self) -> None:
        self._apply_from_body()
        self._close_without_response()

    def _handle_crash(self) -> None:
        self._apply_from_body()
        os._exit(1)

    def _handle_slow(self) -> None:
        body = self._read_body()
        delay_ms = body.get("delayMs")
        if isinstance(delay_ms, (int, float)) and not isinstance(delay_ms, bool):
            delay_seconds = float(delay_ms) / 1000.0
        else:
            delay_seconds = DEFAULT_SLOW_DELAY_MS / 1000.0
        time.sleep(delay_seconds)
        self._respond_json(200, {"status": "applied"})

    def _handle_fail(self) -> None:
        self._read_body()
        self._respond_json(503, {"status": "failed"})

    def _apply_from_body(self) -> None:
        key = self._idempotency_key()
        body = self._read_body()
        if key:
            self._state().apply(key, _str_field(body, "intentId"), _str_field(body, "operation"))

    def _close_without_response(self) -> None:
        """Close the socket with no status line so the client sees a broken answer."""
        self.close_connection = True
        with contextlib.suppress(OSError):
            self.connection.shutdown(socket.SHUT_RDWR)

    def _idempotency_key(self) -> str:
        return self.headers.get("Idempotency-Key") or ""

    def _read_body(self) -> dict[str, object]:
        length = self.headers.get("Content-Length")
        size = int(length) if length is not None and length.isdigit() else 0
        raw = self.rfile.read(size) if size > 0 else b""
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return _as_object(parsed) or {}

    def _respond_json(self, status_code: int, payload: Mapping[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", _JSON_CONTENT_TYPE)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _state(self) -> _EffectState:
        server = self.server
        if not isinstance(server, _EffectSinkServer):
            raise RuntimeError("effect sink server is misconfigured")
        return server.state


def _str_field(body: Mapping[str, object], key: str) -> str:
    value = body.get(key)
    return value if isinstance(value, str) else ""


def _as_object(value: object) -> dict[str, object] | None:
    """Narrow a decoded JSON value to a string-keyed object.

    INVARIANT: the cast is confined to this one JSON boundary and only runs
    after the mapping check; no untyped value leaks past this point.
    """
    if not isinstance(value, dict):
        return None
    return cast("dict[str, object]", value)


def main(argv: list[str] | None = None) -> int:
    """Parse args, print the startup JSON line, then serve until killed."""
    parser = argparse.ArgumentParser(description="Reference R7 effect sink.")
    parser.add_argument("--port", type=int, default=0, help="Port; 0 selects an ephemeral port.")
    parser.add_argument("--journal", required=True, help="JSONL journal path.")
    args = parser.parse_args(argv)
    journal_path = Path(str(args.journal))
    server = _EffectSinkServer(("127.0.0.1", int(args.port)), _EffectRequestHandler)
    server.state = _EffectState(journal_path)
    port = int(server.server_address[1])
    print(json.dumps({"port": port, "journal": str(journal_path)}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
