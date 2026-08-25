"""No-API Source -> Living World reference CLI (G61C/G72G)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wanxiang_domain.errors import WanxiangError
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

from reference_runtime import build_reference_runtime


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wxworld")
    sub = parser.add_subparsers(dest="command", required=True)
    reference = sub.add_parser("reference", help="run the deterministic authoring path")
    reference.add_argument("--source-id", default="cli_source")
    reference.add_argument("--kind", default="text")
    reference.add_argument("--content")
    reference.add_argument("--file", type=Path)
    reference.add_argument("--job-id", default="job_cli")
    reference.add_argument(
        "--profile", choices=("book", "family", "structured", "mixed"), default="book"
    )
    reference.add_argument("--publish", action="store_true")
    reference.add_argument("--instantiate", action="store_true")
    reference.add_argument("--worldness", action="store_true")
    reference.add_argument(
        "--semantic-provider",
        choices=("none", "local"),
        default="none",
        help="explicitly enable the bounded local semantic provider",
    )
    for name in (
        "create",
        "import",
        "status",
        "resume",
        "review",
        "build",
        "preview",
        "worldness",
        "instantiate",
        "publish",
    ):
        lifecycle = sub.add_parser(name, help=f"authoring lifecycle: {name}")
        lifecycle.add_argument("--source-id", default="cli_source")
        lifecycle.add_argument("--kind", default="text")
        lifecycle.add_argument("--content")
        lifecycle.add_argument("--file", type=Path)
        lifecycle.add_argument("--job-id", default=f"job_{name}")
        lifecycle.add_argument(
            "--profile", choices=("book", "family", "structured", "mixed"), default="book"
        )
        lifecycle.add_argument("--semantic-provider", choices=("none", "local"), default="none")
    return parser


def _content(args: argparse.Namespace) -> str:
    if args.content is not None and args.file is not None:
        raise ValueError("use either --content or --file")
    if args.file is not None:
        return args.file.read_bytes().decode("utf-8")
    return args.content or "# Reference\nAlice arrived in 1985.\nrule: keep promises\n"


def run_reference(args: argparse.Namespace) -> dict[str, object]:
    content = _content(args)
    record = SourceRecord(
        source_id=args.source_id,
        kind=args.kind,
        content_hash=payload_hash(content),
        content_ref=f"cli://{args.source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="cli-user", usage="reference", approved=True),
        payload=content,
        provenance="cli:reference",
        access="private",
    )
    providers = (
        ProviderRouter((LocalSemanticProvider(),))
        if args.semantic_provider == "local"
        else ProviderRouter()
    )
    authoring = OneClickAuthoring(AuthoringService(providers=providers))
    one_click = authoring.run(
        args.job_id,
        (record,),
        profile=args.profile,
        semantic_provider=("local" if args.semantic_provider == "local" else None),
    )
    validation = authoring.service.package_validation(args.job_id)
    published = False
    if args.publish:
        authoring.publish(one_click)
        published = True
    status = authoring.service.status(args.job_id)
    output: dict[str, object] = {
        "status": status.to_dict(),
        "package_id": one_click.package.package_id,
        "manifest_hash": one_click.package.manifest.content_hash,
        "preview_ref": one_click.preview.scoped_ref,
        "profile": one_click.source_profile,
        "publishable": validation.publish_ok,
        "published": published,
    }
    if args.instantiate or args.worldness:
        runtime = build_reference_runtime()
        living = authoring.service.instantiate_living(args.job_id, runtime)
        output["living"] = living.to_dict()
        if args.worldness:
            output["worldness"] = authoring.service.evaluate_worldness(
                args.job_id, runtime
            ).to_dict()
    return output


def run_lifecycle(args: argparse.Namespace) -> dict[str, object]:
    """Execute each named lifecycle command through the shared service facade."""
    content = _content(args)
    record = SourceRecord(
        source_id=args.source_id,
        kind=args.kind,
        content_hash=payload_hash(content),
        content_ref=f"cli://{args.source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="cli-user", usage="reference", approved=True),
        payload=content,
        provenance="cli:lifecycle",
        access="private",
    )
    providers = (
        ProviderRouter((LocalSemanticProvider(),))
        if args.semantic_provider == "local"
        else ProviderRouter()
    )
    authoring = OneClickAuthoring(AuthoringService(providers=providers))
    semantic = "local" if args.semantic_provider == "local" else None
    service = authoring.service
    if args.command == "create":
        snapshot = service.create_job(args.job_id, sources=(record,), semantic_provider=semantic)
        return {"command": args.command, "status": snapshot.to_dict()}
    service.create_job(args.job_id, sources=(record,), semantic_provider=semantic)
    status = service.resume(args.job_id) if args.command == "resume" else service.start(args.job_id)
    if args.command == "status":
        return {"command": args.command, "status": status.to_dict()}
    if args.command == "review":
        items = service.review_inbox(args.job_id)
        if items:
            service.review_candidate(
                args.job_id,
                items[0].candidate.candidate_id,
                action="approve",
                reviewer="cli",
                rationale="lifecycle review smoke",
            )
        return {
            "command": args.command,
            "status": service.status(args.job_id).to_dict(),
            "review_items": len(items),
        }
    package = service.build_package(args.job_id)
    output: dict[str, object] = {
        "command": args.command,
        "status": service.status(args.job_id).to_dict(),
        "package_id": package.package_id,
    }
    if args.command in ("preview", "worldness", "instantiate", "publish"):
        install = service.preview(args.job_id)
        output["preview"] = {
            "preview_id": install.preview_id,
            "scoped_ref": install.scoped_ref,
        }
    if args.command in ("worldness", "instantiate", "publish"):
        runtime = build_reference_runtime()
        output["living"] = service.instantiate_living(args.job_id, runtime).to_dict()
        if args.command == "worldness":
            output["worldness"] = service.evaluate_worldness(args.job_id, runtime).to_dict()
    if args.command == "publish":
        output["published"] = service.publish(args.job_id).publish_ok
    output["status"] = service.status(args.job_id).to_dict()
    return output


def main() -> int:
    args = _parser().parse_args()
    if args.command in (
        {"reference"}
        | {
            "create",
            "import",
            "status",
            "resume",
            "review",
            "build",
            "preview",
            "worldness",
            "instantiate",
            "publish",
        }
    ):
        try:
            result = run_reference(args) if args.command == "reference" else run_lifecycle(args)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        except WanxiangError as exc:
            print(
                json.dumps(
                    {"status": "blocked", "error": exc.to_primitive()},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
