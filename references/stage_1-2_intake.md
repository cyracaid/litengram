# Stage 1-2: Intake — 优先级 + 上下文 + 获取全文

> 由 LitEngram meta-skill 调度。你只需执行以下步骤并返回结果。

## 输入

从主 agent 处接收：论文标识（DOI / Zotero itemKey / 标题 / PDF 路径）。

## 步骤

### 1. 读参考文件

先通读：
- `references/paper_priority.md` — 类型分类、等级标准、读前定位 4 问
- `references/zotero_workflow.md` — Zotero API/SQLite 操作细节

### 2. 获取全文 + 已有标注

通过 Zotero 定位论文并提取 PDF，检查已有标注数量：
- `annotations > 0` → 模式 A（混合标注）
- `annotations === 0` → 模式 B（AI 智能标注）

### 3. 优先级判定

按 `paper_priority.md` 标准判定：
- 论文类型
- 重要等级（⛰️ / ⚔️ / 📌 / 🌫️）
- 阅读策略（Deep / Standard / Fast / Skip）
- 用途标签
- 读前定位 4 问

### 4. （可选）上下文注入

如果 `research_profile.md` 存在，载入上下文。所有后续分析须落到具体研究项目上。

## 输出

返回以下 JSON 结构给主 agent：

```json
{
  "paper": {"type": "", "level": "", "strategy": "", "tags": []},
  "zotero": {"parent_item_id": 0, "pdf_path": "", "annotation_count": 0, "mode": "A/B"},
  "context_notes": "研究上下文摘要",
  "full_text_summary": "PDF 全文关键段落摘要（便于下游分析）"
}
```
