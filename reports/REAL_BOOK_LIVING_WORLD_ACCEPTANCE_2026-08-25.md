# Real Book → Living World 用户验收

日期：2026-08-25  
checkout：`feature/source-to-living-world`  
HEAD：`00da555095cb1524f1a2b19abe7fff59b579a01c`  
版本描述：`v5.4.0-rc1-3-g00da555`

## 结论

**NOT ACCEPTED（真实链路被产品缺失阻断）**。

本次没有修改测试数据、没有把原始小说复制到仓库、没有调用内部 Python helper 代替 CLI/API，也没有生成或伪称存在 WorldPackage、Preview、Worldness 或 Living World instance。真实 Book 只生成了一个不可编译的 WorldDraft；阻断项、错误和缺失均保留在本文及同目录 JSON 证据中。

完整证据目录：

- `artifacts/real_book_living_world_acceptance_2026-08-25/input_metadata.json`
- `artifacts/real_book_living_world_acceptance_2026-08-25/cli_failure.txt`
- `artifacts/real_book_living_world_acceptance_2026-08-25/api_primary.json`
- `artifacts/real_book_living_world_acceptance_2026-08-25/api_rights_diagnostic.json`
- `artifacts/real_book_living_world_acceptance_2026-08-25/run_manifest.json`

原始文件仍在用户路径 `D:\下载\我本英雄-周梅森.txt`，未进入 Git。

## 输入与边界

| 项目 | 实际值 |
|---|---|
| 文件 | `D:\下载\我本英雄-周梅森.txt` |
| 类型/profile | `text` / `book` |
| 大小 | 937,500 bytes |
| 解码 | UTF-8 |
| 字符/行 | 323,815 字符 / 8,144 行 |
| 换行 | CRLF |
| SHA-256 | `5c914ea9995f41239b56e06f331ca7e3595b28cb2b15377fa015556a1c99268d` |
| 注入标记 | `system:`、`ignore previous instructions` 等均为 0 |

TXT 内容按 Source Gate 的 data channel 处理；其中的小说叙述没有被当作系统/用户指令。没有从用户请求中推断出版权授权，因此主验收使用 `stage=E0`、`rights_approved=false`、`access=private`、`usage=package`。这不是修改书籍内容，而是如实保留当前 Source/Rights 状态。

为隔离权限门与解析能力，另做了一个**仅诊断、非验收结论**的 metadata 变体：完全相同的 937,500 bytes 和 SHA，发送 `stage=E3`、`rights_approved=true`。这不构成版权授权，也没有被计入 PASS。

## 执行过程

### 1. 版本与质量前置

最初工作树在 `实例-我本英雄 / m56-worlddraft` 且干净；按用户指定切换到本地及远端一致的 `feature/source-to-living-world`。切换没有改源码或测试。

当前分支质量证据：

- `uv run python scripts/architecture_check.py`：PASS
- `uv run python scripts/quality.py`：Ruff lint PASS，Ruff format check PASS，Pyright `0 errors`，pytest `1201 passed, 1 skipped, 2 warnings`，architecture PASS
- `tests/integration/test_m69_one_click.py`：`5 passed, 2 warnings`
- 唯一 skip：未启动 PostgreSQL 的 `tests/integration/test_g16b_postgres.py` live profile；不是本次 Book 的成功证据

### 2. 真实 CLI

执行了真实 `scripts/wxworld.py reference --profile book --kind text --file ...`，读取完整用户文件。CLI 在 `AuthoringService.build_package` 前抛出：

```text
wanxiang_domain.errors.ContractError: draft has zero coverage
```

带 `--publish` 的同一真实文件也得到相同错误。`wxworld --help` 实测只有 `reference` 子命令；`status` 实测为 argparse invalid choice。因此 Goal 所要求的 CLI `status/resume/publish/instantiate` 产品面当前并不完整。原始输出摘要见 `cli_failure.txt`。

### 3. 真实 Studio/API 路由：主验收

Uvicorn 尝试监听 `127.0.0.1:8765`，启动生命周期完成但绑定被 Windows `WinError 10013` 拒绝；即使权限提升也不能完成 socket 验证。之后使用同一 `create_app()` 的真实 FastAPI `/studio` 路由和 `TestClient` 发送完整文件，明确标记为“路由真实、socket 未验证”，没有直接调用 service 或测试 fixture。

主请求：`POST /studio/one-click`，profile `book`，来源 `stage=E0`、未批准 rights、private/package。

| API 步骤 | HTTP | 实际结果 |
|---|---:|---|
| `/studio/one-click` | 500 | `draft status REVIEW_REQUIRED is not compilable` |
| `/studio/jobs/...` | 200 | status=`running`，stage=`drafted`，error 为空，draft 已存在 |
| `/draft` | 200 | WorldDraft 已生成，0 candidates |
| `/scenarios` | 200 | 生成 3 个默认 scenario，但输入世界为空 |
| `/review-inbox` | 200 | 0 items |
| `/review-inbox/audit` | 200 | 0 audits |
| `/build` | 500 | `draft status REVIEW_REQUIRED is not compilable` |
| `/preview` | 500 | `draft status REVIEW_REQUIRED is not compilable` |
| `/publish` | 500 | `draft status REVIEW_REQUIRED is not compilable` |

### 4. 真实 WorldDraft

主验收生成：

```text
draft_id            wd_real-book-api-20260825
revision            1
status              REVIEW_REQUIRED
source_refs         real_book_api_20260825
selected_domains    []
candidate_count     0
entities/relations  [] / []
places/events       [] / []
coverage            0.0
uncertainty         0.3
unresolved_rights   [real_book_api_20260825]
unresolved_conflicts[]
completion_items    actor entities, events, places, relations, rules
```

### 5. Rights-approved 诊断变体

相同原始字节只改变请求 metadata 后，WorldDraft 为：

```text
draft_id            wd_real-book-api-rights-diagnostic-20260825
revision            1
status              READY_TO_COMPILE
candidate_count     0
selected_domains    []
coverage            0.0
uncertainty         0.3
unresolved_rights   []
completion_items    actor entities, events, places, relations, rules
```

它仍在 `/studio/one-click`、`/build`、`/preview`、`/publish` 全部返回 `500 contract_error: draft has zero coverage`。所以即使不考虑 rights gate，当前 deterministic Book path 也没有将这份中文长文本提取为可编译候选。

## 产物、审核与 Worldness 清单

| 产物/动作 | 状态 | 证据/说明 |
|---|---|---|
| Source 注册/解析 | 部分完成 | 输入被读入；没有注入标记；Draft 产生但 0 candidate |
| WorldDraft | 已生成但不可用 | 主验收 `REVIEW_REQUIRED`、coverage 0、rights 未批准 |
| WorldPackage | 未生成 | `package_id=null`；compiler gate 失败 |
| Preview | 未生成 | `preview_id=null`；preview route 失败 |
| Scenario/Genesis | 生成默认空场景 | 3 个 deterministic default scenarios，详见 JSON；不等于 living world |
| Review Inbox | 空 | 0 human-review items |
| Review Audit | 空 | 0 audits；没有执行人工审核 |
| Worldness | 未生成 | 没有 package/preview/runtime 输入；当前 API/CLI 没有 Worldness 输出路由 |
| Living World instance | 未进入 | 未调用 `instantiate_preview`；没有 instance/branch/event/replay 证据 |
| Canonical World State | 未触碰 | 没有 Commit Authority mutation |

当前 OpenAPI 的 Studio 路由实际包含 job/source/start/resume/status/draft/scenarios/review/build/preview/publish 等接口，但没有 Worldness 或 Enter-Living-Instance 接口；仓库 `apps` 只有 `apps/api`，没有可启动的浏览器 Studio 应用。因此“Studio”本次只能以真实 `/studio` API surface 验证，不能声称完成浏览器 UI 验收。

## 缺失与产品问题

1. **中文长 Book deterministic coverage 缺失**：真实 323,815 字符文本输出 0 candidates、0 coverage，无法编译。
2. **未授权 Source 的 job 生命周期不完整**：one-click 返回 500 后，`GET job` 仍是 `running/drafted`，`error` 为空，没有失败状态或可操作的错误 checkpoint。
3. **空 Draft 仍可生成默认 Scenarios**：在没有实体、事件、关系、地点的 Draft 上返回 3 个 scenario，用户容易误认为已有世界。
4. **Worldness 没有产品产物**：当前编排器的默认 `LoopSignals` 值不能当成对这本书的 Worldness 评估；真实流程没有输出 Worldness score/dimensions/replay proof。
5. **Living World 入口缺失**：无 API/CLI 的 instantiate/enter endpoint；没有从真实 Book 产物进入 runtime 的用户路径。
6. **CLI 生活周期不完整**：当前 `wxworld` 只有 `reference`，没有用户要求的 status/resume/publish/instantiate 子命令。
7. **网络 API 未能在本机端口验证**：`uvicorn` bind 被 WinError 10013 阻断；TestClient 只证明路由处理，不证明 socket/浏览器链路。
8. **权限语义需要用户界面/审计输入**：当前请求没有明确版权授权，主验收按未批准处理；不能用 metadata=true 诊断变体冒充实际授权。

## 最终判定

当前 `v5.4.0-rc1 / feature/source-to-living-world` 的代码质量基线通过，但对这份真实《我本英雄》TXT 的 Book → Living World 用户验收 **不通过**：只有不可编译 WorldDraft 和空默认 Scenarios；WorldPackage、Preview、Worldness、人工审核结果和 Living World instance 均未生成。继续前需要明确修复/产品决策，而不是修改书籍或测试数据来绕过 gate。
