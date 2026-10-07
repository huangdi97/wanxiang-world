# R7 玩家快速验证（zh-CN）

本页用于真人体验验证，不替代自动化测试。

## 目标

真实玩家应能在不理解工程术语的前提下：
1. 找到一个世界；
2. 理解“我是谁、在哪里、能做什么”；
3. 进入/选择角色；
4. 完成一次自由行动；
5. 看懂行动造成的世界变化；
6. 离开后 Continue，回到同一世界线和角色状态。

## 原则

- 默认语言 zh-CN；
- Player 与 Studio/debug 分开；
- 世界变化只来自已 Commit 的 StateDiff/历史；
- 玩家不应被要求理解 event/schema/provider/RuntimeLock 等内部 id；
- Continue 不得创建一个历史独立的“相似世界”。

## 正式真人 Gate

v5.5 Stable 的 Gates 62–66 必须由真实测试者完成
`reports/M95_PLAYER_TEST_PACKET_ZH_CN.md`。AI、脚本和合成记录不能代替真人
身份、评分、困惑点或接受结论。
