# 用户需要做什么

## 必做 1：准备第二本真实书

推荐：
- 与第一本不同作者/文风；
- 最好格式也不同；
- 优先 EPUB，其次 DOCX/TXT/MD；
- 不需要上传 GitHub，只放本机。

把本地路径告诉 Codex，例如：
`D:\books\second_book.epub`

并明确：
- 允许本地私有解析：是/否
- 允许发送到当前 semantic provider：是/否
- 允许打包进本地 WorldPackage：是/否
- 允许公开原文：通常否
- 允许训练：默认否

## 必做 2：准备一个 GEDCOM

可以是真实家谱导出，也可以是你自己创建的测试家谱。真实家谱必须 private/local，不进 public Git。

路径例如：
`D:\family\my_family.ged`

如果暂时没有 GEDCOM：可以让 Codex 先做 M79–M81 和 M83，M82 标记 USER_INPUT_REQUIRED，不能伪造“真实 Family 验收”。

## 必做 3：准备结构化测试数据

最简单三份即可：
- people.csv
- places.csv
- events.csv 或 events.json

可以自己构造 10–50 条，不涉及隐私。

## 其余不用你做

Codex 应自动完成：代码修改、benchmark、tests、Studio/API/CLI、Git commits、push、GitHub Actions、修 CI、reports、stable tag/release。

仅当 GitHub 再次要求授权、semantic provider 需要凭证/确认、Family privacy/rights 需要授权选择时，才需要你人工介入。
