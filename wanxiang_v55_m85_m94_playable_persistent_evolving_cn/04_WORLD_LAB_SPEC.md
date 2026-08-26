# World Laboratory Spec

## 目标

把“世界运行”变成可复验的实验对象。

## ExperimentDefinition

至少：
- experiment_id
- world_package/version
- scenario/version
- seed(s)
- provider matrix
- population policy
- interventions
- run horizon
- metrics
- validation profile
- stop conditions

## 能力

- fork from snapshot/event；
- intervention at explicit time/event；
- replay；
- batch worldlines；
- multi-provider parallel worlds；
- mixed-population worlds；
- compare trajectories；
- compare actor/relationship/institution outcomes；
- cost/latency/storage compare；
- export sanitized RunArtifact。

## 不允许

- 用一次随机 run 宣称科学结论；
- 用 Worldness 代替 ValidationStack；
- 把实验 intervention 静默写回 canonical source world；
- 通过 provider-specific hidden state 破坏 replayability。
