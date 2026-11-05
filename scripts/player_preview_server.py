"""Serve the Player Experience locally so a human can review the real product.

This is a review convenience, not a product surface: it wires the same
authoritative runtime the tests use (SQLite persistence, deterministic preview
resolvers, no provider credentials, no network calls) and serves the Player UI
plus the Studio import surface on one address.
"""

from __future__ import annotations

import argparse
import os
import pathlib

from alembic import command
from alembic.config import Config

ROOT = pathlib.Path(__file__).resolve().parents[1]


def upgrade(database_url: str) -> None:
    """Apply migrations so the preview database is usable."""

    previous = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = previous


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Wanxiang Player for human review.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--db",
        default=str(pathlib.Path(".pytest-tmp") / "preview" / "player_preview.sqlite"),
        help="SQLite file used by the preview runtime (created on first run).",
    )
    args = parser.parse_args()

    import uvicorn
    from wanxiang_api.app import build_runtime, create_app

    database = pathlib.Path(args.db)
    database.parent.mkdir(parents=True, exist_ok=True)
    database_url = f"sqlite:///{database.as_posix()}"
    upgrade(database_url)
    app = create_app(build_runtime(database_url))
    print(f"Player:  http://{args.host}:{args.port}/")
    print(f"Studio:  http://{args.host}:{args.port}/studio/ui  (import a source here)")
    print("Locale:  add ?locale=en-US for the English Player")
    print(f"Runtime: {database_url}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
