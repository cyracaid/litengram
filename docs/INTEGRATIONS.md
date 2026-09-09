# Integrations — LitEngram

Connect LitEngram with other tools in your knowledge management workflow.

---

## 🟣 Notion Integration (完整指南)

**最受欢迎的集成!** 同步结构化笔记到 Notion，构建知识仪表板。

### 快速开始

```bash
# 1. 设置 token 和 database ID (见下面详细步骤)
export NOTION_TOKEN=ntn_xxxxx
export NOTION_DATABASE_ID=abc123def456

# 2. 启用 Notion 同步
export NOTION_SYNC=true

# 3. 处理论文时自动同步
python scripts/synthesize_notes.py \
  --paper-id "MyPaper" \
  --parent-item-id 123 \
  --sync-notion

# ✓ 论文和所有 52 条注释自动出现在 Notion!
```

### 核心功能

- ✅ **自动同步**: 4 层结构笔记自动导入 Notion
- ✅ **概念链接**: 相同 Fingerprint 自动创建交叉链接
- ✅ **移动访问**: 手机/网页查看 (不限于 PDF)
- ✅ **跨论文搜索**: 快速找到所有相关注释
- ✅ **协作编辑**: 与他人共享和协作
- ✅ **云端备份**: 自动备份到 Notion

### 完整配置指南

🔗 **详见**: [NOTION_SYNC_COMPLETE.md](NOTION_SYNC_COMPLETE.md) (4KB)

包含:
- Step-by-step 设置 (5 步)
- Notion Database 结构设计
- 4 种同步方式
- Notion 中看到什么
- 权限设置与安全
- 15+ 常见问题解答
- 完整工作流示例

---

## 🟠 Obsidian Integration

Export LitEngram notes to Obsidian vault:

```bash
python scripts/export.py --format obsidian --output ~/Obsidian/LitEngram
```

Features:
- Notes organized by paper
- Wikilinks between concepts (via fingerprints)
- Full 4-layer structure preserved
- Ready for graph view
- Bidirectional backlinks

---

## 🟦 Logseq Integration

Export to Logseq journal format:

```bash
python scripts/export.py --format logseq --output ~/Logseq/journals
```

Features:
- Daily entries per paper processed
- Nested blocks preserve 4-layer structure
- Tags auto-generated
- Ready for Logseq DB
- Compatible with Logseq queries

---

## 🔵 Roam Research

Export as JSON for Roam:

```bash
python scripts/export.py --format json --output ~/notes.json
```

Then in Roam:
1. Tools → Import JSON
2. Select exported file
3. Maps to Roam blocks automatically
4. Bidirectional links work across papers

---

## 📄 LaTeX / Overleaf

Export BibTeX + annotations:

```bash
python scripts/export.py --format bibtex --output ~/thesis.bib
```

Output:
- thesis.bib: All papers with metadata
- thesis-annotations.md: Notes per paper
- thesis-index.md: Concept index

In Overleaf:
1. Upload .bib file to project
2. Reference in main.tex: `\bibliography{thesis}`
3. Use `\cite{AuthorYear}` to cite
4. Annotations available as comments

---

## 🟠 Zotero Sync (Native)

LitEngram works directly with Zotero DB:
- No export needed
- Changes appear instantly in Zotero UI
- Comments visible on highlights
- Bidirectional (edit in Zotero, read in LitEngram)

Native sync **enabled by default** - no extra configuration needed.

---

## 🔗 Other Exports

### Markdown Export
```bash
python scripts/export.py --format markdown --output ~/notes.md
```
- Clean markdown structure
- Cross-paper concept links
- 4-layer structure preserved

### CSV Export (for spreadsheets)
```bash
python scripts/export.py --format csv --output ~/annotations.csv
```
- Rows: One per annotation
- Columns: Paper, layer1, layer2, layer3, layer4, fingerprint
- Import to Google Sheets, Excel, etc

### JSON Export (for developers)
```bash
python scripts/export.py --format json --output ~/data.json
```
- Complete structured data
- Preserves all metadata
- Ready for custom processing

---

## 📊 Integration Comparison Matrix

| 功能 | Notion | Obsidian | Logseq | Roam | Overleaf |
|------|--------|---------|--------|------|----------|
| 云端访问 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 移动App | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ |
| 自动同步 | ✅ | ⏳ | ⏳ | ⏳ | ⏳ |
| 概念链接 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 协作编辑 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 成本 | 免费/付费 | 免费 | 免费 | 免费 | 免费/付费 |
| 学习曲线 | 简单 | 中等 | 中等 | 简单 | 陡峭 |

---

## 🎯 推荐方案

### 初学者
👉 **推荐**: Notion + Zotero (原生)
- 自动同步无需配置
- 移动手机可访问
- 视觉界面友好

### 知识管理爱好者
👉 **推荐**: Notion (主) + Obsidian (备)
- Notion: 云端查看 + 协作
- Obsidian: 本地图谱 + 自定义

### 开发者/极客
👉 **推荐**: JSON 导出 + 自定义处理
- 完全控制数据
- 可构建自己的工具
- 无厂商锁定

### 论文写作
👉 **推荐**: Overleaf + BibTeX 导出
- 直接集成到论文
- 引用自动化
- 标准学术流程

---

## 🔐 集成安全最佳实践

### Notion Token
```bash
# ✅ DO: 环境变量
export NOTION_TOKEN=ntn_xxxxx

# ❌ DON'T: 代码中硬编码
NOTION_TOKEN = "ntn_xxxxx"

# ✅ DO: .env 文件 (git-ignored)
cat > .env << 'EOF'
NOTION_TOKEN=ntn_xxxxx
EOF

# 验证 .gitignore
echo ".env" >> .gitignore
```

### Zotero Database
```bash
# 确保权限正确
ls -la ~/Zotero/zotero.sqlite
# 应该显示: -rw------- (600)

# 如果错误，修复:
chmod 600 ~/Zotero/zotero.sqlite
```

---

## 📚 详细文档

- **[NOTION_SYNC_COMPLETE.md](NOTION_SYNC_COMPLETE.md)** ← Notion 完整指南 (强烈推荐!)
- **[BEST_PRACTICES.md](BEST_PRACTICES.md)** - 各集成的最佳用法
- **[SECURITY.md](SECURITY.md)** - Token 和隐私安全
- **[examples/](examples/)** - 实际工作流示例

---

## 🆘 集成故障排查

### Notion 同步失败
```bash
# 检查 token
echo $NOTION_TOKEN  # 应该不为空

# 检查 database ID
echo $NOTION_DATABASE_ID  # 应该不为空

# 测试连接
python scripts/notion_sync.py --test
```

### Obsidian 导出空文件夹
```bash
# 确保 output 目录存在
mkdir -p ~/Obsidian/LitEngram

# 重试导出
python scripts/export.py --format obsidian --output ~/Obsidian/LitEngram --verbose
```

### 概念链接不工作
```bash
# 确保 fingerprints 已生成
python scripts/synthesize_notes.py --paper-id "MyPaper" --compute-fingerprints

# 重新同步
python scripts/notion_sync.py --sync-all --force-update
```

---

更多帮助见 [FAQ.md](FAQ.md) 和 [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
