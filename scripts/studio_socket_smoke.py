"""Configurable-port browser Studio and API socket smoke."""

from __future__ import annotations

import json
import time
from threading import Thread
from urllib.request import urlopen

import uvicorn
from wanxiang_api.app import create_app

from reference_runtime import build_reference_runtime


def run_smoke() -> dict[str, object]:
    app = create_app(build_reference_runtime())
    config = uvicorn.Config(app, host="127.0.0.1", port=0, log_level="error")
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.02)
    if not server.started or not server.servers:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("uvicorn did not start on an OS-selected port")
    socket = server.servers[0].sockets[0]
    port = int(socket.getsockname()[1])
    base = f"http://127.0.0.1:{port}"
    try:
        with urlopen(f"{base}/healthz", timeout=5) as response:
            health = json.loads(response.read().decode("utf-8"))
        with urlopen(f"{base}/studio/ui", timeout=5) as response:
            studio = response.read().decode("utf-8")
    finally:
        server.should_exit = True
        thread.join(timeout=5)
    return {
        "port": port,
        "health": health,
        "studio_status": "Wanxiang Studio" in studio,
        "socket": "passed",
    }


if __name__ == "__main__":
    print(json.dumps(run_smoke(), ensure_ascii=False, sort_keys=True))
