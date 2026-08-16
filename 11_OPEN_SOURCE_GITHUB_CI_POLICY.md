# M50 开源发布、GitHub 自动建仓与 CI 正式政策

## 1. 本轮最终交付不是“本地代码完成”

M50 的最终完成链必须是：

```text
M43–M49 全部 PASS
→ M50 本地全量回归 PASS
→ Open-source Readiness Audit
→ 清除/排除不能公开的内容
→ 完成开源元数据与治理文件
→ 完成 GitHub Actions CI
→ 创建 public GitHub repository
→ push 所有可公开代码与 Git 历史
→ GitHub Actions 真实触发
→ 查询远端 workflow run
→ 若 CI 失败则定位、修复、commit、再次 push
→ 远端 required CI 全绿
→ tag v5.3.0-rc1
→ GitHub Release Candidate
→ GITHUB_DELIVERY_REPORT
→ M50 PASS
```

## 2. 默认公开仓库

优先仓库名：`wanxiang-world`。

若当前 GitHub 账号已存在同名仓库，依次尝试：

1. `wanxiang-world-os`
2. `wanxiang-world-engine`

不得因为名称冲突覆盖或删除已有仓库。

仓库 visibility：**public**。

Description：

`Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS`

推荐 topics：

`world-model`, `world-os`, `multi-agent`, `simulation`, `digital-humanities`, `generative-agents`, `python`, `typescript`, `fastapi`, `react`

## 3. License

若仓库已有明确 LICENSE：保留，不自动改变。

若没有 LICENSE：本执行程序默认采用 **Apache License 2.0** 作为代码许可证，并在 README 清楚说明：

- Apache-2.0 只覆盖本仓库明确标记的原创代码/文档；
- 第三方依赖遵循各自许可证；
- 文学底本、现代校注本、图片、声音、模型、3D 资产、博物馆数据、家庭数据等不因代码开源自动获得 Apache-2.0 授权；
- 只有 rights metadata 明确允许再分发的示例数据才可进入公开 Git history。

新增 `DATA_AND_ASSET_RIGHTS.md` 说明数据与资产权利边界。

## 4. 开源前必须存在的仓库文件

至少：

- `README.md`
- `README_EN.md` 或 README 中完整英文摘要
- `LICENSE`
- `NOTICE`（若项目使用 Apache-2.0 且有需声明事项）
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `DATA_AND_ASSET_RIGHTS.md`
- `CHANGELOG.md`
- `.gitignore`
- `.gitattributes`
- `.env.example`（只能有占位符）
- `docs/architecture/` 的公开架构入口
- `docs/quickstart/` 或等价 Quickstart
- `docs/package-authoring/` 或等价第三方 World/Domain Pack 教程

## 5. 绝不能公开提交的内容

push 前必须自动检查并排除：

- `.env`、API key、token、credential、cookie、SSH private key；
- 本地数据库、生产数据库 dump；
- 真实个人/家庭隐私数据；
- 未明确允许公开再分发的《红楼梦》现代电子底本/校注本；
- 博物馆受限图像/3D/内部资料；
- 模型权重/缓存；
- 大型 build/cache/temp 文件；
- 用户本地路径、调试日志中的凭证；
- `.venv`, `node_modules`, generated caches；
- 未获得再分发权的第三方素材。

不得通过“删用户本地文件”来解决：优先 `.gitignore`、取消 tracking、迁移到 ignored/local data directory；保留本地原件。

## 6. Git 历史安全

如果 secret/私有数据曾经进入历史：

- 在公开前必须识别；
- 不得只从最新 commit 删除就认为安全；
- 如必须清理 Git history，先创建本地备份 tag/branch，并在报告中记录；
- 不对已有远端做 force push（本仓库尚未存在远端时，可以在首次公开前安全清理本地历史）；
- 任何已泄露 credential 必须视为需要撤销/轮换，不能只改 Git。

## 7. GitHub 创建与 push

只有本地工程、开源审核和 CI 文件全部通过后才创建远端。

若 `gh auth status` PASS 且账号具有建仓权限，可非交互创建：

```bash
gh repo create wanxiang-world --public --source=. --remote=origin --push \
  --description "Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS"
```

具体命令应根据现有 remote/branch 状态安全调整，不机械重复 `origin`。

## 8. Main 与 feature branch

- 不 force push。
- 若本地已有稳定 `main`，首次建仓应推送它。
- 本轮 `feature/wanxiang-v5.3-multiverse` 也要推送。
- 如果 M50 的认证 commit 在 feature branch，优先创建 PR 到 main。
- 只有仓库历史与测试明确适合时才自动 merge；否则保留 PR，不冒险 merge。

## 9. 远端 CI 是正式验收的一部分

“`.github/workflows/ci.yml` 存在”不等于 CI 完成。

Codex 必须：

1. push；
2. 使用 `gh run list` / `gh run view` 查询 workflow；
3. 等待/轮询到 workflow 结束；
4. 对失败 job 获取日志；
5. 修复代码或 workflow；
6. commit + push；
7. 直到核心 workflow PASS；
8. 把 run URL/ID、commit SHA、结论写入报告。

如果 GitHub 服务/权限客观不可用才允许 `EXTERNAL_BLOCKED`。
