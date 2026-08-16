# GitHub Delivery Policy

用户已明确授权本轮完成后上传 GitHub。

## 上传前
1. `git status` / `git remote -v` / `git branch --show-current` / `git log --oneline -20`。
2. 若 `gh` 可用：`gh auth status`。
3. 执行 secret scan、tracked-files review、large-file/private-source scan。
4. 确认不提交 `.env`、token、数据库、用户隐私、受限 corpus、模型缓存、构建缓存、大型生成资产。

## 分支
若当前在 `main/master`，优先创建：`feature/wanxiang-v5.3-multiverse`。

## Push
M50 全部内部认证 PASS 后：
`git push -u origin feature/wanxiang-v5.3-multiverse`

如果权限允许，可创建 PR：`Wanxiang v5.3 Multiverse & Interworld Runtime`。

最终认证 PASS 后可选创建 annotated tag：`v5.3.0-rc1` 并 push。只有现有仓库流程允许且 `gh` 可用时才可选创建 GitHub Release。

## 禁止
不 force push、不删远端分支、不改写用户历史、不伪造 push 成功。

若 remote/auth/permission 缺失，记录 `GITHUB_PUSH=EXTERNAL_BLOCKED` 和本地最终 SHA；工程完成状态与 GitHub 外部阻塞分开判定。
