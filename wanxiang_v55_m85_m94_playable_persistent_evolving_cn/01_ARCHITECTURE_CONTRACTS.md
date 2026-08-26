# v5.5 Architecture Contracts

## 1. Experience Shell

```text
WorldPackage
+ Scenario
+ RuntimeProfile
+ ExperiencePackage
+ ProjectionProfile
→ PlayableWorldProfile
```

Experience Shell 负责产品入口，不拥有 Canonical Reality。

## 2. Free Action

```text
Player Text / UI Action
→ IntentCompiler
→ ActionProposal
→ Validator
→ Resolver / Simulator
→ ProposedDelta
→ CommitAuthority
→ CommittedDelta
→ StateDiff
→ Narrative / Visual Projection
```

禁止 Narrative Generator 直接写状态。

## 3. ActorGoalStack

```text
LifeMotive
→ LongTermGoal
→ MediumPlan
→ ShortTermGoal
→ CurrentIntent
→ ActionProposal
```

所有 Goal / Plan 都属于 Actor cognition，不等于 World Truth。

## 4. EpistemicMemory

```text
World Truth
→ Perception
→ EpisodicMemory
→ Belief
→ Reflection
→ Goal / Plan
```

必须保持：Memory ≠ Belief ≠ World Truth。

## 5. PressureProfile

属于 Scenario/Domain/Experience：
- resource scarcity
- competing goals
- private information
- duties / obligations
- authority
- rewards / sanctions
- reputation
- time pressure
- environmental risk
- social norms

不得进入 Kernel。

## 6. Director Modes

- CANON：尽量维持 source/canon attractor；
- DIRECTED：允许 Director 提议叙事机会/挑战；
- LIVING：Director 只提供环境机会，不控制人物选择；
- EXPERIMENT：显式 Intervention，必须进入实验日志。

Director 永远无 Commit Authority。

## 7. SimulationLOD

- L0 Focal Actor：完整 cognition / provider；
- L1 Active Actor：简化 reasoning；
- L2 Background Actor：policy + memory summary；
- L3 Cohort：aggregate simulation；
- L4 Population：flow/statistical model。

状态仍由 World 拥有，Agent worker 尽量 stateless。

## 8. WorldRunArtifact

一次运行至少记录：
- WorldPackage/Domain/Scenario/Constitution versions；
- seed / RuntimeProfile / Provider versions；
- Runtime Control Ledger refs；
- commits / snapshots / branch graph；
- actor trajectories；
- interventions；
- Worldness / ValidationProfile results；
- cost / latency / storage metrics。

## 9. ValidationStack

Worldness ≠ Scientific Validity。

至少区分：
- V0 Structural Validity
- V1 Source Fidelity
- V2 Behavioral Validity
- V3 Mechanism Validity
- V4 Macro Validity
- V5 Long-Horizon Stability
- V6 Counterfactual Validity
- V7 External Calibration（有外部数据时）

## 10. Visual / Physical Provider Boundary

外部 Provider 可输出：
- ObservationCandidate
- PhysicsResolution
- SceneProjection
- PerceptionFrame
- AssetCandidate
- Prediction

不得直接 Commit Canonical Reality。
