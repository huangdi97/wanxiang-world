# Source Adapter Matrix

## Foundation 必须支持

| 类型 | 本轮最低能力 |
|---|---|
| TXT / Markdown | 结构化文本导入、标题/段落、稳定 locator |
| EPUB | spine / href / chapter / text |
| DOCX | paragraph / heading / table locator |
| text-PDF | page-aware text；扫描版显式 OCR_REQUIRED |
| JSON / YAML | JSON Pointer / path |
| CSV | row/column locator |
| GEDCOM | xref/tag path；Family source |
| Generic Asset | 图片/音频/视频登记为 AssetReference |

## Phase B 扩展

- OCR Provider：扫描 PDF / 古籍图片。
- Image Understanding Provider：人物、物体、场景、地图辅助候选。
- ASR Provider：音频/视频转写。
- Subtitle / Transcript Adapter。
- IIIF / web/API connector port。
- Multi-source bundle manifest。

所有 Provider 都必须可缺省；缺 Provider 时明确返回 capability requirement，不伪装成功。
