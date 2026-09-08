
# MRI 头线圈通道数差异与跨中心 fMRI 可合并性
### 面向焦虑与抑郁临床神经影像研究的方法学综述

**文体:** CAD 实验室内部 PI 备忘录
**日期:** 2026-07-20
**状态:** 在完成引文审计后,对前一版头线圈综述的重写。以下每一条引文在撰写时均已对照 PubMed / 出版方记录或厂商官方文档核实。凡文献无法回答之处,均明确说明,而非以外推填补。

**从审计中保留的两处更正(以下不再重复):**
- 前一版将 Panman 等 2019 引作 *NeuroImage* 2019;186:412–420。**正确引文:*Frontiers in Neuroscience* 2019;13:729,doi:10.3389/fnins.2019.00729。**
- 前一版将 Kaza 等 2011 引作 *JMRI* 34(3):552–562,doi:10.1002/jmri.22644。**正确引文:*JMRI* 34(1):173–183,doi:10.1002/jmri.22614。**

全文使用如下约定:**【已证实】** = 已在已发表的实证研究中显示;**【推断】** = 基于 MRI 物理可预期,但未针对本情形直接测量;**【无直接证据】** = 文献未涉及。

---

## 1. 临床研究背景

焦虑与抑郁的 fMRI 研究越来越依赖数据合并——跨中心、跨时间、跨硬件——因为单中心样本对精神影像中典型的细小、分布式效应而言统计功效不足。REST-meta-MDD 联盟即为典型:它汇集了来自 25 个队列(质控后 17 个中心)的静息态 fMRI 数据,正是因为单中心抑郁研究此前产生了不一致、功效不足、有时相互矛盾的结果(Yan 等 2019, *PNAS*)。

对 CAD 实验室而言,硬件问题并非纸上谈兵。焦虑/抑郁模型中最核心的脑区——杏仁核、膝下/腹内侧前额叶、腹侧纹状体、海马、脑岛、背侧 ACC 与 dlPFC——位于差异很大的深度,因而对接收线圈几何结构的敏感度也各不相同。若某一由线圈引起的测量差异恰好落在这些脑区之一,便可能模仿、放大或掩盖临床效应。当线圈与分组相关时,**组间**对比风险最高;当线圈与时间点相关时,**纵向**对比风险最高。本备忘录的任务,就是厘清关于该风险究竟"已知什么",以及应当"如何应对"。

---

## 2. MRI 物理背景(简明,只保留与决策相关的部分)

- **接收通道 / 相控阵。** 现代头线圈是由许多小型接收元件构成的阵列。每个元件对邻近组织最敏感;信号在各元件间合并。通道越多,一般意味着更高的外周 SNR 与更好的并行成像(GRAPPA/SENSE)性能。**【已证实】**(Wiggins 等 2006;de Zwart 等 2004)。
- **SNR 并非均匀。** 多元件带来的优势在皮层表面最大,随深度衰减;深部/中央结构从增加通道中获益远小。**【已证实】**(de Zwart 等 2004;Wiggins 等 2006)。
- **图像 SNR(SNR₀)与时间 SNR(tSNR)。** BOLD 敏感度取决于 tSNR,它由热噪声(与硬件/线圈相关)与生理噪声(与信号相关)共同构成。在生理噪声占主导处,增加线圈 SNR 几乎不改善 tSNR;在热噪声占主导处(小体素、深部区域、高加速),线圈 SNR 直接起作用。**【已证实】**(Triantafyllou, Polimeni & Wald 2011;Krüger & Glover 2001)。
- **线圈差异为何会使 fMRI 产生偏倚。** 因为线圈几何改变了空间 SNR 分布,它会逐区改变 tSNR,从而改变 BOLD 检测功效,并可能移动连接度估计——且在全脑范围内并不均匀。这类现象的**发生**是【已证实】;而任何具体新装置中的确切幅度则为【推断】,必须在本地测量。
- **B₁⁺(发射)。** 在 3T,发射由体线圈完成;接收阵列并不实质改变发射场。线圈通道差异是**接收侧 / SNR**现象,而非翻转角现象。**【已证实 / 标准结论】**。

---

## 3. 头线圈直接比较研究

**如要求,证据层级分开列示:**
**A** = 同一受试者使用不同线圈扫描(被试内);**B** = 同一扫描仪、不同线圈、不同受试者;**C** = 不同扫描仪/中心/线圈。

### 问题一汇总表——已发表的线圈比较

| 研究 | 扫描仪 / 厂商 | 场强 | 线圈比较 | 样本 | fMRI 类型 | 主要发现 | 层级 |
|---|---|---|---|---|---|---|---|
| Kaza, Klose & Lotze 2011(*JMRI* 34(1):173–183) | Siemens | 3T | 12ch vs 32ch | n=36,被试内 | 视觉运动任务 | 32ch 在**皮层**给出更高 tSNR 与激活;对深部结构(丘脑、小脑)益处**不明显**;预扫描归一化有帮助 | **A** |
| Paolini 等 2015(*Acta Radiol* 56(5):605–613) | Philips | 3T | 8ch vs 32ch | n=26,被试内,平衡设计 | 静息态(ICA) | 32ch 的体模 SNR 更高,但在标准参数下**各静息态网络无显著差异** | **A** |
| Panman 等 2019(*Front Neurosci* 13:729) | Philips | 3T | 8ch vs 32ch | n=77,被试内 | T1 + DTI + 静息态 | 在 GM/WM 体积、FA(约 4–6%)与**静息态 FC(后部网络最高约 27.5%)**上均见线圈相关偏倚;样本大于 Paolini,**确实**检出 FC 差异 | **A** |
| Schmitt & Rieger 2021(*Front Neurosci* 15:735290) | Siemens Prisma | 3T | 20ch vs 64ch(头颈) | n=26,被试内 | 运动 / 听觉 / 视觉任务 | tSNR 与 β 差异呈**区域依赖**,并与**预扫描归一化滤波器交互**(皮层与丘脑方向相反) | **A** |
| Triantafyllou, Polimeni & Wald 2011(*NeuroImage* 55(2):597–606) | Siemens | 3T | 1ch / 12ch / 32ch(SNR 基准) | 体模 + 在体 | SNR₀/tSNR 表征 | 建立热噪声-生理噪声框架;通道越少,越把深部/高分辨率区推向热噪声主导 | A(物理基准) |
| Wiggins 等 2006(*MRM* 56(1):216–223) | Siemens | 3T | 32ch 设计 vs 8ch | 体模 + 在体 | SNR/g 因子基准 | 32ch:外周 SNR 大幅提升,中央提升有限,并行成像改善 | (硬件基准) |

**这批证据实际说明了什么:**

1. 线圈通道差异会对 fMRI 衍生指标产生**真实、可测量**的效应——这一点无可置疑(Panman 2019;Kaza 2011)。
2. 效应具有**区域特异性**——在线圈敏感度差异最大处更大(外周/皮层,以及加速将区域推向热噪声主导之处),在深部结构相对较小(因该处 SNR 本身受源限制)(Kaza 2011;Schmitt 2021)。**【已证实】**
3. 效应**并非在小样本下总能被检出**:Paolini(n=26)未发现 8ch 与 32ch 之间的显著 RSN 差异,而 Panman(n=77)则发现了。这是一个统计功效的问题,直接反驳"该差异可忽略"这一说法——它也许只是在小样本中未被检出而已。**【已证实】**
4. **采集侧滤波很重要,且并非中性:** 预扫描归一化滤波器会以区域依赖的方式改变线圈效应(Schmitt 2021),因此必须保持恒定,不能在两个中心之间来回切换。

**关键空白(直言不讳):**
- **没有已发表研究直接就 fMRI 比较 Siemens 32 通道头线圈与其自身仅下部 20 元件配置。** 最接近的同厂同机 fMRI 比较是 12-vs-32(Kaza)与 20-vs-64(Schmitt)。对确切的 20-vs-32 对比而言,属【无直接证据】。
- 8-vs-32 的证据(Paolini、Panman)使用的是物理设计不同的 **Philips** 线圈,而非 Siemens 的 20/32 配置。有方向性参考价值;但不能替代。
- **B 层级设计(同扫描仪、不同线圈、不同受试者)基本缺失**——线圈比较几乎都是被试内。这一点很重要,因为 B 层级正是对线圈–分组混淆最脆弱的设计,而 CAD 实验室的跨中心设置与之部分相似。

---

## 4. 存在硬件差异的多中心 fMRI 研究

当数据跨扫描仪/线圈/中心合并时,线圈差异**并非**被单独隔离——它是合并的中心/扫描仪/线圈"批次"效应的一个组成部分。主要项目如何处理:

- **人类连接组计划(HCP)**(Van Essen 等 2013, *NeuroImage* 80:62–79):通过**标准化采集**(定制扫描仪、固定协议、相同预处理)来控制硬件方差。其经验是"预防"而非事后修补——与 CAD 实验室的处境正好处于光谱的两端。
- **ABIDE**(孤独症脑影像数据交换;联盟数据集):各中心扫描仪/线圈/协议高度异质;下游使用者通常将**中心**作为因子建模,或在分析前对衍生指标应用 **ComBat**。*(本备忘录已核实 HCP、ENIGMA 与 REST-meta-MDD 的引文;具体的 ABIDE 引文在写入正式稿前应对照你所引用的版本再确认。)*
- **ENIGMA**(Thompson 等 2014, *Brain Imaging Behav* 8(2):153–182):向各中心分发标准化分析协议并进行元/巨分析,明确将**中心**作为协调化的单位。
- **REST-meta-MDD**(Yan 等 2019, *PNAS* 2019, doi:10.1073/pnas.1900390116):最相关的临床先例。17 个中心,静息态 fMRI,抑郁症。通过 (i) 在每个中心以相同方式运行的**标准化本地预处理流程**,以及 (ii) 在组分析中对**中心**进行统计处理来应对异质性。它**并未**忽略硬件差异。

### 问题三表——各研究是否合并了不同硬件,及如何合并

| 研究 / 项目 | 硬件差异 | 分析方式 | 控制方法 | 结果 |
|---|---|---|---|---|
| Paolini 2015 | 8ch vs 32ch,同一受试者 | 比较(未合并) | 被试内、平衡设计 | n=26 时 RSN 无显著差异 |
| Panman 2019 | 8ch vs 32ch,同一受试者 | 比较(未合并) | 被试内 | n=77 时体积/FA/FC 出现显著线圈偏倚 |
| Yu 等 2018(*HBM* 39:4213–4227) | 多中心扫描仪 | 合并 FC 指标 | 对连接度做 **ComBat**,中心为批次,生物学量为协变量 | ComBat 去除中心效应,保留/增强年龄效应 |
| Yan 等 2019(REST-meta-MDD) | 17 个中心、混合扫描仪/线圈 | 巨分析 | 标准化流程 + 中心建模 | 可复现的 DMN 发现(复发性 MDD) |
| Wang, Chen & Yan 2023(*NeuroImage* 274:120089) | 多中心 + 巡回受试者 | 基准比较 11 种方法 | **SMA** vs ComBat 等 | SMA 在静息态整体最佳,含个体可识别性 |

**要点:** 在可信的多中心文献中,**无人在忽略硬件差异的情况下跨硬件合并数据。** 他们要么标准化采集/预处理,要么将中心/扫描仪/线圈作为建模因子纳入,要么应用协调化方法(通常施于*衍生*指标)。直接、无控制的合并并非被接受的做法,也**【无直接证据】**表明其安全。

---

## 5. 统计与技术控制方法

### 问题四——按控制层级组织

**采集层级**
- 同扫描仪 / 同序列 / 匹配的 TR、TE、分辨率、GRAPPA、带宽。属**预防**而非纠正偏倚。是可获得的最强控制。原则上有效属【已证实】(HCP)。
- **预扫描归一化滤波器保持恒定**——因为它与线圈以区域依赖方式交互(Schmitt 2021)。在两中心间切换它反而会*制造*偏倚。
- **巡回受试者设计**(同一批人在两套装置上扫描):这是直接测量实际本地线圈/中心效应的唯一途径,也是协调化方法最需要的输入。价值属【已证实】(Wang 2023;Yamashita 2019)。
- 体模定标:对 SNR/QC 基线有用;单靠它无法捕捉在体 BOLD/FC 效应。

**质控层级**
- **每次会话的 tSNR 图**(分区域,尤其 dlPFC 与皮层下 ROI)。
- **逐帧位移 / 头动**——必须在线圈/中心组间匹配,因为头动会混淆 FC,且可能与幽闭恐惧(从而与线圈选择)相关。
- **MRIQC 类指标**与**信号丢失 / 覆盖检查**(尤其 OFC 与颞极)。
- 在分析数据库中标记并记录每次会话的确切线圈/配置。

**统计控制**
- 将**中心 / 扫描仪 / 线圈作为协变量**纳入组模型:仅能捕捉*全局*均值偏移。是必要下限,但对线圈差异所产生的空间非均匀偏倚**并不充分**。局限属【已证实】。
- **区域特异性 tSNR 作为协变量**:更佳,因为它允许干扰项随区域变化。
- **混合效应模型**(含中心/受试者随机效应):适合纵向/多中心结构。

**协调化方法**

| 方法 | 目的 | 证据基础 | 是否专门适用于*线圈*差异? |
|---|---|---|---|
| **ComBat / NeuroComBat**(Johnson 2007;Fortin 2017、2018) | 以经验贝叶斯去除衍生特征上的加性+乘性中心/批次效应 | 对跨中心 DTI、皮层厚度证据充分 | **【推断】**——针对*中心/扫描仪*批次验证,而非专门针对线圈通道差异;若将线圈视为(部分)批次且每批次样本充足则合理 |
| **对功能连接的 ComBat**(Yu 等 2018, *HBM*) | 对 FC/网络指标的中心校正 | 多中心静息态 FC 已证实 | 对线圈专门而言属**【推断】**;是最接近 FC 层级的证据 |
| **纵向 ComBat**(Beer 等 2020, *NeuroImage* 220:117129) | 当同一受试者随时间在不同扫描仪上扫描时进行协调 | 在纵向/巡回数据上已证实 | **若** CAD 会话在同一受试者内随时间混用线圈/中心(情景 C),则是正确变体 |
| **SMA——子采样最大均值距离校正**(Wang, Chen & Yan 2023) | 静息态的分布漂移校正 | 静息态整体优于 ComBat,含可识别性 | 对线圈属**【推断】**;若问题确为多中心静息态,则为当前最佳选择 |
| **ComBat-GAM**(Pomponio 等 2020) | 非线性(如年龄)协变量的协调 | 在寿命跨度结构数据上已证实 | **【推断】**;若非线性协变量重要则相关 |

**对本用途下所有协调化方法的诚实提醒:** 上述每种方法都是在**中心/扫描仪**批次效应上验证的。**【无直接证据】**表明其中任何一种曾专门在*20ch-对-32ch 线圈*差异上得到验证。它们是合理、站得住脚的工具——但对线圈通道协调而言属推断而非证实;并且它们需要每批次足够的扫描量才能估计批次参数。若线圈与分组混淆,它们还有去除真实生物学信号的风险。

---

## 6. 对 CAD 实验室问题的直接回答

**处境:** 韩国中心——32 通道头线圈;美国中心——20 通道头线圈。

**首先,答案所依赖的一个前提。** 确定美国"20 通道"线圈物理上究竟是什么:(a) Siemens 32 通道头线圈的仅下部 20 元件模式,(b) 独立的 Siemens 20 通道头/颈线圈,还是 (c) 其他厂商/型号。这会改变物理性质。**切勿**假定它就是 32 通道线圈的下部 20 元件模式——那正是前一版综述的一个缺陷。

### 问题二——通道数不同的数据能否合并?

**情景 A——同扫描仪型号 + 同序列 + 不同线圈通道数(如同型扫描仪上的 32ch vs 20ch):**
- **合并:有条件地可接受。** 唯一被隔离的变量是线圈敏感度。
- **偏倚:** 区域性 tSNR/BOLD 敏感度差异(在外周/背侧皮层最大;在深部结构较小但非零);在样本充足时可检出的 FC 移位(Panman 2019)。效应存在属【已证实】;此处确切幅度属【推断】。
- **风险:** 若线圈在组/时间点间平衡且主要 ROI 为皮层下,则低到中等;若主要分析针对背侧/上部皮层,或线圈与组/时间点相关,则中到高。
- **必需:** 匹配序列 + 预扫描归一化保持恒定;线圈协变量(最好用区域 tSNR);纳入与不纳入少数线圈会话各做一次敏感性分析。

**情景 B——不同中心 + 不同扫描仪 + 不同线圈(CAD 实验室的实际情形):**
- **合并:仅在主动协调化下可接受;单靠协变量调整不行。** 此时线圈差异已与扫描仪、中心不可分割。
- **偏倚:** 完整的中心/扫描仪/线圈批次效应——比单纯线圈更大、更难预测。
- **风险:** 无巡回受试者数据时**高**;有则中等。
- **必需:** 跨中心标准化采集与预处理(REST-meta-MDD 模式);对中心/扫描仪建模;对衍生指标做协调化(静息态 FC 用 SMA 或 ComBat;若在受试者内随时间变化则用纵向 ComBat);最好有若干巡回受试者以量化实际效应。**【无直接证据】**表明韩国-32ch 与美国-20ch 数据可在*不*采取上述控制的情况下合并,也没有已发表研究把"跨中心的 20-对-32 通道"作为已解决的案例来隔离。

### 按硬件匹配情况给出的建议

- **若两中心为同一扫描仪型号:** 视为情景 A。配合"采集 + 协变量 + 敏感性分析"套餐,有条件合并是合理的。
- **若扫描仪型号不同:** 情景 B。需要协调化;仅靠协变量不充分。
- **若为不同中心(实际情形):** 情景 B,应优先做标准化流程 + 协调化 +(最好)巡回受试者。可考虑把主要假设限定在线圈效应最小的皮层下/边缘系统 ROI,并将背侧皮层的发现作为次要结果处理。

---

## 7. 审稿人视角(NeuroImage / HBM / Biological Psychiatry)

**担忧:** "线圈/中心与你的分组或时间点混淆;该效应可能是硬件而非精神病理。"
→ **回应:** 报告线圈/中心 × 组(以及 × 时间点)的交叉表并检验不平衡;对中心/线圈建模;纳入与不纳入少数配置各跑一次主要分析。
→ **分析:** 线圈–组独立性的 χ²/逻辑回归检验;协变量 + 协调化后的再分析;完整报告敏感性分析。

**担忧:** "你跨不同线圈合并了——我们怎么知道组效应不是测量偏倚?"(审稿人会引用 Panman 2019 的 27.5% FC 差异。)
→ **回应:** 承认线圈偏倚真实存在并加以引用;说明效应在协调化后依然存在,且位于与线圈偏倚图不同的区域/边。
→ **分析:** 对 FC 做 ComBat/SMA(Yu 2018;Wang 2023);将发现叠加在实证测得的(巡回受试者或试点)线圈差异图上。

**担忧:** "协变量调整无法修正空间非均匀的偏倚。"
→ **回应:** 同意;这正是为何全局协变量只是下限而非解决方案。
→ **分析:** 区域特异性 tSNR 协变量和/或特征层级协调化,而非单一二值回归项。

**担忧:** "对于纵向分支,线圈更换会模仿变化。"
→ **回应:** 在可能处让线圈/中心在时间点间平衡;使用纵向协调化模型。
→ **分析:** 纵向 ComBat(Beer 2020);逐受试者 tSNR 质控;报告转换平衡情况。

**担忧(结构性):** "没有直接文献验证跨中心的 20-对-32 通道合并。"
→ **回应:** 正确——把这一点讲明,并提供你自己的本地证据(试点/巡回受试者的线圈差异图),而不是宣称文献支持而实际并不存在。

---

## 8. 最终建议

**结论:** **有条件可接受**——前提是 (1) 确定美国线圈的确切硬件,以及 (2) 实施中心/线圈协调化,而非仅靠协变量调整。若主要假设需要背侧/上部皮层 fMRI 且无法获得巡回受试者数据,则对这些特定分析降级为**不推荐**。

**置信度:** **低到中等。** 一般现象(线圈差异会使 fMRI 产生区域性、在样本充足时可检出的偏倚)已被充分证实。而具体的跨中心 20-对-32 情形**并未**被直接研究;本建议依托于相邻证据加标准多中心实践,且必须以实验室自身的测量为支撑。

**必需步骤**
1. **采集文档化:** 确认并记录每次会话的确切扫描仪型号、线圈型号/配置、序列与预扫描归一化状态;跨中心保持序列与预扫描归一化恒定。
2. **质控:** 每次会话分区域的 tSNR(dlPFC + 皮层下 ROI)、跨中心/线圈匹配的逐帧位移、覆盖/丢失检查(OFC、颞极)、MRIQC 类指标。
3. **本地证据(以此替代缺失的文献):** 采集一小批在两套装置上都扫描的巡回受试者/试点数据,测量实际的中心+线圈差异图。这是单项最有价值的行动。
4. **预处理:** 两中心使用相同流程(REST-meta-MDD 模式);统一强度缩放。
5. **统计控制:** 对中心/扫描仪/线圈建模;优先使用区域特异性 tSNR 协变量而非单一二值标志;纵向/多中心结构用混合效应。
6. **协调化:** 对静息态衍生指标,用 ComBat(Yu 2018)或 SMA(Wang 2023);若线圈/中心在受试者内随时间变化,则用纵向 ComBat(Beer 2020)——并纳入生物学协变量以保护真实效应。
7. **敏感性分析:** 报告所有主要发现在协调化前后、以及纳入/剔除少数线圈中心时的结果;检验线圈–组与线圈–时间点独立性;无论结果如何,均将线圈/中心作为局限加以讨论。

**任何由此产生的论文中都应明确写出的局限:** 没有已发表研究直接验证跨中心合并 32 通道与 20 通道头线圈 fMRI 数据;结论依托于相邻的线圈比较与多中心协调化文献,以及本地测得的线圈差异估计。

---

## 已核实参考文献

1. Wiggins GC, Triantafyllou C, Potthast A, Reykowski A, Nittka M, Wald LL. 32-channel 3 Tesla receive-only phased-array head coil with soccer-ball element geometry. *Magn Reson Med.* 2006;56(1):216–223. doi:10.1002/mrm.20925
2. Triantafyllou C, Polimeni JR, Wald LL. Physiological noise and signal-to-noise ratio in fMRI with multi-channel array coils. *NeuroImage.* 2011;55(2):597–606. doi:10.1016/j.neuroimage.2010.11.084
3. Krüger G, Glover GH. Physiological noise in oxygenation-sensitive magnetic resonance imaging. *Magn Reson Med.* 2001;46(4):631–637. doi:10.1002/mrm.1246
4. de Zwart JA, Ledden PJ, van Gelderen P, Bodurka J, Chu R, Duyn JH. Signal-to-noise ratio and parallel imaging performance of a 16-channel receive-only brain coil array at 3.0 Tesla. *Magn Reson Med.* 2004;51(1):22–26. doi:10.1002/mrm.10678
5. **Kaza E, Klose U, Lotze M.** Comparison of a 32-channel with a 12-channel head coil: are there relevant improvements for functional imaging? *J Magn Reson Imaging.* 2011;34(1):173–183. doi:10.1002/jmri.22614 *(较前一版已更正)*
6. Paolini M, Keeser D, Ingrisch M, Werner N, Kindermann N, Reiser M, Blautzik J. Resting-state networks in healthy adult subjects: a comparison between a 32-element and an 8-element phased array head coil at 3.0 Tesla. *Acta Radiol.* 2015;56(5):605–613. (PMID 25585849)
7. **Panman JL, To YY, van der Ende EL, et al.** Bias introduced by multiple head coils in MRI research: an 8 channel and 32 channel coil comparison. *Front Neurosci.* 2019;13:729. doi:10.3389/fnins.2019.00729 *(较前一版已更正)*
8. Schmitt T, Rieger JW. Recommendations of choice of head coil and prescan normalize filter depend on region of interest and task. *Front Neurosci.* 2021;15:735290. doi:10.3389/fnins.2021.735290
9. Yan CG, Chen X, Li L, et al. (REST-meta-MDD). Reduced default mode network functional connectivity in patients with recurrent major depressive disorder. *Proc Natl Acad Sci USA.* 2019. doi:10.1073/pnas.1900390116
10. Yu M, Linn KA, Cook PA, et al. Statistical harmonization corrects site effects in functional connectivity measurements from multi-site fMRI data. *Hum Brain Mapp.* 2018;39(11):4213–4227. doi:10.1002/hbm.24241
11. Fortin JP, Parker D, Tunç B, et al. Harmonization of multi-site diffusion tensor imaging data. *NeuroImage.* 2017;161:149–170. doi:10.1016/j.neuroimage.2017.08.047
12. Fortin JP, Cullen N, Sheline YI, et al. Harmonization of cortical thickness measurements across scanners and sites. *NeuroImage.* 2018;167:104–120. doi:10.1016/j.neuroimage.2017.11.024
13. Beer JC, Tustison NJ, Cook PA, et al. Longitudinal ComBat: a method for harmonizing longitudinal multi-scanner imaging data. *NeuroImage.* 2020;220:117129. doi:10.1016/j.neuroimage.2020.117129
14. Wang YW, Chen X, Yan CG. Comprehensive evaluation of harmonization on functional brain imaging for multisite data-fusion. *NeuroImage.* 2023;274:120089. doi:10.1016/j.neuroimage.2023.120089
15. Pomponio R, Erus G, Habes M, et al. Harmonization of large MRI datasets for the analysis of brain imaging patterns. *NeuroImage.* 2020;208:116450. doi:10.1016/j.neuroimage.2019.116450
16. Yamashita A, Yahata N, Itahashi T, et al. Harmonization of resting-state functional MRI data across multiple sites via matching of histogram and principal components. *Hum Brain Mapp.* 2019;40(6):1787–1798. doi:10.1002/hbm.24490
17. Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics.* 2007;8(1):118–127. doi:10.1093/biostatistics/kxj037
18. Van Essen DC, Smith SM, Barch DM, Behrens TEJ, Yacoub E, Ugurbil K; WU-Minn HCP Consortium. The WU-Minn Human Connectome Project: an overview. *NeuroImage.* 2013;80:62–79. doi:10.1016/j.neuroimage.2013.05.041
19. Thompson PM, Stein JL, Medland SE, et al. The ENIGMA Consortium: large-scale collaborative analyses of neuroimaging and genetic data. *Brain Imaging Behav.* 2014;8(2):153–182. doi:10.1007/s11682-013-9269-5

*本轮未独立复核(写入正式稿前请确认):具体的 ABIDE 引文(Di Martino 等,ABIDE I *Mol Psychiatry* 2014 / ABIDE II *Sci Data* 2017)——仅在数据集层面讨论。*
