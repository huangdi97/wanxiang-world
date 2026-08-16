# Model / AI Provider Policy

本轮**不训练自有模型**。

## 可接入能力

- LLM Provider
- Embedding / Reranker
- OCR
- ASR
- Vision / VLM
- Entity linking
- Temporal parser
- Retrieval
- Optional world predictor / planner

## Provider 输出权限

仅允许：
- Observation
- ParsedCandidate
- CandidateEnvelope
- Claim
- Prediction
- CompletionCandidate
- RepairProposal
- AssetCandidate

禁止：
- direct ORM canonical write
- direct Commit
- mutation of source
- mutation of Constitution

## 无 API Key 基准

CI 与 reference E2E 必须使用 deterministic/rule/synthetic Provider 可通过。
真实模型 E2E 可标 optional integration。
