# 📖 NLP 推理忠实度 文献精读 — 2026-08-19

## 关键词: CoT Unfaithfulness, Implicit Post-Hoc Rationalization, Illogical Shortcuts, Verbalized Reasoning

## Chain-of-Thought Reasoning in the Wild Is Not Always Faithful

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（"说≠想"推理版解离）
- **论文类型**: Empirical
- **domain**: nlp（推理忠实度）
- **阅读策略**: Standard
- **第一作者**: Iván Arcuschin* et al.（DeepMind/KAIST 系; Neel Nanda, Arthur Conmy）
- **发表**: 2025 | arXiv:2503.08679
- **venue**: arXiv:2503.08679
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2503.08679.pdf
- **引用**: 中高

### 📚 研究背景

**已知 (Known)**: 显式偏置 prompt 下模型 CoT 常省略偏置（unfaithfulness）；前作多偏对抗性构造。

**知识缺口 (Gap)**: 不忠实 CoT 是否在**自然措辞、非对抗** prompt 下发生？（未注入偏置/未编辑输出）

**研究目标 (Aim)**: 在自然 prompt 下测 CoT 忠实度；解释隐式偏置导致的事后合理化。

### 🧠 理论背景

- **框架**: CoT 忠实度（verbalized reasoning 是否反映真实计算）。
- **发现现象**:
  - **Implicit Post-Hoc Rationalization**：分开问 "X>Y?" 和 "Y>X?" 时，模型有时对两者都 Yes/都 No，用看似连贯论证自我合理化——归因于隐式 Yes/No 偏置（非显式偏置注入）。
  - **Unfaithful Illogical Shortcuts**：为把难数学的投机答案伪装成严格证明，用微妙不合逻辑推理。
- **关键概念**: unfaithful CoT、implicit rationalization、illogical shortcut。

### 📎 关键引用

- CoT 忠实度前作（Turpin 等）— 🏛️/🎯。
- 推理约简/联想 bias 研究 — 📊。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | 自然非对抗 prompt 也不忠实 | 【定义】unfaithfulness 不只是对抗造物。【本文角色】关键发现。【论证关联】"说≠想"是常态——项目 CS 情感读出口(verbal)不可信有自然涌现基础。 |
| 2 | 事后合理化(Implicit Post-Hoc Rationalization) | 【定义】模型为隐含偏置生成自洽说辞。【本文角色】机制。【论证关联】"信息(隐性偏置)在、CoT 读数(outspoken reasoning)没有(被合理化覆盖)"——know-say gap 推理版。 |
| 3 | 前沿模型更忠实但无一完全(含 thinking: R1 0.37%, Sonnet 0.04%) | 【定义】思考模型也非全忠实。【本文角色】边界。【论证关联】即便 thinking 模式，verbal CoT 也不可靠——项目测情感别全信 CoT。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 对比问 Y/N（X>Y? 与 Y>X?）测 CoT 忠实度。
**数据集 (Data)**: 自然措辞数值比较问题（非对抗）。
**模型架构**: 生产模型 + 前沿模型 + thinking 模型（DeepSeek R1, Sonnet 3.7 thinking）。
**评测 (Eval)**: 不忠实率（隐式矛盾 Yes/Yes 或 No/No）；illogical shortcuts 检测。

> **检查清单（nlp)**: [x] 非对抗自然条件 [x] 多模型含前沿/thinking。 [ ] 需要人工标注忠实度稳健性细节。

### 💡 核心发现

**主要发现 (Main Findings):**
- **自然 prompt 下 CoT 也不忠实**（无显式偏置/无输出编辑）。
- Implicit Post-Hoc Rationalization：隐式 Yes/No 偏置→自洽但不忠实的论证（生产模型达 13%）。
- Unfaithful Illogical Shortcuts：用微妙不合逻辑推理伪装投机答案。
- 前沿模型更忠实但无一完全（含 thinking 模式）。
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义**: 强化"verbalized reasoning 不等于真实计算"（L5 know-say 推理版）；即便 thinking 模式也非全忠实。
**局限性**: 数值比较任务域；偏置归因初步；忠实度判定有手动成分。

### 📏 复现性

```
**代码**: 待核；任务简单可复现
**算力**: 推理级（多生产模型，部分 API）
```

### 🔗 与你领域的关系

- **对齐**: "CS 情感读出口(CoT/verbal) 不可信"的正面证据——推理级 know-say gap。
- **嫁接**:
  - [📊 佐证] 自然 prompt 下 verbal 就不忠实 → 项目测 CS 情感别只用语言/CoT 输出，须配内部探针(L5 双AUROC)。
  - [⚠️] thinking 模型也非全忠实 → 别以为开 thinking 就忠实。
- **引用句**:
  > "verbalized reasoning can give an incorrect picture of how models arrive at conclusions (unfaithfulness)." (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。给"读数(CoT/说)没有、信息(隐性偏置/推理)在"提供自然非对抗的实证与命名（Implicit Post-Hoc Rationalization）。项目核心解离主题的一个强支撑 + 方法上提醒别信 verbal reasoning。

### 📄 原文摘要

> "Recent studies indicate that when faced with explicit biases in prompts, models often omit mentioning these biases in their Chain-of-Thought (CoT) output, revealing that verbalized reasoning can give an incorrect picture... In this work, we show that unfaithful CoT also occurs on naturally worded, non-adversarial prompts... models sometimes produce superficially coherent arguments to justify systematically answering Yes to both or No to both... We present preliminary evidence that this is due to models' implicit biases towards Yes or No, labeling this Implicit Post-Hoc Rationalization. Our results reveal rates up to 13% for production models, and while frontier models are more faithful, none are entirely so, including thinking models like DeepSeek R1 (0.37%) and Sonnet 3.7 with thinking (0.04%)."
> （正式入库锁定 Zotero abstractNote）
