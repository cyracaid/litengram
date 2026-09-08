# 📖 NLP 可解释性·诚实性 文献精读 — 2026-08-19

## 关键词: Internal State, Truthfulness Classifier, Hidden Layers, Probing, 奠基

## The Internal State of an LLM Knows When It's Lying

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（解离领域奠基论文之一）
- **论文类型**: Empirical
- **domain**: nlp（cs. 可解释性·诚实性探针）
- **阅读策略**: Standard
- **第一作者**: Amos Azaria (Ariel University) | Tom Mitchell (CMU)
- **发表**: 2023 | EMNLP Findings 2023 | arXiv:2304.13734
- **venue**: EMNLP 2023 Findings
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2304.13734.pdf
- **引用**: 高（诚实性探针奠基）

### 📚 研究背景

**已知 (Known)**: LLM 常自信地生成假信息；概率(confidence)不可靠反映真实性。

**知识缺口 (Gap)**: 内部状态（隐藏层激活）是否承载真伪信号？（此前未系统验证）

**研究目标 (Aim)**: 训练分类器从隐藏层激活预测语句真实性（读或生成时），检验"内部状态知道在说谎"。

### 🧠 理论背景

- **框架**: 探针（classifier）从隐藏激活预测真伪——"信息隐蔽在内部状态中"。
- **方法**: 训练二分类器（输入某层 hidden activations），对给定句子（真/假各半）输出真实概率。
- **关键概念**: internal-state probing、truthfulness classifier、hidden-layer signal。

### 📎 关键引用

- 激活探针技术 — 🔧方法来源。
- 概率(confidence)可靠性 — 🎯批判靶子。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | 分类器 71-83% 从隐藏激活判真伪 | 【定义】内部状态承载真伪信号。【本文角色】核心结论。【论证关联】**"信息在那里(隐藏态探针可读出)"奠基**——项目解离先例的源头之一。 |
| 2 | 探针比概率更可靠 | 【定义】confidence 不可靠。【本文角色】对比。【论证关联】呼应 L5 know-say gap / L11: 读出口(概率)不可靠、内部(探针)可靠。 |
| 3 | 读或生成时均适用 | 【定义】内外通用。【本文角色】广度。【论证关联】探针既可用于输入陈述也可用于模型自产。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 判断语句真/假（半真半假测试集）。
**数据集 (Data)**: 测试句（真假各半）。
**模型架构**: 多 LLM 基座（分类器依赖具体基座）。
**训练细节**: 训练 hidden-activation 二分类器（探针）。
**评测 (Eval)**: 真假分类准确率（71-83%）。

> **检查清单（nlp)**: [x] 多基座。 [ ] 需核层选择/过拟合细微。

### 💡 核心发现

**主要发现 (Main Findings):**
- 隐藏层激活分类器以 71-83% 判真伪（跨基座）。
- 内部状态信号比输出概率更可靠指示真实性。
- 读入陈述与模型自产陈述都适用。
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义**: "内部状态知道在说谎"——首创诚实性激活探针，为后续解离/诚实性工作奠基。
**局限性**: 分类器基座依赖；训练集可能泄漏（Burns 等后批判泛化）；半真半假简化设定。

### 📏 复现性

```
**代码**: 方法简单可复现
**算力**: 推理 + 分类器训练（轻）
**数据**: 半真半假句子集
```

### 🔗 与你领域的关系

- **对齐**: 诚实性/真伪内部信号探针的**奠基**——"信息在那里"的第一批证据之一。
- **嫁接**:
  - [📊 先例] 内部状态承载真伪信号 → 项目"信息在那里"的解离先例源头。
  - [⚠️ 局限] 探针泛化问题（Burns/L4 批判）→ 项目要用 AUROCfail(L5)或因果干预(L9)补强，别只靠探针 AUROCdetect。
- **引用句**:
  > "the LLM's internal state can be used to reveal the truthfulness of statements." (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。解离/诚实性探针的奠基论文，为"信息隐藏于内部状态"的整个研究线开山。虽强于它为后续更严谨解离（L4/L5）铺垫，项目引作内部信号先例源头即可；做具体测度时用 L5 双 AUROC 更严谨。

### 📄 原文摘要

> "While Large Language Models (LLMs) have shown exceptional performance in various tasks, one of their most prominent drawbacks is generating inaccurate or false information with a confident tone. In this paper, we provide evidence that the LLM's internal state can be used to reveal the truthfulness of statements. This includes both statements provided to the LLM, and statements that the LLM itself generates. Our approach is to train a classifier that outputs the probability that a statement is truthful, based on the hidden layer activations of the LLM as it reads or generates the statement. Experiments demonstrate that given a set of test sentences, of which half are true and half false, our trained classifier achieves an average of 71% to 83% accuracy."
> （正式入库锁定 Zotero abstractNote）
