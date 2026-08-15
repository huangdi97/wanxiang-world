# Cross-Domain / Ecosystem / Release 标准
## Family
GEDCOM/GEDZIP、冲突 Claim、Kinship/LifeEvent/Place/Source、Privacy/Consent、Living/Deceased Persona、Family Object Biography。

## Heritage
IIIF、Linked Art/CIDOC selected profile、Physical Object/Digital Surrogate/Semantic Twin/Reconstruction、Provenance、Conservation、Object Biography、3D Asset 只作为 Projection。

## Campaign
Command/Logistics/Movement/Resources/Fog-of-War、Orders/Receipt Time、SimulationAdapter、ValidityEnvelope、Batch Experiment。

三领域都必须复用同一 Identity/Fact/Event/Commit/Ledger/Branch/Source/Package/Host/Projection；若需要 Kernel 特判则 M41 FAIL。

## Ecosystem
第三方只能使用 public SDK/CLI 完成 create→validate→test→certify→build→install→instantiate→run，不允许 import internals。

## Release
fresh clone、SQLite、本地文件、PostgreSQL、对象存储 adapter、migration、backup/restore、observability、security/rights、SDK 文档、RedChamber 用户/作者/运维文档、benchmark、release readiness。
