# 📖 NLP 多语言·SAE 文献精读 — 2026-08-19

## 关键词: SAE, Language-Specific Features, Random-token Filtering, Monolingual, Language Steering, LangFIR

## LangFIR: Discovering Sparse Language-Specific Features from Monolingual Data for Language Steering

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将（β 臂多语言 SAE 特征发现直接可用）
- **论文类型**: Methods + Empirical
- **domain**: nlp（cs.CL 多语言可解释性·SAE）
- **阅读策略**: Standard
- **第一作者**: Sing Hieng Wong | University of Kentucky；Hassan Sajjad (Dalhousie), A.B. Siddique (Kentucky)
- **发表**: 2026 | COLM 2026 会议论文 | arXiv:2604.03532
- **venue**: COLM 2026（conference paper）
- **代码**: 待核
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2604.03532.pdf
- **引用**: 新

### 📚 研究背景

**已知 (Known)**: Representation-level steering（表示层转向）加语言特定向量到激活，推荐于免训练控制；但识别 residual stream 语言特定方向常依赖多语/平行数据（贵）。SAE 分解可解释稀疏特征（含语言控制同族 L6/L7）。

**知识缺口 (Gap)**: 现有 SAE 语言转向法仍受多语/平行数据约束；缺少仅用**少量单语数据**发现语言特定特征的方法。

**研究目标 (Aim)**: LangFIR——用单语 + random-token 序列发现语言特定 SAE 特征（过滤语言无关特征），无需平行/多语数据。

### 🧠 理论背景

- **机制**: 很多被目标语输入激活的 SAE 特征**不编码语言身份**（语言无关）；random-token 序列会激发这些语言无关特征 → 过滤掉 → 隔离稀疏语言特定特征。
- **方法**: ①收集目标语句子 + 生成 random-token 序列 ②SAE 编码 residual 激活 ③sample-wise 过滤（语言一致 vs random-token 语言无关）④用语言特定特征构 steering 向量。
- **关键概念**: random-token filtering、language-specific SAE features、monolingual-only。

### 📎 关键引用

- **SAE / steering（Cunningham, Templeton）** 🔧方法来源。
- **Zhong 2025（数据高效维度）** 🎯批判靶子/对照 — 数据高效但需更强变体。
- **Tang/Gurgurov（neuron 转向）** 🎯批判靶子 — 需数据。

### 📌 关键标注

| # | 区域 | 批注 |
|---|------|------|
| 1 | random-token 过滤语言无关特征 | 【定义】语言特定特征=不被 random-token 激发的稀疏集合。【本文角色】核心创新。【论证关联】β 臂做多语言 SAE 语言操纵，用此法单语即可隔离语言特征（免平行）。 |
| 2 | 单语即可，超平行基线 | 【定义】数据约束大降。【本文角色】卖点。【论证关联】无平行语料 CS 场景（离散叙事）友好。 |
| 3 | best acc×BLEU 跨 3 模型 | 【定义】跨模型稳健。【本文角色】验证。【论证关联】多语操纵可靠。 |

### 🔬 研究方法

> domain=nlp → nlp 版（精简）

**任务定义 (Task)**: 多语生成控制（语言转向）。
**数据集 (Data)**: 目标语少量单语句 + random-token 序列（无需平行/多语）。
**模型架构**: Gemma 3 1B/4B, Llama 3.1 8B。
**训练细节**: 免训练（SAE 预训练 + 特征过滤）。
**评测 (Eval)**: accuracy × BLEU 多语生成控制；对单语基线 4.7×、胜平行法。

> **检查清单（nlp)**: [x] 跨 3 模型 [x] 单语作对照 [x] 超平行数据法。 [ ] 需核实验细节±显著性。

### 💡 核心发现

**主要发现 (Main Findings):**
- 大量被目标语激活的 SAE 特征语言无关；random-token 可滤除。
- LangFIR 用单语 + random-token 隔离语言特定稀疏 SAE 特征，构转向向量。
- 多语生成控制 acc×BLEU 最优跨 3 模型；超单语基线 4.7×，胜平行数据法。
- 语言身份在 LLM 中定位于单语可发现的稀疏特征方向。
- **证据强度**: Direct | **证据来源**: Empirical

**理论意义**: 支持"语言身份=稀疏可发现特征方向"（L7 同族）+ 免平行数据可行性。
**局限性**: 语言/模型规模覆盖面；steering 对复杂生成鲁棒性；单语 vs 平行 trade-off 细节。

### 📏 复现性

```
**代码**: 待核
**算力**: 推理 + SAE 编码（轻）
**数据**: 目标语单语少量句 + random-token（易得，无平行）
```

### 🔗 与你领域的关系

- **对齐**: β 臂多语言 SAE 特征发现——LangFIR 用单语 + random-token 即可隔离语言特定特征，**无平行语料 CS 场景直接可用**。
- **嫁接**:
  - [🔧 方法] random-token 过滤 → 测 CS 情感"语言特定 vs 情感共享"特征分离时，用此法隔离语言维度。
  - [📊 佐证] 语言身份在稀疏方向 → 与 L1/L2/L6/L7 一致，强化"语言外壳可分"。
  - [⚠️] 需注意 steering 复杂生成鲁棒性。
- **引用句**:
  > "language identity in multilingual LLMs is localized in a sparse set of feature directions discoverable with monolingual data." (Abstract)

### ⭐ 为什么这篇重要

⚔️ 级。给 β 臂**免平行数据的语言特定 SAE 特征发现法**，成本最低、低资源友好。与 L6/L7 构成"多语言 SAE 操纵"三件套（层选 L6 + 稀疏维度 L7 + 特征过滤 LangFIR）。方法与核心解离主题衔接（语言=可分离稀疏层）。

### 📄 原文摘要

> "We introduce LangFIR (Language Feature Identification via Random-token Filtering), a method that discovers language-specific SAE features using only a small amount of monolingual data and random-token sequences. Many SAE features consistently activated by target-language inputs do not encode language identity. Random-token sequences surface these language-agnostic features, allowing LangFIR to filter them out and isolate a sparse set of language-specific features. On the multilingual generation control task, LangFIR achieves the best average accuracy × BLEU among steering methods across three models (Gemma 3 1B, Gemma 3 4B, and Llama 3.1 8B)... surpassing methods that use parallel data. Our results suggest that language identity in multilingual LLMs is localized in a sparse set of feature directions discoverable with monolingual data."
> （正式入库锁定 Zotero abstractNote）
