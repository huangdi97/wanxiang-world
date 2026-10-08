# Codex / Claude Code 连续执行总指令：Wanxiang v5.5 M95–M100 Stable Certification

你现在继续开发 `wanxiang-world`。本轮唯一目标是把已经发布的 `v5.5.0-rc1` 在真实证据边界内推进到 `v5.5.0` Stable。不要重做 v5.4，不要重做 M85–M94，不要进入 v5.6，不要训练 Wanxiang 自有模型。

## 0. 开始前必须完整读取

- 当前仓库根目录所有交接/状态/架构/验收文件；
- `万相世界_v5.5-RC1-R3_Playable_Persistent_Evolving_Living_World_OS_完整母版_截至2026-08-28.md`；
- `V55_FINAL_RELEASE_REPORT.md`；
- `M79_M84_STATUS.md`；
- `reports/V55_ACCEPTANCE_MATRIX.md` 及 Final Closure / Gate59 reconciliation；
- 当前 tests / migrations / Studio / API / SDK / scripts / CI / release policy；
- 本 Goal Pack 的 `00_README_FIRST.md`、`01_STABLE_ACCEPTANCE_MATRIX.md` 与 `goals/`。

## 1. 不可违反的冻结边界

1. Reality Root / Commit Authority / canonical state / append-only history / replay / branch isolation 不重构。
2. Provider、LLM、Godot、浏览器、UI、Narrative、Projection 只能产生 Proposal/Candidate/Projection，不得直接改 Canonical Reality。
3. World Truth、Observation、Memory、Belief、Reflection 分离。
4. Source/Canon immutability、rights/privacy/resource controls 保持。
5. Gates 1–60 与历史报告保持原样；Stable 新建 Gates 61–80。
6. Prompt Genesis、bounded long-horizon/World Lab/emergence 即使通过本轮 bounded acceptance，仍保留 EXPERIMENTAL/BOUNDED 标签。
7. heavy physical/visual E2E、live PostgreSQL 没有真实环境就只能 `EXTERNAL_BLOCKED`，禁止 mock 变 PASS。
8. 不训练模型，不做 v5.6，不引入“十万 LLM NPC”目标。
9. 不上传 private source、版权原文、secret/token、私有 family data、model cache。
10. 禁止 force push、改写已发布 tag/release、删除历史失败证据。

## 2. 真实仓库预检

先执行并记录：
- `git status --short --branch`
- `git remote -v`
- `git fetch --tags --prune`
- 当前 HEAD、remote branch SHA、`v5.4.0` 与 `v5.5.0-rc1` tag object/peeled commit；
- 验证当前分支 tip 是 Final Closure 的合法后代，且没有 v5.6/model-training 工作；
- working tree 必须 clean；若不 clean，先分类用户改动，不得覆盖。

若仓库真实状态与 Final Release Report 存在实质冲突：生成 `reports/M95_BASELINE_MISMATCH.md`，STOP release mutation；不要猜测、不要自动修历史。

若一致：从当前 closure-descendant tip 创建/切换 `release/v5.5-stable-certification`（若已存在则验证其 ancestry 后复用）。

## 3. 连续执行顺序

严格按下面 Goal 执行；每个 Goal PASS 后 commit 并继续：

- G98A–G98E → M95
- G99A–G99E → M96
- G100A–G100E → M97
- G101A–G101G → M98
- G102A–G102D → M99（Optional；无 Godot 环境不得阻塞后续）
- G103A–G103I → M100

遇到真实人工玩家缺失：把 G98D / M95 标为 `USER_INPUT_REQUIRED`，生成可直接给用户填写的 test packet，继续所有不依赖 M95 人工结果的 G99/G100 工程准备和 G101/G102；Gate 80 保持 LOCKED。

## 4. 证据要求

每个 Milestone 至少产出：
- `reports/<MILESTONE>_...md`
- `artifacts/v55_stable/<milestone>/...json`
- 可复现命令、输入 hash/ID、seed、版本、world/branch/run refs；
- PASS / FAIL / USER_INPUT_REQUIRED / EXTERNAL_BLOCKED 的机器可读结论；
- 明确 `IMPLEMENTED / VALIDATED / EXPERIMENTAL / NOT_PROVEN / EXTERNAL_BLOCKED` 边界。

不能用 README 文案、硬编码 JSON、静态截图、mock-only、LLM 自评或人工改 matrix 作为唯一 PASS 证据。

## 5. Release 规则

只有 Gate 80 predicate 为真时才允许：
1. 创建 annotated tag `v5.5.0`；
2. push tag；
3. 创建 non-draft、non-prerelease GitHub Release；
4. 从 tag 做 isolated clean clone/install/migrate/quickstart/replay/Studio/TS/Python/post-release verification；
5. 写 `reports/V55_STABLE_RELEASE_REPORT.md`。

Stable release notes 必须继续声明：Prompt Genesis、bounded long-horizon/World Lab/emergence 的边界；heavy physical/visual 和 live PostgreSQL 若仍无真实验证则保留相应边界。

完成后 STOP。不要自动建立 v5.6 分支，不要开始模型训练。
