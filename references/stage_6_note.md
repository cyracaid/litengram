# Stage 6: Engram Note Synthesis

> 由 LitEngram meta-skill 调度。将上文所有产出合成为结构化笔记。

## 输入

从主 agent 处接收：
- Stage 1-2 产出（优先级 + 上下文）
- Stage 3 产出（分析文本 + 概念深挖素材）
- Stage 4-5 产出（标注清单 + 审稿人报告）

## 步骤

### 1. 读参考文件

- `references/literature_note_template.md` — 12 部分结构 + 📎 关键引用 + 结构门禁 checklist + 输出兼容层规则
- `references/concept_excavation.md` — 9 层深挖规格

### 2. 合成笔记

按模板 12 部分填充（方法节按 Stage 1-2 传来的 `paper.domain` 选模板：psych 版 / nlp 版 / hybrid 双版全量）。概念深挖用 `####` 四级标题 + 平铺格式（禁止 `>` 引用块包裹）。

摘要从 Zotero 的 `abstractNote` 读取，不做改写。

📌 关键标注 节从 Stage 4-5 产出的 `ai_annotation_table_markdown` 填入——直接使用，不再改写。

### 3. 门禁检查

写入前跑结构门禁 checklist。缺任何一节 → 报错 → 补全 → 再检查。通过后返回。

## 输出

返回完整的笔记 Markdown 字符串给主 agent。

**格式要求**：
- 纯 Markdown（无原始 HTML）
- 深挖块用 `####` + 平铺格式
- 遵守 `literature_note_template.md` 的输出兼容层规则
