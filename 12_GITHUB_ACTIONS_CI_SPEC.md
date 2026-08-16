# GitHub Actions CI / Open-source Automation 规范

## 1. CI 触发

主 CI 至少对：

- push 到 `main` / feature branches；
- pull_request 到 `main`；

触发。

可对 docs-only changes 使用 path filtering，但不得因此漏掉会影响构建的配置改动。

## 2. CI Jobs

根据仓库真实技术栈实现，不要写不存在的命令。至少覆盖：

### A. repository-safety

- 基础 secret pattern scan / 已有 secret scanner；
- 禁止提交 `.env`、DB dump、known private corpus path；
- 检查超大非必要 tracked files；
- license / required OSS metadata sanity。

### B. python-quality

- 安装仓库指定 Python（至少当前主版本；若项目明确兼容 3.11/3.12，可 matrix）；
- dependency install；
- Ruff/lint；
- format check；
- typecheck；
- unit tests。

### C. core-contracts

- architecture conformance；
- Commit Boundary tests；
- Replay / Branch / Worldline / Lineage；
- deterministic reference tests；
- Kernel freeze guard。

### D. integration

- SQLite integration；
- PostgreSQL service container（若仓库生产支持 PostgreSQL）；
- migrations upgrade；
- API contract / OpenAPI；
- package install/upgrade smoke。

### E. web-quality

若存在 web workspace：

- pnpm install --frozen-lockfile（按真实 lockfile 调整）；
- lint；
- TypeScript typecheck；
- unit tests；
- production build。

### F. e2e-smoke

- 启动必要 backend/frontend；
- Playwright 或现有 E2E；
- 至少跑不依赖真实 LLM key 的 deterministic smoke。

### G. packaging

- Python package/build（如果项目可打包）；
- TS SDK build；
- World/Domain package certification smoke；
- 检查生成 artifacts 能在 clean environment 使用。

## 3. 可拆分 workflow

推荐：

```text
.github/workflows/
  ci.yml
  codeql.yml              # 若适用
  release.yml             # tag/release 构建
  docs.yml                # 仅项目已有文档站时
```

不要为了“看起来专业”建立大量重复 workflow。

## 4. Action 安全

- 优先 GitHub 官方或公认维护良好的 actions；
- 使用当前受支持 major version，并在实现时验证；
- 第三方 action 必须必要且来源可信；
- 最小 `permissions:`；
- PR workflow 不给不需要的 write 权限；
- 不把 repository secrets 暴露给不可信 fork PR。

## 5. 无外部模型依赖

CI 必须在没有 OpenAI/Anthropic/DeepSeek 等 API key 时通过核心测试。

外部 provider tests 使用 fake/deterministic adapters；真实在线模型测试只能是 opt-in/non-required workflow。

## 6. Dependabot / Supply Chain

如果仓库使用 GitHub Dependabot，创建 `.github/dependabot.yml`，至少覆盖实际使用的 package ecosystems（例如 pip/uv、npm/pnpm、github-actions）。

不要创建与仓库不匹配的 ecosystem。

## 7. CodeQL

公开仓库可增加 GitHub CodeQL workflow；但它是补充，不代替普通 CI。

只配置仓库实际存在且 CodeQL 支持的语言。

## 8. Release workflow

`v*` tag 可触发 release build/check：

- 重跑最小 release gate；
- 构建 package artifacts；
- 生成 checksums；
- 不自动发布到 PyPI/npm，除非后续用户明确授权 registry publishing；
- GitHub Release 可以附 release notes 与安全可公开 artifacts。

## 9. CI 成功标准

必须以 GitHub 远端 workflow run 的 conclusion 为准，而不是本地推测。

报告至少记录：

- workflow name；
- run ID / URL；
- commit SHA；
- jobs；
- result；
- 首次失败原因（若有）；
- 修复 commit；
- 最终 PASS run。
