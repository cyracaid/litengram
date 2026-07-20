---
name: litengram
description: >-
  LitEngram — 文献深度精读调度系统（meta-skill）。
  将一篇论文从 PDF → 结构化深度笔记，同步到 Zotero + Notion。
  笔者是心理学研究者，框架偏向心理学文献；其他学科也可用。

  **触发**（用户明确表示需要精读论文时）：
  - 帮我读这篇 / 帮我精读 / 帮我分析这篇论文
  - LitEngram this paper / encode this paper
  - 给 DOI / Zotero key / 论文标题 + 要求深度分析
  
  不触发：一般性文献查询、简单摘要、翻译请求。
compatibility:
  - Zotero Local API (http://127.0.0.1:23119/api/)
  - SQLite (~/Zotero/zotero.sqlite)
---

# LitEngram: 文献深度精读调度系统

## 核心理念

每篇论文不是拿来看，而是拿来**编码成一段持久的研究记忆（engram）**。
读完后应具备 4 种能力：**复刻** · **批判** · **嫁接** · **反驳**

> 隐喻层仅用于叙述和输出标题，不作为触发词。

---

## 架构概览

LitEngram 是 **meta-skill**——主 agent 负责调度，各阶段通过 `task()` 分发到子 agent 执行：

```
用户请求
  ↓
主 agent (你) ← 加载 SKILL.md
  ├─ task(stage_1-2_intake)    ← 优先级 + 上下文 + 获取全文
  ├─ task(stage_3_analysis)     ← 5 维度解剖 + 概念深挖素材收集
  ├─ task(stage_4-5_annotations) ← 混合标注 + 审稿人自审
  ├─ task(stage_6_note)         ← 笔记合成
  └─ Stage 7（主 agent 自己执行） ← 笔记落盘 + Zotero/Notion 同步
```

各阶段可并行或串行，取决于依赖关系。每个 task 的 prompt 模板在 `references/stage_X_*.md` 中。

---

## 调度表

| 阶段 | 方式 | 输入 | 产出 |
|------|------|------|------|
| 1-2 Intake | `task()` | 论文标识（DOI / key / 标题） | 优先级 + 上下文信息 + PDF 全文 + 标注清单 |
| 3 Analysis | `task()` | 上文产出 + `references/` | 5 维度分析文本 + 概念深挖素材 |
| 4-5 Annotations | `task()` | 分析文本 + PDF + 标注清单 | 混合标注（写入 Zotero）+ 审稿人报告 |
| 6 Note | `task()` | 所有上文 + `references/` | 结构化笔记 Markdown |
| 7 Sync | **主 agent 直行** | 笔记 .md + 脚本 | 本地 .md + Zotero note + Notion page |

---

## 各阶段 Prompt 模板

### Stage 1-2: Intake（优先级 + 上下文 + 获取全文）

从用户请求中提取论文标识 → 判定优先级 → 注入研究上下文 → 获取 PDF 和已有标注。

执行 prompt 在 `references/stage_1-2_intake.md`，须先读以下参考：
- `references/paper_priority.md`
- `references/research_profile_template.md`
- `references/zotero_workflow.md`

### Stage 3: Deep Analysis（5 维度解剖）

对论文正文做 5 维度方法论解剖，积累概念深挖素材。

执行 prompt 在 `references/stage_3_analysis.md`，须先读：
- `references/literature_analysis_framework.md`
- `references/concept_excavation.md`（了解深挖素材收集标准）

### Stage 4-5: Cognitive Annotation + Reviewer

生成混合标注（模式 A/B）并写入 Zotero，执行审稿人自审。

执行 prompt 在 `references/stage_4-5_annotations.md`，须先读：
- `references/annotation_guidelines.md`
- `references/concept_excavation.md`
- `references/reviewer_protocol.md`

### Stage 6: Engram Note Synthesis

将上文所有产出合成为结构化笔记 Markdown。

执行 prompt 在 `references/stage_6_note.md`，须先读：
- `references/literature_note_template.md`
- `references/concept_excavation.md`

---

## Stage 7: 同步（主 agent 执行）

笔记合成后，由主 agent 完成最后三处写入：

### 7a. 本地 .md

写入 `litreview/{AuthorYear_ShortTitle}.md`。

### 7b. Zotero

```bash
export NOTION_TOKEN="..."  # 若已设则跳过
python3 scripts/zotero_sync.py <note_path> <parent_item_id>
```

`close_zotero_first()` 会自动尝试优雅关闭 Zotero，如果失败会提示手动关闭。

### 7c. Notion

```python
from scripts.notion_sync import NotionSync
ns = NotionSync()
ns.resolve_page_id()
ns.sync_note(title=..., markdown_content=..., date_str="...", skip_if_exists=False)
```

三处互不阻塞，任一处失败打印错误后继续。

---

## 参考文件索引

| 文件 | 内容 | 被谁读 |
|------|------|--------|
| `references/paper_priority.md` | 论文类型七分类、重要等级、阅读策略 | Stage 1-2 |
| `references/research_profile_template.md` | 研究上下文模板 | Stage 1-2 |
| `references/zotero_workflow.md` | Zotero API/SQLite 技术细节 | Stage 1-2, 7 |
| `references/literature_analysis_framework.md` | 5 维度分析范式 | Stage 3 |
| `references/concept_excavation.md` | 概念深挖 9 层规格 | Stage 3, 4-5, 6 |
| `references/annotation_guidelines.md` | 混合标注规则 | Stage 4-5 |
| `references/reviewer_protocol.md` | 审稿人自审协议 | Stage 4-5 |
| `references/literature_note_template.md` | 笔记模板 + 结构门禁 + 输出兼容 | Stage 6 |
| `references/notion_sync.md` | Notion 同步规格（参考用） | Stage 7 |
| `references/stage_1-2_intake.md` | Intake 阶段 task prompt | task 调度 |
| `references/stage_3_analysis.md` | 分析阶段 task prompt | task 调度 |
| `references/stage_4-5_annotations.md` | 标注阶段 task prompt | task 调度 |
| `references/stage_6_note.md` | 笔记阶段 task prompt | task 调度 |

---

## 目录结构

```
litengram/
  SKILL.md                    ← meta-skill 入口（本文）
  README.md
  scripts/
    notion_sync.py            ← Notion API 同步
    zotero_sync.py            ← Zotero SQLite 写入
  references/
    (原分析指南)               ← 各阶段详细规格
    stage_1-2_intake.md       ← task prompt 模板
    stage_3_analysis.md       ← task prompt 模板
    stage_4-5_annotations.md  ← task prompt 模板
    stage_6_note.md           ← task prompt 模板
```
