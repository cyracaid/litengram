# LitEngram — Structured Knowledge Framework for Zotero

> 将PDF高亮转化为4层结构化理解笔记，自动同步到Notion，零成本本地LLM驱动

## 🎯 What is LitEngram?

LitEngram 是一个针对学术论文阅读的**知识管理框架**，可以将你在Zotero中高亮的内容自动转化为**结构化的4层笔记**：

| 层级 | 内容 | 例子 |
|------|------|------|
| **定义** | 概念定义 + 理论溯源 | "工作记忆(WM)：短时保持信息并操作的能力，Baddeley & Hitch (1974)..." |
| **本文角色** | 这个概念在本文中的作用 | "本文将WM研究从2-back扩展到1-6的完整负荷范围" |
| **论证关联** | 与文章核心论点的关系 | "这个发现直接支持了WM负荷-激活倒U模式假设" |
| **批判延伸** | 你的想法/未来研究方向 | "可在老年样本中重复此设计，比较生命周期变化" |

这样做的好处：
- ✅ 阅读时不分心（高亮后系统自动生成4层）
- ✅ 建立可复用的概念库（跨论文关联）
- ✅ 便于后续写作（有结构化的素材库）
- ✅ 本地运行（Ollama小模型，零API费用）

---

## 🚀 Quick Start (5分钟上手)

### 前置条件
- **Zotero 7+** （PDF阅读器已启用）
- **Ollama** （本地LLM）- [安装指南](https://ollama.ai)
- **Python 3.9+**
- **Notion账户**（可选，用于同步）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/cyracaid/litengram.git
cd litengram

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置环境变量
export ZOTERO_DB_PATH=~/Zotero/zotero.sqlite
export OLLAMA_MODEL=qwen2.5:0.5b
export NOTION_TOKEN=ntn_xxxxx  # 可选，用于Notion同步

# 4. 启动Ollama服务
ollama pull qwen2.5:0.5b
ollama serve

# 在另一个终端运行（保持Ollama服务活跃）
```

### 使用示例

```python
# 在Zotero中对论文的高亮点右键 → "Add comment"
# 输入4层结构（格式见下面的"Annotation Format"）
# 然后运行：

python scripts/synthesize_notes.py \
  --paper-id "Lamichhane2020_Nback" \
  --parent-item-id 4429

# 输出: ✓ 52 annotations processed
#       ✓ 12-part structured note created
#       ✓ Synced to Notion (optional)
```

更多命令见 [Commands Reference](#commands-reference)

---

## 📁 Project Structure

```
litengram/
├── README.md                          ← 你在这里
├── requirements.txt                   ← Python依赖
├── scripts/
│   ├── zotero_sync.py                ← 核心: 将笔记写入Zotero
│   ├── zotero_annotation_sync.py      ← 修复: annotation的comment+authorName
│   ├── notion_sync.py                 ← 可选: 同步到Notion
│   ├── synthesize_notes.py            ← 主流程: 合成结构化笔记
│   └── _markdown_blocks.py            ← 共享: markdown解析工具
├── references/
│   ├── annotation_guidelines.md       ← 4层结构的详细规范
│   ├── literature_analysis_framework.md ← 分析框架 + 领域检测
│   ├── stage_3_analysis.md            ← 第3阶段: 5维度分析
│   ├── stage_4-5_annotations.md       ← 第4-5阶段: 标注生成
│   ├── stage_6_note.md                ← 第6阶段: 笔记合成
│   └── concept_excavation.md          ← 概念深挖: 9层知识模型
├── docs/
│   ├── troubleshooting.md             ← 常见问题
│   ├── API_reference.md               ← 函数文档
│   └── examples/                      ← 真实案例
└── litreview/
    ├── Walther2009_notes.md           ← 论文笔记示例
    └── Lamichhane2020_notes.md        ← 另一个示例
```

---

## 🔑 Core Concepts

### 1. 4-Layer Interpretation Structure

每条高亮的批注都应该包含这4层（用【】标记分隔）：

```markdown
【定义】
核心概念的定义，包括理论出处。尽量引用原始文献。
如果有易混淆的相关概念，做简短的对比说明。

【本文角色】  
这个概念在本论文中的具体功能是什么？
作者用它来论证什么？

【论证关联】
这个概念/发现与论文的核心主张有什么关系？
是支持？是反驳？是补充条件？

【批判延伸】
你对这个观点的想法。可以是：
- 与其他论文的联系
- 潜在的偏差或假设
- 未来研究方向
- 实践应用建议
```

### 2. Knowledge Fingerprinting

系统自动为每个概念生成**MD5指纹**，用于：
- 🔗 跨论文关联相同概念
- 📊 消除重复定义
- 🧠 构建知识图谱

### 3. Hybrid Processing Pipeline

```
输入: Zotero高亮 + 用户批注
  ↓
[Rule-First] 尝试解析【定义】【本文角色】【论证关联】【延伸】
  ↓ (如果失败)
[LLM Fallback] 用本地Ollama模型生成4层结构
  ↓
[Fingerprinting] 生成概念指纹 + 关联相似节点
  ↓
输出: 结构化JSON → 写入Zotero comment字段 → 同步到Notion
```

---

## 📋 Annotation Format Example

**在Zotero中，一条完整的高亮批注应该是这样的：**

```json
{
  "itemID": 4431,
  "text": "Working memory (WM) function",
  "layers": {
    "definition": "工作记忆(WM)：认知心理学核心构念，指短时保持并操作信息以完成当前任务的能力，理论谱系上溯 Baddeley & Hitch (1974) 的多成分模型。",
    "role": "全文研究对象，标题即点明WM是研究焦点。与前作Callicott et al.不同，本文首次覆盖完整的1-6负荷范围。",
    "argument": "这直接回答了RQ1——什么因素能预测WM任务中的个体差异？通过明确现状的两个维度，本文才能孤立出线性负荷斜率的预测价值。",
    "extension": "如果在发展样本中验证，该框架可扩展至儿童WM发展轨迹，区分发展性与个体性差异来源。"
  },
  "confidence": "high",
  "fingerprint": "1f4d3a2c9e8b7c5a",
  "related_concepts": ["Executive Control", "Prefrontal Cortex"]
}
```

---

## 🛠️ How It Works (System Flow)

### Workflow Overview

1. **Read** → 从Zotero数据库读取所有高亮 + 现有批注
2. **Parse** → 用正则表达式提取【定义】【本文角色】【论证关联】【延伸】
3. **Generate** → 若解析失败，用Ollama LLM补充生成
4. **Fingerprint** → 为每个概念生成MD5指纹，关联相似定义
5. **Write** → 更新Zotero的itemAnnotations表（含authorName字段！）
6. **Sync** → 可选同步到Notion的"每日读读文献"页面

### Step-by-Step Example

**输入**: Lamichhane et al. (2020) 论文中的一个高亮

```
原文: "Working memory (WM) function"
用户批注留空或只有【定义】
```

**处理**:

```
① Rule-First Parser尝试提取4层
   → 失败（因为用户只输入了片段）

② LLM Fallback (Ollama qwen2.5:0.5b)
   → 读取本文上下文
   → 生成完整的【本文角色】【论证关联】【延伸】

③ Fingerprinting
   → MD5("Working memory") = "abc123..."
   → 搜索其他论文中是否出现过WM
   → 建立关联

④ SQLite Update
   UPDATE itemAnnotations 
   SET comment = '{4层JSON}', authorName = 'Lintergram'
   WHERE itemID = 4431

⑤ Notion Sync (可选)
   → POST到Notion API
   → 在"每日读读文献"页面下创建toggle
```

**输出**: 
- ✅ Zotero UI点击高亮时显示完整的4层笔记
- ✅ Notion page中有结构化的记录

---

## 📖 Environment Variables

| 变量 | 说明 | 默认值 | 例子 |
|------|------|--------|------|
| `ZOTERO_DB_PATH` | Zotero数据库位置 | `~/Zotero/zotero.sqlite` | `/Users/alice/Zotero/zotero.sqlite` |
| `LITENGRAM_LIBRARY_ID` | Zotero library ID | `1` | `1` (本地库) |
| `OLLAMA_MODEL` | 使用的LLM模型 | `qwen2.5:0.5b` | `qwen2.5:0.5b` 或 `mistral:latest` |
| `NOTION_TOKEN` | Notion集成token | (无) | `ntn_16793090050Z...` |
| `NOTION_DATABASE_ID` | Notion数据库ID | (无) | `abc123def456` |

**设置方式**:

```bash
# macOS/Linux
export ZOTERO_DB_PATH=~/Zotero/zotero.sqlite
export NOTION_TOKEN=ntn_xxxxx

# Windows (PowerShell)
$env:ZOTERO_DB_PATH="$env:USERPROFILE\Zotero\zotero.sqlite"
$env:NOTION_TOKEN="ntn_xxxxx"
```

---

## 📚 Commands Reference

### synthesize_notes.py

生成论文的12部分结构化笔记：

```bash
python scripts/synthesize_notes.py \
  --paper-id "Lamichhane2020_Nback" \
  --parent-item-id 4429 \
  --output-format md | notion | both
```

### zotero_annotation_sync.py

验证和修复annotation的comment+authorName字段：

```bash
# 验证某篇论文的所有annotation
python scripts/zotero_annotation_sync.py verify 4429

# 输出: 
# {
#   "total": 52,
#   "with_comment": 52,
#   "with_author": 52,
#   "missing": []
# }

# 更新单条annotation
python scripts/zotero_annotation_sync.py update 4429 4431 "【定义】..."
```

### notion_sync.py

手动触发Notion同步：

```bash
python scripts/notion_sync.py \
  --paper-key NIY96UDQ \
  --page-name "每日读读文献"
```

---

## ⚙️ Configuration Examples

### Ollama Setup

```bash
# 1. 安装Ollama
brew install ollama  # macOS
# 或从 ollama.ai 下载

# 2. 下载小模型（推荐 qwen2.5:0.5b，~1.3GB）
ollama pull qwen2.5:0.5b
ollama pull mistral:latest  # 备选

# 3. 启动服务（后台运行）
ollama serve &

# 4. 测试连接
curl http://localhost:11434/api/tags
```

### Notion Integration (Optional)

```bash
# 1. 在Notion中创建Internal Integration
#    https://www.notion.so/my-integrations

# 2. 获取token，设置环境变量
export NOTION_TOKEN=ntn_xxxxx

# 3. 在Notion中创建"每日读读文献"数据库
#    （模板: 每行一篇论文 + toggle里是标注）

# 4. 获取Database ID (从URL中提取)
export NOTION_DATABASE_ID=abc123...

# 5. 测试同步
python scripts/notion_sync.py --test
```

---

## 🐛 Troubleshooting

### Issue: "database is locked"

**原因**: Zotero还在使用数据库

**解决**:
```bash
# 1. 关闭Zotero
pkill -f Zotero

# 2. 清理锁文件
rm ~/Zotero/zotero.sqlite-journal
rm ~/Zotero/zotero.sqlite-wal

# 3. 重试
python scripts/synthesize_notes.py ...
```

### Issue: LLM返回空结果

**原因**: Ollama服务未运行或模型未下载

**解决**:
```bash
# 1. 检查Ollama服务
curl http://localhost:11434/api/tags

# 2. 下载模型
ollama pull qwen2.5:0.5b

# 3. 启动服务
ollama serve
```

### Issue: Notion同步失败

**原因**: Token无效或权限不足

**解决**:
```bash
# 1. 验证token
curl -H "Authorization: Bearer $NOTION_TOKEN" \
     https://api.notion.com/v1/databases

# 2. 检查Notion中是否为该Integration授予权限
#    (Notion页面 → ... → Connections → 检查litengram)

# 3. 检查database_id格式（需要去掉所有-）
```

更多见 [troubleshooting.md](docs/troubleshooting.md)

---

## 📊 Papers Currently Supported

| 论文 | 状态 | 高亮数 | 备注 |
|------|------|--------|------|
| Walther et al. (2009) | ✅ 完成 | 25 | "Natural Scene Categories are Reflected in..." |
| Kriegeskorte et al. (2008) | ⏳ 进行中 | 0 | "Matching Categorical Object Representations..." |
| Lamichhane et al. (2020) | ✅ 完成 | 52 | "Exploring brain-behavior relationships in N-back" |

**添加新论文**:
```bash
# 1. 在Zotero中打开PDF，进行高亮和批注
# 2. 运行:
python scripts/synthesize_notes.py --paper-id "YourAuthor2024" --parent-item-id XXXX

# 3. （可选）同步到Notion
```

---

## 🎯 Key Features Explained

### Feature 1: Zero-Cost Local LLM

- **为什么**: API调用费用太高 (OpenAI: $0.002/1K tokens)
- **解决**: 用Ollama本地运行小模型 (qwen2.5:0.5b: ~400MB, 0成本)
- **权衡**: 速度 vs 成本 (推理~5s/条 annotation)

```python
# 本地模型 vs API模型对比
Local:  qwen2.5:0.5b  → 1.3GB模型, 0成本, 无隐私风险
API:    GPT-4 Turbo   → $0.002/1K tokens, 需联网, 有数据留存
```

### Feature 2: Knowledge Fingerprinting

- **为什么**: 同一概念可能在多篇论文中出现
- **解决**: 生成MD5指纹，跨论文关联相同概念
- **用途**: 构建个人的概念知识库

```python
# 例: 学了5篇关于WM的论文
fingerprint("Working Memory") = "abc123..."
# → 自动找到其他4篇论文中对WM的定义
# → 比较异同，构建完整理解
```

### Feature 3: Soft 关联 Mechanism

- **为什么**: 并非所有关联都是"完全相同"
- **解决**: 允许语义相似但措辞不同的定义建立关联
- **例子**: "WM" vs "Working Memory" vs "短时记忆"

---

## 🔄 Workflow Example

**从头到尾使用LitEngram的完整流程**:

```
Day 1: 阅读论文
  → 在Zotero中打开PDF
  → 高亮重要段落（系统自动检测）
  → 手动输入【定义】部分（其他3层可留空）

Night 1: 生成笔记
  → python scripts/synthesize_notes.py --paper-id "MyPaper2024"
  → 系统自动填充【本文角色】【论证关联】【延伸】
  → 生成12部分结构化笔记

Night 1 (可选): 同步到Notion
  → python scripts/notion_sync.py
  → Notion页面自动出现今天的标注

Day 7: 跨论文复习
  → Notion "每日读读文献" 页面
  → 看到过去7天所有的4层笔记
  → 一眼看到哪些概念重复出现
  → 建立论文间的联系

Week 4: 写作时
  → 需要WM相关素材?
  → 搜索knowledge graph
  → 找到所有论文中对WM的理解
  → 组织成文章的一部分
```

---

## 📖 Important Updates

### 🆕 Critical Bug Fix (2026-09-09)

Zotero UI无法渲染注释，尽管数据库中有数据。

**根因**: `authorName = NULL` → Zotero UI跳过渲染  
**修复**: 所有annotation现在都设置 `authorName = 'Lintergram'`  
**防范**: 使用 `scripts/zotero_annotation_sync.py` 进行安全写入

[详见 Root Cause Analysis](README.md#critical-bug-fix-annotation-display-2026-09-09)

---

## 🤝 Contributing

欢迎贡献！主要改进方向：

- [ ] 支持更多论文领域（不仅限neuroscience）
- [ ] Web UI可视化知识图谱
- [ ] 批量导入论文
- [ ] 知识图谱导出 (GraphML / JSON-LD)
- [ ] Obsidian/Logseq集成

参见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 📄 License

MIT License — 详见 [LICENSE](LICENSE)

---

## 👤 Author & Support

**Creator**: LitEngram Agent  
**GitHub**: https://github.com/cyracaid/litengram  
**Issues**: https://github.com/cyracaid/litengram/issues

---

## 🔗 Related Resources

- [Zotero官方文档](https://www.zotero.org/support/)
- [Ollama官方](https://ollama.ai)
- [Notion API](https://developers.notion.com)
- [Literature Analysis Framework](references/literature_analysis_framework.md)

---

**最后更新**: 2026-09-09  
**版本**: v1.3 (with Annotation Display Bug Fix)
