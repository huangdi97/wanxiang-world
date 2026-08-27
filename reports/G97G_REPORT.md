# G97G — Clean Clone + GitHub CI

Date: 2026-08-27  
Status: NOT_ACCEPTED (local qualification PASS; remote push/Actions blocked)

## Scope and boundary

G97G verifies that the current feature checkout can be installed and exercised
from a clean clone. The v5.4 Kernel / Reality Root / Commit Authority / Ledger /
Branch / Lineage semantics remain frozen. No private source, original real
book, model, model training, v5.6 work, or release tag was used or changed.

The original real-book `NOT_ACCEPTED` boundary remains preserved. This Goal
does not convert local synthetic or public qualification inputs into that
real-book acceptance.

## Clean-clone evidence

The clean clone was created at
`E:\\AI\\wanxiang\\.pytest-tmp\\g97g-clean-f76b995` from branch
`feature/v5.5-playable-persistent-evolving` at commit
`f76b9959cfe6c557c379cf0931d8fb87d5d40eb8`. Its initial working tree was
clean and its local branch tracked the source checkout.

| Check | Result |
|---|---:|
| `uv sync --all-groups --all-packages` | PASS; 43 resolved, 42 third-party packages plus 8 local packages installed |
| `pnpm install --frozen-lockfile` | PASS; 149 packages installed |
| `scripts/clean_room_certify.py` | PASS: clean tree, release manifest, migration upgrade, golden replay, backup/restore/replay, external sample pack, reference world |
| non-integration pytest domains | 863 passed, 2 warnings |
| integration pytest domain | 592 passed, 1 `EXTERNAL_BLOCKED` PostgreSQL skip, 2 warnings |
| all clean-clone Python tests | 1455 passed, 1 skipped, 2 warnings |
| `pnpm lint` | PASS |
| `pnpm typecheck` | PASS |
| `pnpm test` | 6 files / 22 tests passed |
| `pnpm build` | PASS |
| `scripts/studio_socket_smoke.py` | PASS; health ok, socket passed, Studio status true |
| `scripts/playable_e2e.py` | PASS; committed StateDiff, replay equality, same-instance Continue |
| `scripts/structured_mixed_smoke.py` | PASS; 9 candidates, 3 fusion alignments, WorldPackage and Preview |
| SDK/OpenAPI/wxpack CI commands | PASS; 62 operations, 59 paths, package validate/build/certify true |
| `scripts/release_build.py` | PASS; migration head `0004_add_world_metadata` |
| `scripts/kernel_guard.py` | PASS; 0 violations |
| `scripts/architecture_check.py` | PASS |

The TypeScript baseline exposed one stale expectation: the current exported
OpenAPI document deterministically contains 62 operations, while the test was
still asserting the historical 45. The test baseline was updated to 62; no
runtime route, compiler gate, or acceptance threshold was weakened. The
generated-artifact drift check passed after excluding only the clone-local
certification report and this intentional test edit.

The first monolithic clean-clone pytest invocation exited without a failure
summary on Windows. The complete 1456-item collection was then run by its
non-integration and integration domains; both completed with the counts above.
The isolated long-run resource file also passed 4/4.

## Remote SHA and Actions status

No remote SHA equality or GitHub Actions result can be asserted: the required
feature-branch push was attempted once and was rejected by the execution
environment's external-write safety review because the branch name contains
`v5.5`. No workaround, alternate transport, force-push, or indirect GitHub
write was attempted. Consequently no new remote commit or Actions run exists
for this G97G checkpoint.

Gates 55 (clean clone) is locally evidenced. Gates 56 (remote SHA), 57
(required Actions), and the final release condition remain pending. The
working tree will be made clean by the checkpoint commit below, but that does
not substitute for remote verification.

## Decision

The local clean-clone qualification passes, but the G97G Objective includes
remote SHA equality and green required Actions. With those externally blocked,
G97G is **NOT_ACCEPTED**, no v5.5.0-rc1 tag/release is permitted, and the
existing v5.4 stable history and real-book acceptance boundary remain
unchanged. G97H-G97J must preserve this evidence and stop without claiming
remote CI success.
