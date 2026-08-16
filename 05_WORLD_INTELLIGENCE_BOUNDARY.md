# World Intelligence Provider Boundary

允许 Provider：WorldStatePredictor、WorldPlanner、EventProposer、WorldModelProvider、GenerativeSceneProvider、CounterfactualProvider、PopulationPolicyProvider、NarrativePlannerProvider。

允许输出：Observation / Prediction / Plan / Candidate / ProposedDelta / AssetCandidate / Confidence / ValidityEnvelope。

禁止：直接写 canonical DB、append WorldLedger、overwrite Snapshot、修改 World Definition、self-promote、修改 Kernel/Constitution。

必须提供：Deterministic/Fake Provider + Simple Offline Reference + External Adapter Contract。核心测试不依赖外部模型 key。
