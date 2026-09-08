# 📖 统计学·PPI 功效 文献精读 — 2026-08-19

## 关键词: Power Analysis, Prediction-Powered Inference, Sample Size, Label Efficiency, Wald Test

## Power Analysis for Prediction-Powered Inference

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（α 臂样本量设计——补 L21 的 inference）
- **论文类型**: Methods（统计/生物统计）
- **domain**: nlp/stats（PPI 功效）
- **阅读策略**: Standard
- **第一作者**: Yiqun T. Chen | Johns Hopkins（Moran Guo, Shengyi Li）
- **发表**: 2026 | arXiv:2603.16041
- **venue**: arXiv:2603.16041
- **代码**: R 包 pppower（github.com/yiqunchen/pppower）
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2603.16041.pdf
- **引用**: 新

### 📚 研究背景

**已知 (Known)**: 研究用 AI/ML 预测做有效推断（PPI）；但经典功效/样本量公式不适用于此类预测。

**知识缺口 (Gap)**: 给定高预测力模型，需多少标注样本达目标功效？无公式。

**研究目标 (Aim)**: 推 PPI 估算器渐近方差 → Wald 检验反演 → 闭式功效/样本量公式。

### 🧠 理论背景

- **方法**: 渐近方差 + Wald 反演得标注样本量；覆盖两样本比较、2×2 表风险度。
- **规则**: 减少所需标注样本量∝预测↔真值 R²。
- **关键概念**: PPI power、label efficiency、Wald inversion、R² 标尺。

### 📎 关键引用

- **PPI（Angelopoulos 等）** 🏛️ — 前作。
- 功效分析/样本量经典 — 📊。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | 所需标注样本减少∝R² | 【定义】R² 决定省样量。【本文角色】规则。【论证关联】**α 臂抽样的样本量计划**——用 LLM 预测 R² 估可省多少人类标注。 |
| 2 | 闭式公式 + R 包 | 【定义】可直接算。【本文角色】工具。【论证关联】项目 α 臂设计样本量直接用 pppower。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: PPI 功效/样本量。
**方法**: 闭式渐近功效公式 + Wald 反演；Monte Carlo 验证。
**评测 (Eval)**: 公式 vs 仿真；3 生物医学应用。

> **检查清单（nlp)**: [x] 理论+仿真 [x] 多场景 [x] 工具公开。

### 💡 核心发现

**主要发现 (Main Findings):**
- 闭式功效/样本量公式（两样本比较、2×2 表）。
- 省样量∝R²（有用标尺）。
- Monte Carlo 验证 + 3 应用 + R 包。
- **证据强度**: Direct（仿真）+ Theoretical | **证据来源**: Empirical + Theoretical

**理论意义**: 让 PPI 设计可直接算样本量，弥合"预测代理推断"到"实验设计"缺口。
**局限性**: 面向两样本/风险度等常见设置；需预测模型 R²。

### 📏 复现性

```
**代码**: R 包 pppower 公开
**算力**: 轻
```

### 🔗 与你领域的关系

- **对齐**: α 臂 PPI 的**样本量规划**。
- **嫁接**:
  - [🔧 方法] 用 pppower 算"CS 情感"需多少人类标注 + LLM 预测省多少。
  - [📊] R² 标尺 → 项目估预测力与省样量。
- **引用句**:
  > "the reduction in required labeled samples relative to classical designs scales roughly with the R² between the predictions and the ground truth." (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。补 L21 给 α 臂**样本量/功效设计**——项目用 PPI 时能定量规划标注预算。α 臂方法论主干完备。

### 📄 原文摘要

> "Given a new AI/ML model with high predictive power, how many labeled samples are needed to achieve a desired level of statistical power? We derive closed-form power formulas by characterizing the asymptotic variance of the PPI estimator and applying Wald test inversion... We find that the reduction in required labeled samples relative to classical designs scales roughly with the R² between the predictions and the ground truth."
> （正式入库锁定 Zotero abstractNote）
