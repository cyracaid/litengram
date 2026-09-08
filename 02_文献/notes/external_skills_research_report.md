# 外部技能库调研报告 — LitForge 优化参考

> 生成日期: 2026-07-20
> 目的: 系统比较 8 个外部仓库的技能体系，识别可纳入 LitForge 的可迁移能力

---

## 目录

1. [仓库总览](#1-仓库总览)
2. [deep-reading-analyst](#2-deep-reading-analyst)
3. [hermes-research-skills](#3-hermes-research-skills)
4. [tashan-research-skills](#4-tashan-research-skills)
5. [agent-auto-sci-skills](#5-agent-auto-sci-skills)
6. [literature-review-skills (5ak3t)](#6-literature-review-skills-5ak3t)
7. [research-paper-lifecycle-skills](#7-research-paper-lifecycle-skills)
8. [awesome-academic-research-skills & research-skills-summary-bilingual](#8-awesome-academic-research-skills--research-skills-summary-bilingual)
9. [交叉分析矩阵](#9-交叉分析矩阵)
10. [优先级改进建议](#10-优先级改进建议)

---

## 1. 仓库总览

| 仓库 | 类型 | 技能/文件数 | 核心范式 | 对 LitForge 适用性 |
|------|------|------------|---------|-------------------|
| deep-reading-analyst | 单技能 | 1 SKILL.md + 8 个 reference | 10+ 思维模型 (SCQA/5W2H/First Principles/Systems) | **高** |
| hermes-research-skills | 多技能 | 20 个技能 | 中文原生深度阅读 pipeline (reader→critic→synthesizer) | **极高** |
| tashan-research-skills | 多技能 | 20 个技能 | 实验设计 (Fisher) + 认知基线 + 学术写作 | **高** |
| agent-auto-sci-skills | 多技能 | ~45 个技能 | 学科化方法论，分 4 条主线 | **高** |
| literature-review-skills (5ak3t) | 多 skill prompt | 8 个 prompt | PRISMA 系统综述 | **中** |
| research-paper-lifecycle-skills | 多技能 | 41 个技能 | 写作/发表生命周期 | **低** |
| awesome-academic-research-skills | awesome list | 无 SKILL.md | 索引列表 | **无** |
| research-skills-summary-bilingual | awesome list | 无 SKILL.md | 摘要列表 | **无** |

---

## 2. deep-reading-analyst

**路径**: `/tmp/deep-reading-analyst-skill/src/deep-reading-analyst/SKILL.md`

### 核心结构

分层分析框架，按时间投入分 4 级：

```
Level 1 (15min): SCQA + 5W2H
Level 2 (30min): + Critical Thinking + Inversion
Level 3 (60min): + Mental Models + First Principles + Systems + Six Hats
Level 4 (120min+): + Cross-source comparison via web search
```

### 关键可迁移能力

#### 2.1 SCQA 结构化入口

将论文的"对话语境"标准化为 4 要素：

| 要素 | 含义 | 在论文中的映射 |
|------|------|--------------|
| **S**ituation | 领域共识背景 | Introduction 第一段 |
| **C**omplication | 困境/矛盾/缺口 | Introduction 的 gap 陈述 |
| **Q**uestion | 核心研究问题 | Research aim / hypothesis |
| **A**nswer | 核心发现 | Discussion 首段 |

**对 LitForge 的价值**: Background 维度目前是自由文本分析，SCQA 可作为前置结构，标准化论文的对话语境后再进入 5 维度解剖。

#### 2.2 First Principles 剥离

剥离所有假设后，验证核心发现是否仍成立。流程：

1. 识别论文的核心假设
2. 逐条验证：这个假设是真的吗？还是领域习惯？
3. 剥离后重建：如果不依赖这个假设，结论还成立吗？

**对 LitForge 的价值**: Importance 维度目前依赖论文自述的贡献，缺少从基本原理出发的再验证。

#### 2.3 Inversion (反向) 思维

"预 mortem 分析"：如果这篇论文是错的，它最可能因为什么原因失败？

- 数据造假？统计误用？实验设计漏洞？样本偏差？概念混淆？

**对 LitForge 的价值**: 可纳入 Methods 维度层 3（反向验证）的结构化指南。

#### 2.4 Content-Type → Framework 映射

```
策略/商业 → SCQA + Mental Models + Inversion
研究论文 → 5W2H + Critical Thinking + Systems Thinking
How-to → SCQA + 5W2H + First Principles
Opinion → Critical Thinking + Inversion + Six Hats
```

**对 LitForge 的价值**: LitForge 目前对所有论文使用同一模板，可以按 paper type (empirical / review / theoretical / meta-analysis) 做框架调整。

### 与 LitForge 的差异

| 维度 | deep-reading-analyst | LitForge |
|------|--------------------|----------|
| 输出目标 | 理解→行动（通用） | 复刻·批判·嫁接·反驳（科研专用） |
| 粒度 | 结构化思考（框架驱动） | 论文解剖（维度驱动） |
| 验证 | 无外部知识库 | Zotero 全流程 |
| 领域特化 | 无 | CAD + 心理学/认知神经科学 |

---

## 3. hermes-research-skills

**路径**: `/tmp/hermes-research-skills/skills/`

### 结构

20 个中文研究技能，覆盖论文阅读→批判→综述→整合→写作的完整 pipeline：

```
paper-explorer → paper-reader → paper-critic
                                       ↓
                               literature-scout
                                       ↓
                            research-synthesizer
                                       ↓
                     critical-iteration-lab + concept-boundary-analyzer
```

### 关键可迁移能力

#### 3.1 paper-critic-zh — 结构化批判

对论文的批判不是自由发挥，而是按 5 个维度逐项评估：

1. **逻辑一致性**: 假设→方法→结论是否自洽
2. **证据充分性**: 每个 claim 的证据是否充分
3. **替代解释**: 是否有未排除的替代解释
4. **方法局限**: 设计是否适合回答研究问题
5. **外部效度**: 结果能否推广

每个维度输出评分 + 理由 + 建议。

**对 LitForge 的价值**: LitForge 的维度 3（核心发现）已有"你信不信"的问题，但缺少结构化评估维度。可以引入这 5 维评估作为 Findings 维度中的批判子模块。

#### 3.2 critical-iteration-lab-zh — 多轮批判迭代

不是一遍过，而是 3 轮迭代：

```
Round 1: 默认阅读 → 输出初步分析
Round 2: 从对立立场审视同一分析 → "如果我不同意我的结论，我会怎么反驳"
Round 3: 综合 → 修正后的最终分析
```

**对 LitForge 的价值**: LitForge 目前是单遍分析。多轮迭代可以显著提升分析深度，尤其是在"反驳"维度上。

#### 3.3 literature-scout-zh — Gap 矩阵三分法

不是所有 gap 都一样。分为三类：

| 类型 | 英文 | 含义 |
|------|------|------|
| 已知已知 | Known Knowns | 领域共识，但本文未涉及 |
| 已知未知 | Known Unknowns | 领域公认的未解问题 |
| 未知未知 | Unknown Unknowns | 本文揭示的新问题方向 |

**对 LitForge 的价值**: 可替换 Grafting 维度中单一的 gap 列表。

#### 3.4 research-synthesizer-zh — 跨论文证据整合

3 层整合：

```
Level 1: 并行罗列（A says X, B says Y）
Level 2: 对比分类（一致/互补/冲突/无关）
Level 3: 机制综合（提出整合框架解释多篇结果）
```

**对 LitForge 的价值**: 适合未来的 LitForge Synthesis 模块。

#### 3.5 concept-boundary-analyzer-zh — 概念边界分析

追踪一个概念在不同论文中的定义变化：

1. 概念 A 在论文 1 中的操作定义
2. 概念 A 在论文 2 中的操作定义
3. 两组定义是否测量同一构念？（收敛/发散？）

**对 LitForge 的价值**: 适合跨论文分析，以及"概念漂移"检测。

### 与 LitForge 的差异

| 维度 | hermes-research-skills | LitForge |
|------|----------------------|----------|
| 语言 | 纯中文 | 中文+英文混写 |
| 输出 | 独立分析输出 | 整合到 Zotero 工作流 |
| pipeline | 端到端（探索→阅读→批判→合成） | 单篇精读为主 |
| 多轮迭代 | 核心特征 | 缺失 |
| 概念追踪 | 内置 | 仅单篇定义 |

---

## 4. tashan-research-skills

**路径**: `/tmp/tashan-research-skills/skills/`

### 结构

20 个技能，偏重实验设计 + 认知科学 + 学术写作。

### 关键可迁移能力

#### 4.1 experiment-design — Fisher 三原则 + 功效分析

Fisher 实验设计的三大原则：

1. **随机化**: 避免系统偏差
2. **重复**: 评估变异
3. **区组**: 控制已知变异来源

附加的统计 rigor：
- 先验功效分析 (power analysis)
- 效应量报告 (Cohen's d, η², 等)
- 多重比较校正 (Bonferroni, FDR, 等)
- 预注册 (pre-registration)

**对 LitForge 的价值**: Methods 维度的层 2 (WHY 分析) 目前比较泛化，可以加入这些具体检查点。

#### 4.2 research-baseline-builder — 研究基线

在阅读新论文前，先建立个人"基线"：
- 我对这个领域的已有知识
- 我的预设/偏见
- 我期望这篇论文告诉我什么

阅读后对比基线变化。

**对 LitForge 的价值**: 可纳入 Step 0 前置确认，培养元认知阅读习惯。

#### 4.3 cognitive-profile — 认知画像

记录自己的认知盲点：
- 我容易忽略什么类型的问题？
- 我倾向于同意什么类型的论证？
- 我过去读错过哪些论文？为什么？

**对 LitForge 的价值**: 长期使用的个人成长工具，适合 LitForge 的元认知扩展。

#### 4.4 research-dream — 长期研究记忆

通过定期回顾笔记，将碎片化的论文阅读整合为长期研究记忆。核心是"重复间隔检索"机制。

**对 LitForge 的价值**: 解决"读完就忘"的问题。LitForge 当前没有内置回顾机制。

### 与 LitForge 的差异

| 维度 | tashan-research-skills | LitForge |
|------|----------------------|----------|
| 核心关注 | 实验设计 rigor | 整体论文解剖 |
| 元认知 | 内置 | 缺失 |
| 回顾机制 | research-dream | 缺失 |
| 统计检查 | 详细 checklist | 仅有原则性要求 |

---

## 5. agent-auto-sci-skills

**路径**: `/tmp/agent-auto-sci-skills/skills/`

### 结构

~45 个技能，分 4 个子目录：

```
kdense-scicomm-selected/     → 科学传播与写作
kdense-data-viz-selected/    → 数据可视化
urban-exposure-review/       → 暴露科学综述方法论
scipilot-writing-skill/      → 学术写作工具链
```

### 关键可迁移能力

#### 5.1 claim-evidence-mapping

对每个 claim 显式标注 evidence level：

| 级别 | 英文 | 含义 |
|------|------|------|
| 直接 | Direct | 本文数据直接支持 |
| 间接 | Indirect | 引用于其他研究/推论 |
| 无支持 | Unsupported | 作者主张但无直接证据 |

以及 evidence source：
| 来源 | 含义 |
|------|------|
| Empirical | 第一手实验数据 |
| Simulation | 模拟/计算 |
| Theoretical | 理论推导 |
| Review | 引用综述 |

**对 LitForge 的价值**: Findings 维度目前要求检查统计合理性，但 claim-evidence 映射不够显式。

#### 5.2 formal-vs-frontier 来源分离

| 类别 | 含义 | 标记 |
|------|------|------|
| Formal | 领域共识，教科书级 | 📘 |
| Frontier | 仍有争议，前沿探索 | 🔬 |

**对 LitForge 的价值**: LitForge 的笔记不区分共识与争议，可能导致读者高估/低估某结论的可靠性。

#### 5.3 citation validation

对论文中的关键引用做交叉验证：
- 引用是否准确反映被引文献的结论？
- 是否 cherry-pick？
- 是否引用综述而非原始文献？

**对 LitForge 的价值**: 可纳入 Grafting 维度，避免引用失真。

#### 5.4 statistical integrity checklist

```
[ ] 效果量报告 (effect size)
[ ] 置信区间
[ ] 多重比较校正
[ ] 先验功效分析
[ ] 预注册
[ ] 原始数据可用性
[ ] 分析方法预先指定 vs. 事后分析
```

**对 LitForge 的价值**: Methods 维度的统计检查可以升级为完整的 checklist。

#### 5.5 Mermaid 图表标准化

要求每个分析输出中包含至少一个 Mermaid 图表：
- 概念关系图
- 流程图
- 思维导图

**对 LitForge 的价值**: LitForge Note 模板目前纯文本，加入图表可显著提升可理解性。

#### 5.6 two-stage writing (scipilot)

学术写作分两阶段：
```
Stage 1: 内容生成（不关心格式/语法/引用格式）
Stage 2: 精炼（格式/语法/引用格式化）
```

**对 LitForge 的价值**: 适合 LitForge Write 模块的写作策略。

### 与 LitForge 的差异

| 维度 | agent-auto-sci-skills | LitForge |
|------|---------------------|----------|
| 学科 | 暴露科学 | 心理学/认知神经科学 |
| 输出 | 综述 + 图表 | 笔记 + 标注 |
| 引用验证 | 内置 | 缺失 |
| 图表 | 强制要求 | 纯文本 |
| 统计检查 | 详细 checklist | 原则性要求 |

---

## 6. literature-review-skills (5ak3t)

**路径**: `/tmp/5ak3t-lr-skills/ (cloned from Supervisor-Skills)`

### 结构

8 个 PRISMA 导向的系统综述 prompt，非 SKILL.md 格式。

### 关键可迁移能力

#### 6.1 RoB (Risk of Bias) 评估框架

不是简单的"好/不好"，而是分维度评估：

```
Selection bias:   低/中/高/不清楚
Performance bias: 低/中/高/不清楚
Detection bias:   低/中/高/不清楚
Attrition bias:   低/中/高/不清楚
Reporting bias:   低/中/高/不清楚
```

**对 LitForge 的价值**: Methods 维度目前评估偏倚风险仅靠个人判断，没有结构化框架。

#### 6.2 PRISMA 流程图

从检索→筛选→纳入→分析的标准化流程。

**对 LitForge 的价值**: 适合 LitForge Review 模块，单篇精读无需。

#### 6.3 PICO 结构化

```
P (Population):  被试群体
I (Intervention): 干预/暴露
C (Comparison):  对照组
O (Outcome):     结果变量
```

### 与 LitForge 的差异

| 维度 | literature-review-skills | LitForge |
|------|------------------------|----------|
| 层级 | 系统综述 | 单篇精读 |
| 格式 | prompt 文本 | SKILL.md + 拆分 guide |
| 深度 | PRISMA 合规 | 维度分析 |
| 自动化 | 无 | Zotero 全流程 |

---

## 7. research-paper-lifecycle-skills

**路径**: `/tmp/research-paper-lifecycle-skills/skills/`

### 范围

41 个技能，主要覆盖论文写作与发表的完整生命周期，包括：
- 论文结构写作
- 回复审稿人
- cover letter
- 图表制作
- 学术简历

### 对 LitForge 的适用性

**低**。该仓库聚焦于"写论文"而非"读论文"，与 LitForge 的核心目标（文献精读）交集有限。少数可参考：
- 引用格式管理的技巧
- 论文结构分析（可用于逆向工程论文组织）

---

## 8. awesome-academic-research-skills & research-skills-summary-bilingual

### 说明

这两个是 **awesome-list / 索引仓库**，不包含实际的 SKILL.md 文件：
- `awesome-academic-research-skills`: 学术 AI 技能生态目录
- `research-skills-summary-bilingual`: 中英双语技能摘要

### 对 LitForge 的价值

**无直接价值**。不过作为索引，它们指向的某些上游仓库可能有用（如文献管理、写作辅助等），但不在本次调研范围内。

---

## 9. 交叉分析矩阵

### 能力覆盖度

| 能力 | deep-reading | hermes | tashan | agent-auto-sci | 5ak3t | lifecycle |
|------|:-----------:|:------:|:------:|:-------------:|:-----:|:---------:|
| 结构化入口 (SCQA) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 多轮批判迭代 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Gap 矩阵三分法 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Claim-Evidence Mapping | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Formal/Frontier 分离 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 统计完整性 checklist | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| RoB 框架 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| 第一性原理剥离 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 反向/预 mortem | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 概念边界追踪 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 跨论文证据整合 | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| Mermaid 图表 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 引用验证 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 元认知/基线 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| 长期回顾机制 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |

### LitForge 当前覆盖度

LitForge 已具备的：
- ✅ 结构化入口（5 维度替代 SCQA，但 SCQA 可作为补充）
- ✅ 批判（维度 3 + 质量检查清单）
- ✅ Gap 识别（维度 1 的缺口 + 维度 4 战略嫁接）
- ✅ 统计合理性（维度 3 + 维度 2 层 2 WHY 分析）
- ✅ 方法学深度（维度 2 三层拆解）

LitForge 缺失的：
- ❌ 多轮批判迭代（单遍分析）
- ❌ Gap 矩阵三分法（单一 gap 类别）
- ❌ Claim-Evidence 显式映射
- ❌ Formal/Frontier 标记
- ❌ 全面的统计完整性 checklist
- ❌ RoB 结构化框架
- ❌ 第一性原理剥离
- ❌ Mermaid 图表
- ❌ 引用验证
- ❌ 元认知基线
- ❌ 长期回顾机制

---

## 10. 优先级改进建议

### 🔴 高优先级（直接影响分析深度）

| # | 改进 | 来源 | 位置 | 预估工作量 |
|---|------|------|------|-----------|
| 1 | **SCQA 结构化入口** | deep-reading | literature_analysis_framework.md | ~1h |
| 2 | **Claim-Evidence Mapping Gate** | agent-auto-sci | literature_analysis_framework.md + note_template.md | ~1h |
| 3 | **Gap 矩阵三分法** | hermes | literature_analysis_framework.md + note_template.md | ~30min |
| 4 | **Formal/Frontier 标记** | agent-auto-sci | note_template.md | ~30min |
| 5 | **统计完整性 checklist** | tashan + agent-auto-sci + 5ak3t | literature_analysis_framework.md | ~45min |

### 🟡 中优先级（深度优化）

| # | 改进 | 来源 | 位置 | 预估工作量 |
|---|------|------|------|-----------|
| 6 | **论文类型 → 框架映射** | deep-reading | literature_analysis_framework.md | ~30min |
| 7 | **RoB 结构化框架** | 5ak3t | literature_analysis_framework.md 的 Methods 维度 | ~1h |
| 8 | **多轮批判迭代协议** | hermes | note_template.md 末尾 | ~1h |
| 9 | **第一性原理剥离** | deep-reading | literature_analysis_framework.md 的 Importance 维度 | ~30min |
| 10 | **Mermaid 图表标准化** | agent-auto-sci | note_template.md | ~30min |

### 🟢 低优先级（未来扩展）

| # | 改进 | 来源 | 位置 | 说明 |
|---|------|------|------|------|
| 11 | 引用验证 | agent-auto-sci | 新文件 / 可选步骤 | 适合 LitForge Review |
| 12 | 元认知基线 | tashan | paper_priority.md 扩展 | 适合 LitForge Design |
| 13 | 长期回顾机制 | tashan | 新文件 | 适合 LitForge Synthesis |
| 14 | 概念边界追踪 | hermes | 新文件 | 跨论文分析，适合 LitForge Compare |
| 15 | 反向/预 mortem | deep-reading | literature_analysis_framework.md 的 Methods 维度层 3 | 已部分覆盖 |

---

## 附录：LitForge 现有文件结构

```
~/.agents/skills/litforge/
  SKILL.md                 ← 技能入口（协调整体工作流）

~/Documents/CAD/
  prompt_guides/
    literature_analysis_framework.md   ← 5 维度分析范式（三遍读法）
    annotation_guidelines.md           ← 4 层标注结构
    literature_note_template.md        ← 8 部分笔记模板
    paper_priority.md                  ← 重要等级 + 用途标签
    zotero_workflow.md                 ← Zotero 写入速查
  _zotero_workflow.md                  ← Zotero 完整技术工作流（权威版本）
  litreview/
    Ponzo2021_CARED.md                 ← 示例笔记
    archive/                            ← 归档
  external_skills_research_report.md   ← 本文件
```
