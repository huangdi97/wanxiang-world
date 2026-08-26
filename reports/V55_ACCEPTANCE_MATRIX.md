# v5.5 M85-M94 Acceptance Matrix

Status at G88A: **IN_PROGRESS / NOT_ACCEPTED**. This ledger is frozen for the
v5.5 run; thresholds may not be lowered to obtain a release.

| Gate | Area | Status | Evidence |
|---:|---|---|---|
| 1 | PlayableWorldProfile from v5.4 world | PENDING | — |
| 2 | Plaza / Continue / My Worlds / My Characters E2E | PENDING | — |
| 3 | Character / Observer / Embodiment permissions | PENDING | — |
| 4 | Free Action proposal-to-commit loop | PENDING | — |
| 5 | Committed StateDiff | PENDING | — |
| 6 | Leave / Continue continuity | PENDING | — |
| 7 | ActorGoalStack persistence/replay | PENDING | — |
| 8 | Memory / Belief / Truth separation | PENDING | — |
| 9 | Secret / rumor / future-knowledge isolation | PENDING | — |
| 10 | RelationshipState time/event provenance | PENDING | — |
| 11 | 7-day actor continuity | PENDING | — |
| 12 | From Source regression | PENDING | — |
| 13 | From Prompt E5 Candidate/WorldDraft | PENDING | — |
| 14 | Hybrid E0-E5 provenance | PENDING | — |
| 15 | Publish visibility/rights gates | PENDING | — |
| 16 | PressureProfile outside Kernel | PENDING | — |
| 17 | CANON/DIRECTED/LIVING/EXPERIMENT modes | PENDING | — |
| 18 | Director has no Commit authority | PENDING | — |
| 19 | Opportunity can be ignored | PENDING | — |
| 20 | Intervention branch/artifact isolation | PENDING | — |
| 21 | 24-hour smoke | PENDING | — |
| 22 | 7-day runtime | PENDING | — |
| 23 | 30-day literary run | PENDING | — |
| 24 | 90-day selected-world run | PENDING | — |
| 25 | Checkpoint/resume/crash recovery | PENDING | — |
| 26 | Compaction replay equality | PENDING | — |
| 27 | LOD transition continuity | PENDING | — |
| 28 | Cost/storage/memory quantification | PENDING | — |
| 29 | Evolution delta taxonomy separation | PENDING | — |
| 30 | 30-day Actor/Relationship/Organization evolution | PENDING | — |
| 31 | Evolution explainability/replay | PENDING | — |
| 32 | Source/canon immutability | PENDING | — |
| 33 | Positive/negative pattern benchmark | PENDING | — |
| 34 | Evidence-backed emergence candidate | PENDING | — |
| 35 | High-level promotion review | PENDING | — |
| 36 | False-positive controls | PENDING | — |
| 37 | No universal-emergence claim | PENDING | — |
| 38 | WorldRunArtifact re-verification | PENDING | — |
| 39 | Recoverable Experiment Registry | PENDING | — |
| 40 | Fork/intervention parent isolation | PENDING | — |
| 41 | Four or more parallel worldlines | PENDING | — |
| 42 | Multi-provider/policy or mixed population | PENDING | — |
| 43 | Worldline trajectory/cost comparator | PENDING | — |
| 44 | ValidationProfile V0-V7, unknown != pass | PENDING | — |
| 45 | Physical Provider ABI | PENDING | — |
| 46 | Visual Provider ABI | PENDING | — |
| 47 | Reference physical provider E2E | PENDING | — |
| 48 | Reference visual projection E2E | PENDING | — |
| 49 | Multi-perspective privacy isolation | PENDING | — |
| 50 | Provider output cannot write reality | PENDING | — |
| 51 | Browser Experience/Studio E2E | PENDING | — |
| 52 | Security/private-source/UGC scan | PENDING | — |
| 53 | v5.4 critical regression | ACCEPTED | G88A baseline: 1219 passed, 1 skipped |
| 54 | Full Python/TypeScript quality | ACCEPTED | G88A baseline: local Python and prior stable TS evidence |
| 55 | Clean clone | ACCEPTED-INHERITED | v5.4 post-release evidence; v5.5 clean clone pending |
| 56 | Remote SHA equals local HEAD | PENDING | v5.5 branch not pushed yet |
| 57 | Required GitHub Actions | PENDING | v5.5 branch not pushed yet |
| 58 | Working tree clean | PENDING | G88A commit pending |
| 59 | Evidence boundary separation | PENDING | Final evidence goal |
| 60 | Release gate / rc1 only if all ACCEPTED | LOCKED | G97H/G97J |

Required release condition: Gates 1-59 must be ACCEPTED with real evidence;
then and only then may G97H create annotated `v5.5.0-rc1` and a GitHub
prerelease. Otherwise the final status remains `NOT_ACCEPTED`.
