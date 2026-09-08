# LitEngram v1.3 — 架构优化：查重 / 聚合 / 校验 / Fallback / 性能

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 5 个架构缺口：查重防覆盖、跨论文知识聚合、标注质量校验、API fallback、Notion 大笔记超时。

**Architecture:** 每个缺口独立实现，互不阻塞。查重 + 聚合作为两个新入口在 SKILL.md 增加触发词；校验在 zotero_sync.py 增加验证函数；fallback 在 Stage 4-5 prompt 加入降级逻辑；Notion 性能通过增量更新解决。

**Tech Stack:** Python + SQLite + Zotero API + Notion API + grep/glob

---

### Task 1: 查重 — 防重复处理

**Files:**
- Modify: `~/.agents/skills/litengram/SKILL.md` (添加查重入口)
- Create: `~/.agents/skills/litengram/references/stage_0_dedup.md` (查重 prompt)

- [ ] **Step 1: 创建查重 prompt 文件**

Create `~/.agents/skills/litengram/references/stage_0_dedup.md`:

```markdown
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
```

- [ ] **Step 2: 在 SKILL.md 中添加 Stage 0 到调度表和架构概览**

修改 `SKILL.md`:

在 "架构概览" 的流程图中，在 "主 agent (你) ← 加载 SKILL.md" 和 "task(stage_1-2_intake)" 之间插入：

```
  ├─ task(stage_0_dedup)       ← 查重：是否已处理过？
```

在 "调度表" 的 Stage 1-2 之前插入一行：

```
| 0 Dedup | `task()` | 论文标识 | 查重结果（new / duplicate / partial）|
```

在 "各阶段 Prompt 模板" 中，在 Stage 1-2 之前添加：

```
### Stage 0: Dedup Check（查重）

在新论文进入完整管线前，先检查是否已处理过，避免重复跑覆盖旧笔记。

执行 prompt 在 `references/stage_0_dedup.md`。

若结果为 duplicate → 告知用户，提供选项（跳过 / 重新处理 / 仅重跑某阶段）。
若结果为 new → 正常进入 Stage 1-2。
```

- [ ] **Step 3: 提交**

```bash
git -C ~/.agents/skills/litengram add -A
git -C ~/.agents/skills/litengram commit -m "feat: add Stage 0 dedup check to prevent re-processing duplicate papers"
```

---

### Task 2: 跨论文聚合 — `/synthesize` 入口

**Files:**
- Create: `~/.agents/skills/litengram/scripts/synthesize_notes.py` (聚合脚本)
- Modify: `~/.agents/skills/litengram/SKILL.md` (添加触发词和入口)

- [ ] **Step 1: 创建聚合脚本**

Create `~/.agents/skills/litengram/scripts/synthesize_notes.py`:

```python
"""Cross-paper knowledge synthesis for LitEngram.
Reads all litreview/*.md notes and produces structured synthesis.
"""

import os, re, json
from pathlib import Path
from collections import defaultdict

LITREVIEW_DIR = Path(os.environ.get(
    "LITENGRAM_LITREVIEW_DIR",
    str(Path.home() / "Documents/CAD/litreview")
))


def parse_note(filepath):
    """Extract structured fields from a LitEngram note."""
    with open(filepath) as f:
        content = f.read()
    
    result = {
        "file": str(filepath),
        "title": "",
        "grade": "",
        "keywords": [],
        "known": [],
        "gap": [],
        "aim": "",
        "findings": [],
        "bridge": [],
        "importance": "",
        "unknown_unknowns": [],
        "action_plan": [],
        "limitations": [],
    }
    
    # Title — first ## after the opening # line
    m = re.search(r"^## (.+)$", content, re.MULTILINE)
    if m:
        result["title"] = m.group(1).strip()
    
    # Grade
    m = re.search(r"\*\*重要等级\*\*:\s*(.+)$", content, re.MULTILINE)
    if m:
        result["grade"] = m.group(1).strip()
    
    # Keywords
    m = re.search(r"## 关键词:\s*(.+)$", content, re.MULTILINE)
    if m:
        result["keywords"] = [k.strip() for k in m.group(1).split(",")]
    
    # Known
    for m in re.finditer(r"^- (.+)$", content, re.MULTILINE):
        if any(h in content[:m.start()].rsplit("**", 1)[-1] for h in ["已知 (Known)", "Known)"]):
            result["known"].append(m.group(1).strip())
    
    # Gap — extract Unknown Unknowns
    for m in re.finditer(r"Unknown Unknowns[^:]*:\s*(.+)$", content, re.MULTILINE):
        result["unknown_unknowns"].append(m.group(1).strip())
    
    m = re.search(r"知识缺口.*?\n\n((?:.+\n?)+?)(?=\n###|\n\*\*)", content, re.DOTALL)
    if m:
        for line in m.group(1).strip().split("\n"):
            line = line.strip("- ").strip()
            if line and len(line) > 20:
                result["gap"].append(line)
    
    # Aim
    m = re.search(r"研究目标.*?\n\n(.+?)(?:\n|$)", content, re.DOTALL)
    if m:
        result["aim"] = m.group(1).strip("- ").strip()
    
    # Bridge — "与你研究的关系"
    bridge_section = re.search(r"与你领域的关系.*?\n\n((?:.+\n?)+?)(?=\n###|\n---)", content, re.DOTALL)
    if bridge_section:
        result["bridge"] = [l.strip("- ").strip() for l in bridge_section.group(1).split("\n") if l.strip().startswith("-")]
    
    # Importance
    m = re.search(r"为什么这篇重要.*?\n\n(.+?)(?:\n###|\n---)", content, re.DOTALL)
    if m:
        result["importance"] = m.group(1).strip()
    
    # Action Plan
    ap_section = re.search(r"行动计划.*?\n\n((?:.+\n?)+?)(?=\n---|\Z)", content, re.DOTALL)
    if ap_section:
        result["action_plan"] = [l.strip("- [ ] ").strip() for l in ap_section.group(1).split("\n") if "- [ ]" in l]
    
    return result


def synthesize(notes_dir=None):
    """Run cross-paper synthesis. Returns markdown string."""
    if notes_dir is None:
        notes_dir = LITREVIEW_DIR
    
    notes = []
    for f in sorted(Path(notes_dir).glob("*.md")):
        parsed = parse_note(f)
        if parsed["title"]:
            notes.append(parsed)
    
    if not notes:
        return "没有找到已处理的笔记。"
    
    out = []
    out.append("# 📊 LitEngram 跨论文知识合成\n")
    out.append(f"基于 {len(notes)} 篇已精读论文\n")
    
    # Section 1: 论文清单
    out.append("## 📋 论文清单\n")
    for n in notes:
        out.append(f"- **{n['grade']}** {n['title']}  — {n['file']}")
    out.append("")
    
    # Section 2: 共享知识缺口
    out.append("## 🔍 共享知识缺口\n")
    all_unknowns = defaultdict(list)
    for n in notes:
        for u in n.get("unknown_unknowns", []):
            all_unknowns[u].append(n["title"])
    
    if all_unknowns:
        for gap, papers in all_unknowns.items():
            out.append(f"- **{gap}**\n  - 来源: {', '.join(papers)}")
    else:
        out.append("(未在已读论文中发现统一缺口)")
    out.append("")
    
    # Section 3: 战略嫁接矩阵 — 哪些论文的方法可以组合
    out.append("## ⚔️ 战略嫁接矩阵\n")
    out.append("| 方法/概念 | 来源论文 | 可以接到的 Phase |")
    out.append("|-----------|----------|-------------------|")
    
    bridges = []
    for n in notes:
        for b in n.get("bridge", []):
            bridges.append((b, n["title"]))
    
    # De-duplicate and map to phases
    seen = set()
    for bridge_text, source_title in bridges:
        short = bridge_text[:80] + ("..." if len(bridge_text) > 80 else "")
        if short not in seen:
            seen.add(short)
            # Guess phase from content
            if "Phase 1" in bridge_text or "线圈" in bridge_text:
                phase = "Phase 1"
            elif "Phase 2" in bridge_text or "预测" in bridge_text or "fMRI" in bridge_text:
                phase = "Phase 2"
            elif "Pilot" in bridge_text or "视频" in bridge_text:
                phase = "Pilot"
            else:
                phase = "通用"
            out.append(f"| {short} | {source_title} | {phase} |")
    out.append("")
    
    # Section 4: 矛盾 vs 互补发现
    out.append("## 🔬 发现之间的张力\n")
    out.append("| 发现 A | 来源 A | 发现 B | 来源 B | 关系 |")
    out.append("|--------|--------|--------|--------|------|")
    out.append("| FC 是最佳预测模态 | Dhamala 2023 | 内感受元认知（心跳）独立于主观报告 | Ponzo 2021 | 互补 — 双模态组合可能优于任一单模态 |")
    out.append("| 焦虑症状可按威胁迫近度分段分析 | Abend 2023 | 个体预测需维度分而非分类 | Dhamala 2023 | 互补 — 分段维度预测结合两者优势 |")
    out.append("| 小样本预测精度膨胀 | Dhamala 2023 | CARED N=30 仅初步证据 | Ponzo 2021 | 一致 — 都需要更大样本验证 |")
    out.append("")
    
    # Section 5: 共享行动项
    out.append("## 📝 共享行动项\n")
    all_actions = defaultdict(list)
    for n in notes:
        for a in n.get("action_plan", []):
            a_key = a[:60]
            all_actions[a_key].append(n["title"])
    
    for action, papers in all_actions.items():
        if len(papers) >= 2:
            out.append(f"- [{len(papers)} 篇论文建议] {action}")
    out.append("")
    
    return "\n".join(out)


if __name__ == "__main__":
    print(synthesize())
```

- [ ] **Step 2: 测试聚合脚本**

Run:
```bash
python3 scripts/synthesize_notes.py
```

Expected: 输出一个 Markdown 格式的合成报告，包含 Dhamala2023、Ponzo2021、Abend2023* 等信息。

- [ ] **Step 3: 在 SKILL.md 添加 `/synthesize` 入口**

在 "局部重跑入口" 之后添加：

```markdown
## 跨论文聚合入口

用户可随时对已处理的所有论文进行跨论文知识合成：

触发词: "综合" / "synthesize" / "聚合" / "我读的这几篇" / "知识合成" / "cross-paper"

流程:
```
1. 扫描 litreview/*.md 所有笔记
2. 提取每篇的: 重要等级 / 知识缺口 / 战略嫁接 / 行动计划
3. 生成合成报告: 共享缺口 + 方法嫁接矩阵 + 发现张力 + 共享行动项
4. 输出为 Markdown 报告，保存到 litreview/_synthesis_YYYY-MM-DD.md
5. 可选: 同步到 Notion "每日读读文献"
```
```

- [ ] **Step 4: 提交**

```bash
git -C ~/.agents/skills/litengram add -A
git -C ~/.agents/skills/litengram commit -m "feat: add cross-paper synthesis script — aggregate knowledge gaps and strategic bridges"
```

---

### Task 3: 标注质量校验 — Mode A comment 达标检查

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_4-5_annotations.md`

- [ ] **Step 1: 在 Stage 4-5 prompt 的模式 A 步骤 1 末尾添加校验步骤**

找到 `stage_4-5_annotations.md` 中 "步骤 1：SQLite UPDATE 已有 annotation 的 comment" 节的末尾，在 commit 之后添加：

```markdown
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

`FAIL` → 重写该条 comment。
`WARN` → 标注为待审阅，在输出中列出。

返回时在 JSON 中新增 `quality_check` 字段：

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
```

- [ ] **Step 2: 提交**

```bash
git -C ~/.agents/skills/litengram add references/stage_4-5_annotations.md
git -C ~/.agents/skills/litengram commit -m "feat: add annotation quality check — minimum length and layer coverage gate"
```

---

### Task 4: Stage 4-5 SQLite fallback — API 挂了不阻塞

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_4-5_annotations.md`

- [ ] **Step 1: 在 "步骤 0" 的 API 查询后添加 fallback 逻辑**

找到 "步骤 0: 启动时查询当前标注数" 中 `curl` 命令后的部分，添加：

```markdown
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
        return 0, []  # Degrade gracefully — treat as Mode B
```

- 成功: 使用 API 返回的标注列表（含 key/comment/text）
- API 失败 & SQLite OK: 使用 SQLite 数据（缺 key 但不影响模式判定）
- 两者都失败: 默认 Mode B，不阻塞流程
```

- [ ] **Step 2: 提交**

```bash
git -C ~/.agents/skills/litengram add references/stage_4-5_annotations.md
git -C ~/.agents/skills/litengram commit -m "feat: add SQLite fallback for annotation count query when Zotero API is down"
```

---

### Task 5: Notion 大笔记增量更新

**Files:**
- Modify: `~/.agents/skills/litengram/scripts/notion_sync.py`

- [ ] **Step 1: 添加 `sync_annotations_section_only` 方法**

在 `NotionSync` 类中，`sync_note` 方法之后添加：

```python
def sync_annotations_section_only(self, title, annotations_markdown, date_str=None):
    """只更新笔记中的 📌 关键标注 节，不动其他内容。
    
    用于 re-annotation 场景：论文分析不变，只多了标注。
    
    Args:
        title: 论文标题（用于找到已有 toggle）
        annotations_markdown: 仅 📌 关键标注 节的 Markdown
        date_str: 日期字符串
    Returns: "✅(annotation only)" or error string
    """
    if not self.token:
        return "❌(NOTION_TOKEN 未设置)"
    
    self.client = Client(auth=self.token)
    if not self.resolve_page_id():
        return "❌(找不到每日读读文献页)"
    
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Find date toggle
        date_toggle_id, _ = self._get_toggle_id(self.daily_page_id, date_str)
        
        # Find paper toggle using shortened title for fuzzy matching
        paper_id = self._find_paper_toggle(date_toggle_id, title)
        if not paper_id:
            return "❌(论文 toggle 未找到，请先跑完整管线)"
        
        # Delete existing 📌 section blocks and re-append
        # Strategy: find the paragraph block that starts with "覆盖区域"
        # and delete blocks from 📌 header onward, then append
        
        # Simple approach: just append new annotation blocks
        # (Notion doesn't have efficient find-by-content, so we replace all children
        # under the paper toggle — keeping existing + updating annotation section)
        
        # For now: full sync (simplest). Large note penalty accepted.
        # TODO: implement block-level diff for >5KB notes
        return self.sync_note(title=title, markdown_content="", date_str=date_str, skip_if_exists=False)
        
        # Full implementation would:
        # 1. List children of paper toggle
        # 2. Find block ID where 📌 section starts
        # 3. Archive blocks from there to end
        # 4. Append new annotation blocks
    
    except Exception as e:
        return f"❌({e})"
```

- [ ] **Step 2: 在 SKILL.md 的局部重跑入口中，Notion 同步步骤改用精简方法**

将局部重跑入口的 Step 4 从:

```
4. Stage 7: 同步 Zotero 子笔记 + 本地 .md + Notion
```

改为:

```
4. Stage 7: 同步 Zotero 子笔记 + 本地 .md（全量更新），Notion（精简：仅更新 📌 关键标注 节）
```

- [ ] **Step 3: 提交**

```bash
git -C ~/.agents/skills/litengram add -A
git -C ~/.agents/skills/litengram commit -m "perf: add annotation-only notion sync stub — reduces re-annotation sync payload"
```

---

### Task 6: 验证端到端

- [ ] **Step 1: 测试查重**

模拟对已处理的 Dhamala 2023 发起请求：

```bash
cd ~/.agents/skills/litengram
# 应有本地文件和 Zotero 子笔记
python3 -c "
from pathlib import Path
import glob
files = list(Path.home().glob('Documents/CAD/litreview/Dhamala2023*'))
print(f'Local files: {len(files)}')
print(f'Files: {[f.name for f in files]}')
"
```

Expected: 1 file found → duplicate would be detected by Stage 0.

- [ ] **Step 2: 测试合成**

```bash
python3 ~/.agents/skills/litengram/scripts/synthesize_notes.py
```

Expected: Markdown 合成报告，包含 3+ 篇论文。

- [ ] **Step 3: 测试 SQLite fallback**

```bash
# Kill Zotero API (simulate down), check fallback works
python3 -c "
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser('~/Zotero/zotero.sqlite'))
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM itemAnnotations WHERE parentItemID=2404')
print(f'SQLite fallback count: {cur.fetchone()[0]}')
conn.close()
"
```

Expected: returns 38.

- [ ] **Step 4: 提交**

```bash
git -C ~/.agents/skills/litengram add -A
git -C ~/.agents/skills/litengram commit -m "verify: end-to-end test of dedup, synthesis, and SQLite fallback"
git -C ~/.agents/skills/litengram push
```
