# Zotero Workflow (LitEngram v1.1)

> 用途：Zotero API 读取 + SQLite 写入的完整技术参考。
> 阅读阶段：Stage 2 · 获取全文 + Stage 4 · Cognitive Annotation + Stage 7 · 写入/验证。
> **v1.1 更新**：修正 Zotero 7 note itemTypeID（14→28）、模式 A 改为混合模式、新增 AI 标注写入流程。

## 快速参考

### API (Read Only)
```
GET  /api/users/0/items/{itemKey}
GET  /api/users/0/items/{itemKey}/children
GET  /api/users/0/items?q={query}&itemType=journalArticle
GET  /api/users/0/items/{attachmentKey}/children?itemType=annotation
```

### SQLite (Write)
Database: `~/Zotero/zotero.sqlite`

安全流程（Kill → Write → Restart → Verify）：
```bash
osascript -e 'quit app "Zotero"'
sqlite3 ~/Zotero/zotero.sqlite "UPDATE ..."
open -a Zotero
sleep 3  # wait for startup
curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"
```

### Key Tables (Zotero 7)
- `items`: itemID, itemTypeID (1=annotation, 2=attachment, **28=note**), key, dateAdded, dateModified
  - **注意**：Zotero 7 中 `items` 表无 `parentItemID` 列。父关系通过类型特定表建立。
- `itemAnnotations`: itemID, parentItemID, type, comment, text
- `itemNotes`: itemID, parentItemID, note (HTML)
- `itemAttachments`: itemID, parentItemID, path
- `collections` / `collectionItems`: collection membership

> **v1.1 修正**：Zotero 7 将 note 的 itemTypeID 从 14 改为 28。旧文档(type=14)已废弃。

---

## 完整技术工作流

### 一、核心原则

```
有 highlight → 混合模式（逐条加批注 + AI 补充 ~10 条新建标注）
无 highlight → 创建 ~20 条新的 annotation 条目 + 批注
笔记副本 → CAD/litreview/{AuthorYear_ShortTitle}.md（可选）
```

### 二、前置确认

- [ ] 论文已在 Zotero 条目库中 → 记录 itemKey
- [ ] PDF 附件已在 Zotero storage 中 → 记录 attachmentKey
- [ ] Zotero Local API 运行正常 → `http://127.0.0.1:23119/api/`

### 三、获取全文 + 检查标注

```bash
# 通过 Zotero API 找到 item
curl -s "http://127.0.0.1:23119/api/users/0/items?q={search_term}&itemType=journalArticle"

# 找到 PDF attachment
curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"

# 解析 attachmentKey → ~/Zotero/storage/{attachmentKey}/*.pdf
# 用 PyMuPDF / PyPDF2 / pdfminer 提取文本

# 检查已有标注
curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}/children?itemType=annotation"
```

- `annotations.length > 0` → **模式 A：混合标注**（注释全部用户划线 → AI 补充 ~10 条）
- `annotations.length === 0` → **模式 B：AI 智能标注**（识别 ~20 个关键点）

### 四、SQLite 写入参考

#### 更新已有标注批注（模式 A 步骤 1）

```sql
-- 对每一条用户 highlight/underline 写批注
UPDATE itemAnnotations SET comment = '…' WHERE itemID = {annotationItemID};
```

#### 创建新的标注条目（模式 A 步骤 2：AI 补充 ~10 条 / 模式 B：~20 条）

```sql
-- itemTypes: 1=annotation, 2=attachment, 28=note
-- Zotero 7: items 表无 parentItemID 列，父关系存 itemAnnotations

-- 新建标注条目
INSERT INTO items (itemTypeID, key, dateAdded, dateModified)
VALUES (1, 'random_hex_key', datetime('now'), datetime('now'));

-- 添加标注内容（parentItemID 在此指定）
INSERT INTO itemAnnotations (itemID, parentItemID, type, annotatesItemID, comment, text)
VALUES ({newItemID}, {parentItemID}, 'highlight', {pdfItemID}, '批注内容', '高亮原文');

-- AI 补充标注的 comment 以 🤖 [AI补充] 开头
INSERT INTO itemAnnotations (itemID, parentItemID, type, annotatesItemID, comment, text)
VALUES ({newItemID}, {parentItemID}, 'highlight', {pdfItemID}, '🤖 [AI补充] 批注内容', '高亮原文');
```

#### 创建笔记条目

```sql
-- 注意：Zotero 7 中 note 的 itemTypeID 是 28（非旧版 14）
INSERT INTO items (itemTypeID, key, dateAdded, dateModified)
VALUES (28, 'random_hex_key', datetime('now'), datetime('now'));

-- 父关系在 itemNotes 表中建立
INSERT INTO itemNotes (itemID, parentItemID, note)
VALUES ({newItemID}, {parentItemID}, '<h2>笔记标题</h2><p>笔记内容</p>');
```

> key 生成：`import secrets; secrets.token_hex(6)` 生成 12 位十六进制字符串。

### 五、安全流程

```
1. 关闭 Zotero
   osascript -e 'quit app "Zotero"'

2. 写入批注 + 笔记到 SQLite
   sqlite3 ~/Zotero/zotero.sqlite "UPDATE ..."
   sqlite3 ~/Zotero/zotero.sqlite "INSERT INTO ..."

3. 重启 Zotero
   open -a Zotero

4. 验证
   curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"
   
   # 检查 note 属性
   curl -s "http://127.0.0.1:23119/api/users/0/items/{noteKey}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'ItemType: {d[\"data\"][\"itemType\"]}, Parent: {d[\"data\"][\"parentItem\"]}')"
   
   # 检查 annotation comments
   curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}/children?itemType=annotation" | python3 -c "import json,sys; items=json.load(sys.stdin); print(f'Total: {len(items)}, With comments: {sum(1 for i in items if i[\"data\"].get(\"annotationComment\",\"\").strip())}')"
```

### 六、文件存储

| 内容 | 路径 | 说明 |
|------|------|------|
| 阅读笔记 (.md) | `CAD/litreview/{AuthorYear_ShortTitle}.md` | 本地副本（可选） |
| Zotero 子笔记 | Zotero 条目库 (API/SQLite) | 权威版本 |
| Zotero 标注批注 | Zotero PDF 附件 | 绑定到具体高亮/下划线 |
| 本工作流文档 | `references/zotero_workflow.md` | 当前文件 |

### 七、技术备忘

- Zotero Local API: `http://127.0.0.1:23119/api/users/0/`
- 已启用配置: `extensions.zotero.httpServer.localAPI.enabled = true`
- SQLite 备用: `~/Zotero/zotero.sqlite`
- 条目定位: 通过 DOI / title / itemKey
- **Zotero 7 关键差异**:
  - `items` 表无 `parentItemID` 列（Zotero 6 有）— 父关系通过 `itemNotes`/`itemAnnotations` 表建立
  - note 的 `itemTypeID` 为 **28**（非旧版 14）
  - 写入后需重启 Zotero 才可通过 API 读取到新数据
