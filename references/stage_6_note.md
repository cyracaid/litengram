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

按模板 12 部分填充（方法节按 Stage 1-2 传来的 `paper.domain` 选模板：psych 版 / nlp 版 / hybrid 双版全量 / neuroscience 版全量）。概念深挖用 `####` 四级标题 + 平铺格式（禁止 `>` 引用块包裹）。

**neuroscience 版特别注意**：
- **🔬 研究方法** 中的 fMRI 专属子项（刺激范式、fMRI 获取、预处理、分析）必须在 **📋 基本信息** 中注明
- **💡 核心发现** 中的每个发现均需附加 **证据强度**（Direct fMRI激活 / Indirect 行为关联 / Theoretical）和 **证据来源**
- **📊 复现性** 中需特别覆盖 **算力/显存门槛**（fMRI 复现通常需要整脑分析的算力/时间成本）
- **🚧 概念阻滞点** 需要在 **🔬 研究方法** 或 **🧠 理论背景** 中追踪 fMRI 术语（搜光峰、GLM 设计矩阵 等）
- **⭐ 为什么这篇重要** 中的神经科学关注点请参考对应 "神经科学注意点" 章节

### 3. 门禁检查

写入前跑结构门禁 checklist。缺任何一节 → 报错 → 补全 → 再检查。通过后返回。

## 输出

返回完整的笔记 Markdown 字符串给主 agent。

**格式要求**：
- 纯 Markdown（无原始 HTML）
- 深挖块用 `####` + 平铺格式
- 遵守 `literature_note_template.md` 的输出兼容层规则
