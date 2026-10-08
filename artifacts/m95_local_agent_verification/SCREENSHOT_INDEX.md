# M95 本地代理验证 —— 截图索引

生成时间：2026-10-08（会话内实时采集）
截图来源：真实 Chromium/Edge（headless，`chrome.exe`）驱动真实 Player 服务
（`scripts/m95_player_server.py`，uvicorn + migrated SQLite WorldRuntime）。

## 自动化 E2E（`test_m95_player_experience_browser.py`）

| 文件 | 尺寸 | 阶段 |
|---|---|---|
| `artifacts/m95_local_agent_verification/screenshots/desktop.png` | 1440×2182 | 桌面端完整首页（Plaza 世界广场，含推荐世界/我的世界/最近经历/我的角色） |
| `artifacts/m95_local_agent_verification/screenshots/mobile.png` | 390×3392 | 移动端完整首页（390×844 视口） |

## 补充旅程分阶段截图（真实 Player 服务 + 真实浏览器）

| 阶段 | 文件 | 尺寸 | 内容 |
|---|---|---|---|
| 01 Plaza | `stage_01_plaza.png` | 1440×2182 | 世界广场首页，zh-CN 默认（`万相｜进入世界`、`lang=zh-CN`） |
| 02 世界详情 | `stage_02_world_detail.png` | 1440×1069 | 世界详情「江南机关城」+ 场景「潮汐门初启」+ 角色「沈砚」选择 |
| 03 进入世界 | `stage_03_enter_world.png` | 1440×1170 | 角色体验 Play 视图（地点/时间/环境/人物/叙事） |
| 04 行动已提交 | `stage_04_action_committed.png` | 1440×1170 | 自由行动「让自己保持清醒」→ committed → 世界变化投影 |
| 05 离开返回 | `stage_05_leave_plaza.png` | 1440×2405 | Leave 后回到 Plaza，Continue 槽显示同实例续玩入口 |
| 06 继续同实例 | `stage_06_continue_same_instance.png` | 1440×1170 | Continue 恢复同一 `prv_playable_1` play 视图 |
| 移动端 | `mobile_plaza.png` | 390×3392 | 移动端首页（390×844 视口） |
| 边界探测 | `probe_after_actions.png` | 1440×2182 | 边界探测结束态（重复进入 409 提示/不安全动作拒绝后） |

## 对应运行证据

- `artifacts/m95_local_agent_verification/runtime_evidence.json`：旅程证据，
  `locale=zh-CN`、action `committed/changed=true`、leave/continue 同实例。
- `artifacts/m95_local_agent_verification/edge_probe.json`：边界探测，
  重复进入显示结构化中文错误（非通用连接错误）、无运行时 ID 泄露、零页面错误。
- `artifacts/m95_local_agent_verification/verification_summary.json`：机器可读汇总
  （SHA、测试结果、门、边界、索引）。

全部 PNG 均已校验（`\x89PNG` 签名 + IHDR 尺寸）。