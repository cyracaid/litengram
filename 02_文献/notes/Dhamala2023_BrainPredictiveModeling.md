# 📖 Precision Psychiatry 方法论文献精读 — 2026-08-03

## 关键词: predictive modeling, machine learning, functional connectivity, precision psychiatry, methodological bias

## One Size Does Not Fit All: Methodological Considerations for Brain-Based Predictive Modeling in Psychiatry

### 📋 基本信息

- **重要等级**: ⚔️ 精兵强将
- **论文类型**: Review
- **阅读策略**: Standard
- **第一作者**: Elvisha Dhamala | Yale University, Dept. of Psychology / Kavli Institute
- **通讯作者**: Elvisha Dhamala / Avram J. Holmes
- **发表**: 2023 | Biological Psychiatry 93(8): 717-728
- **DOI**: 10.1016/j.biopsych.2022.09.024
- **Zotero**: `V2F9HE9C` | **PDF**: `KEFDT4YT` | **笔记**: (待写入)
- **引用**: ~(综述, 引用持续增长)

### 📚 研究背景

**已知 (Known)**

- 传统精神科影像研究以**群体水平 (group-level)** 分析为主，发现了多种精神疾病相关的"平均"神经生物学改变
- 精神疾病本质上是**异质性的 (heterogeneous)**——同一诊断内部，病人间症状谱差异极大，健康与疾病边界模糊（Hyman, 2010 的 reification 批判）
- 精准医疗 (precision medicine) 由群体范式转向**个体水平**，结合生物学与环境因素理解个体临床呈现
- 机器学习的崛起 + 大型公开数据集（如UK Biobank、ABCD）催生了"数据驱动的发现科学"

**知识缺口 (Knowledge Gap)**

- **已知未知 (Known Unknowns)**：尽管已有多个预测建模指南（Scheinost et al. 2019; Varoquaux et al. 2017; Woo et al. 2017 等），却**没有一篇系统综述**讨论"不同的方法论选择会如何影响模型表现"——这正是本文要填补的空白
- **未知未知 (Unknown Unknowns)**：不同人群（性别、种族、交叉身份）中，脑-行为关系本身可能不同，普通模型在新人群里会失效（general predictions often fail）；以及 Intersectionality（多种边缘化身份交叉）对泛化性的影响——这些是本文揭示的需更多文献佐证的新方向

**研究目标 (Research Aim)**

- 综述神经影像-机器学习预测模型在精神医学的应用，并系统讨论"算法、模态、数据转换、表型、脑分区、样本量、人群定位"这些选择如何影响模型的表现，从而指导精准精神病学的正确实施。

### 🧠 理论背景

**核心理论框架**

- **Precision Psychiatry 精准精神病学**（Vieta, 2015）：将精准医疗理念应用于精神科——从"一刀切"转向个体化诊断、预后与治疗推荐。本文的通篇理论底座。
- **离散 vs. 维度模型**：诊断标签（离散/分类）与精神病理学层级特征（维度/维度评分）提供互补信息；两个模型结合才能改善个体水平的理解。这决定了后面 **phenotype selection** 的争论（该预测诊断还是症状维度）。
- **预测性建模的三大分析类别**（Descriptive / Predictive / Prescriptive）——对应监督/半监督/无监督算法（Figure 1）。

**关键概念**

#### 精准精神病学 (Precision Psychiatry) 🔬

**一句话粗暴定义**：把"个体化诊断、预测预后、推荐个体化治疗"纳入精神医学的决策框架，不再一套方案打天下。

**溯源**：Vieta (2016, *Rev Psiquiatr Salud Ment*) 明确提出 precision psychiatry 一词；其源头是 National Research Council (2011) 的 *Toward Precision Medicine* 报告（肿瘤领域的成功范式）。属于"基于生物标志物"的精准医学传统。

**易混辨析**：
| 概念 | 含义 | 与"一刀切"的关系 |
|------|------|------|
| 传统的 based models | 群体均值 | 把群体当同质整体 |
| Precision peronalized | 利用个体生物+环境信息 | 承认个体差异 |
| Predictive modeling | 用统计学习做个体化预测 | 精准医学落地的工具层 |

**核心机制**：通过机器学习把脑影像等特征映射到个体行为/诊断/预后，从而识别"这个病人身上到底哪里不一样"。

**与你研究的关联**：你的 proposal 用 fMRI + 心跳检测任务（CARED）+ 元认知指标做个体水平的 interoception-anxiety 建模，本质上就是在做 precision psychiatry。本文是你论证"为什么要个体化建模、为什么要小心选择方法"的引用支柱。

**人话类比**：群体分析好比"测全班平均成绩"；predictive modeling 好比"专门给某个学生诊断他哪科偏科、怎么补"。

**一句话总结**：**精准精神病学 = 用脑数据给每个病人做"个体化画像"，而非问"这类病人平均什么样"。**

#### 连接组预测模型 (Connectome-based Predictive Modeling, CPM) 🔬

**一句话粗暴定义**：从全脑功能连接里自动找出与某个行为/表型最相关的连接特征，用这些特征搭一个线性模型去预测行为，全程数据驱动。

**溯源**：Shen et al. (2017, *Nature Protocols*)。属于"脑连接组学 + 数据驱动特征选择"方法族。

**易混辨析（与深度学习）**：
| 维度 | CPM（线性、可解释） | BrainNetCNN等深度学习（非线性、黑箱） |
|------|------|------|
| 特征选择 | 数据驱动、基于皮尔逊相关 | 网络自动学习特征 |
| 可解释性 | 高（能看哪条连接最重要） | 低（黑箱） |
| 跨数据集泛化 | 往往更稳健 | 更易过拟合（见 autism challenge 25） |

**在本文中的角色**：作为"算法选择"一节的开篇范例，说明数据驱动 + 内置交叉验证 + 连续预测 3 大好处；也用它在整个预测工具集里的位置来说明——不同算法适合不同任务，选择应由**研究目标**驱动而非跟风。

**与你研究的关联**：如果你用 fMRI 功能连接预测焦虑症状，CPM 是一个直接可移植的起点；而你的多模态（fMRI + 心跳/外刺激）可用它验证"叠加信号是否带来精度增益"。

**人话类比**：CPM 像一个看全文找出"哪些词最能猜到本文主题"的搜索机器——不靠预设，而是从数据里自己挑。

**一句话总结**：**CPM 是自己挑特征的线性预测器，透明、稳健、易移植，是精准精神预测建模的实用底座。**

#### 脑分区 Parcellation 与维数灾难 (Curse of Dimensionality)

- **粗暴定义**：大脑有几十万个体素，直接做特征会陷入"维数灾难"；分区把脑切成几十到几百个区/网络来降维。
- **来源高**：分区可基于细胞构筑/沟回定位/数据驱动（内在功能、task、ICA）。这是脑网络分析的标准预处理。
- **核心机制**：降维减少噪声、降低计算复杂度、增强可解释性——但同时**丢失体素级生物信号**，并掩盖个体化网络拓扑差异。
- **在本文**：分区定义/分辨率会影响预测表现（引 26/27/110/111 部分证据），也有研究认为跨分区结果一致（24）。因此建议**ensemble（跨分区集成）**与**个体特异性分区 (individual-specific parcellations)**。
- **与你研究**：你的功能连接分析如果不谨慎选分区，可能引入系统性 bias——可考虑用 ensemble 或多模态分区来 robustify。
- **人话类比**：分区就像把照片打成"马赛克格子"——简单好处理但细节丢了；分细了反而过度复杂。

#### 功能连接参数化：full correlation vs. partial correlation vs. tangent space

- **cross-correlation（全相关）**：标准化协方差；**部分相关**：靠 precision 矩阵逆，除去其它 parcel 后两 parcel 的相关；**切线空间**：把相关矩阵投影到黎曼流形的切线空间，让操作保持"相关矩阵"的数学性质。
- **证据**：有研究指出 tangent space 表示在多种精神疾病分类中比 full/partial 更准确、更可靠 (26)。
- **人话类比**：全相关是"测两个人合拍的粗相关"，部分相关是"排除其他人的干扰后看两人专不专"。

#### 样本量与迁移学习 (Sample Size + Transfer Learning)

- **核心**：ML 在精神影像中的核心问题是样本量——算法需要样本量 > 维度以防过拟合；几十人的旧研究给出的精度估计过于乐观，且无法泛化到独立样本。
- **关键结论**：诊断/行为预测的精度与样本量往往存在**强负相关**（117/120，见 AD、抑郁、精神分裂、自闭症）。
- **迁移补充（meta-matching）**：大样本学到的脑-行为映射可迁移到小样本、甚至非脑影像特征；能"巨幅减少临床小样本所需规模"。
- **易混**：overfitting(过拟合) vs underpowered(功效不足) —— 都是小样本问题的表现，方向相反。
- **人话类比**：小样本上课资料=死记硬背考试题（过拟合），大样本=真懂规律融会贯通。迁移学习=用高考真题库教，然后去教小型培训班。

**理论→本研究的逻辑链**

```
精神疾病高度异质 + 群体分析无法捕获个体差异
   ↓
机器学习的个体化预测模型可以逐一预测诊断/维度/认知/人格
   ↓
但很多"方法论选择"（算法/模态/转换/分区/样本/人群）都会偏差模型
   ↓
不处理这些选择 → 精度再好也只在自己样本上有效，无临床价值
   ↓
因此必须以具体研究目标为准，谨慎选择方法，并对结果解读谨慎
```

### 📎 关键引用

- **Shen, X. et al. (2017)** 🔧 方法来源
  Connectome-based Predictive Modeling (CPM) 的方法学论文 (*Nature Protocols*)。
  → 本文"算法选择"一节的招牌例子，也是读者可直接移植的预测协议。

- **Scheinost, D. et al. (2019)** 🏛️ 理论基石 / 🎯
  "Ten simple rules for predictive modeling of individual differences in neuroimaging" (*NeuroImage*).
  → 已有预测建模规范之一；本文指出还没有"专门谈多大方法选择如何影响模型"的综述，此为其空白定位。

- **Caspi, A. et al. (2014)** 🏛️ 理论基石
  P因子 (精神病理学共同潜在因子)。
  → 论证精神疾病跨诊断共性，支撑"做维度/维度相关预测比分类更有价值"的论点

- **Hyman, S. E. (2010)** 🎯 批判靶子
  "The diagnosis of mental disorders: The problem of reification" (*Annu Rev Clin Psychol*)。
  → 批判诊断标签的实体化，为"为什么仅靠诊断做预测不够"提供理论基础。

- **Varoquaux, G. et al. (2017)** 🔧 方法来源
  "Assessing and tuning brain decoders: Cross-validation, caveats, and guidelines" (*NeuroImage*)。
  → 为本文关于交叉验证/泛化性与小样本过拟合的论点提供统计基础。

- **Shen, X. (2016) / Hyman or 5 revisit** — 其余为数据支撑性引用（如 Kawahara BrainNetCNN 2017, Hu et al. 认知预测比较 21/22/23）。⚔️ 级选以上 5 条承重引用即可。

### 🔬 研究方法

**被试 (Participants)**
- 本文为**综述/理论文，无被试**。

**实验设计 (Experimental Design)**
- 本文为**综述/理论文，无实验设计**。改为拆解论证结构。

**实验流程 (Procedure)**
- 系统性回顾文献，按"方法论选择"维度组织论证：算法 → 模态 → 数据转换 → 表型 → 分区 → 样本量/迁移 → 人群特异性。

**数据分析 (Data Analysis)**
- 综述论证：对每个方法论维度，给出"已发表证据 → 影响模型的方向/趋势 → 应对策略/建议"。

> **论证结构拆解（Review/Ttheory/Position应用）**
> - **主张链条**：
>   1. 精神疾病异质 → 群体分析不足（已知）
>   2. ML + 个体化可填补（预测/解释）
>   3. 但方法选择会影响精度/可解释性/泛化
>   4. 不同选择间有 trade-off（精度 vs 泛化 vs 可解释性）
>   5. 最终决策应由"研究目标"驱动，而非算法潮流
> - **证据类型**：以摘要 + 已发表实证综述（citation堆叠）为主（Review级证据）；几乎无本文自己的原始实验。
>
> **论证缺口/跳跃点（批判）**：
> - 综述主要为**引用证据的汇总**，缺少"方法选择影响大小的量化对照框架"——比如多大样本量才算"足够"？作者只给趋势未给硬性阈值。
> - "functional connectivity 最佳模态"有很多证据，但作者对"结构/扩散在某些疾病中也重要"的占比把控可能是主观平衡。

### 📌 关键标注 (AI Annotation Highlights)

| # | 原文 | 区域 | 批注 |
|---|------|------|------|
| 1 | "Psychiatric illnesses are heterogeneous in nature. No illness manifests in the same way across individuals, and no two patients with a shared diagnosis exhibit identical symptom profiles." | Intro | 【定义】综述出发论据：精神疾病异质性导致群体分析无法捕捉个体差异。【本文角色】论证链条第一环，驱动后文 phenotype selection 和 population-specific models 两节。【延伸】你的个体化预测课题正是这个论点的自然产物。 |
| 2 | "Precision medicine transitions away from the one-size-fits-all model of traditional medicine and seeks to identify the underlying causes of disease and appropriate therapeutic interventions at a patient-specific level." | Intro | 【定义】精准医疗核心定义（NRC 2011）。【本文角色】全文理论底座——从群体诊断转向个体预测。【延伸】你用 fMRI+心跳做 individual prediction，正是 precision psychiatry 的实现路径。 |
| 3 | "Data-driven machine learning analyses can be applied to identify disease-relevant biological subtypes, predict individual symptom profiles, and recommend personalized therapeutic interventions." | Intro | 【定义】三大分析类型：亚型识别(descriptive)→症状预测(predictive)→治疗推荐(prescriptive)。【论证关联】你的分析目标决定你的算法选择——这是后文 algorithm selection 的前提。【延伸】你的课题在 predictive 层面，应优先选回归而非分类。 |
| 4 | "Psychiatric diagnoses categorize clusters of co-occurring symptoms that often lack clear, discernible borders between health and disease." | Intro | 【溯源】Hyman (2010) reification 批判。【本文角色】phenotype selection 节的理论前提——诊断边界模糊→预测维度比预测类别更可靠。【延伸】你的焦虑/内感受指标如果走 dimensional 回归，信号会比 binary classification 更强。 |
| 5 | "Remarkably, there are 636,120 distinct clinical presentations of posttraumatic stress disorder. It is naive to believe that the same neurobiological properties will underlie the unique clinical presentations of a given diagnosis." | Intro | 【攻击点】全文最强的"one size does not fit all"证据句——PTSD 有 63 万+ 种临床表现。【延伸】这个数字可以直接引用到你的 proposal 里，论证为什么不做简单的 case/control 分类。 |
| 6 | "Connectome-based predictive modeling is a data-driven protocol to predict behavior from connectivity data." | Methods | 【方法】CPM (Shen et al. 2017 Nature Protocols)：数据驱动特征选择+线性模型+内置交叉验证。【延伸】如果你用 fMRI 功能连接预测焦虑分，CPM 是你的直接可移植 baseline。 |
| 7 | "Different machine learning algorithms are suitable for distinct predictions, and algorithm selection should consider whether accuracy, interpretability, or both should be prioritized." | Methods | 【立场】全文核心 methodological thesis：不存在最佳算法，只有最适合你目标的算法。【延伸】混合证据表明线性方法在泛化性上往往优于深度学习——选 CPM 而非 CNN 有文献支撑。 |
| 8 | "Individual differences in cognition, personality, and emotional traits, as well as psychiatric diagnoses, are most accurately predicted by functional connectivity." | Methods | 【证据】跨 8+ 研究一致结论：功能连接对个体差异的预测精度优于结构 MRI 和 DWI。【延伸】你的 fMRI 方案选功能连接做特征，本文提供直接引用支撑。 |
| 9 | "Global signal regression is a highly debated method used to remove the effects of global variations in activity from the functional time series of each voxel." | Methods | 【方法争议】GSR 从每个体素时间序列减去全脑均值——去除噪声还是丢失信号？【延伸】大多数行为预测受益于 GSR(引39/62)，但非绝对——你的预处理 pipeline 需明确声明是否做 GSR。 |
| 10 | "Full correlation is a standardized form of covariance. Partial correlation is derived using the inverse of the precision matrix and represents the correlation between a pair of brain parcels after adjusting for the time series of all other parcels." | Methods | 【辨析】三种 FC 计算方式：full(简单协方差)/ partial(排除其他区域后)/ tangent space(黎曼几何，分类精度常最高·引26)。【延伸】默认选 tangent space 有文献支撑——在你的方法部分声明选择理由。 |
| 11 | "Stringent quality control is likely to result in samples that are less representative of the population in terms of age, sex, race, and socioeconomic status and remove meaningful variance in the data." | Methods | 【反直觉】严格 QC 会选择性剔除少数族裔/低 SES/重症患者样本→丧失代表性。【延伸】你的质控阈值需要在"数据干净"和"样本代表性"之间取舍——这是个 trade-off 不是纯技术决策。 |
| 12 | "garbage in, garbage out: If relying on poor phenotypic data and/or labels to train predictive models, the predictions and underlying associations captured are also likely to be of poor quality." | Methods | 【核心警告】MDD/GAD 评定者间信度仅 0.28/0.21(引80)——标签不可靠，模型无救。【延伸】你的 CARED 心跳任务 + 元认知指标的重测信度需要提前报告，这是表型质量的前提。 |
| 13 | "Brain parcellations reduce dimensionality by segmenting the brain into tens or hundreds of regions or networks." | Methods | 【方法】分区降维：减少噪声、降低计算复杂度、增强可解释性——但也丢失体素级信号。【延伸】建议 ensemble 跨分区或 individual-specific parcellation，尤其焦虑/内感受可能存在拓扑个体差异。 |
| 14 | "Normative modeling can be used to model expected variations in a given neuroimaging feature. Deviations from normative models of regional cortical volumes more accurately predict overall and dimension-specific psychopathology than raw measures of cortical volume." | Methods | 【方法创新】规范建模——建正常人群"预期值模型"，标出每个个体的偏离程度——偏离量比绝对值更有预测力(引68)。【延伸】你的心跳元认知+fMRI 可以用 normative 框架做个体异常检测而非简单分类。 |
| 15 | "A meta-matching framework developed to translate predictive models based on neuroimaging features from large samples into nonbrain imaging features in smaller samples has shown promising results." | Methods | 【解决方案】Meta-matching：大样本(UK Biobank)训练的脑-行为映射→迁移到小临床样本→大幅减少所需临床 N。【延伸】你的焦虑样本如果太小，可 borrow UKB/HCP 的基础映射再 transfer。 |
| 16 | "There appears to be a strong negative relationship between accuracy and sample size for diagnostic and behavioral predictions in Alzheimer's disease, depression, schizophrenia, psychosis, and autism." | Results | 【硬核警告】样本量越小→精度估计越膨胀→精度-样本量在整个精神疾病领域呈负相关。【延伸】你的 proposal 必须加入 nested CV + independent test set，这是避免 overoptimistic 的核心防线。 |
| 17 | "Sex-specific predictions of cognition and personality are more accurate and insightful than sex-independent ones." | Results | 【证据】人群特异性模型优于通用模型——性别分层建模揭示独特脑-行为关联。【延伸】焦虑/内感受有已知性别差异，pooling 可能 mask 效应——建议性别分层分析。 |
| 18 | "behavioral prediction models trained on datasets dominated by White Americans may fail to generalize to African American populations." | Results | 【泛化失败】跨种族泛化失败——白人主导样本训练的模型对黑人群体预测偏误。【延伸】intersectionality 提醒：个体可能同时属于多个边缘化群体，模型泛化是系统性而非单变量问题。 |
| 19 | "models with high accuracy and interpretability but low generalizability may offer important insights into brain-behavior relationships in clinical populations but lack clinical utility." | Discussion | 【Trade-off 框架】精度 vs 可解释 vs 泛化三者不可兼得。【延伸】你的研究目标应先明确优先哪两方——机制探索优先解释+精度，临床应用优先精度+泛化。 |
| 20 | "scale development and clinical evaluation. predictive and prescriptive analyses must be clinically evaluated prospectively in appropriately preregistered randomized controlled clinical trials." | Discussion | 【未来方向】两个优先事项：①开发可靠代表性的行为量表 ②前瞻性预注册 RCT 评估。【延伸】你的 proposal Future Directions 可直接引用——任何模型进临床前必须过 RCT。 |

**覆盖区域**: Intro (5条) / Methods (7条) / Results (4条) / Discussion (4条)

> 本节由 Stage 4-5 生成。20 条 AI 标注，每条 ~80-150 字，含 4 层结构（定义/本文角色/论证关联/批判延伸），按区域分配覆盖全文。

### 💡 核心发现

**主要发现**（按重要性排序；每条附 Evidence mapping）

1. **没有"一刀切"的最佳算法——方法选择应由目标/权衡驱动** [Indirect / Review]
   证据：Head-to-head 比较结果"mixed"——KRR/前馈网络/BrainNet/图卷积脑预测精度近似（21），一般线性/弹性网可比或优于深度学习（22），深度学习灰质体积上最强（23）；但核弹如国际自闭症挑战中深度学习更易过拟合（25）。**证据强度：间接（靠综述他文引述）**。

2. **功能连接（functional connectivity）是最佳预测载体** [Indirect / Review]
   多处证据(24/25/27-31)一致表明个体差异(cognition/personality/emotion/诊断)由功能连接预测最好；但结构/扩散在特定疾病（AD、自闭、ADHD、精神分裂）也有预测价值。

3. **数据转换是隐蔽魔障**：Global signal regression、full vs partial correlation vs tangent space、确定性 vs 概率性追踪、颅内体积比例校正，都会影响预测及偏离 [Indirect / Review]
5. **样本量负相关 + 迁移/人群特异性**：小样本 → 过度乐观估计 + 泛化失败 + 精度-样本量负相关（117/120）；而迁移（meta-matching）可消减需求；人口分组模型（性别特异性、跨种族泛化失败）需要 intersectionality 考量 [Indirect / Review]。

6. **可解释性 vs 精度 vs 泛化的三难**：高精度+可解释+低泛化 = 有洞见但无临床实用；高精度+高泛化+低可解释 = 临床有用但难辅助决策 [Theoretical / Review]。

**理论意义**
- 把精准精神病学的核心难题从"选算法"重新定义为"**综合权衡多个方法学术语**"。
- 强标题"One Size Does Not Fit All"本身就是一个理论立场：个体化模型的泛化瓶颈在于样本选择与方法选择，而非单靠算法升级。

**局限性**
- 作者自评：综述为主观综合，无统一量化基准；缺乏"每种选择影响幅度/效应量"的系统 meta-analysis。
- 批判性评估：部分主张是"混合证据"，作者未量化"cross-validation直接决定算温 fed"的程度；某些"最佳"结论过度依赖特定数据集（如公开整合池）。
- 【反驳/疑问】：作者对"需要多大样本量"给不出硬阈值，且 major reliance on总结性引用（citation）而非元分析——因此本文是"概念地图"而非"操作手册"。

### 🔗 与你领域的关系

**直接关系（落地到你的具体课题）**：

| 本文概念 | 你要借鉴/落地 | 对应你的 Phase |
|---------|--------------|----------------|
| 精准人文/预测建模 | 你的 fMRI + 心跳(CARED) + 元认知 → 个体化焦虑预测 | Phase 1-2 |
| CPM / 功能连接作特征 | 用功能连接 + 心跳内感受正向特征联合预测症状 | Phase 2 |
| 样本量负相关教训 | 避免小样本过拟合；用人群(GAD→healthy) 迁移/跨数据集验证 | Phase 2 |
| Cross-validation / 过拟合 | 你 MCI/ROC 分析时用 nestedCV 防信息泄漏 | Phase 2 |
| population-specific 模型 | 性别分层，但注意 intersectionality——不要过拟合单一人群 | 数据/分析策略 |

**可引用的 proposal 段落（英文）**：
> "As highlighted by Dhamala et al. (2023), predictive models based on neuroimaging must carefully consider how methodological choices—such as feature definition, sample size, cross-validation and population specificity—shape both the accuracy and the generalizability of the results. Accordingly, our analytic pipeline adopts leave-one-out or nested cross-validation with explicit evaluation on held-out / independent data to guard against the over-optimistic estimates that plague undersourced small-sample neuroimaging models."

> "The heterogeneous nature of psychiatric illness (Hyman, 2010) and the promise of individual-level precision psychiatry (Vieta, 2015) motivate data-driven, participant-specific prediction rather than one-size-fits-all classification. We therefore predict a dimensional metric of interoceptive-anxiety regulation, rather than a group diagnostic label."

### ⭐ 为什么这篇重要

这份综述把"为何个体化建模、为何每种方法选择不可大意"讲得最系统，是你 proposal 的**理论根据地与方法论**（直接支撑你要做的 fMRI 个体水平预测）。② 它直接指出了你 Phase 2 的"大坑"——小样本过拟合与跨样本泛化失败——你可以用它的框架引入交叉验证、人群验证。它是⚔️精兵强将：兼具理论奠基 + 方法借鉴双重价值。

### 📄 原文摘要

> Psychiatric illnesses are heterogeneous in nature. No illness manifests in the same way across individuals, and no two patients with a shared diagnosis exhibit identical symptom profiles. Over the last several decades, group-level analyses of in vivo neuroimaging data have led to fundamental advances in our understanding of the neurobiology of psychiatric illnesses. More recently, access to computational resources and large, publicly available datasets alongside the rise of predictive modeling and precision medicine approaches have facilitated the study of psychiatric illnesses at an individual level. Data-driven machine learning analyses can be applied to identify disease-relevant biological subtypes, predict individual symptom profiles, and recommend personalized therapeutic interventions. However, when considering these predictive models, methodological choices must be carefully considered to ensure accurate, robust, and interpretable results. ... An understanding of these effects is essential for the proper implementation of predictive models in psychiatry.

### 行动计划 (Action Plan)

- [ ] 把你 Phase 2 的 fMRI + 心跳(interoception) 预测模型的流程，按本文的 Check"method-choice"框架重新审视（算法→转换→分区→样本量→人群）
- [ ] 在 proposal 的 Method 一节加入一条"避免小样本过拟合，加入嵌套/leave- 交叉验证"的方法学声明
- [ ] 决定你的预测目标用**维度**（症状分/内感受）而非诊断，呼应本文"离散 vs 维度"之争
- [ ] 若采用功能连接特征：明确选用 full/partial correlation / 或 tangent space，说明理由