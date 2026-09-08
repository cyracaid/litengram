# Research Profile — CAD Lab

> 最后更新: 2026-08-03
> 用途: LitEngram 维度 4 战略嫁接的目标锚点。每篇论文的"与你研究的关系"必须落到以下具体 Phase/RQ。

## Current Projects

### Phase 1: Multi-Coil fMRI Pooling — 方法学综述
- **问题**: 在同一台 Siemens 扫描仪上混用 20ch 和 32ch 头线圈采集的 fMRI 数据，能否在统计上安全地合并分析？
- **当前方法**: PI-level evidence review (7 篇关键文献)，三场景分析（同扫描仪部分阵列 / 多中心不同线圈 / 纵向混合线圈），三层统计方案（Minimal / Recommended / Gold-Standard）
- **数据**: 已有扫描数据（混线圈），需 ROI-specific tSNR 协变量和 traveling-subject 验证
- **瓶颈**: 需要实证验证 — 目前停留在理论/综述层面，缺实际数据的 cross-coil reliability 分析

### Phase 2: 内感受元认知的个体化预测模型
- **问题**: 能否从 fMRI 功能连接 + 心跳检测任务（CARED）+ 元认知校准指标，构建个体化的焦虑/内感受失调预测模型？
- **计划方法**: 
  - fMRI: 功能连接特征 (tangent space representation)，CPM / 弹性网预测
  - 行为: CARED task (心跳升高检测 + 信心评分) → AUROC 元认知指标
  - 统计: nested cross-validation，性别分层，迁移学习（借用 UK Biobank 基础映射）
- **预期数据**: 临床焦虑样本 + 健康对照，Garmin 手环 + EMA 生态采样
- **开放问题**: 
  - 样本量可能不够（焦虑临床组难招募）→ meta-matching / transfer learning 是否可行？
  - 功能连接计算参数（full/partial/tangent space，GSR yes/no，分区方案）需预先声明
  - 预测目标：走维度（焦虑症状分连续值）还是分类（case/control）？

### Pilot: 多模态自我叙事视频的隐私安全标记
- **问题**: 能从简短自我叙事视频中提取不包含原始身份信息的多模态特征（声学/面部/语言），关联抑郁/焦虑症状和内感受觉知？
- **当前方法**: 标准化提示（压力身体感/困难日/内感受变化/中性日常），PHQ-9 + GAD-7 + MAIA/BPQ
- **数据**: 拟招募，尚未开始
- **瓶颈**: IRB/DRC 审批，数据隐私保护协议

## Research Questions

- **RQ1**: 混线圈 fMRI 数据在 ROI 级别上的 tSNR / 功能连接 / 预测精度的差异是否在可接受范围内？（Phase 1）
- **RQ2**: 功能连接特征是否优于结构/扩散特征，用于预测个体焦虑症状维度分？（Phase 2 + Dhamala 2023）
- **RQ3**: 心跳元认知准确性（AUROC）是否能作为内感受失调的个体差异标记，且独立于主观内感受敏感性？（Ponzo 2021 → Phase 2）
- **RQ4**: 威胁迫近度分段分析（pre-encounter / encounter / post-encounter）是否能提高焦虑效应的 fMRI 检测灵敏度？（Abend 2023 → Phase 2）

## Current Hypotheses

- **H1**: 经过 ROI-specific tSNR 协变量校正后，20ch 和 32ch 数据在皮层下区域（纹状体/杏仁核）可以安全合并，但在背外侧前额叶需要独立建模或排除
- **H2**: 心跳元认知（AUROC）与焦虑症状分存在负相关——即越焦虑的人越不能准确判断自己的心跳状态（反向元认知）
- **H3**: fMRI 功能连接 + 心跳元认知的双模态特征组合，在预测焦虑分时优于任一单模态

## Existing Datasets

| 数据集 | 类型 | 状态 | 关键变量 |
|--------|------|------|----------|
| CAD Lab multi-coil fMRI | 静息态 + 任务态 fMRI (20ch + 32ch) | 已采集，待分析 | 头线圈型号，tSNR，功能连接矩阵 |
| CAD Lab behavioral | 临床量表 | 伴随采集 | 焦虑/抑郁/内感受问卷 |
| UK Biobank (外部) | 静息态 fMRI + 行为 | 可获取 | 用于 transfer learning / meta-matching |

## Experimental Pipeline

- **Phase 1**: 多线圈数据 → 预处理 (motion correction + GSR decision) → ROI-wise tSNR → 统计比较 → 综述发表
- **Phase 2**: 临床被试 → CARED 心跳任务 + 静息态 fMRI → 功能连接 (tangent space) → CPM 预测 → nested CV → 焦虑分预测 + 元认知校准
- **Pilot**: 招募 → 自我叙事视频录制 → 多模态特征提取（声学/面部/语言）→ 隐私加密 → 回归分析（PHQ-9/GAD-7/MAIA）

## Core Theoretical Frameworks

- **Garfinkel 三维内感受模型** (2015): Accuracy / Sensibility / Awareness 可分离 — Phase 2 的测量学基石
- **Murphy 2×2 内感受因子模型** (2020): Accuracy × Attention 交叉 — CARED 同时收两维的理由
- **Precision Psychiatry** (Vieta 2015 + Dhamala 2023): 个体化预测代替一刀切诊断 — 整个 Phase 2 的哲学底座
- **Threat Imminence Continuum** (Fanselow, Mobbs): 焦虑症状按迫近度分段 — Phase 2 的分析策略启示

## Open Problems

1. 临床焦虑样本量不足 — meta-matching 真的靠谱吗？需要验证
2. GSR yes/no 在焦虑人群中是否有特殊影响？焦虑本身与全脑信号波动有关
3. 功能连接定义 (full/partial/tangent) 和分区方案的选择 — 目前倾向 tangent + ensemble parcellations，但需要预注册声明
4. 交叉验证策略 — nested CV vs leave-one-out，在 N<50 下哪种更 honest？
5. CARED 任务在韩国人群中的可行性 — 目前只有英国样本 (Ponzo 2021 N=30)

## Current TODOs

- [ ] 完成 Phase 1 综述的 empirical evidence 部分（真实数据分析）
- [ ] Phase 2 的分析 pipeline 预注册 — 明确 GSR/分区/连接定义/交叉验证策略
- [ ] 在 proposal 中引用 Dhamala 2023 的方法论选择框架作为 justification
- [ ] 建立 research_profile.md → 这是后续所有维度 4 嫁接的目标文件
