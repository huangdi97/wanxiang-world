# GitHub / Release Policy

继续现有公开仓库 `wanxiang-world`。

建议 feature branch：
`feature/v5.5-playable-persistent-evolving`

若当前分支上已有合法 v5.5 work，则复用，不制造无意义分支。

每个 Goal PASS 后：
- local commit；
- milestone gate；
- 自动继续。

M94 前：
- secret/private-source scan；
- no copyrighted raw source；
- no private family data；
- full local quality；
- push feature branch；
- required GitHub Actions；
- FAIL → logs → fix → commit → push → rerun；
- remote SHA == local HEAD。

只有 M94 real certification ACCEPTED 才允许：
- annotated tag `v5.5.0-rc1`；
- GitHub prerelease；
- post-release clean-clone verification。

禁止 force push，禁止移动/覆盖 `v5.4.0` stable tag。
