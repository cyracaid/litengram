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
  - Zotero Web API (https://api.zotero.org/) — 用于云端下载缺失 PDF
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
  ├─ task(stage_0_dedup)       ← 查重：是否已处理过？
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
| 0 Dedup | `task()` | 论文标识 | 查重结果（new / duplicate / partial）|
| 1-2 Intake | `task()` | 论文标识（DOI / key / 标题） | 优先级 + 上下文 + PDF 全文 + 标注清单 + litreview_dir |
| 3 Analysis | `task()` | 上文产出 + `references/` | 5 维度分析文本 + 概念深挖素材 |
| 4-5 Annotations | `task()` | 分析文本 + PDF + 标注清单 | UPDATE 已有注释 + AI 标注表格（嵌入笔记）+ 审稿人报告 |
| 6 Note | `task()` | 所有上文 + `references/` | 结构化笔记 Markdown |
| 7 Sync | **主 agent 直行** | 笔记 .md + 脚本 | 本地 .md + Zotero note + Notion page |

---

## 局部重跑入口

用户可随时对已完成论文单独重跑标注阶段（Stage 4-5-6-7）：

触发词: "重新标注" / "reannotate" / "处理划线" / "加标注" / "标注这篇" + 论文标识

流程:
```
1. 从 Zotero 获取论文 itemKey / attachmentKey / parentItemID
2. Stage 4-5: 运行时查询当前标注数 → 动态判定模式 → 生成标注
3. Stage 6: 更新笔记中 📌 关键标注 节
4. Stage 7: 同步 Zotero 子笔记 + 本地 .md + Notion
```

跳过: Stage 1-2（无需重新判定优先级）和 Stage 3（已有分析文本复用）。

---

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

实现脚本: `scripts/synthesize_notes.py`

---

## 各阶段 Prompt 模板

### Stage 0: Dedup Check（查重）

在新论文进入完整管线前，先检查是否已处理过，避免重复跑覆盖旧笔记。

执行 prompt 在 `references/stage_0_dedup.md`。

若结果为 duplicate → 告知用户，提供选项（跳过 / 重新处理 / 仅重跑某阶段）。
若结果为 new → 正常进入 Stage 1-2。

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

执行 prompt 在 `references/stage_4-5_annotations.md`。主 agent 传入 attachmentKey + attachmentItemID，
Stage 4-5 启动时自行查询 Zotero API 获取当前标注数，动态判定模式。

须先读：
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

写入 `{litreview_dir}/{AuthorYear_ShortTitle}.md`。

`litreview_dir` 由 Stage 1-2 从 Zotero collection 自动解析并传入。默认值为 `~/Documents/litengram/litreview/`。

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
| `references/stage_0_dedup.md` | Stage 0 查重 task prompt | task 调度 |
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
    stage_0_dedup.md          ← task prompt 模板
    stage_1-2_intake.md       ← task prompt 模板
    stage_3_analysis.md       ← task prompt 模板
    stage_4-5_annotations.md  ← task prompt 模板
    stage_6_note.md           ← task prompt 模板
```
