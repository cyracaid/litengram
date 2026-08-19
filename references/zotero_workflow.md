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

### Web API (Cloud Download — requires ZOTERO_API_KEY)
```
GET  https://api.zotero.org/users/{userID}/items/{attachmentKey}/file
Header: Zotero-API-Key: {key}
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
> ⚠️ **v1.3 修正（重大）**：`token_hex(6)` 生成的 key **非法**！
> Zotero item key 必须是 8 位，字符集 `[2-9A-NP-Z]`（排除 0、1、O）。
> 12 位小写 hex 或含 0/1/O 的 key，客户端同步会被服务器拒
> （`Error 400 ... 'KEY' is not a valid item key`）。
> 正确生成：
> ```python
> import random
> _KEY_CHARS = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
> key = "".join(random.choice(_KEY_CHARS) for _ in range(8))
> ```
> 或直接用 `scripts/zotero_sync.py` 的 `zotero_key()`。
>
> 另注：SQLite 直插的条目 `synced=0`，需用户手动点同步（或 `open -a Zotero`
> 后等客户端自动同步）才会推到云端。写入后记得提示用户同步。

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
| PDF 下载暂存 | `~/Zotero/pdf-inbox/` | 云端下载的 PDF 落点（`LITENGRAM_PDF_INBOX` 可覆盖） |
| 本工作流文档 | `references/zotero_workflow.md` | 当前文件 |

> PDF 下载落点：`LITENGRAM_PDF_INBOX` 设置时用该目录，否则默认
> `~/Zotero/pdf-inbox/`。下载成功会打印路径 + 手动拖入指引。

### 七、技术备忘

- Zotero Local API: `http://127.0.0.1:23119/api/users/0/`
- 已启用配置: `extensions.zotero.httpServer.localAPI.enabled = true`
- SQLite 备用: `~/Zotero/zotero.sqlite`
- 条目定位: 通过 DOI / title / itemKey
- **Zotero 7 关键差异**:
  - `items` 表无 `parentItemID` 列（Zotero 6 有）— 父关系通过 `itemNotes`/`itemAnnotations` 表建立
  - note 的 `itemTypeID` 为 **28**（非旧版 14）
  - 写入后需重启 Zotero 才可通过 API 读取到新数据

---

## 八、Web API 上传完整流程（DOI → 条目 → PDF 附件）— v1.3

> 场景：论文条目已有（或需新建）但本地无 PDF，或 PDF 在云端缺失。
> 优先用现成脚本：`python3 scripts/zotero_upload.py --doi <DOI> --pdf <path> [--collection <名>]`
> 或 `--item-key <key>` 跳过 DOI 查找。下面是人肉/调试版步骤。

### 手动模式（推荐：慢速/限流时）

Web API 上传慢或坚果云 503 限流时，用 `--manual` 只下载 PDF 到
inbox（`LITENGRAM_PDF_INBOX` 或 `~/Zotero/pdf-inbox/`），然后手动拖入 Zotero：

```
python3 scripts/zotero_upload.py --manual --doi <DOI>
python3 scripts/zotero_upload.py --manual --item-key <itemKey>
```

脚本打印 PDF 路径 + 打开目录命令 + 拖入指引。手动拖入后 Zotero 客户端
自己处理文件复制与同步（走 WebDAV），绕开 API 上传与坚果云限流。

### 前置
- `ZOTERO_API_KEY` 已设置（zshrc 或 export）
- `ZOTERO_USER_ID`（默认 11261922）

### Step 1 — 建/找父条目
```
# 查 DOI 是否已在库
GET https://api.zotero.org/users/{userID}/items?q={doi}&qmode=everything
# 无则建 journalArticle（元数据可来自 CrossRef: https://api.crossref.org/works/{doi}）
POST /users/{userID}/items   [{itemType: journalArticle, title, creators, DOI, ...}]
```
collection key 解析：`GET /users/{userID}/collections` → 按 name 匹配 → 取 `key`，
建条目时放 `collections: [key]`。

### Step 2 — 建 attachment 子条目（关键坑）
```json
{
  "itemType": "attachment",
  "parentItem": "9BKZ3QUE",
  "linkMode": "imported_file",
  "title": "nsaf102-epmc.pdf",
  "filename": "nsaf102_epmc.pdf",
  "contentType": "application/pdf",
  "collections": [],
  "relations": {}
}
```
> ⚠️ **不要带 md5 / mtime 字段**。带了会 412 `If-None-Match: * set but file exists`
> （WebDAV 同步模式下 md5 被当作"文件已存在"）。文件信息在 Step 3 再传。
> key 由服务器自动生成（8 位 `[2-9A-NP-Z]`），客户端创建时**禁止**手造 key。

### Step 3 — 上传授权
```
POST /users/{userID}/items/{attachmentKey}/file
Header: If-None-Match: *
Content-Type: application/x-www-form-urlencoded   ← 不是 multipart！
Body:   md5=<hex>&filename=<name>&filesize=<bytes>&mtime=<毫秒>&params=1
```
- `mtime` 必须**毫秒**（秒 × 1000）
- `params=1` 让响应返回可直接 POST 的 S3 表单字段
- 响应 200：`{url, params{...}, uploadKey}`；若 `{"exists":1}` 说明文件已存在，跳过上传

### Step 4 — 上传到 S3
```
POST {url}   (multipart form)
字段顺序：key 必须第一个，file 必须最后
  key, acl, Content-MD5, success_action_status, policy,
  x-amz-algorithm, x-amz-credential, x-amz-date, x-amz-signature, x-amz-security-token,
  file=@/path/to.pdf
期望 201 Created
```

### Step 5 — 注册
```
POST /users/{userID}/items/{attachmentKey}/file
Header: If-None-Match: *
Body:   upload=<uploadKey>
期望 204 No Content；之后 GET item 可见 md5 已关联
```

### 错误速查
| 状态 | 含义 | 处理 |
|------|------|------|
| 400 `POST data not provided` | Step3 用错了 Content-Type / multipart | 改 form-urlencoded |
| 412 `If-None-Match: * set but file exists` | 附件创建时带了 md5 | 重建附件（不带 md5）|
| 413 | 云配额满 | 清理附件或升级 |
| 428 | 删除/更新缺版本头 | 加 `If-Unmodified-Since-Version: {version}` |

### 清理误建附件
```
GET  /users/{userID}/items/{key}            → version
DELETE /users/{userID}/items/{key}
Header: If-Unmodified-Since-Version: {version}
期望 204
```
