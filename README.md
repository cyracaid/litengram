# LitEngram — 文献深度精读系统

> Single-Paper Deep Reading OS · 单篇论文深度处理管线

LitEngram 是一个面向科研工作者的 AI 驱动的文献精读框架。它将一篇论文从原始 PDF 转换为结构化的深度笔记，并同步到 **Zotero** 和 **Notion** 两个知识库。

> 笔者是心理学研究者，框架偏向心理学文献（实验设计、EEG/fMRI 方法、临床样本等）。
> **v1.5 起支持 CS/NLP 双域**：通过 domain 判定自动分发分析模板与审稿清单，心理学路径保持原样、
> NLP/ACL 路径走旁路（sidecar）。能力等价，两域互补（NLP 吃心理学的显著性/效应量纪律，
> 心理学用 AI 工具的论文吃 NLP 的可复现性/数据污染检查）。

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

> ⚠️ **使用前先同步（刷新）**：LitEngram 的部分写入走本地 SQLite（`synced=0`），
> 或依赖云端条目/附件。**每次开始前先在 Zotero 客户端点一次同步**，
> 确保本地库与云端一致，避免旧状态导致重复条目、附件缺失或同步冲突。
> 脚本写入后同样建议再同步一次，把新条目/标注推到云端。

### 环境变量（可选覆盖）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `NOTION_TOKEN` | — | Notion Integration Token（必填以启用 Notion 同步） |
| `ZOTERO_API_KEY` | — | Zotero Web API Key（上传 PDF 附件 / 云端下载缺失 PDF / 批量导入 必需） |
| `ZOTERO_USER_ID` | `11261922` | Zotero 用户 ID（配合 API Key 使用） |
| `LITENGRAM_CONFIG_PATH` | `~/Documents/CAD/.litengram_config.json` | Notion 页面 ID 缓存 + project_dirs 映射路径 |
| `ZOTERO_DB_PATH` | `~/Zotero/zotero.sqlite` | Zotero SQLite 数据库路径 |
| `LITENGRAM_PDF_INBOX` | `~/Zotero/pdf-inbox/` | PDF 下载落点（云端下载/手动模式） |
| `LITENGRAM_LIBRARY_ID` | `1` | Zotero 库 ID（通常为 1） |

### 论文落点（project_dirs 映射）

笔记本地 `.md` 的写入目录由「论文所属 Zotero collection 名 → 磁盘目录」映射决定，
在 `.litengram_config.json` 的 `project_dirs` 里配置：

```json
{
  "project_dirs": {
    "CAD": "~/Documents/CAD"
  }
}
```

- Zotero collection 名命中 `project_dirs` 键 → 该 collection 的论文笔记写入 `{dir}/litreview/`
- collection 无匹配 → 默认 `~/Documents/CAD/litreview/`
- 不同研究各自注册独立的 collection → 目录映射，笔记按项目归置（如 `2608NLP` → `~/Documents/CAD/2608NLP/litreview/`），多个项目互不混入默认目录

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

# DOI → Zotero 条目 → PDF 附件 上传（Web API，需 ZOTERO_API_KEY）
# 先从 Zotero 客户端同步一次，再执行：
python3 scripts/zotero_upload.py --doi 10.1093/scan/nsaf102 --pdf /tmp/paper.pdf --collection CAD
# 或挂在已有条目下：
python3 scripts/zotero_upload.py --item-key 9BKZ3QUE --pdf /tmp/paper.pdf

# 手动模式（推荐：上传慢 / WebDAV 限流时）：只下载 PDF 到 inbox + 打印拖入指引
python3 scripts/zotero_upload.py --manual --doi 10.1093/scan/nsaf102
python3 scripts/zotero_upload.py --manual --item-key 9BKZ3QUE
```

> 首次使用前先同步 Zotero（右上角旋转箭头），脚本执行后也建议再同步一次。
> PDF 下载默认落在 `~/Zotero/pdf-inbox/`（`LITENGRAM_PDF_INBOX` 可改）。
> 手动模式打印文件路径与拖入指引，PDF 拖进 Zotero 后由客户端自行同步。

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
│   ├── zotero_sync.py            # Zotero SQLite 写入（XHTML 转换）
│   ├── zotero_cloud.py           # 云端 PDF 下载 → inbox + 手动挂载指引
│   └── zotero_upload.py          # Zotero Web API 上传（DOI→条目→PDF 附件 / --manual）
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

## v1.2 修复记录

### v1.2 — Annotation position 字段 SQLite INSERT 卡死（已修复）

修复方式: 方案 C — 放弃 SQLite INSERT 新 annotation。UPDATE 已有 comment 保留；
AI 补充标注嵌入笔记正文 📌 关键标注 节（Markdown 表格 → Zotero HTML table）。

修改文件: annotation_guidelines.md, stage_4-5_annotations.md, literature_note_template.md,
stage_6_note.md, SKILL.md

---

## v1.3 修复记录

### v1.3 — Zotero key 生成 bug（重大） + Web API 上传脚本

**根因**：`zotero_sync.py` 和 `zotero_workflow.md` 用 `secrets.token_hex(6)`
生成 12 位小写 hex key —— Zotero 服务器拒绝（`400 'KEY' is not a valid item key`，
key 必须 8 位 `[2-9A-NP-Z]`，不含 0/1/O），导致新增条目/标注永远无法同步。

修复：
- `scripts/zotero_sync.py`：key 生成改为 `zotero_key()`（8 位 `[2-9A-NP-Z]`）
- `references/zotero_workflow.md`：修正 key 生成文档 + 新增「八、Web API 上传完整流程」
- `scripts/zotero_upload.py`：**新增** —— DOI → 条目 → PDF 附件一键上传（Web API v3）
- `README.md`：新增「使用前先同步」提示

**上传流程关键坑**（已验证）：
- 附件创建时**不能带 md5/mtime**，否则上传授权 412 "file exists"
- 上传授权必须 form-urlencoded + `If-None-Match: *`，`mtime` 用毫秒
- S3 POST 字段顺序：`key` 第一个、`file` 最后

修改文件: scripts/zotero_sync.py, scripts/zotero_upload.py,
references/zotero_workflow.md, README.md

---

## v1.4 修复记录

### v1.4 — PDF inbox + 手动挂载模式

新增：
- `scripts/zotero_cloud.py`：PDF 下载落点统一到 inbox
  （`LITENGRAM_PDF_INBOX` 优先，默认 `~/Zotero/pdf-inbox/`），
  下载成功打印路径 + 打开目录 + 手动挂载指引
- `scripts/zotero_upload.py`：新增 `--manual` —— 只下载 PDF 到 inbox，
  打印拖入 Zotero 指引，不做 Web API 上传（WebDAV 限流/上传慢时的推荐路径）
- `scripts/zotero_upload.py`：**WebDAV 模式守卫** —— 自动上传检测到客户端
  `storage.protocol=webdav` 时拒绝执行并提示 `--manual`（WebDAV 客户端拉不到
  S3 文件会成孤儿附件），`--force` 可覆盖
- 失败输出统一为 `✗ 步骤: 原因: 处理:`，不再裸 traceback

动机：Web API 上传慢 + 坚果云 WebDAV 503 限流（见 docs/issues/2026-08-13-jianguoyun-webdav-503.md），
手动拖 PDF 由 Zotero 客户端自己同步，绕开 API 与限流。

修改文件: scripts/zotero_cloud.py, scripts/zotero_upload.py,
references/zotero_workflow.md, README.md

---

## v1.5 修复记录

### v1.5 — NLP/ACL 双域支持（sidecar，psych 零破坏）

新增 CS/NLP 一侧的并行分析路径，共用核心分析引擎（三遍读法 / 5 维度 / 9 层深挖 / 结构门禁 / 输出兼容层）。

- **domain 判定**：Stage 3 维度 2 按三个信号（术语 / venue / 内容）判定 `psych / nlp / hybrid / review-theory`，下游 Stage 5/6 按它选清单与模板
- **NLP 评测公平性 checklist**：基线同预算调参、显著性检验、指标 cherry-pick、多次 seed 方差、消融完整、数据污染/预训练泄漏、人类评估一致性、代码公开 —— 与 psych 统计完整性 checklist 并行，互不覆盖
- **方法节 domain 分发**：psych 版（被试/设计/流程/分析）保留原样；nlp 版新增（任务/数据/架构/训练/评测 + AI 实验设计检查点）；hybrid 双版全量
- **📏 复现性节**（全类型必填）：代码状态 / 数据 license / 算力门槛 / 复现数字核对
- **核心发现**：nlp/hybrid 加 SOTA vs 本文 vs 强基线 对比表
- **📎 关键引用**：新增 🧰 实现来源 角色符号；arXiv 论文引用格式
- **论文类型** 七分类 → 九分类：+🗂️ Dataset/Resource、🖥️ System
- **审稿人自审**：维度 4 按 domain 分发；新增 NLP 域攻击点（评测不公 / 指标挑软 / 污染泄漏 / human-eval 缺一致性）
- **arXiv 直抓分支**：无 Zotero / 输入 arXiv ID 时，从 `export.arxiv.org` 拿元数据 + 下 PDF 到 pdf-inbox，`pdf_status=not_imported` 时 Stage 7b 跳过 Zotero 写入

> psych 路径零改动：统计完整性 checklist、psych 方法四子节、七类型（现九类）均保留。
> 唯一全类型新增是 📏 复现性节（psych 也对应对应 open data 项）。

修改文件: references/literature_analysis_framework.md, literature_note_template.md,
paper_priority.md, reviewer_protocol.md, stage_1-2_intake.md, stage_6_note.md

---

### 批量导入候选清单（收件，非精读）

文献扫描产出的候选 arXiv 清单可用 `zotero_add_batch_2608NLP.py`（在项目 `literature/` 目录）
一键导入 Zotero 指定 collection：

```bash
python3 zotero_add_batch_2608NLP.py --collection 2608NLP --dry-run   # 预览
python3 zotero_add_batch_2608NLP.py --collection 2608NLP             # 真实导入
```

- 元数据抓取走 `export.arxiv.org`，**必须在你本机（能连外网）终端跑**；云端沙箱 egress 挡该 host
- 导入的是**收件箱**（inbox），全部条目 `❓未核实` —— 不等同于精读笔记
- 精读仍是 LitEngram 逐篇管线：从 collection 取一篇 → Stage 0-7 → 单独成笔记
- README 顶部"一次只读一篇"不变：批量导入只是把候选归拢进 Zotero，Depth 精读依旧逐篇

---

## 许可证

MIT
