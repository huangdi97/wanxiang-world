"""Operator/dev CLI for persisted R7 runtime locks.

Run from the repository root::

    uv run python -m wanxiang_reality.lock_cli create-worldline --root DIR \\
        --world-id W --world-instance-id I --worldline-id L
    uv run python -m wanxiang_reality.lock_cli verify-worldline --root DIR --worldline-id L

``create-worldline`` composes the reference reality/world profiles and the
declared runtime facts, then opens the worldline with ``create_if_missing``.
``verify-worldline`` reads the stored lock and re-opens it against the reference
composition, translating the typed errors into a printed status instead of a
traceback. Both print exactly one JSON line on stdout.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import replace

from wanxiang_reality.contracts import SERVICE_CONTRACTS
from wanxiang_reality.errors import LockDriftError, LockStoreError, WanxiangRealityError
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.lock_store import FileLockStore
from wanxiang_reality.profiles import RealityProfile, WorldProfile
from wanxiang_reality.reference_profiles import (
    reference_provider_versions,
    reference_reality_profile,
    reference_schema_versions,
    reference_world_profile,
)
from wanxiang_reality.versions import Version
from wanxiang_reality.worldline_open import RuntimeFacts, WorldlineLockIdentity, open_worldline

DEFAULT_COMPOSITION_RUNTIME = "cordis"
DEFAULT_COMPOSITION_RUNTIME_VERSION = "4.0.0-rc.10"
_RUNTIME_CONFIG_SCHEMA = "wanxiang.r7.reference-runtime-config.v1"


def _emit(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")


def _pairs(values: list[str]) -> dict[str, str]:
    """Parse repeated ``name=value`` flags into a mapping."""
    result: dict[str, str] = {}
    for item in values:
        name, separator, value = item.partition("=")
        if not separator or not name or not value:
            raise WanxiangRealityError(f"expected name=value, got {item!r}")
        result[name] = value
    return result


def _service_contract_versions() -> dict[str, str]:
    return {contract.contract_id: contract.api_version for contract in SERVICE_CONTRACTS}


def _reference_runtime_config_hash() -> str:
    return canonical_digest({"schema": _RUNTIME_CONFIG_SCHEMA, "profile": "reference"})


def _default_facts(composition_runtime: str, composition_runtime_version: str) -> RuntimeFacts:
    return RuntimeFacts(
        composition_runtime=composition_runtime,
        composition_runtime_version=composition_runtime_version,
        service_contract_versions=_service_contract_versions(),
        provider_versions=reference_provider_versions(),
        artifact_hashes={},
        schema_versions=reference_schema_versions(),
        runtime_config_hash=_reference_runtime_config_hash(),
    )


def _reality(version_text: str) -> RealityProfile:
    return replace(reference_reality_profile(), version=Version.parse(version_text))


def _world(reality: RealityProfile, version: Version) -> WorldProfile:
    return replace(
        reference_world_profile(),
        version=version,
        reality_profile_ref=f"{reality.profile_id}@{reality.version}",
    )


def _create(args: argparse.Namespace) -> int:
    store = FileLockStore(pathlib.Path(args.root))
    reality = _reality(args.reality_version)
    base_world = reference_world_profile()
    world_version = (
        Version.parse(args.world_definition_version)
        if args.world_definition_version
        else base_world.version
    )
    world = _world(reality, world_version)
    facts = RuntimeFacts(
        composition_runtime=args.composition_runtime,
        composition_runtime_version=args.composition_runtime_version,
        service_contract_versions=_service_contract_versions(),
        provider_versions=_pairs(args.provider) or reference_provider_versions(),
        artifact_hashes=_pairs(args.artifact),
        schema_versions=_pairs(args.schema) or reference_schema_versions(),
        runtime_config_hash=_reference_runtime_config_hash(),
    )
    identity = WorldlineLockIdentity(
        world_id=args.world_id,
        world_definition_version=str(world_version),
        world_instance_id=args.world_instance_id,
        worldline_id=args.worldline_id,
    )
    try:
        outcome = open_worldline(
            identity=identity,
            reality=reality,
            world=world,
            facts=facts,
            store=store,
            create_if_missing=True,
        )
    except LockDriftError as exc:
        _emit(_status_payload(args.worldline_id, "DRIFT", None, exc.drifted_dimensions))
        return 1
    except LockStoreError:
        _emit(_status_payload(args.worldline_id, "TAMPERED", None, ()))
        return 1
    _emit(
        {
            "worldlineId": args.worldline_id,
            "status": outcome.status.value,
            "lockDigest": outcome.lock_digest,
            "revision": outcome.revision,
            "path": str(store.path_for(args.worldline_id)),
        }
    )
    return 0


def _verify(args: argparse.Namespace) -> int:
    store = FileLockStore(pathlib.Path(args.root))
    try:
        stored = store.read(args.worldline_id)
    except LockStoreError:
        _emit(_status_payload(args.worldline_id, "TAMPERED", None, ()))
        return 1
    if stored is None:
        _emit(_status_payload(args.worldline_id, "MISSING", None, ()))
        return 1
    lock = stored.lock
    identity = WorldlineLockIdentity(
        world_id=lock.world_id,
        world_definition_version=lock.world_definition_version,
        world_instance_id=lock.world_instance_id,
        worldline_id=lock.worldline_id,
    )
    try:
        outcome = open_worldline(
            identity=identity,
            reality=reference_reality_profile(),
            world=reference_world_profile(),
            facts=_default_facts(DEFAULT_COMPOSITION_RUNTIME, DEFAULT_COMPOSITION_RUNTIME_VERSION),
            store=store,
            create_if_missing=False,
        )
    except LockDriftError as exc:
        _emit(
            _status_payload(args.worldline_id, "DRIFT", stored.lock_digest, exc.drifted_dimensions)
        )
        return 1
    except LockStoreError:
        _emit(_status_payload(args.worldline_id, "TAMPERED", None, ()))
        return 1
    if outcome.status.value != "OPENED":
        _emit(
            _status_payload(
                args.worldline_id,
                "DRIFT",
                stored.lock_digest,
                tuple(entry.dimension for entry in outcome.drift),
            )
        )
        return 1
    _emit(_status_payload(args.worldline_id, "OPENED", stored.lock_digest, ()))
    return 0


def _status_payload(
    worldline_id: str, status: str, lock_digest: str | None, drift: tuple[str, ...]
) -> dict[str, object]:
    return {
        "worldlineId": worldline_id,
        "status": status,
        "lockDigest": lock_digest,
        "drift": list(drift),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wanxiang_reality.lock_cli")
    subcommands = parser.add_subparsers(dest="command", required=True)
    create = subcommands.add_parser("create-worldline", help="create and persist a worldline lock")
    create.add_argument("--root", required=True)
    create.add_argument("--world-id", required=True)
    create.add_argument("--world-instance-id", required=True)
    create.add_argument("--worldline-id", required=True)
    create.add_argument("--world-definition-version", default=None)
    create.add_argument("--reality-version", default="1")
    create.add_argument("--composition-runtime", default=DEFAULT_COMPOSITION_RUNTIME)
    create.add_argument(
        "--composition-runtime-version", default=DEFAULT_COMPOSITION_RUNTIME_VERSION
    )
    create.add_argument("--provider", action="append", default=[], metavar="name=version")
    create.add_argument("--schema", action="append", default=[], metavar="name=version")
    create.add_argument("--artifact", action="append", default=[], metavar="name=sha256")
    verify = subcommands.add_parser("verify-worldline", help="verify a persisted worldline lock")
    verify.add_argument("--root", required=True)
    verify.add_argument("--worldline-id", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI; return the process exit code."""
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "create-worldline":
            return _create(args)
        return _verify(args)
    except WanxiangRealityError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
