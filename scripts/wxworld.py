"""No-API Source -> Living World reference CLI (G61C/G72G)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wanxiang_substrate.authoring.service import AuthoringService
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
    service = AuthoringService()
    service.create_job(args.job_id, sources=(record,), created_by="cli")
    service.start(args.job_id)
    package = service.build_package(args.job_id)
    install = service.preview(args.job_id)
    return {
        "status": service.status(args.job_id).to_dict(),
        "package_id": package.package_id,
        "manifest_hash": package.manifest.content_hash,
        "preview_ref": install.scoped_ref,
    }


def main() -> int:
    args = _parser().parse_args()
    if args.command == "reference":
        print(json.dumps(run_reference(args), ensure_ascii=False, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
