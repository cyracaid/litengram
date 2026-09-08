# 📖 NLP 代码切换·LLM 文献精读 — 2026-08-19

## 关键词: Code-Switching, LLM Comprehension, CSW Benchmarks, Qwen, Fine-tuning, CS 理解下降

## Lost in the Mix: Evaluating LLM Understanding of Code-Switched Text

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（CS 主题域最直接相关——LLM CS 理解下降）
- **论文类型**: Empirical（评测 + 基准）
- **domain**: nlp（代码切换 CS）
- **阅读策略**: Standard
- **第一作者**: Amr Mohamed | MBZUAI（Guokan Shang）
- **发表**: 2025 | arXiv:2506.14012v1 [cs.CL] 16 Jun 2025
- **venue**: arXiv:2506.14012
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2506.14012.pdf
- **引用**: 中（CS-LLM 评测）

### 📚 研究背景

**已知 (Known)**: 代码切换(CSW)在日常/线上普遍；LLM 常接触 CSW 输入；CSW 受语言理论约束（Sankoff/Poplack）。

**知识缺口 (Gap)**: LLM 对 CSW 文本理解如何系统评测？现基准是否覆盖 CSW 复杂性？

**研究目标 (Aim)**: 生成 CSW 变体（基于语言理论的约束）评测 LLM 阅读理解/推理；测 prompting/fine-tune 补救。

### 🧠 理论背景

- **框架**: 语言理论约束的合成 CSW 生成（noun-token 交换等）；阅读/推理基准扩到 CSW。
- **关键概念**: CSW variants、noun-token methodology、cross-lingual reading。

### 📎 关键引用

- CSW 语言理论（Sankoff/Poplack）— 🏛️。
- CSW 评测/生成 — 🎯/📊。
- Qwen 等模型 — 📊。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | LLM CS 理解被显著破坏（Qwen 家族尤其）| 【定义】CSW 使 LLM 性能大跌。【本文角色】核心发现。【论证关联】**项目核心前提**：LLM 处理 CS 文本能力下降/信息读出口受限——"CS × 情感读出口"的综述级佐证。 |
| 2 | prompting mixed 结果, fine-tuning 提升 | 【定义】补救有限。【本文角色】发现。【论证关联】LLM 读 CS 情感需特殊适配，不能裸用。 |
| 3 | 基于语言理论约束生成 CSW | 【定义】评测科学性。【本文角色】方法。【论证关联】项目 CS 语料建设可参考其基于理论的合成法。 |

### 🔬 研究方法

> domain=nlp → nlp 版

**任务定义 (Task)**: LLM CSW 阅读理解/推理评测。
**数据集 (Data)**: 既有基准生成 CSW 变体（语言理论约束）。
**模型**: 多 LLM（Qwen 家族等）。
**方法**: noun-token CSW；prompting vs fine-tuning。
**评测 (Eval)**: 阅读/推理准确率（CSW vs 单语对照）。

> **检查清单（nlp)**: [x] 语言理论约束 [x] 多模型 [x] 补救对照。

### 💡 核心发现

**主要发现 (Main Findings):**
- LLM 对 CSW 理解**显著下降**（嵌入语言干扰，Qwen 最甚）。
- Prompting mixed 结果；fine-tuning 提升理解。
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义**: CSW 是 LLM 理解清单短板——支持"LLM 读 CS 内容能力受限"（项目前提）。
**局限性**: 合成 CSW（可能未覆盖自然 CSW 全貌）；结构化英语基准适配。

### 📏 复现性

```
**代码/基准**: 可复现
**算力**: 推理级
```

### 🔗 与你领域的关系

- **对齐**: **主题域直接相关**——项目核心就是"CS × 情感"，此文证 LLM 处理 CS 的理解短板。
- **嫁接**:
  - [📊 佐证] LLM CS 理解下降 → 项目"CS 情感读出口受限"提供综述级支撑。
  - [🔧 方法] 语言理论约束 CSW 生成 → 项目 CS 语料建设参考。
  - [⚠️] LLM 需 fine-tune 才能读 CS → 项目读出口工具要适配。
- **引用句**:
  > "LLM's [CSW] understanding is significantly disrupted by the introduction of code-switching." (paper)

### ⭐ 为什么这篇重要

⚔️ 级。项目**主题域直接锚点**：证 LLM 对代码切换文本理解显著下降，为"CS × 情感"项目的现象前提提供实证。CS 语境点睛文献。

### 📄 摘要（一文）

LLM 对代码切换正文理解显著下降（Qwen 家族最甚）；基于语言理论约束生成 CSW 变体评测；prompting 有限、fine-tuning 可提升理解。
（正式入库锁定 Zotero abstractNote）
