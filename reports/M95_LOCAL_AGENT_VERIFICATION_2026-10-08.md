# M95 本地代理验证报告（Phase A–G）

日期：2026-10-08　　范围：`E:\AI\wanxiang`（`huangdi97/wanxiang-world`，分支 `feature/r7-cordis-native`）
执行方式：本地代理按用户 6 条要求 + 仓库 M95 文档链（G98B–G98E、`reports/M95_*`）+ 根目录 2026-10-08 接续文档作为契约，连续执行 A→G。

> 附件按精确文件名 `WANXIANG_M95_LOCAL_AGENT_VERIFICATION_GOAL_2026-10-08.md` 在本机不存在；
> 本会话以仓库既有 M95 文档链与用户 6 条要求为可执行契约，并由接续文档
> `WANXIANG_R7_NEW_CONVERSATION_HANDOFF_2026-10-08.md` 提供环境基线，全程遵循其"GitHub 实时事实优先"。

---

## Phase A — 环境与基线核验

| 项 | 值（本会话实时核验，非静态文档） |
|---|---|
| 本地 HEAD | `9c71a5c29624b44497ab989af3948f8bf41a765a` |
| 远端 HEAD（`git ls-remote`/fetch 后 `rev-parse origin/...`） | `9c71a5c29624b44497ab989af3948f8bf41a765a`（== 本地） |
| 分支 | `feature/r7-cordis-native` |
| 与本会话开始时差异 | 本地曾落后远端 173 commits（`540a7f6`→`9c71a5c`）；已 fast-forward 对齐远端基线，未改写历史 |
| 工作树起点 | 含 2026-09-29 未提交 R7 reference-world 草稿（`r7_reference_worlds*.py`、`test_r7_two_experiences.py`、`artifacts/r7/reference_worlds/`、`scripts/r7_final_qualification.py` 本地修改），与远端 `ecfe9f5` 已落库的正式实现重名同目标但不同文件 |
| 远端 CI（`gh run list`） | `ci` = **SUCCESS**、`r7-qualification` = **SUCCESS**（SHA `9c71a5c`） |
| 现存 PR | 无（`gh pr list --head feature/r7-cordis-native` = `[]`），需创建 |
| 工具链 | uv 0.9.18、Python 3.12 venv、node v22.15.0、pnpm 11.16.0、Playwright 1.62.0、Chrome + Edge 可执行文件存在、gh 2.96.0 已认证（`repo`+`workflow` 权限，用户 `huangdi97`）、`git ls-remote`/push 可用 |
| PostgreSQL 实况 | `EXTERNAL_BLOCKED`（无实例，SQLite 档案绿） |

**R7 草稿处理**：本地未提交草稿已完整备份至会话 scratch
（`$env:PI_SCRATCH_DIR\m95_backup_20261008\r7_wip\` 含 5 个 py 文件 + `reference_worlds/` 目录 + 本地 diff），
工作树恢复到远端基线内容；这与"GitHub 实时事实优先"一致，远端 `ecfe9f5` 已是该目标的正式实现。
**保留**：用户放置于根目录的接续文档未纳入 git，仍以未跟踪文件保留。

## Phase B — 启动真实 Player + 真实浏览器 E2E

- **真实服务**：`scripts/m95_player_server.py`（alembic 升级 migrated SQLite + 真实 app runtime + 预置世界「江南机关城」/角色「沈砚」），uvicorn 于 `127.0.0.1:8056/`。
- **真实浏览器**：Playwright 驱动系统 Chrome（`C:\Program Files\Google\Chrome\Application\chrome.exe`，headless），1440×1000 与 390×844 视口。
- **旅程**：世界广场 → 世界详情（角色体验 潮汐门初启）→ 沈砚进入 → 自由行动「让自己保持清醒」→ committed + 世界变化 → Leave → Continue 同一 `prv_playable_1`。

运行证据：

| 检查 | 结果 | 依据 |
|---|---|---|
| `uv run pytest tests/integration/test_m95_player_experience_browser.py -q` | **1 passed** | zh-CN 默认、进入、行动提交、「世界变化」、Leave→Continue |
| 补充旅程分阶段截图 | 6 阶段 + 移动端 + 探测共 10 张 PNG | 见 `artifacts/m95_local_agent_verification/SCREENSHOT_INDEX.md` |
| 旅程证据 JSON | `locale=zh-CN`、action `committed`、`changed=true`、`continue.active=true` | `artifacts/m95_local_agent_verification/runtime_evidence.json` |
| 服务器日志 | 全 200，无 5xx/Traceback | `server.out.log`（scratch） |
| 浏览器页面错误 | 0 | `page_errors: []` |

## Phase C — Bug 定位、修复与复测

本验证未发现 P0/P1/P2 产品缺陷；对可观测边界做了主动对抗探测：

| 探测 | 结果 | 依据 |
|---|---|---|
| 空动作输入 | 客户端拦截，显示「先写下你想做的事。」 | `edge_probe.json` |
| 重复进入（同角色 409） | 结构化错误「这个角色正在另一个会话中使用，请先结束原来的进入状态再重试。」，**非**通用连接错误 | `edge_probe.json`（修复回归有效，`tests/api/test_player_experience_remediation.py` 4 passed） |
| 不安全动作文本 | 结构化拒绝（`contract_error` 422），无崩溃 | `edge_probe.json` + `route_readiness.json` |
| 隐私泄露 | 页面无 `state_hash/event_id/branch_id/profile_id/cmd_/evt_/WorldPackage` | `edge_probe.json`（`no_runtime_id_leak: true`） |
| action 响应 | `committed`，view 为投影（`recent_changes/narrative`），不暴露原始 state | `edge_probe.json` |

**发现并修复的 P2 证据漂移**：全量测试揭示 v5.1/v5.2 取证与预算账本
（`reports/V5_1_DUPLICATE_FORENSICS.md`、`reports/V5_2_MINIMALITY_BUDGET.md`、
`reports/v52_minimality_budget.json`）的 git 内容落后当前树（如 `production_files` 633→655、
缺 R7 `FileExecutionCheckpointStore`/`ActorTrajectoryLedger` 等），
且 `artifacts/r7/composition/resolved_graph.json` 携带旧 scope 映射。
已用仓库自带确定性扫描器/组合 spike 重新生成并以当前真相提交（commit `05a205f`）。

## Phase D — 质量门与验证

| 门 | 命令 | 结果 |
|---|---|---|
| 架构守卫 | `uv run python scripts/architecture_check.py` | **PASS** |
| Ruff 检查（M95 面） | `uv run ruff check …` | **PASS** |
| Ruff 格式（M95 面） | `uv run ruff format --check …` | **31 files already formatted** |
| Pyright（M95 面） | `uv run pyright …` | **0 errors / 0 warnings** |
| 全量 pytest | `uv run pytest -q` | **1801 passed, 2 skipped, 0 failed**（skip：PostgreSQL `EXTERNAL_BLOCKED`、Docker daemon 不可用） |
| M95 焦点回归 | browser / evidence / remediation / g97e sessions | 1+2+4+1 = **8 passed** |
| 幂等性焦点 | `test_compile_preview.py` + `test_playable_service.py` | **5 passed** |
| TS / cordis | `pnpm -r test` | sdk_ts **22/22**、cordis_host **77/77** |

## Phase E — M95 证据与资格产物

- `artifacts/v55_stable/m95/route_readiness.json`：按当前 SHA `9c71a5c` 重生成，**conclusion=PASS**，7/7 checks（三动作提交、六阶段 trace、拒绝 422、leave/continue 同实例、replay 相等）。
- `artifacts/v55_stable/m95/player_acceptance.json`：保持 **USER_INPUT_REQUIRED**；`human_actions/ratings/free_text_notes = None`，**未代填**（可经 git diff 验证无人填写）。
- `reports/M95_PLAYER_TEST_PACKET.md`：按当前 SHA 刷新 build 字段；`M95_PLAYER_TEST_PACKET_ZH_CN.md` 未触碰。
- 无 `v5.5.0` tag、无 v5.5.0 GitHub Release（`git tag -l v5.5.0` 空；`gh release list` 无）。

## Phase F — 本地提交与 GitHub 交付

已创建 commits（最终 SHA 与 CI 结论见「交付记录」）：

1. `05a205f` — `m95: regenerate stale v5.1/v5.2 ledger and R7 composition graph to current tree`
2. `03f2c1f` — `m95: add local agent verification evidence, screenshots and readiness artifact`
3. `405370a` — `m95: local agent verification phase a-g report`
4. `ae5e33c` — `m95: add delivery record section to verification report`

- 推送：`git push origin feature/r7-cordis-native`（非 force），远端 SHA == 推送后本地 SHA。
- CI：等待该 SHA 的 `ci` 与 `r7-qualification` 完成后记录结论。
- PR：本分支无现存 PR → 创建 PR（base 按仓库默认，链接见「交付记录」）。

## 交付记录（Phase F/G 实时更新）

- 验证基线：`9c71a5c29624b44497ab989af3948f8bf41a765a`（远端与本地一致）
- 交付 commits：`05a205f`（账本/组合图刷新）、`03f2c1f`（M95 验证证据与截图）、`405370a`（本报告）、`ae5e33c`（交付记录）、`d9b9f3d`（PR/CI 记录）、`c781a0c`/`be36f3b`/`aed23c0`/`302e10f`（交付记录对齐）、`bf665c4`（记录定稿）
- 工作树最终状态：仅用户放置的接续文档 `WANXIANG_R7_NEW_CONVERSATION_HANDOFF_2026-10-08.md` 保持未跟踪保留

- 推送 SHA（最终 head）：`7a0d5a5d8654783c77602827f1a6cabc9e4fecb1`（远端 == 本地，非 force）
- exact-SHA CI：`ci` = **SUCCESS**、`r7-qualification` = **SUCCESS**（run 37751178056 / 37751178150 / 37751183448）
- **PR**：https://github.com/huangdi97/wanxiang-world/pull/1 （base `master`，OPEN，MERGEABLE）
## Phase G — 最终交付与剩余阻塞项

交付物（均已入库）：

- 本报告 `reports/M95_LOCAL_AGENT_VERIFICATION_2026-10-08.md`
- 截图索引 `artifacts/m95_local_agent_verification/SCREENSHOT_INDEX.md`
- 机器可读证据 `artifacts/m95_local_agent_verification/verification_summary.json`
  （含 `local_head`/`remote_head`、测试结果、门、边界、截图尺寸）
- 旅程/边界证据 `runtime_evidence.json`、`edge_probe.json`
- 重新生成的 M95 证据 `artifacts/v55_stable/m95/route_readiness.json`、`reports/M95_PLAYER_TEST_PACKET.md`

剩余阻塞项（诚实状态语义）：

- **Gates 62–66（真人 M95）**：`WAITING_HUMAN` / `USER_INPUT_REQUIRED` —— 需真人完成
  `reports/M95_PLAYER_TEST_PACKET_ZH_CN.md`；本代理未代填。
- **Gate 78（Godot/real-engine）**：`EXTERNAL_BLOCKED` —— 本机无受支持 Godot 可执行文件。
- **live DSH（官方 DeepSeek Harness model E2E）**：`EXTERNAL_BLOCKED` —— 本机无官方 harness 二进制/凭据（adapter 与集成契约测试绿）。
- **live PostgreSQL**：`EXTERNAL_BLOCKED` —— 本机无实例（SQLite 档案 + migration 回归绿）。
- **v5.5 Stable 发布**：未创建 tag/Release，需用户显式确认后才执行；v5.6 未启动。

边界遵守：未伪造真人证据；未创建 v5.5.0 tag/Release；未降低任何质量 Gate；未 force-push；
未发明新架构；仅在万相项目目录内操作；状态严格区分 PASS / WAITING_HUMAN / EXTERNAL_BLOCKED / NOT_PROVEN。