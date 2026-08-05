# Stage 4-5: Cognitive Annotation + Reviewer

> 由 LitEngram meta-skill 调度。标注已有划线 + 生成 AI 补充标注（嵌入笔记）+ 审稿人自审。
> v1.2 修复：不再通过 SQLite INSERT 创建新 PDF annotation，AI 补充标注改为嵌入笔记 📌 关键标注 节。

## 输入

从主 agent 处接收：
- 分析结果（Stage 3 产出）
- 论文全文
- 已有标注清单（annotation count + 每条内容和 itemID）

## 步骤

### 0. 启动时查询当前标注数（动态模式判定）

不依赖 Stage 1-2 的 annotation_count——运行时自行查询 Zotero API：

```bash
curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}/children?itemType=annotation"
```

- `count > 0` → 模式 A（混合）：标注已有 annotation + AI 补充嵌入笔记
- `count === 0` → 模式 B（纯 AI）：全部 AI 标注嵌入笔记

**Fallback 机制**：

```python
import sqlite3, os, json, urllib.request

def get_annotation_count(attachment_key, attachment_item_id):
    """Try Zotero API, fall back to SQLite on failure."""
    # Try 1: Zotero API
    try:
        url = f"http://127.0.0.1:23119/api/users/0/items/{attachment_key}/children?itemType=annotation"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            annotations = [x for x in data if x["data"].get("itemType") == "annotation"]
            return len(annotations), annotations
    except Exception as e:
        print(f"[LitEngram] Zotero API failed: {e}. Falling back to SQLite...")
    
    # Try 2: SQLite
    try:
        db_path = os.path.expanduser("~/Zotero/zotero.sqlite")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*), ia.itemID, ia.text, ia.comment "
            "FROM itemAnnotations ia WHERE ia.parentItemID=?",
            (attachment_item_id,)
        )
        rows = cur.fetchall()
        conn.close()
        count = rows[0][0] if rows else 0
        return count, rows
    except Exception as e2:
        print(f"[LitEngram] SQLite also failed: {e2}")
        return 0, []
```

- 成功: 使用 API 返回的标注列表
- API 失败且 SQLite OK: 使用 SQLite 数据
- 两者都失败: 默认 Mode B，不阻塞流程

同时通过 SQLite 查询已有 annotation 的 itemID 和当前 comment 状态：

```sql
SELECT ia.itemID, i.key, ia.type, ia.comment, ia.text 
FROM itemAnnotations ia 
JOIN items i ON ia.itemID = i.itemID 
WHERE ia.parentItemID = {attachmentItemID}
```

- `comment 为空或仅含 [AI] 前缀` → 需要写入/覆盖
- `comment 已有有意义内容` → 跳过（保留用户/之前的注释）

### 1. 读参考文件

- `references/annotation_guidelines.md` — v1.2 两路分流规则 + 📌 关键标注格式
- `references/concept_excavation.md` — 9 层深挖规格（标注中嵌深挖）
- `references/reviewer_protocol.md` — 7 维度审稿人自审

### 2. 模式 A：用户有划线 → 注释已有 + AI 补充

**步骤 1：SQLite UPDATE 已有 annotation 的 comment**

```sql
-- 安全操作：只改 comment 字段，不动 position/sortIndex/pageLabel
UPDATE itemAnnotations SET comment = '{4层批注}' WHERE itemID = {annotationItemID};
```

- 对每条用户 highlight/underline 按 4 层结构写批注（定义+溯源 / 本文角色 / 论证关联 / 批判延伸）
- 若标注原文含关键术语，第 1 层按 concept_excavation.md 的 9 层规格展开
- 存在易混概念时做并排辨析表（写在 comment 里）

**步骤 1b：质量校验**

每写完一批 comment，执行 SQL 自检：

```sql
SELECT 
  itemID,
  CASE 
    WHEN comment IS NULL OR length(comment) < 50 THEN 'FAIL — 过短或空'
    WHEN comment NOT LIKE '%定义%' AND comment NOT LIKE '%溯源%' AND comment NOT LIKE '%本文角色%' THEN 'WARN — 缺定义/溯源/角色层'
    ELSE 'OK'
  END AS quality_flag
FROM itemAnnotations 
WHERE parentItemID = {attachmentID}
  AND comment IS NOT NULL
ORDER BY quality_flag DESC;
```

质量标准：
- 长度 ≥ 50 字符
- 至少包含以下 3 层中的 2 层标记：【定义】/【溯源】/【本文角色】

FAIL → 重写该条 comment。
WARN → 标注为待审阅，在输出中列出。

返回时在 JSON 中新增 quality_check 字段：

```json
{
  "quality_check": {
    "total": 38,
    "pass": 36,
    "warn": 2,
    "fail": 0,
    "fail_ids": []
  }
}
```

**步骤 2：AI 补充 ~10 条 → 生成 📌 关键标注 Markdown 表格**

扫描全文，找出用户没划但高价值的段落（满足以下任一条件）：
(a) 含用户很可能不懂的术语
(b) 是让论文成立的承重方法决策
(c) 是核心论点的关键证据句
(d) 作者强调的反直觉结论或局限

为这 ~10 条生成 Markdown 表格，格式：

```markdown
### 📌 关键标注 (AI Annotation Highlights)

| # | 原文 | 区域 | 批注 |
|---|------|------|------|
| 1 | "...exact PDF text..." | Intro | 【定义】... 【本文角色】... 【论证关联】... 【延伸】... |
```

每条批注 ~80-150 字，含 4 层结构但压缩为一段。

### 3. 模式 B：用户无划线 → 全部 AI 标注嵌入笔记

生成 ~20 条 📌 关键标注 Markdown 表格，按区域分配：
- Intro ~5 / Methods ~7 / Results ~4 / Discussion ~4

格式同模式 A 步骤 2。

### 4. 审稿人自审

⛰️ 级强制，⚔️ 级可选，📌/🌫️ 跳过。
用敌对视角审视笔记初稿，输出 7 维度评估 + 攻击点。

## 输出

返回以下结构给主 agent：

```json
{
  "mode": "A" or "B",
  "existing_annotations_updated": N,
  "ai_annotation_table_markdown": "### 📌 关键标注 (AI Annotation Highlights)\n| # | ...",
  "reviewer": {
    "performed": true,
    "weakest_claim": "",
    "challenges": []
  }
}
```
