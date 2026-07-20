# LitEngram — 文献深度精读系统

> Single-Paper Deep Reading OS · 单篇论文深度处理管线

LitEngram 是一个面向科研工作者的 AI 驱动的文献精读框架。它将一篇论文从原始 PDF 转换为结构化的深度笔记，并同步到 **Zotero** 和 **Notion** 两个知识库。

> 笔者是心理学研究者，框架偏向心理学文献（实验设计、EEG/fMRI 方法、临床样本等）。其他学科也完全可用，只是模板细节可能更贴近心理学惯例。

---

## 核心理念

- **一次只读一篇**：不并行，不跳读，每一篇都挖到底
- **标注即笔记**：PDF 高亮 → 结构化字段 → 概念深挖 → 同步输出，一条线走完
- **三端同步**：本地 `.md` + Zotero 子笔记 + Notion 每日文献页，各取所需
- **混合认知标注**：用户划线决定读什么，AI 补充你漏掉的关键维度
- **Meta-skill 调度**：LitEngram 是调度框架，各阶段通过 `task()` 分发到子 agent 专注执行

---

## 管线总览

| 阶段 | 执行方式 | 产出 |
|------|---------|------|
| Stage 1-2 Intake | `task()` 分发 | 优先级 + 上下文 + PDF + 标注清单 |
| Stage 3 Analysis | `task()` 分发 | 5 维度分析文本 + 概念深挖素材 |
| Stage 4-5 Annotation | `task()` 分发 | 混合标注（写入 Zotero）+ 审稿人报告 |
| Stage 6 Note | `task()` 分发 | 结构化笔记 Markdown |
| Stage 7 Sync | **主 agent 直行** | 本地 .md + Zotero + Notion 三端同步 |

---

## 前置条件

### 依赖

```bash
pip install notion-client==3.0.0
```

### Notion（可选）

如使用 Notion 同步：

1. 在 [notion.so/my-integrations](https://www.notion.so/my-integrations) 创建 Integration，复制 Internal Integration Token
2. 把你用于记文献的 Notion 页面 Share 给该 Integration
3. 设置环境变量：

```bash
export NOTION_TOKEN="ntn_你的token..."
```

> Token 只通过环境变量传入，不写入任何文件。

### Zotero

Zotero 自动使用本地的 `zotero.sqlite` 数据库，无需额外配置。

### 环境变量（可选覆盖）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `NOTION_TOKEN` | — | Notion Integration Token（必填以启用 Notion 同步） |
| `LITENGRAM_CONFIG_PATH` | `~/Documents/CAD/.litengram_config.json` | Notion 页面 ID 缓存路径 |
| `ZOTERO_DB_PATH` | `~/Zotero/zotero.sqlite` | Zotero SQLite 数据库路径 |
| `LITENGRAM_LIBRARY_ID` | `1` | Zotero 库 ID（通常为 1） |

---

## 快速开始

### 方式一：Agent 对话（推荐）

在支持 LitEngram Skill 的 AI Agent 中，直接说：

> "帮我读这篇：DOI 10.1038/s41593-024-01650-4"
> "LitEngram this paper: C5WAAYXR"

Agent 会自动加载 meta-skill，通过 `task()` 分发各阶段，最后主 agent 完成三端同步。

### 方式二：手动调用脚本

```python
# Zotero 同步
from scripts.zotero_sync import sync_note
sync_note("/path/to/note.md", parent_item_id=2317)

# Notion 同步
from scripts.notion_sync import NotionSync
ns = NotionSync()
ns.resolve_page_id()
ns.sync_note(title="论文标题", markdown_content="...", date_str="2026-07-20")
```

---

## 输出格式

### 本地 `.md` 文件

路径：`litreview/{AuthorYear}_{ShortTitle}.md`

结构：
- `#` 标题 + 日期
- `##` 关键词
- `###` 基本信息 / 研究背景 / 理论背景 / 关键引用 / 研究方法 / 核心发现 / 与你领域的关系 / 为什么重要
- `####` 概念深挖（9 层结构）
- `| 表 |` 易混辨析

### Zotero 子笔记

渲染为 HTML，自动 wrap 在 `<div class="zotero-note znv1">` 中，支持 h1-h4、table、blockquote、ul/ol、code。

### Notion 每日页

```
每日读读文献
  └─ 2026-07-20 (toggle)
       └─ 论文标题 (toggle)
            ├─ heading_3: 基本信息
            ├─ bulleted_list: 元数据项
            ├─ heading_3: 研究背景
            ├─ ...
            └─ table: 易混辨析
```

---

## 文件结构

```
litengram/
├── SKILL.md                      # Meta-skill 入口（调度表 + 触发词）
├── README.md                     # 本文件
├── .gitignore
├── scripts/
│   ├── notion_sync.py            # Notion API 同步（增量更新，幂等）
│   └── zotero_sync.py            # Zotero SQLite 写入（XHTML 转换）
└── references/
    ├── stage_1-2_intake.md       # Intake 阶段 task prompt
    ├── stage_3_analysis.md       # 分析阶段 task prompt
    ├── stage_4-5_annotations.md  # 标注阶段 task prompt
    ├── stage_6_note.md           # 笔记阶段 task prompt
    ├── annotation_guidelines.md   # 混合认知标注规则
    ├── concept_excavation.md     # 概念深挖 9 层格式
    ├── literature_analysis_framework.md  # 5 维度解剖框架
    ├── literature_note_template.md       # 笔记模板 + 渲染规范
    ├── notion_sync.md            # Notion 同步指南
    ├── paper_priority.md         # 优先级评分标准
    ├── research_profile_template.md
    ├── reviewer_protocol.md      # 审稿人自审协议
    └── zotero_workflow.md        # Zotero 工作流
```

---

## 核心原则

### 增量同步

Notion 同步是**增量**的：
- 从不删除已有的日期 toggle
- 只更新指定的论文 toggle（清空子块 + 重新追加）
- 同日期下其他论文不受影响

### 三端互不阻塞

本地 `.md` / Zotero / Notion 各自独立写入。任何一端失败不影响另两端。

### Token 安全

- `NOTION_TOKEN` 只从环境变量读取
- `.litengram_config.json` 只缓存 Notion 页面 ID（非机密）
- 绝不将 API Token 写入任何文件

---

## 许可证

MIT
