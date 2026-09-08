# 📖 NLP 可解释性·可靠性 文献精读 — 2026-08-19

## 关键词: Knowing-Saying Gap, Linear Probing, Failure Prediction, Confidence Collapse, 探针编码≠输出利用

## The Knowing-Saying Gap: When Probes See Errors that Confidence Misses

### 📋 基本信息

- **重要等级**: ⛰️ 镇山之宝（"信息在那里读数没有"教科书级解离 + 严谨方法模板）
- **论文类型**: Empirical
- **domain**: nlp（cs.AI 可靠性·可解释性）
- **阅读策略**: Deep
- **第一作者**: Jyotin Goel*, Ipshita Bandyopadhyay*, Justin Shenk
- **通讯**: jyotinofficialcc@gmail.com
- **发表**: 2026 | arXiv:2608.07528v1 [cs.AI] 21 Jul 2026
- **venue**: arXiv:2608.07528
- **DOI**: 无 | **arXiv**: 2608.07528
- **代码**: 待核（数据集确定性 seed 42 生成可复现）
- **PDF**: ~/Documents/CAD/2608NLP/pdf-inbox/2608.07528.pdf
- **引用**: 新

### 📚 研究背景

**已知 (Known)**: 线性探针广泛用于提取激活中的结构/语义（syntax Hewitt-Manning, truthfulness Burns/Marks, refusal Arditi）。Elicited confidence / CoT self-critique / 结构化验证预测可靠性（Kadavath, Xiong, Weng）。CoT 可不忠实（Turpin, Lanham, Paul）。

**知识缺口 (Gap)**: 无人干净分离"**成功探测内部状态**"vs"**成功预测行为**"——两者常被混为一谈。CoT 不忠实有正面解码结果缺失；verbalized confidence 被当成"带噪声定量"而非"分类失准"。

**研究目标 (Aim)**: 用对比式探针验证：LLM 已**线性编码**相关事实（检测损坏 AUROC>0.98）但该信息**不传播到输出或行为**（失败预测、表面置信、行为全部失效）——即"knowing but not saying"解离。

### 🧠 理论背景

- **框架**：对比式探针（contrastive probing）——clean vs corrupted context 仅差注入错误，共享 question/hop 结构，控制难度/结构混淆。
- **核心概念**: knowing-saying gap（知-说鸿沟）；detection vs failure-prediction 解离；confidence collapse（结构化信心塌缩成二值）；coT 不忠实=输出层不咨询中间信号。
- **方法**: 线性探针（residual stream）；AUROCdetect vs AUROCfail 双指标；六种表面不确定性信号对照；三种探针触发干预策略；预注册假设（persistence beats peak）。

### 📎 关键引用

- **Burns 2023 / Marks & Tegmark 2023 / Arditi 2024** 🔧方法来源 — 线性探针提取真理/拒绝（前身）。
- **Hewitt & Manning 2019** 🔧方法来源 — 线性探针句法。
- **Kadavath 2022 / Tian 2023 / Lin 2022 / Xiong 2024** 🎯批判靶子 — elicited confidence（假设内部状态可经口头输出访问——本文证伪）。
- **Turpin 2023 / Lanham 2023 / Paul 2024** 📊数据支撑 — CoT 不忠实（本文给出正面解码）。

### 📌 关键标注

| # | 原文区域 | 批注 |
|---|------|------|
| 1 | §5: AUROCdetect>0.98 但同探针 AUROCfail 近 chance (0.49-0.53) | 【定义】detection-failure dissociation。【本文角色】核心解离。【论证关联】**"信息在那里(编码0.98)读数/行为没有(失败预测0.5)"最干净实证**——直接作为项目核心命题的教科书先例。 |
| 2 | §5: 表面信号六种无一>0.70; peak entropy=0.500 | 【定义】verbalized confidence 分类失准（非噪声）。【本文角色】口头通道不可靠。【论证关联】"读数(口头信心)读不出"——支撑项目对 readout 的怀疑。 |
| 3 | §5 行为沉默: 258 traces 零 hedging/零 overconfident, 不用结构化信心 | 【定义】behavioral silence。【本文角色】模型自信流畅地错。【论证关联】fluency without fidelity——部署场景"信息在那里但表面完全看不见"。 |
| 4 | §5: CoT 开启→精度 27.9%→1.2% 但探针编码不变(∆-0.001) | 【定义】encoding persists, output channel disrupted。【本文角色】单变量 ablation。【论证关联】**"表征保持、读出口坏掉"的最强单变量证据**——项目"信息在那里读数没有"机制支撑。 |
| 5 | §K 预注册 "persistence beats peak" 证伪 | 【定义】探针跨 hop 持久性不预测失败。【本文角色】诚实报告证伪。【论证关联】提醒：测"信号存在"≠测"信号有用"——项目 CSA 情感探针要测行为预测力而非仅在性。 |
| 6 | §5: substitute 编码非近因: probe fires 96-100% 但 replace-prior 只救 32-39% 正确 | 【定义】编码存在≠行为近因。【本文角色】干预局限。【论证关联】处理相关性不强特征时应测因果干预，防误判"信息"为"机制"。 |
| 7 | robust: base-problem-grouped CV + leave-one-error-type-out | 【定义】防 fold leakage + 防类型表面签名。【本文角色】严谨控制。【论证关联】项目复现解离时应照搬这两层鲁棒对照。 |

### 🔬 研究方法

> domain=nlp → nlp 版

**任务定义 (Task)**: 多跳算术链（2-4 hops）中静默损坏上游上下文，检测损坏 vs 预测最终正确性。
**数据集 (Data)**: 1,400 traces / 500 base problems；5 错误类型(off_by_one/wrong_operator/wrong_unit/magnitude_error/wrong_percentage_base)；确定性 seed 42 生成，无人工标注/无 LLM 参与。
**模型架构**: Qwen2.5-3B-Instruct, Qwen3-4B(standard+thinking), Llama-3.2-3B-Instruct, Llama-3.1-8B-Instruct；bf16 冻结权重，探针是唯一学习组件。
**训练细节**: 探针训练于冻结模型激活；对比式嵌入（clean vs corrupt 仅差嵌入 hop-0 答案）；3 条件/problem（Clean, Error-standard, Error-verbalized）。
**评测 (Eval)**: AUROCdetect（检测注入）vs AUROCfail（预测错误）双指标；六表面信号；三种干预（branch-and-pick/reprompt/replace-prior）；base-problem-grouped CV + leave-one-error-type-out 鲁棒对照。

**AI 实验设计检查点 (Experiment Design)**:
```
· 对比式探针：同问题 clean vs corrupt 共享结构 → 探针无法靠学难度糊弄
· 单变量 ablation：thinking vs standard 仅差 CoT 模板 (同权重)
· 预注册假设：persistence beats peak（如实报告证伪）
· 三层鲁棒：base-problem-grouped CV(防泄漏) + leave-one-error-type-out(防类型签名) + last vs mean pooling
· 干预对照：三种策略 × 错误类型 × 跨模型
· 表面信号对照：六种(UQ基线)全部近 chance
· ℓ=0 last-token=0.500 → 信号来自计算非token身份
```

> **WHY 分析（层 2）**:
> - 为什么多跳算术？生产 agentic 循环核心失效模式的可控隔离，表面形式固定。
> - 为什么对比式而非普通探针？排除"探针靠学难度/结构"混淆——同问题对仅差注入错误。
> - 为什么双 AUROC？区分"能不能检测到损坏(编码)"与"能否预测失败(行为)"——这是论文的命门解离。
> - 为什么预注册？防事后合理化——"persistence beats peak"证伪是诚实信用的体现。
>
> **检查清单（nlp 评测公平性）**:
> [x] 基线公平：六表面信号对照 + 对比式配对
> [x] 多次运行：2 家族 × 5 模型
> [x] 消融完整：thinking/standard 单变量 + 三层鲁棒
> [x] 显著性：AUROC + 置信；pre-registered
> [x] 数据：确定性生成，无泄漏(分组CV)
> [ ] 失效模式：样本少时 error-type 切分(9-16/slice) 探索性(作者自认)

### 💡 核心发现

**主要发现 (Main Findings):**

**发现 1 — 探针检测损坏但预测不了失败（core dissociation）**
- AUROCdetect >0.98（best 0.997 Llama-3.1-8B）vs 同探针 AUROCfail 0.49-0.53 近 chance。探针在最佳检测层"看到"错误但无法用同一编码预测最终答案。
- **证据强度**: Direct | **证据来源**: Empirical

**发现 2 — 表面信号近 chance + 行为沉默**
- 六种表面不确定性无一 >0.70（peak entropy 0.500）；258 traces 零 hedging、零 overconfident、不用结构化信心。口头通道完全不可靠。
- **证据强度**: Direct | **证据来源**: Empirical

**发现 3 — CoT 扰乱输出通道但不改变编码**
- Qwen3-4B thinking 开启→错误条件精度 27.9%→1.2%（~5× tokens）但探针编码 ∆=-0.001——编码持续、输出坏掉。
- **证据强度**: Direct | **证据来源**: Empirical（单变量 ablation）

**发现 4 — 无单一干预主导，需模型/错误类型感知路由**
- branch-and-pick 唯一严格非破坏（Llama 救4破0）；replace-prior 破对≈救错；replace-prior per-type 强异质（wrong_unit +37.5% vs wrong_percentage_base -18.2%）。
- **证据强度**: Indirect（探索性，样本少） | **证据来源**: Empirical

**SOTA vs 本文 vs 基线（双 AUROC，Table 3）**:

| 模型 | AUROCdetect(best layer) | AUROCfail | Best surface |
|------|------|------|------|
| Llama-3.2-3B | 0.985 | 0.49 | 0.574 |
| Llama-3.1-8B | 0.993/0.997(mean) | 0.53 | 0.622 |
| Qwen2.5-3B | 0.994 | 0.51 | 0.587 |
| (Qwen3-4B thinking 反转 <0.5) | — | — | 0.308 |

**理论意义**: 探针成功编码内部状态**不是**行为可预测性保证——两者是独立通道。fluency without fidelity 是部署可靠性核心问题。verbalized confidence 是"分类失准"（二值化 plausibility filter）而非带噪定量。

**局限性 (Limitations)**: 单任务域（多跳算术，非开放生成）；03-8B 规模；忽略 recall 限制；错误类型切分样本少（9-16/slice）探索性；thinking 模式仅 1 模型。

### 📏 复现性

```
**代码**: 待核（确定性 seed 42 1400 traces 可复现；5 模型 open-weight 可下载）
**数据**: 1400 traces 确定性生成，无人工标注/LLM 参与 → 完全可复现
**算力**: 推理级 + 探针训练（轻）；5 模型需中等 GPU（8B 内）
**复现核对**: 表格可复现；需对齐对比式配对/双AUROC/三层鲁棒协议
**种子/超参**: seed 42；对比式嵌入；AUROC 双目标
**接口可用性**: 开源模型 + 自建数据集
```

> 判断门槛：**"最贵的一步？"** 5 模型推理 + 探针训练均轻量。**对本项目：这是最可移植的"探针编码 vs 行为预测"双 AUROC 模板**——项目若测"CS 情感探针能检测(编码)但预测不了情感行为(读出口)"，直接套这套对比式 + 双指标 + 鲁棒对照。

### 🔗 与你领域的关系

- **直接对齐**：这是本项目核心命题"**信息在那里，读数没有**"的字面实证——探针 0.98 编码损坏（信息在）但失败预测 0.49/表面置信 0.5/行为零 hedging（读数没有）。
- **可借用的具体方法（战略嫁接）**:
  - **[🔧 方法] 双 AUROC 解离框架**：AUROCdetect（信息编码）vs AUROCfail（行为读出）——把"信息在那里读数没有"操作化为两个可测指标，这是项目最需要的量化模板。
  - **[🔧 方法] 对比式探针设计**：clean vs corrupt 仅差注入，控制难度——测 CS 情感时同理配对。
  - **[📊 先例] 编码持续、输出坏掉**（thinking 单变量）：直接支持"表征保持、读出口坏"的机制主张。
  - **[🔧 方法] 三层鲁棒对照**（分组 CV + leave-one-type-out + 双 pooling）——项目复现必备。
  - **[⚠️ 警示] 探针能测"存在"≠能测"有用"**：项目要么测行为预测力(AUROCfail)，要么做因果干预，别只看探针 AUROCdetect——否则会误判"信息在那里"为"机制关键"。
- **可引用的引述段落（英文）**:
  > "The model has linearly encoded the relevant fact about its context, but that information does not propagate into its verbal outputs or downstream behaviour." (this paper)
  > "successful probing of state does not entail success at predicting behaviour" (Related work)
  > "the encoding persists while the output channel is disrupted" (§5, thinking mode)
- **方法学关联（四篇互补）**:
  - 2607.15495 (J-lens)：输入层视角（能否 verbalize）
  - 2411.08745 (patching)：干预视角（语言/概念分层）
  - 2604.19974 (SAE 解离)：特征群体视角（哪类惰性/必需/有害）
  - 2608.07528 (Know-Say gap)：**指标视角（编码 AUROC vs 行为 AUROC 双测）** ← 项目量化"信息在 vs 读数没有"最直接
  - 四篇构成完整工具箱：**探针(2608) + 特征(2604) + 干预(2411) + 工作空间(2607)**

### ⭐ 为什么这篇重要

如果说项目命题是"信息在那里，读数没有"，这篇给出**最精确的操作化度量**（双 AUROC 把"信息在哪"和"读数没有"拆成两个可测数字）+ 最干净的实证（0.98 vs 0.5）+ 最严谨的对照（对比式 + 预注册证伪 + 三层鲁棒）。同时警示"探针能测存在≠测有用"，避免项目陷入探针生态效度误区。⛰️ 级，几乎必引。

### 📄 原文摘要

> "Linear probes detect corrupted context in language models with near-perfect accuracy, yet this does not translate into reliable failure prediction. The result is a dissociation with direct implications for deployment monitoring. Across multi-hop arithmetic chains, probes that detect corruption turn out to be uninformative about final answer correctness; models forced into structured confidence formats collapse to two values with indistinguishable error rates; and probe persistence across hops fails to separate correct from incorrect outcomes, refuting our pre-registered 'persistence beats peak' hypothesis. This pattern of knowing but not saying generalises across model families including reasoning models. As a real-time monitor, probe-based interventions are sharply model and error-type dependent: branch-and-pick is net-positive across models and uniquely non-breaking on Llama-3.1-8B, while reprompt and replace-prior break correct traces at roughly the rate they rescue wrong ones. Probe-based monitoring is a necessary complement to verbalised confidence, but no single intervention dominates, and the deployable answer is model-aware, error-type-aware routing."
> （正式入库锁定 Zotero abstractNote）
