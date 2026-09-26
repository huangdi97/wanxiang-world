"""Behaviour of the JSON-RPC 2.0 over-stdio history-authority server."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from wanxiang_reality.contracts import SERVICE_CONTRACTS
from wanxiang_reality.rpc import HistoryAuthority, RpcError, dispatch, serve_stdio
from wanxiang_reality.rpc_support import seam_digest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[3]
HEX64 = re.compile(r"^[0-9a-f]{64}$")

INFO = {
    "server": "wanxiang-reality-rpc",
    "version": "0.1.0",
    "schema": "wanxiang.r7.history-rpc.v1",
}


def parse_object(text: str) -> dict[str, object]:
    parsed: object = json.loads(text)
    assert isinstance(parsed, dict)
    return cast(dict[str, object], parsed)


def call(
    a: HistoryAuthority, method: str, params: dict[str, object] | None = None
) -> dict[str, object]:
    return dispatch(a, method, params or {})


def request(
    request_id: int, method: str, params: dict[str, object] | None = None
) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}


def grant_token(a: HistoryAuthority, holder: str = "h1") -> str:
    call(a, "authority.register_holder", {"holderId": holder, "auditRef": "a1"})
    token = call(a, "authority.grant", {"holderId": holder})["capabilityToken"]
    assert isinstance(token, str)
    return token


def ev(event_id: str) -> dict[str, object]:
    return {"eventId": event_id, "kind": "observed", "payloadDigest": f"d-{event_id}"}


def params(
    worldline: str, revision: int, events: Sequence[dict[str, object]], token: str
) -> dict[str, object]:
    return {
        "worldlineId": worldline,
        "expectedRevision": revision,
        "events": list(events),
        "capabilityToken": token,
    }


def fold(events: Sequence[dict[str, object]]) -> str:
    state = ""
    for item in events:
        material = f"{state}|{item['eventId']}:{item['payloadDigest']}"
        state = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return state


def untouched(a: HistoryAuthority, worldline: str) -> None:
    assert call(a, "history.head", {"worldlineId": worldline}) == {"revision": 0, "stateHash": ""}
    assert call(a, "history.worldlines") == {"worldlines": []}


def run(lines: Sequence[str]) -> list[dict[str, object]]:
    writer = io.StringIO()
    serve_stdio(io.StringIO("\n".join(lines)), writer)
    return [parse_object(line) for line in writer.getvalue().splitlines()]


def result(response: dict[str, object]) -> dict[str, object]:
    value = response["result"]
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def error(response: dict[str, object]) -> dict[str, object]:
    value = response["error"]
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def test_runtime_info_reports_frozen_server_identity() -> None:
    assert call(HistoryAuthority(), "runtime.info") == INFO


def test_seam_digest_matches_the_frozen_sha256_rule() -> None:
    response = call(HistoryAuthority(), "seam.digest")
    contracts = [{"id": c.contract_id, "apiVersion": c.api_version} for c in SERVICE_CONTRACTS]
    contracts.sort(key=lambda entry: entry["id"])
    encoded = json.dumps(contracts, separators=(",", ":"), ensure_ascii=False)
    assert response["digest"] == hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    assert response["contracts"] == contracts


def test_seam_digest_is_stable_and_changes_when_a_contract_is_added() -> None:
    baseline = seam_digest(SERVICE_CONTRACTS)
    extra = replace(SERVICE_CONTRACTS[0], namespace="wanxiang.extra", service_id="extra")
    assert seam_digest(SERVICE_CONTRACTS) == baseline
    assert seam_digest((*SERVICE_CONTRACTS, extra)) != baseline


def test_register_holder_is_idempotent_and_returns_the_frozen_shape() -> None:
    a = HistoryAuthority()
    first = call(a, "authority.register_holder", {"holderId": "h1", "auditRef": "a1"})
    second = call(a, "authority.register_holder", {"holderId": "h1", "auditRef": "a2"})
    assert first == second == {"holderId": "h1", "registered": True}


def test_grant_issues_a_distinct_token_per_call() -> None:
    a = HistoryAuthority()
    call(a, "authority.register_holder", {"holderId": "h1", "auditRef": "a1"})
    first = call(a, "authority.grant", {"holderId": "h1"})["capabilityToken"]
    second = call(a, "authority.grant", {"holderId": "h1"})["capabilityToken"]
    assert isinstance(first, str) and isinstance(second, str) and first != second


def test_grant_denies_unknown_holder_with_32002() -> None:
    with pytest.raises(RpcError) as excinfo:
        call(HistoryAuthority(), "authority.grant", {"holderId": "ghost"})
    assert excinfo.value.code == -32002
    assert excinfo.value.data.get("reason") == "unknown-holder"


def test_append_without_a_valid_capability_token_is_denied_and_changes_nothing() -> None:
    a = HistoryAuthority()
    missing: dict[str, object] = {"worldlineId": "w1", "expectedRevision": 0, "events": [ev("e1")]}
    unknown = params("w1", 0, [ev("e1")], "unknown-token")
    wrong_type = params("w1", 0, [ev("e1")], "unused-token")
    wrong_type["capabilityToken"] = 123
    for denied in (missing, unknown, wrong_type):
        with pytest.raises(RpcError) as excinfo:
            call(a, "history.append", denied)
        assert excinfo.value.code == -32002
    untouched(a, "w1")


def test_stale_expected_revision_is_rejected_without_state_change() -> None:
    a = HistoryAuthority()
    token = grant_token(a)
    first = call(a, "history.append", params("w1", 0, [ev("e1")], token))
    with pytest.raises(RpcError) as excinfo:
        call(a, "history.append", params("w1", 0, [ev("e2")], token))
    assert excinfo.value.code == -32001
    assert excinfo.value.data == {"expectedRevision": 0, "actualRevision": 1}
    head = call(a, "history.head", {"worldlineId": "w1"})
    assert head == {"revision": 1, "stateHash": first["stateHash"]}
    tail = call(a, "history.read", {"worldlineId": "w1", "fromRevision": 0})
    assert tail == {"events": [ev("e1")]}


def test_append_with_empty_or_malformed_events_is_rejected_with_invalid_params() -> None:
    a = HistoryAuthority()
    token = grant_token(a)
    malformed: dict[str, object] = {"eventId": "e1", "kind": 7, "payloadDigest": "d1"}
    for bad in ([], [malformed]):
        with pytest.raises(RpcError) as excinfo:
            call(a, "history.append", params("w1", 0, bad, token))
        assert excinfo.value.code == -32602
    untouched(a, "w1")


def test_state_hash_fold_is_invariant_to_batch_splitting() -> None:
    a = HistoryAuthority()
    token = grant_token(a)
    events = [ev("e1"), ev("e2"), ev("e3")]
    single = call(a, "history.append", params("single", 0, events, token))
    split = call(a, "history.append", params("split", 0, events[:1], token))
    split = call(a, "history.append", params("split", 1, events[1:], token))
    step: dict[str, object] = {}
    for index, item in enumerate(events):
        step = call(a, "history.append", params("step", index, [item], token))
    assert [single["revision"], split["revision"], step["revision"]] == [3, 3, 3]
    assert single["stateHash"] == split["stateHash"] == step["stateHash"] == fold(events)


def test_history_read_returns_only_the_requested_tail() -> None:
    a = HistoryAuthority()
    events = [ev("e1"), ev("e2"), ev("e3")]
    call(a, "history.append", params("w1", 0, events, grant_token(a)))
    first_two = call(a, "history.read", {"worldlineId": "w1", "fromRevision": 1})
    assert first_two == {"events": [ev("e2"), ev("e3")]}
    assert call(a, "history.read", {"worldlineId": "w1", "fromRevision": 3}) == {"events": []}
    assert call(a, "history.read", {"worldlineId": "w1", "fromRevision": 0}) == {"events": events}
    assert call(a, "history.read", {"worldlineId": "other", "fromRevision": 0}) == {"events": []}


def test_history_worldlines_are_sorted_ascending() -> None:
    a = HistoryAuthority()
    for worldline in ("zeta", "alpha", "mid"):
        call(a, "history.append", params(worldline, 0, [ev("e")], grant_token(a)))
    assert call(a, "history.worldlines") == {"worldlines": ["alpha", "mid", "zeta"]}


def test_head_and_checkpoint_agree_for_new_and_written_worldlines() -> None:
    a = HistoryAuthority()
    empty = {"revision": 0, "stateHash": ""}
    assert call(a, "history.head", {"worldlineId": "never"}) == empty
    assert call(a, "history.checkpoint", {"worldlineId": "never"}) == empty
    call(a, "history.append", params("w1", 0, [ev("e1")], grant_token(a)))
    head = call(a, "history.head", {"worldlineId": "w1"})
    assert call(a, "history.checkpoint", {"worldlineId": "w1"}) == head


def test_stdio_skips_blank_lines_and_returns_frozen_error_codes() -> None:
    responses = run(
        [
            "",
            "   ",
            "[1,2,3]",
            '{"jsonrpc":"2.0","method":"history.head"}',
            '{"id":1,"method":"history.head"}',
            "{not json",
            '{"jsonrpc":"2.0","id":7,"method":"nope"}',
        ]
    )
    assert [error(r)["code"] for r in responses] == [-32600, -32600, -32600, -32700, -32601]
    assert [r["id"] for r in responses] == [None, None, 1, None, 7]


def server_command() -> list[str]:
    probe = subprocess.run(
        [sys.executable, "-c", "import wanxiang_reality.rpc"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode == 0:
        return [sys.executable, "-m", "wanxiang_reality.rpc", "--stdio"]
    if "No module named" in probe.stderr:
        pytest.skip(f"sys.executable cannot import wanxiang_reality.rpc: {probe.stderr.strip()}")
    pytest.fail(f"wanxiang_reality.rpc failed to import: {probe.stderr.strip()}")


def round_trip(process: subprocess.Popen[str], message: dict[str, object]) -> dict[str, object]:
    assert process.stdin is not None and process.stdout is not None
    process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    process.stdin.flush()
    line = process.stdout.readline()
    assert line, "server closed stdout before answering"
    return parse_object(line)


def test_subprocess_serves_info_digest_append_and_conflict_over_stdio() -> None:
    process = subprocess.Popen(
        server_command(),
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        info = round_trip(process, request(1, "runtime.info"))
        digest = round_trip(process, request(2, "seam.digest"))
        holder: dict[str, object] = {"holderId": "h1", "auditRef": "a1"}
        registered = round_trip(process, request(3, "authority.register_holder", holder))
        granted = round_trip(process, request(4, "authority.grant", holder))
        token = result(granted)["capabilityToken"]
        assert isinstance(token, str)
        fresh = params("w1", 0, [ev("e1")], token)
        stale = params("w1", 0, [ev("e2")], token)
        appended = round_trip(process, request(5, "history.append", fresh))
        conflict = round_trip(process, request(6, "history.append", stale))
        assert process.stdin is not None
        process.stdin.close()
        assert process.wait(timeout=60) == 0
    finally:
        if process.poll() is None:
            process.kill()
    assert result(info) == INFO
    assert result(registered) == {"holderId": "h1", "registered": True}
    assert HEX64.fullmatch(str(result(digest)["digest"])) is not None
    assert result(appended) == {"revision": 1, "stateHash": fold([ev("e1")]), "eventIds": ["e1"]}
    assert error(conflict)["code"] == -32001
    assert error(conflict)["data"] == {"expectedRevision": 0, "actualRevision": 1}
