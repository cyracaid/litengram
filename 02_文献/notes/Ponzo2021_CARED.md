# 📖 Interoception & Metacognition 文献精读 — 2026-07-13

## 关键词: interoception, CARED task, interoceptive awareness, metacognition, ROC-AUC, ecological momentary assessment

## Measuring Interoception: The CARdiac Elevation Detection Task

### 📋 基本信息

- **重要等级**: ⚔️精兵强将
- **论文类型**: Empirical
- **阅读策略**: Standard
- **第一作者**: Sonia Ponzo | Huma Therapeutics Ltd., London
- **通讯作者**: David Plans
- **发表**: 2021 | Frontiers in Psychology
- **DOI**: 10.3389/fpsyg.2021.712896
- **Zotero**: `C5WAAYXR` | **PDF**: `96JGGS5Q` | **笔记**: `TOMXVWCX`
- **引用**: ~150+

### 📚 研究背景

**已知 (Known)**

- 内感受 (interoception) 与精神健康密切相关，有学者称其为精神病理学的 P 因子 (Caspi et al., 2014; Barrett & Simmons, 2015)
- 然而，现有任务的测量学效度存在问题：HCT (Schandry, 1981) 可能依靠静息心率知识估算而非真实感知；HDT (Whitehead, 1977) 仅用两个延迟条件，忽略个体差异；MCS/6AFC 精确度高但需要实验室环境，不适合临床

**知识缺口 (Knowledge Gap)**

- 上述任务都仅在一种生理唤醒状态（通常是静息态）下测量内感受
- Jones & Hollandsworth (1981) 和 Schandry et al. (1993) 的证据表明心动力与内感受准确性存在个体内共变——一个人在静息时的能力不一定能预测其他状态下的表现
- 缺乏能随时间、在生态化条件下持续测量内感受的任务
- 现有任务只测量准确性 (accuracy)，缺少对内感受注意力/敏感性维度的捕捉

**研究目标 (Research Aim)**

- 开发一种生态效度高、可远程部署的 CARdiac Elevation Detection (CARED) 任务，在 4 周时间内持续采样，覆盖日常心率波动范围，同时捕获准确性 + 注意力 + 元认知觉知

### 🧠 理论背景

**核心理论框架**

- Garfinkel 三层次模型 (Garfinkel et al., 2015, *Biological Psychology*)：内感受分为准确性 Accuracy（客观行为表现）、敏感性 Sensibility（主观自评倾向）、觉知 Awareness（元认知层面——你知道不知道自己的判断准不准）
- Murphy 2×2 模型 (Murphy et al., 2020)：内感受的结构可能是"准确性 × 注意力"的 2×2 因子结构

**关键概念**

- **内感受 (Interoception)**：感受自身身体内部状态的能力 (Craig, 2002)。区别于外感受 (exteroception，视觉/听觉) 和本体感觉 (proprioception，身体位置/运动)
- **元认知 (Metacognition)**：个体对自己认知过程的认知。在本文中具体指：被试是否知道自己的内感受判断准不准 → 通过信心评分与正确性的匹配度来量化
- **自适应采样 (Adaptive Sampling)**：通知概率与心率的经验频率成反比——罕见 HR 值获得更高的采样概率，确保数据覆盖全范围。标准静息态测量好比"只在停车场测一辆车的性能"，CARED 的自适应采样则是在"高速公路、山路、市区拥堵路段都测一遍"

**理论→本研究的逻辑链**

```
Garfinkel 三层次模型 (2015) 提出 accuracy / sensibility / awareness 可分离
  ↓
但现有任务 (HCT/HDT/MCS) 只能在实验室一次测量，无法分离这些维度
  ↓
CARED 通过 4 周日常采样 + 信心评分，同时捕获 accuracy 和 awareness
  ↓
首次在生态化条件下检验三维模型的适用性
```

### 📎 关键引用

- **Garfinkel et al. (2015)** 🏛️理论基石
  内感受三维模型 (accuracy/sensibility/awareness) 的原始出处，发表于 Biological Psychology。
  → 本文整个测量框架建立在这三维之上，CARED 就是要同时抓 accuracy + awareness 两维。

- **Schandry (1981)** 🎯批判靶子 / 🔧方法来源
  心跳计数任务 (HCT) 的原始范式——让被试默数心跳。
  → 本文既借它当内感受测量的传统起点，又批判它：被试可能靠静息心率知识估算而非真实感知。

- **Desmedt et al. (2018)** 📊数据支撑
  实证发现 HCT 即便加控制条件仍掺入大量非内感受过程。
  → 本文引它作为"旧任务测量学效度有问题"的关键证据，替 CARED 的必要性铺路。

- **Murphy et al. (2020)** 🏛️理论基石
  提出内感受可能是"准确度 × 注意力"的 2×2 因子结构。
  → 本文是这个 2×2 模型的一次实证检验，决定了 CARED 为什么同时收准确度和注意力数据。

- **Caspi et al. (2014)** 🏛️理论基石
  精神病理学 P 因子（共同潜在因子）的原始文献，发表于 Clinical Psychological Science。
  → 本文用它论证内感受障碍的跨诊断性质，是 CARED 临床应用价值的底层逻辑。

（说明：⚔️级写 4-6 条承重引用，以上 5 条覆盖全部核心论证支柱。）

### 🔬 研究方法

**被试 (Participants)**
- N=30 健康成人（16 名女性；年龄 18-51, M=27.43, SD=9.01）
- 原始招募 52 人，attrition 22 人 (42%)：10 人收到设备前失联，12 人退出
- 排除标准：怀孕、精神/神经疾病诊断

**实验设计 (Experimental Design)**
- 4 周生态瞬时评估，每日 ≤ 6 次通知
- 通知算法：自适应概率 P = 1.67% × (段内总测量数 / 段内该桶测量数)
- 被试每次回答：心率是否比平时快 (Yes/No) + 信心评分 (1-10) + 前 30分钟活动描述
- 三种内感受维度同时收集：准确性 (Mann-Whitney U 效应量)、觉知 (ROC AUC)、敏感性 (BPQ 问卷)

**实验流程 (Procedure)**
1. 基线日：填写 IAS、BPQ、STAI-6、DASS-21、WEMWBS 问卷，佩戴 Lifesense Band 2
2. 4 周日常采样：9:00-21:00 自适应通知，每日平均 ≤ 6 次
3. 质控：排除高强度活动/情绪相关试次（如运动、"stressed"、"upset"等）
4. 结束：取下手环，数据导出

**数据分析 (Data Analysis)**

- 内感受准确性：每位被试独立进行 Mann-Whitney U 检验，效应量 ES = (一致对数 - 不一致对数) / 总对数，p < 0.05 → 分类为 interoceptive
- 内感受觉知/元认知：个体水平 ROC 分析，AUC 指标，单样本 t 检验 vs 理论值 0.5
- 主客观关联：IAS × 效应量、BPQ × 效应量的 Pearson 相关
- 探索性分析：DASS-21, WEMWBS, BMI 与效应量的相关

> **WHY 分析**：
> 为什么用 U 检验？（1）数据非均匀采样——自适应通知算法故意不随机，t 检验的均值比较会被扭曲；（2）心率数据天生右偏；（3）对极端异常值稳健；（4）直接对应假设。
> 为什么用 ROC AUC 而不是 meta-d'？本文是探索性工作，AUC 更简单直观，meta-d' 需要更多试次数。
>
> **统计完整性**：
> [x] 效应量报告（U 检验效应量 + AUC）
> [x] 置信区间（AUC 有 CI）
> [ ] 多重比较校正——探索性分析未校正，属可接受范围
> [ ] 先验功效分析——未报告
> [ ] 预注册——未预注册
> [x] 原始数据可用性——有补充材料

### 💡 核心发现

**主要发现**

1. **内感受准确性 — 1/3 被试为 interoceptive** [Direct / Empirical]
   9/30 获得 p < 0.05，与 Brener & Ring (2016) 的经典比例一致。

2. **元认知觉知 — 整体 AUC 显著 > 0.5** [Direct / Empirical]
   M = 0.58, SD = 0.09, t(29) = 4.96, p < 0.001
   26/30 信心预测正确性方向正确。
   但 4/30 呈反向元认知（AUC < 0.5）——越自信越错，可能对应 (a) 错误线索归因、(b) Dunning-Kruger 式元认知盲点、(c) 高焦虑躯体过度警觉、(d) 任务策略翻转。

3. **主客观分离 — 无显著相关** [Direct / Empirical]
   IAS × 效应量、BPQ × 效应量均 n.s.，支持 Murphy et al. (2020) 成分分离模型。

4. **精神健康关联 — 无显著发现** [Indirect / Empirical]
   可能因健康样本的组间变异太小。📘（健康样本中常见 null）

**理论意义**
- CARED 是首个生态采样型内感受任务，支持多维模型在生态条件下的可分离性
- 反向元认知亚组（4/30）值得深入——可能在焦虑/抑郁患者中比例更高

**局限性**
- N=30 太小，无法区分 interoceptive vs non-interoceptive 进行 AUC 组间比较
- 阈值法 (mean + 1SD) 而非无阈值法 (如 meta-d')，元认知精度受限
- 42% attrition 率——连续佩戴 4 周的依从性挑战
- 作者声明为"初步证据"(proof of concept)，需更大样本验证

### 🔗 与你领域的关系

**直接连接**：
1. **元认知方法**: CARED 用 ROC/AUC → 直接对应你 Phase 2 的 MCI 设计
2. **内感受 × 情绪**: 本文讨论内感受障碍与精神病理学的关联 → 你关心 anxiety/depression 中的内感受元认知失调
3. **EMA + 生态采样**: CARED 与 CAD Lab 的 14 天 EMA + Garmin 手环设计本质相同
4. **Garfinkel 框架**: 本文的核心理论框架也是你的 proposal 核心

**你的 Phase 2 与本文的关系**：
```
Ponzo (2021) — CARED: 信心评分 → ROC → AUC（群体水平元认知）
  ↓
你的 Phase 2: 信心评分 → ROC → AUC + MCI + 情绪调节 + 临床组比较 + HEP/EEG
```

**可引用的 proposal 段落**：
> "Ponzo et al. (2021) demonstrated that ecological sampling of interoceptive judgments with confidence ratings can yield reliable metacognitive indices (AUROC). However, their small healthy sample (N=30) precluded examination of individual differences in metacognitive calibration."

### ⭐ 为什么这篇重要

中等优先级的方法论文献。概念创新突出（自适应采样 + 生态化 + 信心评分），但统计验证仍处早期。对你的价值在于：(1) 提供了 ROC/AUC 分析元认知的完整技术路线；(2) 暴露了当前生态采样的局限；(3) 论证了内感受元认知失调可能是情绪障碍的跨诊断机制。

### 📄 原文摘要

> Interoception has increasingly been the focus of psychiatric research, due to its hypothesized role in mental health. Existing interoceptive tasks either suffer from important methodological limitations, impacting their validity, or are burdensome and require specialized equipment, which limits their usage in vulnerable populations. We report on the development of the CARdiac Elevation Detection (CARED) task. Participants' heart rate is recorded by a wearable device connected to a mobile application. Notifications are sent to participants' mobile throughout the day over a period of 4 weeks. Participants are asked to state whether their heart rate is higher than usual, rate their confidence and describe the activity they were involved in when the notification occurred. Data (N = 30) revealed that 1/3 of the sample was classified as interoceptive and that participants presented overall good insight into their interoceptive abilities. Given its ease of administration and accessibility, the CARED task has the potential to be a significant asset for psychiatric and developmental research.
