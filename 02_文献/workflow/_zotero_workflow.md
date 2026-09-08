# Zotero 联动读论文工作流 + 笔记标准

## 一、核心原则

```
有 highlight → 逐条加批注（annotationComment）
无 highlight → 写子笔记（itemNote）
笔记副本 → CAD/litreview/{AuthorYear_ShortTitle}.md
```

## 二、启动流程

### Step 0: 前置确认
- [ ] 论文已在 Zotero 条目库中 → 记录 itemKey
- [ ] PDF 附件已在 Zotero storage 中 → 记录 attachmentKey
- [ ] Zotero Local API 运行正常 → `http://127.0.0.1:23119/api/`

### Step 1: 读论文 + 检查标注
- 提取全文文本，理解研究问题/方法/结果/讨论
- 查询 API: `/api/users/0/items/{ATTACHMENT_KEY}/children?itemType=annotation`
- **有 highlight/underline** → 逐条加详细批注
- **无 highlight** → 在 Zotero 创建子笔记

### Step 2: 写本地笔记副本
`CAD/litreview/{AuthorYear_ShortTitle}.md` 按以下模板填写

---

## 三、笔记模板（必须遵循）

```
# 📖 [主题领域] 文献精读 — [日期]

## 关键词: [3-5个核心关键词]

## [论文完整标题]

### 📋 基本信息

- **重要等级**: {⛰️镇山之宝 / ⚔️精兵强将 / 📌补充参考}
- **第一作者**: [姓名] | [机构] | [实验室]
- **通讯作者**: [姓名]
- **发表**: [年份] | [期刊]
- **DOI**: [doi]
- **Zotero**: `itemKey` | **PDF**: `attachmentKey` | **笔记**: `noteKey`
- **引用**: ~[次数]

### 📚 研究背景

**已知 (Known)**

- 领域内已有的关键发现
- 与本论文最直接相关的 2-3 个背景

**知识缺口 (Knowledge Gap)**

- 尚不清楚/未解决的问题
- 前人方法的局限

**研究目标 (Research Aim)**

- 本文要解决的具体问题

### 🧠 理论背景

**核心理论框架 (Theoretical Framework)**

- 核心理论名称 + 来源文献
- 2-3 句话解释该理论的核心主张

**关键概念 (Key Constructs)**

- 定义本文涉及的核心概念
- 必要时附概念解释 (见下方"概念详解"一节)

**理论→本研究的逻辑链 (Rationale)**

- 用箭头/流程图展示理论如何推导出研究假设

### 🔬 研究方法

**被试 (Participants)**

- N, 性别, 年龄范围, 排除标准

**实验设计 (Experimental Design)**

- 范式名称 + 变量类型 (自变量/因变量)
- 试次结构 / 条件对比

**实验流程 (Procedure)**

- 分阶段描述

**数据分析 (Data Analysis)**

- 统计方法 + 关键参数
- 软件/工具包

### 💡 核心发现

**主要发现 (Main Findings)**

- 按重要性排序的 2-3 个结果
- 效应量 / 统计值

**理论意义 (Theoretical Implications)**

- 这些发现对理论框架意味着什么
- 支持/挑战/修正了哪个理论

**局限性 (Limitations)**

- 作者的自我批评
- 你的批判性评估

### 🔗 与你领域的关系

- 这篇论文如何直接对齐你的研究方向
- 你可以从中借用/改进/反驳的具体方法或论点
- 可用的引述段落 (英文)

### ⭐ 为什么这篇重要

简要说明本文在你这边的战略价值。

### 📄 原文摘要

> 英文摘要原文

### 📌 方法详解（可选）

对本文最核心的技术/统计方法展开解释。

---

## 四、概念详解标准

笔记中嵌入的术语解释用以下格式：

- **术语**: 1-2 句话的人话版定义
- 必要时分条目展开：定义 → 拆解 → 在本研究中的角色 → 延伸/关联

解释的粒度标准：
- **⛰️镇山之宝**: 每个关键术语都需详细解释
- **⚔️精兵强将**: 核心 2-3 个术语深入解释
- **📌补充参考**: 仅解释最晦涩的术语

## 五、标注批注标准

PDF 的每条 highlight/underline 在 Zotero 中写入 `annotationComment`，每条包含：

1. **定义和背景**: 该概念是什么，从哪来的
2. **在本研究中的角色**: 为什么作者在这里提到它
3. **与整体论证的关联**: 它如何服务于本文的核心论点
4. **批判性延伸（可选）**: 你的思考或与其他文献的连接

格式：纯中文，分段清晰，avg 150-300 字/条。

## 六、文件存储

| 内容 | 路径 | 说明 |
|------|------|------|
| 阅读笔记 (.md) | `CAD/litreview/{AuthorYear_ShortTitle}.md` | 本地副本 |
| Zotero 子笔记 | Zotero 条目库 (API/SQLite) | 权威版本 |
| Zotero 标注批注 | Zotero PDF 附件 | 绑定到具体高亮/下划线 |
| 工作流文档 | `CAD/_zotero_workflow.md` | 本文件 |

## 七、技术备忘

- Zotero Local API: `http://127.0.0.1:23119/api/users/0/`
- 已启用配置: `extensions.zotero.httpServer.localAPI.enabled = true`
- SQLite 备用: `~/Zotero/zotero.sqlite`
- 条目定位: 通过 DOI / title / itemKey
