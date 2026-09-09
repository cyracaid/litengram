# Notion Integration — LitEngram 完整指南

完整的 Notion 同步配置与使用指南。

---

## 🎯 Notion 同步是什么？

Notion 同步让你可以将结构化笔记从 Zotero 自动导出到 Notion，构建**知识仪表板**。

### 工作流程

```
Zotero (本地)
  ↓ (LitEngram处理)
  ├─ 4层结构注释
  ├─ 知识指纹
  └─ 元数据
       ↓ (自动同步)
Notion (云端)
  ├─ 每日读读文献 (主database)
  ├─ 概念链接 (fingerprints)
  └─ 论文仪表板 (dashboard)
```

### 为什么需要 Notion？

| 需求 | Zotero 本地 | + Notion 云端 |
|------|-----------|------------|
| 查看笔记 | ✅ (在PDF中) | ✅ (网页/手机) |
| 搜索跨论文 | ⚠️ (麻烦) | ✅ (快速) |
| 链接相关概念 | ❌ | ✅ (自动fingerprint链接) |
| 分享给他人 | ❌ | ✅ (共享页面) |
| 协作编辑 | ❌ | ✅ (多人实时) |
| 移动访问 | ❌ | ✅ (手机App) |
| 数据备份 | ⚠️ (Zotero自己管) | ✅ (Notion云端) |

---

## 🔧 完整设置步骤

### Step 1: 在 Notion 创建 Internal Integration

**目的**: 让 LitEngram 获得 Notion 访问权限

```
1. 打开: https://www.notion.so/my-integrations
2. 点击: "Create new integration"
3. 填写:
   - Name: "LitEngram"
   - Logo: (可选)
   - Associated workspace: 你的workspace
4. 点击: "Submit"
5. 复制: "Internal Integration Token"
   格式: ntn_xxxxx...
```

**重要**: 这个 token 要保密！相当于你的 Notion 密钥。

```bash
# 保存到环境变量 (不要提交到git!)
cat >> ~/.bash_profile << 'EOF'
export NOTION_TOKEN=ntn_xxxxx_your_token_here
EOF

source ~/.bash_profile

# 验证
echo $NOTION_TOKEN  # 应该显示你的token
```

### Step 2: 在 Notion 创建 Database

**在 Notion 中创建一个新页面作为 Papers Database**:

1. 打开 Notion
2. 创建新页面，命名: "LitEngram" (或你喜欢的名字)
3. 添加 Database：点击 "+" → 选择 "Table" Database
4. 配置列 (Columns):

| 列名 | 类型 | 用途 |
|------|------|------|
| **Title** | Text | 论文标题 + 作者 |
| **Authors** | Text | 第一作者 + et al |
| **DOI** | Text | 论文DOI (便于查找) |
| **Year** | Number | 发表年份 |
| **Journal** | Text | 期刊名 |
| **Annotations** | Toggle | 展开查看4层笔记 |
| **Concept Tags** | Multi-select | Fingerprints (概念标签) |
| **Status** | Select | 未读/阅读中/已完成 |
| **Summary** | Text | 一句话摘要 |
| **Notes** | Text | 个人评论 |

**示例配置**:
```
Title: "Lamichhane et al. (2020) - Exploring brain-behavior relationships"
Authors: "Lamichhane, P."
DOI: "10.1234/nature.12345"
Year: 2020
Journal: "Nature Neuroscience"
Annotations: [展开] ← 52条注释
Concept Tags: working-memory, fMRI, load-effects
Status: ✅ 已完成
Summary: "发现工作记忆负荷与激活呈倒U关系，peak at load 4"
```

### Step 3: 获取 Database ID

Database ID 是一个长字符串，用来告诉 LitEngram 要往哪个 Notion Database 写数据。

**从 URL 找到 Database ID**:

```
打开你刚创建的 Database (Notion 网页)
URL 会看起来像:
https://www.notion.so/workspace/abc123def456?v=xyz789

abc123def456 就是 Database ID
```

或者用 Notion API 自动查找:

```bash
# 测试 token 并列出所有 databases
python3 << 'EOF'
import os
import requests

token = os.environ['NOTION_TOKEN']
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

# 列出所有数据库
response = requests.post(
    "https://api.notion.com/v1/search",
    headers=headers,
    json={"filter": {"value": "database", "property": "object"}}
)

for db in response.json()['results']:
    print(f"{db['title'][0]['plain_text']}: {db['id']}")
EOF
```

### Step 4: 配置环境变量

```bash
cat >> ~/.bash_profile << 'EOF'
export NOTION_TOKEN=ntn_xxxxx_your_token_here
export NOTION_DATABASE_ID=abc123def456xyz789
export NOTION_SYNC=true  # 启用自动同步
EOF

source ~/.bash_profile

# 验证
echo $NOTION_TOKEN
echo $NOTION_DATABASE_ID
```

### Step 5: 在 Notion 给 LitEngram 权限

**关键步骤**: 告诉 Notion 允许 LitEngram Integration 访问你的 Database

```
1. 打开你的 Database
2. 点击右上角 "..." → "Connections"
3. 看到 "Integrations" 部分
4. 点击 "Connect to..."
5. 选择 "LitEngram"
6. 点击 "Select a connection"
7. 选择你的 Database
8. 点击 "Allow access"
```

**验证权限成功**:
```bash
python3 scripts/notion_sync.py --test

# 预期输出:
# ✓ Token valid
# ✓ Database accessible
# ✓ Can read: True
# ✓ Can write: True
```

---

## 🚀 使用 Notion 同步

### 方式 1: 自动同步 (推荐)

```bash
# 处理论文时自动同步到 Notion
python scripts/synthesize_notes.py \
  --paper-id "Lamichhane2020_Nback" \
  --parent-item-id 4429 \
  --sync-notion

# 输出:
# ✓ Processed 52 annotations
# ✓ Synced to Notion: abc123def456
```

### 方式 2: 手动同步单篇论文

```bash
python scripts/notion_sync.py \
  --paper-key "NIY96UDQ" \
  --database-id $NOTION_DATABASE_ID

# 输出:
# ✓ Paper: Lamichhane2020
# ✓ Title: "Exploring brain-behavior relationships..."
# ✓ Page ID: page_abc123def456
# ✓ Properties updated: 8
# ✓ Annotations block created: 52 items
```

### 方式 3: 批量同步所有论文

```bash
python scripts/notion_sync.py --sync-all

# 将所有处理过的论文同步到 Notion
# 输出:
# ✓ Paper 1/5: Walther2009 → page_1
# ✓ Paper 2/5: Kriegeskorte2008 → page_2
# ✓ Paper 3/5: Lamichhane2020 → page_3
# ... (more)
# ✓ All 5 papers synced successfully
```

### 方式 4: 禁用同步 (仅本地)

```bash
# 如果你不想用 Notion，可以禁用:
export NOTION_SYNC=false

python scripts/synthesize_notes.py \
  --paper-id "MyPaper" \
  --parent-item-id 123
  
# 只会在 Zotero 中更新，不会同步到 Notion
```

---

## 📊 Notion 中看到什么

### Database 视图

```
论文数据库 (Notion)
│
├─ Walther2009 - Natural Scene Categories
│   Authors: Walther, D.
│   Year: 2009
│   Concept Tags: scene-category, visual-recognition
│   Status: ✅ 已完成
│   Annotations: [展开] ▼
│       52 annotations grouped by type
│
├─ Lamichhane2020 - Exploring brain-behavior relationships  
│   Authors: Lamichhane, P.
│   Year: 2020
│   Concept Tags: working-memory, fMRI, load-effects ← fingerprints自动链接!
│   Status: ✅ 已完成
│   Annotations: [展开] ▼
│       52 annotations with 4-layer structure
│
└─ Kriegeskorte2008 - Matching Categorical Object Representations
    Authors: Kriegeskorte, N.
    Year: 2008
    Status: ⏳ 阅读中
```

### Annotations 展开视图

```
【定义】
Working memory (WM): short-term storage and manipulation of information,
Baddeley & Hitch (1974), capacity limit ~7±2 items

【本文角色】
This paper extends WM research from 2-back to full 1-6 load range

【论证关联】
Finding of inverted-U (peak at load 4) supports compensation hypothesis

【延伸】
- Test in aging populations (expect delayed peak)
- Compare with OSPAN working memory capacity measures
- Link to cognitive control literature
```

### Concept 链接视图

```
Concept: "working-memory"
出现在:
  ✓ Lamichhane2020 (52条)
  ✓ Smith2019 (定义相同)
  ✓ Kaplan2018 (相关概念)
  
Fingerprint: abc123def456
Link strength: 100% (定义相同)
```

---

## 🔗 高级: Notion 中的链接

### 概念链接 (Fingerprint Linking)

LitEngram 自动为相同概念创建链接:

```
在 Notion 中:

纸条1: "Working memory = short-term storage"
Fingerprint: abc123

纸条2: "WM = temporary information holding"
Fingerprint: abc123 ← 相同!

→ Notion 自动创建链接
→ 点击 Concept Tags 可看到相关论文
```

### 跨论文搜索

```
在 Notion 中查找所有讨论 "working memory" 的论文:

搜索框: "working-memory"
结果:
  ✓ Lamichhane2020 (52条注释)
  ✓ Smith2019 (15条注释)
  ✓ Kaplan2018 (8条注释)
  
总共: 75条相关注释
```

### 手动添加笔记

在 Notion 中编辑:

```
Lamichhane2020 页面
↓
Notes 字段:

"这篇论文的倒U形关系与我之前看的 Smith2019 不一致。
可能原因: 
  1. 样本差异 (年龄, 教育背景)
  2. 任务难度不同 (记忆力 vs 理解力)
  3. 扫描参数差异 (3T vs 7T fMRI)

下次阅读 Smith2019 时需要检查这些因素。"
```

---

## 💾 备份与导出

### 定期备份 Notion

```bash
# 每周自动备份 Notion 到本地
cat > ~/backup_notion_litengram.sh << 'EOF'
#!/bin/bash

# 导出整个 Database 为 CSV
python scripts/export.py \
  --format csv \
  --notion-database $NOTION_DATABASE_ID \
  --output ~/litengram-backups/backup-$(date +%Y%m%d).csv

# 导出为 JSON (完整数据)
python scripts/export.py \
  --format json \
  --notion-database $NOTION_DATABASE_ID \
  --output ~/litengram-backups/backup-$(date +%Y%m%d).json

echo "✓ Backup completed: ~/litengram-backups/"
EOF

chmod +x ~/backup_notion_litengram.sh

# 设置每周日晚上10点自动运行
crontab -e
# 添加这一行:
# 0 22 * * 0 ~/backup_notion_litengram.sh
```

### 从 Notion 导出

```bash
# 导出为 Markdown (用于其他工具)
python scripts/export.py \
  --format markdown \
  --notion-database $NOTION_DATABASE_ID \
  --output ~/notes-exported.md

# 导出为 BibTeX (用于论文)
python scripts/export.py \
  --format bibtex \
  --notion-database $NOTION_DATABASE_ID \
  --output ~/thesis.bib

# 导出为 Obsidian 格式
python scripts/export.py \
  --format obsidian \
  --notion-database $NOTION_DATABASE_ID \
  --output ~/Obsidian/LitEngram
```

---

## 🔐 安全 & 隐私

### Token 安全

```bash
# ✅ DO: 存在环境变量
export NOTION_TOKEN=ntn_xxxxx

# ❌ DON'T: 存在代码中
NOTION_TOKEN = "ntn_xxxxx"  # 不要!

# ❌ DON'T: 提交到git
git add .env  # 不要!
git add credentials.txt  # 不要!

# ✅ DO: 在 .gitignore 中
echo ".env" >> .gitignore
git add .gitignore
```

### 权限最小化

```
在 Notion Integration 中只给予必要权限:
✅ 读取 database
✅ 更新 database entries
✅ 创建 blocks
❌ 删除 database (除非需要)
❌ 创建新 database (除非需要)
❌ 删除 database (不要!)
❌ 转移 database (不要!)
```

### Token 轮换

```bash
# 每90天重新生成一次 token

# 1. 在 Notion 创建新 token
#    https://www.notion.so/my-integrations
#    → "LitEngram"
#    → Regenerate secret

# 2. 更新环境变量
export NOTION_TOKEN=ntn_xxxxx_new_token

# 3. 测试新 token
python scripts/notion_sync.py --test
# ✓ Token valid

# 4. 删除旧 token (可选)
```

---

## ❓ 常见问题

### Q: Notion 同步需要 Zotero 运行吗？

**A**: 不需要！同步只需要:
- ✅ Zotero DB (已在本地)
- ✅ Notion token (在环境变量)
- ✅ 网络连接 (上传到Notion)

关闭 Zotero 也可以同步。

### Q: 同步后能在 Notion 中编辑吗？

**A**: 可以！但要知道:
- ✅ 编辑 Notes/Summary 字段 → 保存在 Notion (推荐)
- ⚠️ 编辑 Annotations → 下次 LitEngram 运行时会被覆盖
- ✅ Annotations 中添加评论 → 保存在 Notion

### Q: 如果 Notion token 过期怎么办？

**A**: 重新生成 token:
```bash
# 1. 在 https://www.notion.so/my-integrations 中 Regenerate
# 2. 更新环境变量
export NOTION_TOKEN=ntn_xxxxx_new_token
# 3. 重新同步
python scripts/synthesize_notes.py ... --sync-notion
```

### Q: 可以与他人共享 Notion Database 吗？

**A**: 可以！两种方式:

方式1: 邀请为成员
```
在 Notion 中:
页面 → ... → Share
→ 输入邮箱 → 选择权限 → 发邀请
```

方式2: 公开共享链接
```
页面 → Share → Allow editing
→ 获得公开链接 → 分享给任何人
```

### Q: Notion 同步会暴露隐私吗？

**A**: 不会！数据流:
```
你的电脑 ──(你的token)──> Notion
                ↓
          只有你能访问
          (除非你主动分享)
```

LitEngram 不会:
- 记录你的 token
- 保存任何同步数据
- 追踪你的使用
- 与第三方分享

### Q: 如何删除 Notion 中的同步数据？

**A**: 在 Notion 中手动删除页面:

```
打开 LitEngram Database
→ 找到要删除的论文
→ 右键 → Delete
```

或者禁用同步后清空:

```bash
export NOTION_SYNC=false
python scripts/notion_sync.py --clear-all
# 警告: 这会删除所有 Notion 中的 LitEngram 数据!
```

---

## 📚 完整工作流示例

### Week 1: 阅读 + 处理 + 同步

```
Monday (Day 1):
  1. 在 Zotero 打开论文
  2. 阅读并高亮 52 处关键点
  3. 运行: python scripts/synthesize_notes.py --paper-id "MyPaper" \
           --parent-item-id 123 --sync-notion
  4. ✅ Notion 中看到论文已添加，52条注释已显示

Tuesday-Thursday:
  1. 在 Notion 中查看和编辑笔记
  2. 在 Notes 字段添加个人想法
  3. 标记 Concept Tags 用于交叉引用

Friday:
  1. 查看 Concept 链接，发现与其他论文的关系
  2. 基于链接，计划下周阅读的论文
```

### Month 1: 构建知识图谱

```
Week 1: 3 papers (47 annotations)
Week 2: 2 papers (34 annotations)  
Week 3: 4 papers (98 annotations)
Week 4: 2 papers (52 annotations)
─────────────────────────────────
Total: 11 papers, 231 annotations

在 Notion 中看到:
✓ 231 条结构化笔记
✓ 45 个链接的概念 (fingerprints)
✓ 所有论文可搜索
✓ 可基于 Concept Tags 浏览
```

---

## 🎯 总结

**Notion 同步让你能够**:
- 📱 在手机/网页上查看笔记 (不仅限PDF)
- 🔗 自动链接相同概念 (跨论文)
- 🔍 快速搜索所有注释
- 📊 构建知识仪表板
- 👥 与他人分享和协作
- 💾 云端自动备份

**记住**: Notion 同步是**可选的**。LitEngram 在本地也能完美工作！

---

更多信息见:
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - 如何有效使用
- [SECURITY.md](SECURITY.md) - Token 安全指南
- [FAQ.md](FAQ.md) - 常见问题解答
