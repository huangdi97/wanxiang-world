"""Launch a repeatable local Chinese Player Experience human-test build."""

from __future__ import annotations

import os
from pathlib import Path

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from wanxiang_api.app import build_runtime, create_app
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = "sqlite:///./.pytest-tmp/m95-human-zh/wanxiang.db"
SOURCE_ID = "m95_human_zh_source"
JOB_ID = "m95_human_zh_job"


def _database_url() -> str:
    return os.environ.get("WANXIANG_DATABASE_URL", DEFAULT_DATABASE_URL)


def _prepare_sqlite_parent(database_url: str) -> None:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        return
    raw_path = database_url[len(prefix) :]
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)


def _upgrade(database_url: str) -> None:
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old


def source_record() -> SourceRecord:
    content = (
        "# Synthetic chapter\nCharacter: Alice\nCharacter: Bob\n"
        "Alice arrived at the Jiangnan water gate in 1985.\n"
        "Bob waited beside the night watcher's lane.\n"
        "relationship: Alice -> Bob\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id=SOURCE_ID,
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://{SOURCE_ID}",
        stage="E3",
        rights=RightsEnvelope(
            owner="m95-local-fixture-owner",
            usage="creator-owned synthetic acceptance fixture",
            approved=True,
            package_inclusion_allowed=True,
        ),
        payload=content,
        provenance="synthetic:m95-player-experience",
        access="private",
    )


def _seed(app: FastAPI) -> tuple[str, str]:
    authoring: AuthoringService = app.state.authoring
    result = OneClickAuthoring(authoring).run(JOB_ID, (source_record(),), profile="book")
    playable: PlayableService = app.state.playable
    profile = playable.register_package(
        result.package,
        owner_id="studio",
        visibility="public",
        display_name="江南机关城",
        description="一座沿水道展开的机关城，机关与人情都从清晨开始。",
        scenario_name="潮汐门初启",
        opening_hint="先听一听城门内外的水声，再决定往哪里走。",
    )
    character = playable.entry.create_character(
        "studio",
        "沈砚",
        compatible_profile_ids=(profile.profile_id,),
        character_id="ent_alice",
        identity="守夜人",
        intro="熟悉城门与水道的守夜人。",
        stance="谨慎观察",
        starting_location="沉水巷",
        knowledge_boundary="只知道自己亲眼见过的事。",
    )
    return profile.profile_id, character.character_id


def main() -> None:
    database_url = _database_url()
    _prepare_sqlite_parent(database_url)
    _upgrade(database_url)
    runtime = build_runtime(database_url)
    app = create_app(runtime)
    profile_id, character_id = _seed(app)
    host = os.environ.get("WANXIANG_HOST", "127.0.0.1")
    port = int(os.environ.get("WANXIANG_PORT", "8055"))
    print(f"Player URL: http://{host}:{port}/")
    print(f"Recommended world: 江南机关城 ({profile_id})")
    print(f"Recommended character: 沈砚 ({character_id})")
    print(f"Fixture source: {SOURCE_ID}; job: {JOB_ID}")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
