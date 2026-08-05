# Stage 0: Dedup Check — 防重复处理

> 由 LitEngram meta-skill 调度。在 Stage 1-2 Intake 之前执行。

## 输入

从主 agent 处接收：论文 Zotero itemKey / 标题 / DOI。

## 步骤

### 1. 查询 Zotero 子笔记

通过 Zotero API 检查是否已有子笔记：

```bash
curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"
```

解析返回，查找 `itemType: "note"` 的条目。

### 2. 检查本地文件

```bash
ls /Users/sloblucyra/Documents/CAD/litreview/ | grep -i "{AuthorYear}"
```

或搜索文件内容中的 Zotero key：

```bash
grep -l "Zotero: .*{itemKey}" /Users/sloblucyra/Documents/CAD/litreview/*.md
```

### 3. 判定

- 如果 Zotero 有子笔记 **且** 本地有 .md 文件 → 已处理过
- 如果只有其一 → 部分处理（可能中断），询问用户
- 如果都没有 → 新论文，正常进入 Stage 1-2

## 输出

返回以下 JSON：

```json
{
  "status": "new" or "duplicate" or "partial",
  "existing_note": {"zotero_note_key": "..." or null, "local_md_path": "..." or null},
  "existing_grade": "⛰️/⚔️/📌/🌫️ or null",
  "suggestion": "skip / overwrite / ask_user"
}
```
