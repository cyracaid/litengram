# 📖 NLP 可解释性·不确定性 文献精读 — 2026-08-19

## 关键词: Sparse Autoencoder, Functional Dissociation, Uncertainty vs Correctness, Feature Suppression, 表征惰性

## Are LLM Uncertainty and Correctness Encoded by the Same Features? A Functional Dissociation via Sparse Autoencoders

### 📋 基本信息

- **重要等级**: ⛰️ 镇山之宝（功能解离方法模板 + "信息在那里读数没有"直接先例）
- **论文类型**: Empirical（+ Methods 框架）
- **domain**: nlp（cs.LG 可解释性·不确定性）
- **阅读策略**: Deep
- **第一作者**: Het Patel (UC Riverside) | 合作: Tiejin Chen, Hua Wei (ASU), Evangelos Papalexakis, Jia Chen (UCR)
- **发表**: 2026 | arXiv:2604.19974v1 [cs.LG] 21 Apr 2026
- **venue**: arXiv:2604.19974
- **DOI**: 无 | **arXiv**: 2604.19974
- **代码**: 待核（方法基于 Llama Scope / Gemma Scope 公开 SAE）
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2604.19974.pdf
- **引用**: 新论文

### 📚 研究背景

**已知 (Known)**: UQ 方法用 AUROC/AUPRC 判别正确/错误预测；隐含假设=不确定性↔正确性紧密耦合。LLM 隐藏态编码自身正确性/知识意识（Kadavath, Burns, Azaria-Mitchell）——但都沿单轴研究。

**知识缺口 (Gap)**: 无人测试不确定性特征和正确性特征**是否同一批特征**、能否**独立识别与控制**。单轴方法可能混淆两个独立现象。

**研究目标 (Aim)**: 用 SAE 分解内部表示，检验不确定性 vs 正确性是否由**不同/重叠的特征群体**编码，并测各群体的**功能角色**（必需/惰性/有害）。

### 🧠 理论背景

- **框架**：2×2 象限（correctness × confidence），沿两轴独立做统计检验，识别三类特征：纯不确定性 / 纯错误性 / 混杂。
- **方法**：SAE 特征（Llama Scope 4B/m 32K for Llama-3.1-8B；Gemma Scope 3.5K/m 16K for Gemma-2-9B）；Mann-Whitney U + Cohen's d；抑制实验（encode-modify-decode，zero 目标特征）。
- **关键概念**：functional dissociation（功能解离）、feature inertness（特征惰性）、suppression protocol、predictive dissociation（预测解离）。

### 📎 关键引用

- **SAE / Llama Scope / Gemma Scope (2024)** 🔧方法来源 — 激活稀疏分解工具。
- **Kadavath 2022 / Burns 2023 / Azaria & Mitchell 2023** 📊数据支撑 — 内部正确性信号存在（单轴先行）。
- **Kuhn 2023 semantic entropy / Lin 2024 / Chen 2024** 🔧方法来源 — 输出级 UQ（对照，无法达内部）。
- **Ferrando 2024 (SAE+Gemma steering)** 🔧方法来源 — SAE 特征可干预（实体/幻觉）。

### 📌 关键标注

| # | 原文区域 | 批注 |
|---|------|------|
| 1 | §5.2: 纯错误特征抑制→行为近零 (mean Δacc -0.03%) | 【定义】feature inertness。【本文角色】功能解离核心。【论证关联】**"信息在那里(激活显著)读数没有(抑制无效应)"直接先例**——本项目"表征正效应+行为null"的最佳现成模板。 |
| 2 | §5.4: 纯错误特征正确性预测近 chance("faint correlational traces rather than structured representations")| 【定义】预测解离；混杂特征 3 个 AUROC 0.787 vs 纯错误 near-chance。【本文角色】信息性差异。【论证关联】区分"结构化表征 vs 微弱相关痕迹"的量尺——项目测 CS 情感时用来区分真编码 vs 伪迹。 |
| 3 | §7: "model does not fully exploit [signal] in its output" | 【定义】混杂特征=可行动内部信号未被输出利用。【本文角色】abstention 应用。【论证关联】直接对应"信息在那里读数没有"——内部有预测可靠性信号但输出没用。 |
| 4 | §5.2 深度梯度: 效应集中晚层，早期(max depth<0.3)弱 | 【定义】表示解缠随层深增强。【本文角色】层位敏感性。【论证关联】呼应前两篇（J-lens 早层盲区）：测表征别忽略层位。 |
| 5 | Limitations: MCQ only + 无多重比较校正 | 【定义】边界。【本文角色】诚实。【论证关联】功能惰性可能任务依赖；项目若复现需扩到生成/情感任务。 |
| 6 | §5.1: 纯错误特征对熵阈值敏感(7.5% retention) | 【定义】错误信号扩散 vs 不确定性 tail 驱动。【本文角色】稳健性警示。【论证关联】"错误/负面信号"比"不确定性/极端信号"更散——项目找 CS 情感解离信号要考虑信噪。 |

### 🔬 研究方法

> domain=nlp → nlp 版

**任务定义 (Task)**: MCQ 推理；测不确定性(输出熵) vs 正确性(答案匹配)——均沿内部分解。
**数据集 (Data)**: MMLU test (14,042；发现/验证各 ~7,021)；泛化 ARC-Challenge / RACE。
**模型架构**: Llama-3.1-8B + Llama Scope SAE；Gemma-2-9B + Gemma Scope SAE（跨架构复现）。
**训练细节**: 无需训练；用 pretrained SAE 编码残差流；无梯度更新。
**评测 (Eval)**: 特征发现(Mann-Whitney, p<0.05, d>0)；抑制(encode-zero-decode)测 acc & 熵变化；发现-验证分离协议；跨数据集无需再选择；跨架构整管复现；预测性分类器 AUROC。

**AI 实验设计检查点 (Experiment Design)**:
```
· 控制变量：2×2 象限沿两轴独立检验；熵阈值 25/75 percentile (tail-vs-tail)
· 发现-验证分离：discovery 只在半数，validation 全新 held-out
· 关键对照：随机特征抑制 (features-per-layer matched + same screening) → 验证效应特异于混杂类别
· SAE reconstruction-error 对照：不加抑制编解码无变化 → 排除重建误差
· 选择标准 ablation：accuracy+entropy vs accuracy-only vs entropy-only → 单独熵会灾难(-10.78%)
· 阈值敏感性：25/75 vs 中位数切分，混杂 90.2% 保留 / 纯错误 7.5% 保留
· 泛化：跨数据集 6 方向 + 跨架构整管
```

> **WHY 分析（层 2）**:
> - 为什么 SAE 而非 probe/神经元？需逐特征独立识别+干预；SAE 把激活拆成可寻址特征方向，是仅有的能"独立抑制一个信号"的工具。
> - 为什么 MCQ？正确性二值可判，不确定性直接从答案 token 熵读出，跨模型可比；开放式需手工 UQ 难比。
> - 为什么抑制"零过去"而非 steering？要测"功能必需/惰性/有害"三态——零化后行为变化直接反映该特征是否参与计算。
> - 为什么发现-验证分离？避免特征选择过拟合——筛出的 55 特征在全新 held-out 上复现效应才是真。
>
> **检查清单（nlp 评测公平性）**:
> [x] 基线公平：随机特征匹配对照
> [x] 多次运行：跨 2 架构 + 跨 3 数据集
> [x] 消融完整：选择标准三态ablation + 阈值敏感性
> [x] 显著性：Mann-Whitney p<0.05 + Cohen's d
> [x] 代码/数据：MMLU/ARC/RACE 公开 + Scope SAE 公开
> [ ] 多重比较校正：未做(formal)（作者自认，可能影响计数）
> [ ] 人工抽查：特征语义无人工验证

### 💡 核心发现

**主要发现 (Main Findings):**

**发现 1 — 三类特征功能角色截然不同（three-way dissociation）**
- 纯不确定性：d>6，功能必需（抑制→精度崩，-10.21%@Llama layer31）
- 纯错误性：d<0.8，**功能惰性**（68% 特征抑制→近零变化，mean Δacc -0.03%）
- 混杂：有害（抑制 +1.1% acc & -0.62 熵，Llama）
- **证据强度**: Direct | **证据来源**: Empirical + 干预

**发现 2 — 特征信息性也解离（predictive dissociation）**
- 纯错误特征正确性预测近 chance；3 个混杂特征 AUROC 0.787（对照输出熵 0.805），跨数据集迁移。
- **证据强度**: Direct | **证据来源**: Empirical

**发现 3 — 混杂特征抑制改善输出 + 选择性弃权**
- 弃权：3 特征 → 精度 62%→81%@53% coverage，胜过模型自弃权（self-abstained +1.8% vs +19.4%@52.8%）。
- **证据强度**: Direct | **证据来源**: Empirical

**SOTA vs 本文 vs 基线（抑制效果，Table 5.2）**:

| 设置 | Llama acc/ent | Gemma acc/ent |
|------|------|------|
| Baseline | 61.91% / 0.824 | 67.63% / 0.528 |
| Random suppression | 61.96% / 0.818 | 67.67% / 0.528 |
| Confounded suppression | 63.01% / 0.205 | 67.85% / 0.278 |

**理论意义**: 不确定性(confidence)与正确性(correctness)是**内在不同的现象**——标准单轴 UQ 评估系统性混淆二者。揭示 transformer"用功能不同特征群体组织不确定性与错误"的一般组织原则（跨 2 架构复现）。

**局限性 (Limitations)**: MCQ only（惰性可能 task-dependent）；8-9B 规模未测更大；依赖特定 SAE；无多重比较校正；抑制只是多种干预之一（patching/steering 可能揭示零化看不到的关系）。

### 📏 复现性

```
**代码**: 基于公开 Llama Scope / Gemma Scope SAE + MMLU/ARC/RACE 数据，可复现
**数据**: MMLU/ARC/RACE 公开；需 Scope SAE 权重
**算力**: 推理级 + SAE 编解码；8B 单卡可跑
**复现核对**: 图表可复现；需对齐熵阈值/筛选/发现-验证分离协议
**种子/超参**: 25/75 熵阈值、p<0.05、d>0、top-5/layer/category、k(sparsity)
**接口可用性**: TransformerLens/SAE Hub 生态可加载 Llama/Gemma Scope
```

> 判断门槛：**"最贵的一步？"** Scope SAE 权重 + 多模型推理。对本项目：**"2×2 象限 + SAE 特征 + 抑制"是测"信息在表征 vs 读出口"的直接模板**——若项目有足够 MCQ 化的 CS 情感探测任务可套用。

### 🔗 与你领域的关系

- **直接对齐**：这是**"信息在那里读数没有"最精确的功能解离模板** + 非 CS 领域直接先例。
- **可借用的具体方法（战略嫁接）**:
  - **[🔧 方法] 2×2 象限框架**：把"CS 情感读出"换成"行为轴"、"情感信息轴"，同法识别哪些特征编码情感但行为惰性。
  - **[🔧 方法] SAE 特征抑制协议**（encode-zero-decode + 随机对照 + 发现-验证分离）——项目测"去除 CS 情感表征后行为是否变化"的现成协议。
  - **[📊 先例] 纯错误特征惰性** = "表征正效应 + 行为 null"的最干净实证——直接可引。
  - **[🔧 方法] 预测解离判据**：用"特征能否预测行为轴"区分结构化表征 vs 微弱相关痕迹——项目区分"CS 情感真编码"vs"伪迹"用此法。
  - **[🔥 反向]** 混杂特征可行动性：项目若发现"混杂特征"，抑制可改善——提示可作干预点。
- **可引用的引述段落（英文）**:
  > "The model maintains internal features that reliably track prediction errors, yet suppressing these features produces no measurable change in accuracy or entropy." (Discussion)
  > "These features correlate reliably with incorrectness but produce no measurable behavioral effect under our suppression protocol." (§5.2)
  > "confounded features encode a compact, transferable signal about prediction reliability that the model does not fully exploit in its output." (Discussion)
- **方法学关联（三篇互补）**:
  - 2607.15495 (J-lens)：测"是否 verbalizable/在 J-space"——输入层视角
  - 2411.08745 (activation patching)：测"语言/概念分层、能否独立操纵"——干预视角
  - 2604.19974 (SAE disssociation)：测"哪类特征惰性/必需/有害"——特征群体视角
  - 三篇共同支撑"表征正效应+行为 null"是**真实、可测、可干预**的现象。

### ⭐ 为什么这篇重要

如果把"信息在那里读数没有"当作项目核心命题，这篇给的是**最难的实证缺口**——不是"能不能读到"，而是**"信息确实在里面（激活显著）但行为完全不用它（抑制无效应）"的可干预、跨架构复现证据**。同时给出 SAE 抑制 + 预测解离 + 随机对照的完整方法模板，是项目设计解离实验的直接参照。⛰️ 级。

### 📄 原文摘要

> "Large language models can be uncertain yet correct, or confident yet wrong, raising the question of whether their output-level uncertainty and their actual correctness are driven by the same internal mechanisms or by distinct feature populations. We introduce a 2 × 2 framework that partitions model predictions along correctness and confidence axes, and uses sparse autoencoders to identify features associated with each dimension independently. Applying this to Llama-3.1-8B and Gemma-2-9B, we identify three feature populations that play fundamentally different functional roles. Pure uncertainty features are functionally essential: suppressing them severely degrades accuracy. Pure incorrectness features are functionally inert: despite showing statistically significant activation differences between correct and incorrect predictions, the majority produce near-zero change in accuracy when suppressed. Confounded features that encode both signals are detrimental to output quality, and targeted suppression of them yields a 1.1% accuracy improvement and a 75% entropy reduction, with effects transferring across the ARC-Challenge and RACE benchmarks. The feature categories are also informationally distinct: the activations of just 3 confounded features from a single mid-network layer predict model correctness (AUROC ~0.79), enabling selective abstention that raises accuracy from 62% to 81% at 53% coverage. The results demonstrate that uncertainty and correctness are distinct internal phenomena."
> （正式入库锁定 Zotero abstractNote）
