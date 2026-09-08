# CAD Lab 项目状态快照

> 生成日期: 2026-07-20
> 用途: 记录当前 CAD 文件夹内所有已完成工作的详细状态，便于后续会话恢复

---

## 一、项目概览

**研究领域**: 认知情感神经科学 (Cognitive Affective Neuroscience)
**核心方向**: fMRI 数据分析 | 机器学习 | 多模态信号处理 | 内感受 (Interoception) | 计算精神病学
**所在 Lab**: CAD Lab (Cognitive Affective Neuroscience Lab)
**使用者语言**: 韩语母语，中文/英文研究

---

## 二、文献系统 (LitForge)

### 2.1 核心体系文件

| 文件 | 路径 | 说明 |
|------|------|------|
| Zotero 联动工作流 | `CAD/_zotero_workflow.md` | 完整的 Zotero API/SQLite 操作流程，含笔记模板、标注标准、文件存储结构 |
| Literature Analysis Framework | `CAD/prompt_guides/literature_analysis_framework.md` | 三遍读法 + 5 维度分析范式 (解剖刀/方法论三层拆解/核心发现/战略嫁接/重要性判断) + 质量检查清单 |
| Annotation Guidelines | `CAD/prompt_guides/annotation_guidelines.md` | 4 层标注结构 (定义&背景/在本文中的角色/与论证的关联/批判性延伸)，选标策略，质量自检 |
| Literature Note Template | `CAD/prompt_guides/literature_note_template.md` | 8 个必须部分的笔记模板，含概念解释粒度标准和笔记写作原则 |
| Paper Priority | `CAD/prompt_guides/paper_priority.md` | 重要等级分类 (⛰️镇山之宝 / ⚔️精兵强将 / 📌补充参考 / 🌫️过眼云烟) + 用途标签 + 研究版图定位 |
| Zotero Quick Reference | `CAD/prompt_guides/zotero_workflow.md` | API 快速参考 + SQLite 写入命令 + 关键数据库表结构 |

### 2.2 Head Coil Literature Review (PI-Level, 2026-07-20)

| 文件 | 路径 | 说明 |
|------|------|------|
| Head Coil PI Review | `CAD/headcoil_literature_review.md` | PI-level technical review of 20‑ch vs 32‑ch head coil fMRI on the same Siemens scanner. ~550 lines, 7 sections + 2 appendices. Written at senior MRI physicist / fMRI methods expert depth — not a general literature summary. |

**Key sections:**
1. **Hardware Physics** — Coil architecture (soccer‑ball geometry, 12 upper + 20 lower elements), region‑specific SNR scaling (dlPFC: 40–55% loss; cerebellum: <5% loss), g‑factor penalty, B₁⁺ considerations
2. **Paper‑by‑Paper Deep Reading** — 7 papers (Triantafyllou 2011, Schmitt 2021, Panman 2019, Fortin 2017/2018, Wang 2023, de Zwart 2002/2004, Kruger & Glover 2001) in structured format with limitations and direct relevance
3. **Evidence Hierarchy** — 10 claims ranked by strength (Strong / Moderate / Weak) with CAD Lab confidence level
4. **Three CAD Lab Scenarios** — (1) Same scanner same coil partial‑array, (2) Multi‑site different coils, (3) Longitudinal mixed‑coil per participant
5. **Reviewer Perspective Q&A** — NeuroImage, BiolPsych, MR Physics, and Statistical reviewer criticisms with scientific responses
6. **Statistical Analysis Plan** — Three tiers (Minimal / Recommended / Gold‑Standard) with specific implementation steps
7. **Final PI Recommendation** — Yes/no/conditional. Voting **Yes** if 7 conditions met (acquisition standardisation, pilot validation, ROI‑specific tSNR covariate, longitudinal balance, pre‑registration, sensitivity analysis, documentation). **No** if primary analyses target dorsal cortex, >30% 20‑ch sessions without traveling subjects, or group×coil confounding

**Appendixes:** Acquisition protocol checklist, quick‑reference bias magnitude table per ROI per metric.

### 2.3 已精读论文

#### (1) Ponzo2021_CARED — 内感受生态采样任务
- **路径**: `CAD/litreview/Ponzo2021_CARED.md`
- **重要等级**: ⚔️精兵强将
- **核心内容**:
  - CARED 任务: 用可穿戴设备 + 手机 App 在 4 周内生态采样内感受判断
  - Garfinkel 三层次模型 (Accuracy / Sensibility / Awareness)
  - Mann-Whitney U 检验用于个体水平内感受准确性判定
  - ROC/AUC 用于元认知测量 (群体 AUC = 0.58, p < 0.001)
  - 4/30 反向元认知亚组深度分析
  - 自适应采样算法公式详解
- **战略嫁接**: 直接链接 Phase 2 的 MCI 元认知校准设计
- **Zotero**: `C5WAAYXR` | PDF: `96JGGS5Q` | 笔记: `TOMXVWCX`

#### (2) Abend2023_ThreatImminence — 威胁迫近与焦虑
- **路径**: `CAD/litreview/Abend2023_ThreatImminence.md`
- **重要等级**: ⚔️精兵强将
- **核心内容**:
  - Threat Imminence Continuum (Fanselow/Mobbs 传统) 的四阶段: pre-encounter / encounter / post-encounter / contact
  - 系统将焦虑症状 (担忧/生理唤起/回避/惊恐) 映射到不同迫近阶段
  - 担忧 = encounter 阶段的重复性威胁评估 (有争议的原创提法)
  - 惊恐发作 = contact 阶段的病理激活
  - Box 1 含原始数据: 50 名青少年热痛预期范式
- **战略嫁接**: 分段分析 (按迫近度而非聚合) 可提高焦虑效应检测灵敏度
- **Zotero**: `N2CDQSAY` | PDF: `RTKJDNJM`

### 2.3 外部技能库调研
- **路径**: `CAD/litreview/external_skills_research_report.md` (546 行)
- **内容**: 比较 8 个外部仓库 (deep-reading-analyst, hermes-research-skills, tashan-research-skills, agent-auto-sci-skills 等) 的技能体系，含交叉分析矩阵和优先级改进建议
- **目的**: 为 LitForge 系统优化提供参考

### 2.4 存档
- **路径**: `CAD/litreview/archive/`
- **内容**: 早期版本存档 `archived_20260713_165815.json` + `.md`

---

## 三、视频加工 (Tic Videos)

### 3.1 数据源
- `CAD/image_sources__tic.xlsx` — 包含 YouTube URL 和时间码的视频来源表

### 3.2 处理结果
从 YouTube 下载 18 个视频，按 excel "구간" 列时间码精确裁剪:

**Motor Tics (GIF 格式)**:
| 文件 | 说明 |
|------|------|
| Motor-1 (Eye blinking).mp4 | 眨眼 |
| Motor-2 (Other facial tics).mp4 | 面部抽动 |
| Motor-3 (Head jerks).mp4 | 头部抽动 |
| Motor-4 (Shoulder jerks).mp4 | 肩部抽动 |
| Motor-5 (Arm movements).mp4 | 手臂动作 |
| Motor-6 (Stomach twitches).mp4 | 腹部抽动 |
| Motor-7 (Leg movements).mp4 | 腿部动作 |
| Motor-8 (Touching-tapping things)_1.mp4 | 触摸/敲打 片段1 |
| Motor-8 (Touching-tapping things)_2.mp4 | 触摸/敲打 片段2 |
| Motor-10 (Echokinesis).mp4 | 模仿动作 |
| Motor-11 (Hurts self).mp4 | 自伤行为 |

**Vocal Tics (MP4 格式)**:
| 文件 | 说明 |
|------|------|
| Vocal-1 (sniffing-coughing-throat clearing).mp4 | 嗅/咳/清嗓 |
| Vocal-2 (snorting-grunting)_1.mp4 | 喷鼻/咕噜 片段1 |
| Vocal-2 (snorting-grunting)_2.mp4 | 喷鼻/咕噜 片段2 |
| Vocal-3 (Repeat own words-sentences).mp4 | 重复自己话语 |
| Vocal-4 (Repeat others speech).mp4 | 模仿他人说话 |
| Vocal-5 (Coprolalia).mp4 | 秽语 |
| Vocal-6 (Insults-racial slurs).mp4 | 侮辱/种族歧视语 |

**注意**: Motor-9 被排除，最终 18 个视频

### 3.3 相关文件夹
| 文件夹 | 说明 |
|--------|------|
| `CAD/crop_vids/` | 裁剪后的 18 个原始 MP4 文件 |
| `CAD/cropped_video_archive/` | 裁剪视频存档 |
| `CAD/cropped_video_v2/` | 裁剪视频第二版 |
| `CAD/cropped_vid_gif/` | GIF 格式输出 |
| `CAD/frames/` | 视频帧提取 |
| `CAD/gif_frames/` | GIF 帧提取 |
| `CAD/tic_videos/` | 原始下载视频 |

### 3.4 共享链接
Google Drive: `https://drive.google.com/drive/folders/1vG_GfT8-poo4WbXQ-pbSYGo5NrtVWgPL`

---

## 四、学习计划

**路径**: `CAD/学习计划与目标.md`
**最后更新**: 2026-06-29

### 4 阶段路线

| 阶段 | 时间 | 内容 | 状态 |
|------|------|------|------|
| Phase 1: fMRI 基础与 SPM 入门 | 1-2 个月 | BOLD 信号原理、SPM 实操 (Auditory/Face 数据)、BIDS 规范、pre-processing | 🔲 |
| Phase 2: 统计与机器学习基础 | 2-4 个月 | 线性代数 (SVD/PCA)、ISLR (回归/分类/重抽样/树/SVM)、GLM 进阶 | 🔲 |
| Phase 3: 高级分析与多模态 | 4-6 个月 | CanlabCore 教程、计算精神病学入门、强化学习、多模态特征提取 | 🔲 |
| QC 与实验流程 | 贯穿全程 | T1+fMRI QC、伪影识别、CAD Lab 实验全流程、HRV 测量 | 🔲 |

### 推荐资源
- Martin Lindquist fMRI 原理 YouTube
- SPM 官方手册/Andy's Brain Book
- ISLR (statlearning.com)
- Gilbert Strang MIT 18.06 线性代数
- CanlabCore / Dartmouth fMRI Tutorial (Tor Wager Lab)
- Computational Psychiatry 入门视频系列

---

## 五、研究提案与协议翻译

### GETREADY 文件夹
**路径**: `CAD/GETREADY/`

| 文件 | 说明 |
|------|------|
| `5. 심의용 연구계획서_신진과제_ver2.1_원문.docx` | 韩文原版研究计划书 (新进课题) |
| `5. 심의용 연구계획서_신진과제_ver2.1_원문추출.txt` | 韩文原文提取文本 |
| `5. 심의용 연구계획서_신진과제_ver2.1_中文.docx` | 中文翻译版 |
| `5. 심의용 연구계획서_신진과제_ver2.1_中文段落.txt` | 中文翻译段落文本 |
| `5. 심의용 연구계획서_신진과제_ver2.1.hwp` | 韩文原版 HWP 格式 |
| `신진과제 프로토콜_20260522 (최종)_中文翻译.docx` | 协议中文翻译 DOCX |
| `신진과제 프로토콜_20260522 (최종)_中文翻译.md` | 协议中文翻译 Markdown |
| `신진과제 프로토콜_20260522 (최종).docx` | 韩文原版协议 |
| `신진과제 프로토콜_20260522 (최종).pdf` | 韩文原版协议 PDF |
| `CAD_multimodal_self_narrative_proposal.md` | 多模态自传体叙事研究提案 (被引用，但文件当前不存在) |
| `protocol_original.md` | CAD Lab 原始实验协议 |
| `convert_hwp_to_docx.py` | HWP → DOCX 转换脚本 |

---

## 六、文件结构总览

```
CAD/
├── _zotero_workflow.md                 # Zotero 联动工作流 (核心文档)
├── CAD_session_state.md                # 本文件 — 会话状态快照
├── image_sources__tic.xlsx             # Tic 视频来源表
├── session_summary_email.md            # 视频加工完成邮件草稿 (韩文)
├── 学习计划与目标.md                    # fMRI 学习路线图
│
├── litreview/                          # 文献精读笔记
│   ├── Ponzo2021_CARED.md              # CARED 内感受任务笔记
│   ├── Abend2023_ThreatImminence.md    # 威胁迫近综述笔记
│   ├── external_skills_research_report.md  # 外部技能库调研报告
│   └── archive/                        # 存档版本
│
├── prompt_guides/                      # 提示词/指南系统
│   ├── literature_analysis_framework.md
│   ├── annotation_guidelines.md
│   ├── literature_note_template.md
│   ├── paper_priority.md
│   └── zotero_workflow.md
│
├── GETREADY/                           # 研究提案与协议翻译
│   ├── 5. 심의용 연구계획서_신진과제_ver2.1_*  (韩文原版/中文翻译/HWP)
│   ├── 신진과제 프로토콜_20260522 (최종)_*       (韩文原版/中文翻译)
│   ├── protocol_original.md
│   └── convert_hwp_to_docx.py
│
├── 看看文献/                           # 论文 PDF 原文
│   ├── Abend2023_NaBR.pdf
│   └── Ponzo 등 - 2021 - CARED.pdf
│
├── crop_vids/                          # 裁剪后视频 (18 个文件)
├── cropped_video_archive/              # 裁剪视频存档
├── cropped_video_v2/                   # 裁剪视频第二版
├── cropped_vid_gif/                    # GIF 格式输出
├── frames/                             # 视频帧提取
├── gif_frames/                         # GIF 帧
├── tic_videos/                         # 原始下载视频
│
└── .DS_Store
```

---

## 七、技术栈参考

| 工具/语言 | 用途 |
|-----------|------|
| Zotero Local API + SQLite | 文献管理、标注同步 |
| Python | HWP 转换、视频处理脚本 |
| MATLAB + SPM | fMRI 分析 (学习目标) |
| ISLR (R/Python) | 统计学习 (学习目标) |
| CanlabCore | fMRI 高级分析 (学习目标) |
| FFmpeg | 视频裁剪 |
| React Native (TypeScript/JS) + Kotlin | CARED 任务 App (Ponzo 2021) |

---

## 八、恢复工作指引

下次继续时可从以下方向选择:

1. **继续读论文**: 用 `CAD/_zotero_workflow.md` 流程，找新论文按 LitForge 框架精读
2. **深入学习**: 按 `学习计划与目标.md` 推进 Phase 1 fMRI 基础或 Phase 2 统计学习
3. **研究提案**: 完善 GETREADY 中的多模态自传体叙事 proposal
4. **视频加工**: 如有新的视频数据需要处理，参考 `image_sources__tic.xlsx` 的处理流程
5. **LitForge 优化**: 参考 `external_skills_research_report.md` 中的改进建议
