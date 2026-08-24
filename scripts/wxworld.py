"""No-API Source -> Living World reference CLI (G61C/G72G)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


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
    return parser


def _content(args: argparse.Namespace) -> str:
    if args.content is not None and args.file is not None:
        raise ValueError("use either --content or --file")
    if args.file is not None:
        return args.file.read_text(encoding="utf-8")
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
    authoring = OneClickAuthoring()
    result = authoring.run(
        args.job_id,
        (record,),
        profile=args.profile,
    )
    validation = authoring.service.package_validation(args.job_id)
    published = False
    if args.publish:
        authoring.publish(result)
        published = True
    status = authoring.service.status(args.job_id)
    return {
        "status": status.to_dict(),
        "package_id": result.package.package_id,
        "manifest_hash": result.package.manifest.content_hash,
        "preview_ref": result.preview.scoped_ref,
        "profile": result.source_profile,
        "publishable": validation.publish_ok,
        "published": published,
    }


def main() -> int:
    args = _parser().parse_args()
    if args.command == "reference":
        print(json.dumps(run_reference(args), ensure_ascii=False, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
