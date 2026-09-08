# 📖 统计学方法·PPI 文献精读 — 2026-08-19

## 关键词: Prediction-Powered Inference, Surrogate Outcomes, Recalibration, Statistical Inference, Effective Sample Size

## Predictions as Surrogates: Revisiting Surrogate Outcomes in the Age of AI

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（α 臂抽样设计主干——AI 预测作代理）
- **论文类型**: Methods（统计学）
- **domain**: nlp/stats（prediction-powered inference）
- **阅读策略**: Standard
- **第一作者**: Wenlong Ji | Stanford（Lihua Lei, Tijana Zrnic）
- **发表**: 2026 | arXiv:2501.09731
- **venue**: arXiv:2501.09731
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2501.09731.pdf
- **引用**: 中高（PPI 线）

### 📚 研究背景

**已知 (Known)**: outcome 昂贵/耗时，代理(surrogate)结果加速分析（生物统计/经济）；PPI（prediction-powered inference）用预训练模型预测作代理提高统计功效。

**知识缺口 (Gap)**: PPI 与 surrogate outcome 文献的正式联系未建立；PPI 效率可提升。

**研究目标 (Aim)**: 建立 surrogate-PPI 联系 + 发展**再校准 PPI**（更高效，用 flexible ML 学最优 imputed loss）。

### 🧠 理论背景

- **框架**: 预测作代理 → 统计推断（不浪费真结果）。
- **方法**: recalibrated PPI——用 ML 学最优 imputed loss（recalibration 步）；凸目标（损失凸）。
- **性质**: 总优于只用真数据；一致时最小渐近方差。
- **关键概念**: surrogate outcome、PPI、imputed loss、recalibration、effective sample size。

### 📎 关键引用

- **PPI（Angelopoulos 等 2023）** 🏛️ — 前作。
- **Surrogate outcomes（Prentice 1989, Robins）** 🏛️ — 生物统计源头。
- **Mathematical stats 推断** — 🔧。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | AI 预测作廉价代理 → 统计功效↑ | 【定义】不浪费未标注数据。【本文角色】核心。【论证关联】**α 臂替代人类臂主干**——AI 当 surrogate，少量人类标注校准。 |
| 2 | 总优于纯真数据（即使 imputed loss 估计有偏）| 【定义】稳健保证。【本文角色】性质。【论证关联】项目 α 臂用 PPI 有理论保证。 |
| 3 | 一当一致最小渐近方差 | 【定义】最优性。【本文角色】理论。【论证关联】方法选择依据。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 用 AI 预测作代理做统计推断。
**数据集 (Data)**: 有标签(真)+无标签(预测)混合。
**方法**: recalibrated PPI（ML 学 imputed loss）。
**评测 (Eval)**: 渐近方差、effective sample size；3 AI 应用验证。

> **检查清单（nlp)**: [x] 理论保证 [x] 3 应用 [x] 对照 PPI。 [ ] 需核数值细节。

### 💡 核心发现

**主要发现 (Main Findings):**
- 建立 surrogate-outcome 与 PPI 的正式联系。
- Recalibrated PPI 更高效，总优于纯真数据（有偏也）。
- 一致时最小渐近方差；凸目标可解。
- 3 应用（SOTA AI 模型）显著提升 effective sample size。
- **证据强度**: Direct（数值）+ Theoretical | **证据来源**: Empirical + Theoretical

**理论意义**: 给"AI 预测代理统计推断"提供更优方法 + 与经典 surrogate 文献统一。
**局限性**: 需代理与结果相关假设；imputed loss 估计复杂度。

### 📏 复现性

```
**代码**: 待核；算法可复现
**算力**: 低（推断为主）
```

### 🔗 与你领域的关系

- **对齐**: **α 臂替代人类臂方法论主干**（LITSCAN 推荐 DSL/PPI）。
- **嫁接**:
  - [🔧 方法] Recalibrated PPI → α 臂用 LLM 预测（surrogate）+ 少量人类标注校准做 CS 情感统计推断。
  - [📊 保证] 总优于纯真数据 → 项目可放心用预测代理补样本。
- **引用句**:
  > "treats predictions from pre-trained models... as cost-effective surrogates for expensive outcomes." (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。α 臂抽样设计主干——LLM 预测作代理 + 人类标注校准的统计推断法，给项目替代人类臂提供理论保证的方法。项目 core 方法之一。

### 📄 原文摘要

> "We establish a formal connection between the surrogate outcome model... and prediction-powered inference (PPI). We develop recalibrated prediction-powered inference, a more efficient approach... using flexible machine learning techniques to learn the optimal 'imputed loss' through recalibration. The method always improves upon the estimator that relies solely on the data with available true outcomes... and achieves the smallest asymptotic variance among PPI estimators if the estimate is consistent."
> （正式入库锁定 Zotero abstractNote）
