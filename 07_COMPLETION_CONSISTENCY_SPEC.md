# Completion / Consistency / Missingness

## Missingness Graph

系统必须能表达“世界为什么还不能稳定运行”，例如：
- Actor 缺初始 location；
- location 不连通；
- object ownership 未知；
- scenario 缺初始时间；
- rule 缺 resolver；
- character knowledge boundary 缺失；
- schedule 缺关键时段；
- Domain requirement 未满足。

## Completion 分级

- E0 直接证据
- E1 多来源支持重建
- E2 领域/时代规则推导
- E3 运行必需系统默认
- E4 体验性生成
- E5 用户虚构

任何 E1–E5 永远不能静默升级为 E0。

## Consistency

至少验证：
- temporal consistency
- identity consistency
- topology connectivity
- ownership/custody consistency
- knowledge non-leakage
- organization/role validity
- scenario completeness
- package dependency consistency
- rights compatibility
