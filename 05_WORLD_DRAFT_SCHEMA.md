# WorldDraft 正式定位

WorldDraft 是 Forge 的**可编辑编译中间产物**，不是运行世界，不拥有 Commit Authority。

## 必备结构

- draft_id / revision
- source_refs / source_versions
- constitution_ref
- selected_domains / dependency_lock
- entities / aliases
- character_profiles
- organizations / roles
- relations
- places / topology
- objects / biographies
- events / timeline
- knowledge_boundaries
- rules / norms / institutions
- skills / affordances
- completion_items
- unresolved_conflicts
- unresolved_rights
- scenario_candidates
- genesis_candidates
- coverage / uncertainty / quality metrics
- compiler metadata

## Draft lifecycle

```text
CREATED
→ INGESTING
→ DISTILLING
→ FUSING
→ REVIEW_REQUIRED
→ COMPLETION_REQUIRED
→ VALIDATING
→ READY_TO_COMPILE
→ PREVIEWABLE
→ PUBLISHABLE
```
