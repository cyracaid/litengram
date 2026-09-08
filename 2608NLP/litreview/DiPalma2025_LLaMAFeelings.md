# 📖 NLP 情感·探针 文献精读 — 2026-08-19

## 关键词: Sentiment Probing, Layer-wise, Pooling, LLaMA, Mid-layer Sentiment

## LLaMAs Have Feelings Too: Unveiling Sentiment and Emotion Representations in LLaMA Models Through Probing

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（情感读出口层位探针——项目直接）
- **论文类型**: Empirical
- **domain**: nlp（情感·可解释性）
- **阅读策略**: Standard
- **第一作者**: Dario Di Palma | Politecnico di Bari（ACL 2025 Main）
- **发表**: 2025 | ACL 2025 Main | arXiv:2505.16491v2
- **venue**: ACL 2025 Main
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2505.16491.pdf
- **引用**: 可（情感探针常用）

### 📚 研究背景

**已知 (Known)**: LLM 情感分析能力强；隐藏态含可探信号（线性表示假设）。

**知识缺口 (Gap)**: 情感特征在哪个层、用哪种 pooling 最被代表——未系统探明。

**研究目标 (Aim)**: 层-wise 探针定位 Llama 情感表征的最佳层 + 评测 6 pooling。

### 🧠 理论背景

- **框架**: 探针分类器沿层 + 跨尺度定位情感表征；线性表示假设。
- **方法**: layer-wise probe + 6 pooling（mean/max/last-token/等）。
- **关键概念**: layer-specific probing、sentiment pooling、mid-layer。

### 📎 关键引用

- **线性表示假设（Mikolov 等）** 🏛️ — 方向性表示。
- 探针技术 — 🔧。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | 情感在中层(core layers)最可检测, +14% 精度 | 【定义】情感表征层位。【本文角色】核心。【论证关联】呼应 L18(L 定位)/L4(深度梯度)/L1(Jspace)：情感深中层编码。项目测 CS 情感读出口选层有据。 |
| 2 | 早层弱; last-token 非最优; 6 pooling 需评测 | 【定义】pooling 影响。【本文角色】实操。【论证关联】项目测读出口要选对层+pooling，别默认 last-token。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 情感探测（层 + pooling）。
**数据集 (Data)**: 情感/sentiment 任务。
**模型**: Llama 多尺度。
**方法/评测 (Eval)**: layer-wise probe 分类器 + 6 pooling 对比。

> **检查清单（nlp)**: [x] 层-wise [x] 跨尺度 [x] 多 pooling。 [ ] 需核任务/数据多样性。

### 💡 核心发现

**主要发现 (Main Findings):**
- 情感特征在**中/核心层**最可检测（binary polarity 提升 +14%）。
- 早层弱；last-token 非始终最优；pooling 选择影响（6 种评测）。
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义**: 情感表征的层位/坐标是可定位的——支持规范化探针；为情感读出口提供操作层位。
**局限性**: Llama 单家族主体；SA 分类任务；pooling/layer generality 需核。

### 📏 复现性

```
**代码**: 待核；探针可复现
**算力**: 推理级
```

### 🔗 与你领域的关系

- **对齐**: 项目"CS 情感读出口"的**层位/坐标**依据——情感在中层，pooling 影响读出。
- **嫁接**:
  - [🔧] 项目测 CS 情感选**中层 + 合适 pooling**（勿默认 last-token）——与 L18 locating、L4 深度梯度一致。
  - [📊] 情感层位可定位 → 支持"信息在特定层、读写分离"的项目命题。
- **引用句**:
  > "identifying the layers and pooling methods that best capture sentiment signals" (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。给项目情感读出口的**实操层位 + pooling** 依据，与 L18 情感定位互证。项目 CS 情感探针设计可直接参考其 layer/pooling 方法。

### 📄 原文摘要

> "We probe the hidden layers of Llama models to pinpoint where sentiment features are most represented... Using probe classifiers, we analyze sentiment encoding across layers and scales, identifying the layers and pooling methods that best capture sentiment signals. Our results show that [sentiment is most detectable in mid-layers, with detection accuracy increasing up to 14% over baselines]."
> （正式入库锁定 Zotero abstractNote）
