# 📖 NLP 数字人文 文献精读 — 2026-08-19

## 关键词: Oral History, LLM Annotation, Sentiment Analysis, Prompt Engineering, RAG, Densho

## Large Language Models for Oral History Understanding with Text Classification and Sentiment Analysis

### 📋 基本信息

- **重要等级**: 📌 补充参考（碰撞检查用）
- **论文类型**: Empirical（LLM 标注基准 + 数据集建设）
- **domain**: nlp（数字人文·LLM 标注）
- **阅读策略**: Fast
- **第一作者**: Komala Subramanyam Cherukuri | University of North Texas
- **合作**: Pranav Abishai Moses, Aisa Sakata, Jiangping Chen (UIUC), Haihua Chen* (UNT)
- **发表**: 2025 | arXiv:2508.06729
- **venue**: arXiv:2508.06729（ACM JOCCH 投稿风格）
- **DOI**: 无 | **arXiv**: 2508.06729
- **代码**: 官方仓库（code + annotated data + prompts 全公开）
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2508.06729.pdf
- **引用**: 待核

### 📚 研究背景

**已知 (Known)**: 口述史档案非结构化+情感复杂+人工标注昂贵，规模分析受限；LLM 已用于历史文本分类/情感。

**知识缺口 (Gap)**: 缺乏可规模化的口述史自动语义+情感标注框架；低资源、文化敏感领域的 LLM 标注缺实证。

**研究目标 (Aim)**: 构建可扩展框架，用 LLM 自动标注日裔美国人拘留口述史(JAIOH)，产出高质量数据集 + 多模型对比 + prompt 策略研究。

### 🧠 理论背景

- **框架**：LLM 文本分类 + 情感标注（语义：多类主题；情感：Positive/Neutral/Negative 三分类）
- **方法**：558 句人工标注(15 位叙述者) → zero-shot / few-shot / RAG 三种 prompt 策略 → ChatGPT/Llama/Qwen 对比 → 选最优配置标全库 92,191 句(1,002 访谈, Densho 档案)
- **关键概念**：RAG 检索增强标注；数据来源 = **Densho Digital Repository**（日裔拘留档案库）

### 📎 关键引用

- Densho Digital Repository — 📊数据支撑 — JAIOH 语料来源。
- RAG/Llama/Qwen/ChatGPT 标注研究 — 🔧方法来源 — prompt 工程对照。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | F-1: 语义 ChatGPT 88.71% / Llama 84.99% / Qwen 83.72%；情感三模型相近 82-83% | 语义>情感精度；情感标注所有模型指着接近——**情感是更难/更模糊的自动标注任务**——支撑本项目"情感读出口更难"的直觉。 |
| 2 | Densho 档案 + 558 句人工标注 | **可直接复用**：本项目若要 CS 离散叙事情感语料，Densho 或类似少数族裔口述史档案是可借鉴的公开语料源。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 口述史记**语义分类 + 情感三分类**（自动标注）。
**数据集 (Data)**: Densho 日裔拘留档案；558 句人工标注(15 叙述者)；全库 92,191 句/1,002 访谈。
**模型**: ChatGPT / Llama / Qwen。
**评测 (Eval)**: F-1；zero-shot / few-shot / RAG 三策略。

> **检查清单（nlp）**: [x]多模型对比 [x]多策略 [x]数据全公开 [x]基准明确。 [ ] 人类一致性(kappa)未报告（弱项）。

### 💡 核心发现

**主要发现 (Main Findings):**
- **语义分类**：ChatGPT F-1 最高 88.71%（>Llama 84.99% > Qwen 83.72%）
- **情感分类**：Llama 82.87% / Qwen 82.66% / ChatGPT 82.29%（相近）
- **产出**：92K 句标注语料 + prompt 标注基准（低资源文化敏感域）
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义 / 局限**: 证明 LLM 在精心设计 prompt 下可规模化标注文化敏感档案；局限=自动标注有误标风险、情感分类精度瓶颈明显。

### 📏 复现性

```
**代码/数据**: 全公开（code + annotated + prompt templates）
**算力**: 标注推理级，ChatGPT 需 API、Llama/Qwen 可本地
**复现**: 558 句基准可复现；92K 全库标注需 Densho 语料
```

### 🔗 与你领域的关系

**碰撞检查结论：不撞题。**
- **话题域共享**：口述史 × 情感 × 少数族裔离散叙事——本项目 CS 离散叙事的潜在语料场景。
- **方法域不同（核心）**：本篇=LLM **自动标注/分类管线**（数据集建设），无表征分析、无 activation patching、无机理、无"信息在表征里 vs 读出口"解离。它们也**不碰代码切换(CS)**。
- **问题域不同**：目标=可扩展标注语料；本项目目标=CS 情感在 LM 表征里的编码/表达解离机理。**不构成竞争，反而是可借鉴的语料/标注前端**。

**可嫁接**:
- [📊 语料源] Densho / 少数族裔口述史档案——CS 离散叙事情感的天然语料候选（本项目有用）。
- [🔧 方法] RAG 增强标注 + 人工基准校准——若本项目需要给 CS 情感语料做标注前端，这套 pipeline 可借鉴。
- [📊 佐证] 情感自动标注精度低于语义（~82% vs ~88%）——**给"情感是更难读出的信息"直觉提供实证**，呼应本项目"读数没有"。

### ⭐ 为什么这篇重要

非方法基座，但**完成竞争风险检查**：确认本项目(表征-读出解离 × CS × 情感)与现有 LLM 口述历史标注工作**不撞题**，且对方提供了可复用的公开语料源与标注管线。列为 📌 参考即可，不占用核心方法设计。

### 📄 原文摘要

> "This paper aims to develop a scalable framework to automate semantic and sentiment annotation for oral history archives, with a particular focus on Japanese American Incarceration Oral History (JAIOH). Using LLMs, this study seeks to construct a high-quality dataset... We labeled 558 sentences... evaluated across zero shot, few shot, and RAG... ChatGPT achieved the highest F-1 score (88.71%) for semantic classification... automatically annotate 92,191 sentences from 1,002 interviews... This paper introduces a large scale annotated oral history corpus and offers a comparative benchmark for prompt based LLM annotation in low resource, culturally sensitive domains."
> （正式入库锁定 Zotero abstractNote）
