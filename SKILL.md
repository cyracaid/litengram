---
name: litengram
description: >-
  LitEngram v1.1: 文献深度精读系统（Single-Paper Deep Reading OS）。
  对学术论文进行优先级分类、研究上下文注入、5 维度方法论解剖、混合认知标注（用户划线+AI补充）、
  概念溯源引擎（含术语深挖9层+易混辨析+递归展开）、审稿人自审、结构化 Engram Note（内联深挖块）、
  并同步到 Zotero。

  **必须触发**（用户提到以下任意场景）：
  - 读论文、精读、深度精读、帮我读、分析论文、paper reading、paper analysis
  - 标注论文、做笔记、这篇怎么说、帮忙看一篇论文、帮我理解这篇
  - 给 DOI / Zotero itemKey / 论文标题时表明需要分析
  - encode this paper、LitEngram this、帮我把这篇变成笔记
  - 用户提到文献精读框架/范式时

  适用领域：心理学、认知神经科学、情感科学、临床心理学、任何需要深度精读的学科。
  自动处理：Zotero API 交互、PDF 全文提取、高亮检测、混合标注生成、4 层中英批注+概念溯源深挖、完整笔记。

  **不适用场景**：一般性摘要翻译、简单的文献查询、搜索论文元数据、跨论文综述（见 v2）。

  **触发提示**：如果你是替用户执行分析任务的 agent，当对话中出现论文标题、DOI、Zotero itemKey 且用户明显需要深度理解时，优先触发本技能。
  宁可误触也不要漏触——用户随时可以说"不需要这么深"。
compatibility:
  - Zotero Local API (http://127.0.0.1:23119/api/)
  - SQLite (~/Zotero/zotero.sqlite)
---

# LitEngram: Single-Paper Deep Reading OS

## 品牌语言

> 每篇论文不是拿来看，而是拿来**编码成一段持久的研究记忆（engram）**。

读完后应具备 4 种能力：**复刻** · **批判** · **嫁接** · **反驳**

**神经科学原则**：Encoding precedes consolidation。先把单篇编码扎实，跨论文关系才可能有意义地涌现。

> 隐喻层（engram / encode / cognitive annotation / memory trace）仅用于叙述和输出标题，**不作为触发词**。触发仍使用功能性短语。

---

## 参考文件

LitEngram 自包含：所有指南在本 skill 的 `references/` 目录中。

| 文件 | 内容 | 阅读阶段 |
|------|------|----------|
| `references/literature_analysis_framework.md` | 5 维度分析范式、三遍读法、质量检查 | Stage 3 |
| `references/annotation_guidelines.md` | **v1.1** 4 层标注结构 + **混合标注模式** + **概念溯源引擎钩子** | Stage 4 |
| `references/concept_excavation.md` | **v1.1 新增** 概念溯源引擎——9 层深挖规格、递归规则、深度分级、黄金范例 | Stage 4/6 |
| `references/literature_note_template.md` | **v1.1.1** 10 部分笔记模板 + 📎 关键引用 + 内联深挖块骨架 + Zotero 摘要读取 + **结构门禁 checklist** | Stage 6 |
| `references/paper_priority.md` | 论文类型七分类、重要等级、阅读策略四档 | Stage 0 |
| `references/reviewer_protocol.md` | 审稿人自审协议（⛰️ 强制 / ⚔️ 可选） | Stage 5 |
| `references/research_profile_template.md` | 用户研究上下文模板 | Stage 1 |
| `references/notion_sync.md` | **v1.2 新增** Notion 同步规格——日期聚合、Markdown→Notion blocks 转换、嵌套 toggle、容错降级 | Stage 7 |
| `references/zotero_workflow.md` | Zotero API/SQLite 完整技术工作流（含 v1.1 模式更新） | Stage 2/4/7 |

> **兼容说明**：若用户环境有 `~/Documents/CAD/` 目录（旧 LitForge 工作区），笔记副本仍写入 `CAD/litreview/{AuthorYear_ShortTitle}.md`。
> research_profile 优先读取 `CAD/research_profile.md`，其次 skill 同级目录，最后用户指定路径。

---

## 完整工作流（8 Stages）

### Stage 0 · Intake（读前定位）

读 `references/paper_priority.md`：

1. 判定论文类型：Theory / Methods / Empirical / Review / Benchmark / Replication / Position
2. 判定重要等级：⛰️镇山之宝 / ⚔️精兵强将 / 📌补充参考 / 🌫️过眼云烟
3. 确定阅读策略：⛰️→Deep / ⚔️→Standard / 📌→Fast / 🌫️→Skip
4. 回答读前定位 4 问
5. **[ ] NOTION_TOKEN 已设置？「每日读读文献」页已分享给 integration？**（未配置不阻塞，仅 Notion 降级跳过）

策略决定：标注密度、笔记长度、分析深度、是否执行审稿人自审、是否同步 Notion。

---

### Stage 1 · Context Injection（研究上下文注入）

**关键**——确保嫁接落到具体研究上。

1. 尝试加载 `research_profile.md`：
   - 优先 `CAD/research_profile.md`
   - 其次 skill 同级目录
   - 最后用户指定路径
2. 若存在：把用户的当前课题/研究问题/假设/数据集/pipeline/open problems 载入上下文。所有后续解读必须落到具体研究上。
3. 若不存在：读 `references/research_profile_template.md`，提示用户可创建，本次仍继续但降级为通用嫁接。

> ❌ "这个方法很有意思" → ✅ "这个预处理 pipeline 可以直接替换你双语情感分析的 Phase 2"

---

### Stage 2 · 获取全文 + 检查标注

1. 通过 Zotero API 定位论文（itemKey / DOI / 标题 / PDF 路径）
2. 提取 PDF 全文
3. 检查已有标注，确定模式：
   - `annotations.length > 0` → **模式 A：混合标注**（注释全部用户划线 → AI 补充 ~10 条）
   - `annotations.length === 0` → **模式 B：AI 智能标注**（识别 ~20 个关键点）

技术参考：`references/zotero_workflow.md`

---

### Stage 3 · Deep Analysis（5 维度解剖）

读 `references/literature_analysis_framework.md`，按 5 维度分析：

1. **解剖刀**：已知·缺口·目标（缺口用三分法）
2. **方法论三层拆解**：操作描述 → 三个 WHY → 反向验证（含统计完整性 checklist）
3. **核心发现**：2-4 个发现 + Claim-Evidence 映射
4. **战略嫁接**：必须落到 research_profile 的具体项目
5. **重要性判断**：在你研究版图中的定位

**论文类型适配**：
- Empirical / Methods / Benchmark → 方法论三层拆解
- Review / Theory / Position → 论证结构拆解（主张链条→证据类型→推理跳跃点）

**Stage 3 阶段即开始积累概念深挖素材**：遇到关键术语时记录其名称和位置，
供 Stage 4 标注和 Stage 6 笔记中使用 `references/concept_excavation.md` 的 9 层规格展开。

---

### Stage 4 · Cognitive Annotation（生成标注）

读 `references/annotation_guidelines.md`，按 4 层结构 + 概念溯源引擎逐条写批注。

**模式 A（用户已划线）→ 混合模式**：
1. 提取全部用户高亮原文，逐条按 4 层 + `concept_excavation.md` 规格生成批注
2. 扫描全文找出 ~10 条高价值未划线原文，新建 annotation 并做同等深度的挖掘
3. AI 补充的标注 comment 以 `🤖 [AI补充] ` 前缀开头

**模式 B（无划线）→ AI 智能标注 ~20 条**，同样套用概念溯源深度。

写入 Zotero SQLite（安全流程：关→写→开）。

Stage 4 结束时打印小结：用户高亮 N 条 + AI 补充 M 条，分别覆盖哪些区域。

---

### Stage 5 · Reviewer Thinking（审稿人自审）

读 `references/reviewer_protocol.md`。

- ⛰️ 级：**强制**执行
- ⚔️ 级：可选
- 📌 / 🌫️ 级：跳过

**放在笔记初稿完成后执行**。用敌对视角审视自己刚写的分析，找出漏洞。

输出：
1. 7 维度审视评估
2. 站得住的攻击点写回笔记，标记 **【反驳】**
3. 一句"最脆弱结论判定"

---

### Stage 6 · Engram Note（写笔记）

读 `references/literature_note_template.md`，生成：

1. **笔记结构**：10 部分（含 📎 关键引用），深挖块内联嵌入在对应部分内（不堆在末尾）
2. **概念深挖**：按 `references/concept_excavation.md` 的 9 层规格 + 递归规则 + 深度分级
3. **摘要来源**：从 Zotero item 的 `abstractNote` 字段直接读取，原样显示，不重新生成、不改写
4. **输出兼容**：笔记主体用纯 Markdown 书写（无原始 HTML），遵守 `references/literature_note_template.md` 的输出兼容层规则。深挖块用 `####` 四级标题 + 平铺格式，禁止 `>` 引用块包裹
5. **本地副本**：写入 `CAD/litreview/{AuthorYear_ShortTitle}.md`（若 CAD 目录存在），用 Markdown 保留同样的深挖层级
6. **结构门禁检查**：写入前跑 literature_note_template.md 的结构门禁 checklist（10 部分逐项核对），缺任何一节 → 报错 → 补全 → 再写入。通过后打印通过结果。

---

### Stage 7 · 写入三处(本地+Zotero+Notion) + 质量检查

**核心原则**：增量无损（incremental, lossless）。从不删除已有文献条目，只追加或更新当前论文。

**输出目标适配**：同一个 `.md` 源文件，按目标平台分别渲染。

按以下顺序写入，任一处失败不阻塞其余：

1. **本地 .md**：写入 `CAD/litreview/{AuthorYear_ShortTitle}.md`
2. **Zotero 子笔记**：关闭 Zotero → 用 `scripts/zotero_sync.py` 将纯 Markdown 转为 **Zotero 安全 HTML**（自定义转换器，非通用 markdown 库）→ 写 SQLite → 重启 Zotero → API 验证
   - 关键转换规则：`####`→`<h4>`，`**粗体**`→`<b>`，`*斜体*`→`<i>`，表格→`<table><tr><th>/<td>`，引用→`<blockquote>`，代码→`<code>`
   - 无原始 HTML 标签、无 `<div>` 包裹、无嵌套 blockquote
3. **Notion 同步**：
   - 读 `references/notion_sync.md` 规格 → 调用 `scripts/notion_sync.py`
   - 找/建日期 toggle（永不删除已有日期 toggle）
   - 查论文 toggle 是否已存在：若不存在 → 新建；若存在且生成模式为 update → 清空子块后重新追加（原地更新）；若存在且生成模式为 skip → 跳过
   - **从不影响同一日期 toggle 下的其他论文条目**
4. **末尾打印三处同步状态汇总**：`本地 ✅ / Zotero ✅ / Notion ✅`

**写入后自动验证**：
   - 确认已有文献条目未丢失（对比写入前后 Notion 日期 toggle 下论文计数）
   - 确认未修改非目标论文
   - Notion: 层级正确、表格渲染、引用块渲染、间距正确
   - Zotero: 无原始 HTML、无断裂 Markdown、无嵌套 blockquote、表格正确、标题层级正确

---

## Zotero SQLite 写入参考

```sql
-- itemTypes: 1=annotation, 2=attachment, 28=note（v1.1 修正：Zotero 7 中 note 为 28，非 14）

-- 更新已有标注的批注
UPDATE itemAnnotations SET comment = '…' WHERE itemID = {annotationItemID};

-- 创建新的标注条目（AI 补充标注）
INSERT INTO items (itemTypeID, key, dateAdded, dateModified)
VALUES (1, 'random_hex_key', datetime('now'), datetime('now'));
INSERT INTO itemAnnotations (itemID, parentItemID, type, annotatesItemID, comment, text)
VALUES ({newItemID}, {parentItemID}, 'highlight', {pdfItemID}, '🤖 [AI补充] …', 'highlighted text');

-- 创建笔记条目（Zotero 7: itemTypeID=28, 父关系存 itemNotes）
INSERT INTO items (itemTypeID, key, dateAdded, dateModified)
VALUES (28, 'random_hex_key', datetime('now'), datetime('now'));
INSERT INTO itemNotes (itemID, parentItemID, note)
VALUES ({newItemID}, {parentItemID}, '<h2>HTML内容</h2>');
```

> key 生成：`import secrets; secrets.token_hex(6)` 生成 12 位十六进制字符串。
> Zotero 7 注意：items 表无 parentItemID 列，父关系通过 itemNotes 或 itemAnnotations 表建立。

安全流程：
```bash
osascript -e 'quit app "Zotero"'
sqlite3 ~/Zotero/zotero.sqlite "UPDATE ..."
sqlite3 ~/Zotero/zotero.sqlite "INSERT INTO ..."
open -a Zotero
sleep 3
curl -s "http://127.0.0.1:23119/api/users/0/items/{itemKey}/children"
```

---

## Future Modules (v2+)

以下模块不纳入 v1 范围，仅作为设计方向预留：

| 模块 | 说明 |
|------|------|
| Associated Engrams | 跨论文关联记忆——当新论文的维度 3/4 与已有笔记存在概念重叠时自动提示 |
| Knowledge Graph | 从所有笔记中提取概念/方法/理论节点，构建个人知识图 |
| Claim Verification | 对论文中的关键引用做自动化交叉验证 |
| Research Idea Generator | 基于 Gap × Method × Dataset 的组合空间，生成可测试的研究想法 |
| PI Conversation | 模拟与领域 PI 对话，用研究版图帮你评估 paper 的战略价值 |

**设计原则**：Encode（v1）→ Consolidate（v2）→ Retrieve & Generate（v3）。

---

## 目录结构

```
litengram/
  SKILL.md                    ← 技能入口 + 完整 8 Stage 工作流
  references/                 ← 自包含指南（LitEngram 不依赖外部路径）
    literature_analysis_framework.md
    annotation_guidelines.md       ← v1.1 混合标注 + 概念溯源钩子
    concept_excavation.md          ← v1.1 新增：概念溯源引擎
    literature_note_template.md    ← v1.1.1 10部分+📎关键引用+结构门禁+Zotero摘要
    paper_priority.md
    reviewer_protocol.md
    research_profile_template.md
    zotero_workflow.md             ← 合并版
```
    notion_sync.md                 ← v1.2 Notion 同步规格
  scripts/
    notion_sync.py                 ← v1.2 Notion API 交互实现（增量同步，update-in-place）
    zotero_sync.py                 ← v1.2 Zotero 安全 HTML 生成器（自定义转换器）
