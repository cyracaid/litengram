# Notion 同步指南 (v1.2)

## 定位

Stage 7 的第三写入目标。三处同步互不阻塞：

| 目标 | 位置 | 角色 |
|------|------|------|
| 本地 .md | `CAD/litreview/{AuthorYear_ShortTitle}.md` | 存档副本 |
| Zotero 子笔记 | 论文条目下 `itemNote` | 与文献绑定的权威版 |
| **Notion (新)** | "每日读读文献"页 → 日期 toggle → 论文 toggle | 人类日常翻阅的主界面 |

🌫️ 级论文不产笔记，三处都不写。

---

## 前置配置

### Token

```python
import os
token = os.environ.get("NOTION_TOKEN")
if not token:
    raise RuntimeError("Notion token not found: set NOTION_TOKEN env var")
```

**绝不写 token 到任何文件。**

### Integration 权限

用户须在 Notion 中把 "每日读读文献" 页 Share 给该 integration，否则 API 看不到该页。
检测不到时提示用户去分享，不要静默失败。

### 目标页 ID 缓存

`CAD/.litengram_config.json`:

```json
{
  "notion_daily_page_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

读取流程：
1. 读缓存 → 命中则用
2. 未缓存 → Notion Search API, query=`每日读读文献`, filter=`page`, 精确匹配标题 → 取 `page_id` 写回缓存
3. 找不到 → 提示用户检查页名与分享设置，跳过 Notion

---

## 写入逻辑

### 找或建日期 toggle

```
今日日期 = datetime.now().strftime("%Y-%m-%d")   # 如 2026-07-20
```

1. 拉取 "每日读读文献" 页的 children（注意分页，每页 100 块，可能要翻页）
2. 找文本内容 == 今日日期的 toggle 块：
   - **存在** → 取该 toggle 的 block_id
   - **不存在** → 在页尾新建 toggle，标题=今日日期，取回 block_id
3. 在该日期 toggle 下追加论文 toggle

### 找或建论文 toggle

在日期 toggle 的 children 中搜索标题含论文标题的 toggle：
- **存在** → 询问用户覆盖还是跳过（默认跳过）
- **不存在** → 新建

### 幂等保护

同日同论文重复运行默认跳过，不产生重复 toggle。

---

## Markdown → Notion Blocks 转换

| 笔记元素 | Notion 块 |
|----------|-----------|
| `##` 论文标题 | 作为"论文 toggle"的标题（不单独建块） |
| `###` 章节（📚/🧠/📎/🔬/💡/🔗/⭐/📄） | `heading_3`（Notion 最深只到 h3） |
| `**`子标题（已知/缺口/被试…） | `paragraph` 加粗，或 heading_3 用尽后用加粗段 |
| 普通段落 | `paragraph`，`**x**` 映射 rich_text annotations |
| 无序列表 | `bulleted_list_item` |
| 概念深挖块 | 嵌套 `toggle`（见下） |
| 易混辨析表 | Notion `table`（table + table_row，首行 header）；转换失败降级为每行 bullet：`列1: … ｜ 列2: …` |
| `>` 引用 / WHY 提示 | `callout` 或 `quote` 块 |

### API 约束

- 单次 append 最多 100 个 block → 超了分批
- 单次请求嵌套最多 2 层 → 更深层级先建父块拿 block_id，再递归 append
- 单个 rich_text 文本 ≤ 2000 字符 → 超长切分成多个 rich_text 对象

---

## 概念深挖块 → 嵌套 toggle（faithful 复刻）

每个概念深挖块转成：

```
toggle(标题 = "术语中英 + 🔬/📘 符号")
  ├─ paragraph: 一句话粗暴定义
  ├─ paragraph: 溯源（谁提出/哪年/哪个传统）
  ├─ table:     易混辨析（如有）
  ├─ paragraph: 核心机制 / 在本文角色 / 与你研究关联
  ├─ paragraph: 人话类比
  ├─ paragraph(加粗): 一句话总结
  └─ toggle(递归子概念，如有，最多再 1 层)
```

关键引用节（📎）里每条引用若挂了精简挖掘块，同样用小 toggle，保持本节简洁。

---

## 容错与降级

| 失败场景 | 行为 |
|---------|------|
| Token 缺失 | 打印 `Notion: ❌ NOTION_TOKEN 未设置` → 继续本地+Zotero |
| 页未分享 / 未找到 | 打印 `Notion: ❌ 页"每日读读文献"不可见，请分享给 integration` → 继续 |
| API 报错 | 打印错误摘要 → 继续 |
| 限流 (429) | 退避重试 2 次 → 仍失败则降级 |
| 某一步失败 | 不阻塞同趟内的本地/Zotero 写入 |

---

## Python 依赖

```bash
pip install notion-client==3.0.0
```

---

## 参考实现

LitEngram 的 Notion 同步通过 `scripts/notion_sync.py` 实现。Agent 调用方式：

```python
from scripts.notion_sync import NotionSync

syncer = NotionSync()
result = syncer.sync_note(
    title="⚔️ Measuring Interoception: The CARdiac Elevation Detection Task",
    markdown_content="# ... 完整笔记 markdown ...",
    date_str="2026-07-20"  # 可选，默认当日
)
# result 格式: {"local": "✅/❌", "zotero": "✅/❌", "notion": "✅/❌(原因)"}
```
