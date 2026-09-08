# LitEngram Annotation Position Fix — 标注写入架构修复

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 Stage 4-5 标注写入机制：已有划线 UPDATE comment 正常工作，AI 补充标注改为嵌入笔记正文（不再通过 SQLite INSERT 创建新 PDF annotation），消除 Zotero 卡死问题。

**Architecture:** 两路分流 — 模式 A（用户有划线）SQLite UPDATE 已有 annotation 的 comment 字段 + AI 补充写入笔记 📌 关键标注节；模式 B（无划线）全部 AI 标注写入笔记 📌 关键标注节。术语提取作为标注智能化的前置步骤。放弃 SQLite INSERT 新 annotation（position 无法构造）。

**Tech Stack:** Python + SQLite (UPDATE only) + Markdown → Zotero HTML (zotero_sync.py 已有) + Notion API (notion_sync.py 已有)

---

### Task 1: 更新 annotation_guidelines.md — 标注规则改为两路分流

**Files:**
- Modify: `~/.agents/skills/litengram/references/annotation_guidelines.md`

- [ ] **Step 1: 更新核心规则节**

将文件开头的核心规则从：

```
有 highlight/underline → 混合模式（注释全部用户划线 + AI 补充 ~10 条）
无 highlight/underline → AI 智能标注 ~20 条
```

改为：

```markdown
## 核心规则（v1.2 修复：SQLite 只 UPDATE 不 INSERT 新 annotation）

```
有 highlight/underline → 模式 A（混合）：
  步骤 1: 对已有 annotation → SQLite UPDATE comment（安全，不动 position）
  步骤 2: AI 补充 ~10 条 → 写入笔记 📌 关键标注 节（不创建新 PDF 高亮）
  
无 highlight/underline → 模式 B（纯 AI）：
  生成 ~20 条 → 全部写入笔记 📌 关键标注 节（不创建新 PDF 高亮）
```

> **架构约束**：`itemAnnotations.position` 需要合法的 PDF 坐标（pageIndex + rects），
> 这些数据只能由 Zotero 内部的 PDF 渲染引擎生成，SQLite 不可能构造合法 position。
> 因此 **禁止 INSERT 新 annotation 条目到 itemAnnotations 表**。
> UPDATE 已有 annotation 的 comment 字段是安全的（不改 position）。
```

- [ ] **Step 2: 在文件末尾添加 📌 关键标注 节格式规范**

```markdown
---

## 📌 关键标注 节格式（嵌入笔记正文）

当无法创建 PDF annotation 时，AI 标注以 Markdown 嵌入笔记正文：

```markdown
### 📌 关键标注 (AI Annotation Highlights)

| # | 原文 | 区域 | 批注 |
|---|------|------|------|
| 1 | "...exact PDF text..." | Intro | 1️⃣定义 2️⃣本文角色 3️⃣论证关联 4️⃣批判延伸 |
| 2 | "...exact PDF text..." | Methods | ... |
| ... | ... | ... | ... |

**覆盖区域**: Intro (N条) / Methods (N条) / Results (N条) / Discussion (N条)
```

每行批注按 4 层结构写——但长度控制在一段内（~80-150 字），不同于独立 PDF annotation 的不限字数版。
```

- [ ] **Step 3: 提交**

```bash
git add ~/.agents/skills/litengram/references/annotation_guidelines.md
git commit -m "docs: update annotation guidelines — SQLite UPDATE only, AI supplements embed in note"
```

---

### Task 2: 更新 stage_4-5_annotations.md — 标注阶段 task prompt

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_4-5_annotations.md`

- [ ] **Step 1: 替换整个文件内容**

```markdown
# Stage 4-5: Cognitive Annotation + Reviewer

> 由 LitEngram meta-skill 调度。标注已有划线 + 生成 AI 补充标注（嵌入笔记）+ 审稿人自审。
> v1.2 修复：不再通过 SQLite INSERT 创建新 PDF annotation，AI 补充标注改为嵌入笔记 📌 关键标注 节。

## 输入

从主 agent 处接收：
- 分析结果（Stage 3 产出）
- 论文全文
- 已有标注清单（annotation count + 每条内容和 itemID）

## 步骤

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
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/references/stage_4-5_annotations.md
git commit -m "docs: update stage_4-5 task prompt — SQLite UPDATE only, AI annotations embedded in note"
```

---

### Task 3: 更新 literature_note_template.md — 添加 📌 关键标注 节

**Files:**
- Modify: `~/.agents/skills/litengram/references/literature_note_template.md`

- [ ] **Step 1: 在"10 个必须部分"列表中添加第 11 部分**

将文件中的 10 部分列表改为 11 部分。在 `### 💡 核心发现` 之前插入一行 `### 📌 关键标注          【必填 · v1.2 新增】`。

具体修改：将模板的 10 部分说明从：

```markdown
## 10 个必须部分（每节/子节均不可省）

每份阅读笔记必须包含以下 10 个部分。若某节在论文中无对应内容...
```

改为：

```markdown
## 11 个必须部分（每节/子节均不可省 · v1.2）

每份阅读笔记必须包含以下 11 个部分。若某节在论文中无对应内容...

```
### 📋 基本信息
### 📚 研究背景
  ...
### 📎 关键引用          【必填】
### 🔬 研究方法          【必填】
### 📌 关键标注          【必填 · v1.2 新增】
### 💡 核心发现          【必填】
  ...
```
```

- [ ] **Step 2: 在模板中 📎 关键引用 与 🔬 研究方法 之间插入 📌 关键标注 节模板**

在完整模板的 `### 📎 关键引用` 节之后，`### 🔬 研究方法` 节之前，插入：

```markdown

### 📌 关键标注 (AI Annotation Highlights)

| # | 原文 | 区域 | 批注 |
|---|------|------|------|
| 1 | "...exact PDF text from Introduction..." | Intro | 【定义】... 【本文角色】... 【论证关联】... 【延伸】... |
| 2 | "...exact PDF text from Methods..." | Methods | ... |
| ... | ... | ... | ... |

**覆盖区域**: Intro (5条) / Methods (7条) / Results (4条) / Discussion (4条)

> 本节由 Stage 4-5 生成。若论文已有用户划线，AI 补充 ~10 条；若无划线，AI 生成 ~20 条。
> 每条批注 ~80-150 字，含 4 层结构（定义/本文角色/论证关联/批判延伸）。
```

- [ ] **Step 3: 更新结构门禁 checklist，添加 📌 关键标注 条目**

在结构门禁 checklist 的 `📎 关键引用` 行之后添加：

```
[ ] ### 📌 关键标注 — 存在且非空（表格 ≥5 行，覆盖 ≥3 个区域）
```

- [ ] **Step 4: 更新输出兼容层，说明 📌 关键标注 是表格 → Zotero HTML table**

在输出兼容层的 "HTML 渲染" 表中添加一行说明表格渲染为 `<table>`。

- [ ] **Step 5: 提交**

```bash
git add ~/.agents/skills/litengram/references/literature_note_template.md
git commit -m "docs: add 📌 key annotations section to note template — embedded AI annotation table"
```

---

### Task 4: 更新 stage_6_note.md — 笔记合成阶段包含标注表格

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_6_note.md`

- [ ] **Step 1: 在合成步骤中说明 📌 关键标注 的来源**

在步骤 2 "合成笔记" 中添加：

```markdown
### 2. 合成笔记

按模板 11 部分填充。概念深挖用 `####` 四级标题 + 平铺格式（禁止 `>` 引用块包裹）。

摘要从 Zotero 的 `abstractNote` 读取，不做改写。

📌 关键标注 节从 Stage 4-5 产出的 `ai_annotation_table_markdown` 填入——直接使用，不再改写。
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/references/stage_6_note.md
git commit -m "docs: update stage_6 to include embedded annotation table from stage_4-5"
```

---

### Task 5: 更新 SKILL.md — Meta-skill 调度表

**Files:**
- Modify: `~/.agents/skills/litengram/SKILL.md`

- [ ] **Step 1: 更新调度表中 Stage 4-5 的描述**

将调度表中的 Stage 4-5 行从：

```
| 4-5 Annotations | `task()` | 分析文本 + PDF + 标注清单 | 混合标注（写入 Zotero）+ 审稿人报告 |
```

改为：

```
| 4-5 Annotations | `task()` | 分析文本 + PDF + 标注清单 | UPDATE 已有注释 + AI 标注表格（嵌入笔记）+ 审稿人报告 |
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/SKILL.md
git commit -m "docs: update SKILL stage_4-5 description — annotations embed in note, no SQLite INSERT"
```

---

### Task 6: 更新 README.md — 标记 v1.2 修复完成

**Files:**
- Modify: `~/.agents/skills/litengram/README.md`

- [ ] **Step 1: 将已知问题节状态从 TODO 更新为 v1.2 已修复**

将 "已知问题 / 待维护" 节的标题改为：

```markdown
## v1.2 修复记录
```

将问题描述改为带版本的修复记录：

```markdown
### v1.2 — Annotation position 字段 SQLite INSERT 卡死（已修复）

**修复方式**: 方案 C — 放弃 SQLite INSERT 新 annotation。UPDATE 已有 comment 保留；AI 补充标注嵌入笔记正文 📌 关键标注 节（Markdown 表格 → Zotero HTML table）。

**修改文件**: annotation_guidelines.md, stage_4-5_annotations.md, literature_note_template.md, stage_6_note.md, SKILL.md
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/README.md
git commit -m "docs: mark annotation position fix as resolved in v1.2"
```

---

### Task 7: 验证 — 对 Dhamala 2023 这篇论文重跑 Stage 4-5 + Stage 6

**Files:**
- 只读: `litreview/Dhamala2023_BrainPredictiveModeling.md`（现有笔记）
- 修改: `litreview/Dhamala2023_BrainPredictiveModeling.md`（添加 📌 关键标注 节）

- [ ] **Step 1: 基于现有笔记，生成 20 条 📌 关键标注 Markdown 表格**

从 PDF 全文取出 20 条关键原文，按 Intro(5)/Methods(7)/Results(4)/Discussion(4) 分配，写入 📌 关键标注 表格。

- [ ] **Step 2: 用 Python 验证表格格式合法**

运行:

```python
import re
with open("litreview/Dhamala2023_BrainPredictiveModeling.md") as f:
    content = f.read()

assert "### 📌 关键标注" in content, "Missing section header"
table_lines = [l for l in content.split("\n") if l.startswith("|") and "---" not in l and "原文" not in l]
assert len(table_lines) >= 20, f"Expected ≥20 annotation rows, got {len(table_lines)}"

# Check coverage
regions = set()
for line in table_lines:
    parts = line.split("|")
    if len(parts) >= 4:
        for r in ["Intro", "Methods", "Results", "Discussion"]:
            if r in parts[3]:
                regions.add(r)
assert len(regions) >= 3, f"Expected coverage of ≥3 regions, got {len(regions)}: {regions}"
print("✅ Annotation table valid")
```

- [ ] **Step 3: 关闭 Zotero → 用 zotero_sync.py 重新写入笔记 → 重启 Zotero**

```bash
osascript -e 'quit app "Zotero"'
sleep 3
python3 ~/.agents/skills/litengram/scripts/zotero_sync.py \
  "/Users/sloblucyra/Documents/CAD/litreview/Dhamala2023_BrainPredictiveModeling.md" 2405
open -a Zotero
```

- [ ] **Step 4: 确认 Zotero 正常启动（不卡 loading）**

等待 ~15 秒，检查 Zotero 窗口正常打开，条目可浏览。

```bash
sleep 15
pgrep -x Zotero && echo "✅ Zotero running" || echo "❌ Zotero not running"
```

- [ ] **Step 5: 重新同步 Notion**

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.agents/skills/litengram/scripts"))
from notion_sync import NotionSync

with open("/Users/sloblucyra/Documents/CAD/litreview/Dhamala2023_BrainPredictiveModeling.md") as f:
    content = f.read()

ns = NotionSync()
ns.resolve_page_id()
result = ns.sync_note(
    title="Dhamala et al. (2023) One Size Does Not Fit All: Methodological Considerations for Brain-Based Predictive Modeling",
    markdown_content=content,
    date_str="2026-08-03",
    skip_if_exists=False
)
print(result)
```

- [ ] **Step 6: 提交**

```bash
git add litreview/Dhamala2023_BrainPredictiveModeling.md
git commit -m "feat: add 📌 key annotations table to Dhamala2023 note (v1.2 annotation fix)"
```
