# GitHub / CI / Release Policy

使用现有公开 `wanxiang-world` 仓库，不新建 repo。

## 分支

优先：`feature/source-to-living-world`

## 每个 Milestone

- 本地 qualification PASS；
- commit；
- 自动继续。

## 最终 M70

1. secret/private/copyright corpus scan；
2. full local CI；
3. push feature branch；
4. 查询真实 GitHub Actions；
5. CI FAIL → 读日志 → 修 → commit → push；
6. required CI 全绿；
7. 可创建 PR；
8. 若 release policy 与权限允许，打 `v5.4.0-rc1`；
9. 生成 GitHub Release Candidate；
10. 记录 final SHA / workflow runs / release evidence。

禁止 force push、泄露真实 family data、上传受限书籍 corpus、重指已发布 tag。
