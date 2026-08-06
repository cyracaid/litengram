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

通过 Zotero 定位论文并提取 PDF。

**步骤 2a: 定位 PDF 文件**

从 Zotero API 获取 attachment，解析 storage 路径：

```bash
# 1. 找到 attachment key
curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"

# 2. 获取 attachment 详情
curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}"
# 从 Location header 获取文件路径（Zotero 返回 302 redirect）
```

**步骤 2b: 检查 PDF 可用性**

```python
import os
from pathlib import Path

pdf_path = Path("~/Zotero/storage/{key}/{filename}.pdf").expanduser()

if pdf_path.exists():
    status = "available"
elif pdf_path.parent.exists():
    # storage dir exists but file missing — Zotero metadata corruption
    status = "missing"
else:
    # storage dir doesn't exist — never downloaded
    status = "not_imported"
```

**步骤 2c: 获取 PDF 文本**

- `status == "available"`: 用 PyMuPDF / pdfminer 提取全文
- `status != "available"`: 标记 PDF 不可用，后续 Stage 降级处理

**步骤 2d: 检查已有标注数量**

```bash
curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}/children?itemType=annotation"
```

- `count > 0` → 初步标记为"有划线"（最终模式由 Stage 4-5 运行时动态判定）
- `count === 0` → 初步标记为"无划线"

> 注：Stage 4-5 启动时会重新查询当前标注数，用户在 Stage 1-3 期间新增的划线不会被遗漏。

### 3. 优先级判定

按 `paper_priority.md` 标准判定：
- 论文类型
- 重要等级（⛰️ / ⚔️ / 📌 / 🌫️）
- 阅读策略（Deep / Standard / Fast / Skip）
- 用途标签
- 读前定位 4 问

### 4. 解析目标目录（Zotero Collection → litreview 路径）

从 Zotero API 返回的 paper 条目中提取 `data.collections`（collection key 数组）。对每个 key 查 collection 名称：

```bash
curl -s "http://127.0.0.1:23119/api/users/0/collections/{collectionKey}"
```

将 collection name 与 `.litengram_config.json` 中的 `project_dirs` 映射表匹配：

```json
{
  "project_dirs": {
    "CAD": "~/Documents/CAD",
    "James Gross": "~/Documents/James Gross"
  }
}
```

- 匹配成功 → `litreview_dir = {project_dir}/litreview/`（不存在则 mkdir）
- 论文在多个 collection → 取第一个匹配的
- 无匹配 → 默认 `~/Documents/CAD/litreview/`

### 5. （可选）上下文注入

如果 `{litreview_dir}/../research_profile.md` 存在，载入上下文。所有后续分析须落到具体研究项目上。

## 输出

返回以下 JSON 结构给主 agent：

```json
{
  "paper": {"type": "", "level": "", "strategy": "", "tags": []},
  "zotero": {
    "parent_item_id": 0,
    "pdf_path": "",
    "pdf_status": "available / missing / not_imported",
    "annotation_count": 0,
    "mode": "A/B",
    "collection_name": "James Gross"
  },
  "litreview_dir": "~/Documents/James Gross/litreview",
  "context_notes": "研究上下文摘要",
  "full_text_summary": "PDF 全文关键段落摘要（便于下游分析）"
}
```
