# FAQ — Frequently Asked Questions

## Installation & Setup

### Q: Ollama 占用多少空间？

**A**: 取决于模型大小：
- qwen2.5:0.5b: ~1.3GB (推荐 ✅)
- mistral:latest: ~7GB
- llama2: ~5GB

总共占用 (Ollama + 1 model): ~2-10GB

建议：SSD充足的机器（>50GB可用空间）

### Q: 支持 Windows 吗？

**A**: 支持！三种方式：

1. **WSL2 (推荐)**: Windows Subsystem for Linux
   ```bash
   wsl --install -d Ubuntu
   # Then follow macOS/Linux instructions
   ```

2. **Native Python** (直接)
   ```cmd
   pip install -r requirements.txt
   # But Ollama must run separately
   ```

3. **Docker**:
   ```bash
   docker run -it litengram:latest
   ```

### Q: 必须使用 Notion 吗？

**A**: 不必须。Notion 是**可选的**：

- ✅ **Without Notion**: 完整功能，笔记存在 Zotero 中
- ✅ **With Notion**: 额外获得知识图谱 + 仪表板

```bash
# 禁用 Notion (节省时间)
export NOTION_SYNC=false
python scripts/synthesize_notes.py ...
```

---

## Usage & Processing

### Q: 为什么需要本地 LLM？

**A**: 三个主要原因：

1. **成本**: 
   - Ollama 本地: $0 (一次性下载)
   - API 调用 (OpenAI/Claude): $0.50-2.00 per 1000 annotations
   - 50 papers × 50 annotations = $1250-5000 💸

2. **隐私**:
   - 本地: 你的笔记永远不离开电脑 ✅
   - API: 你的笔记被发送到云服务 ⚠️

3. **离线工作**:
   - 本地: 无需网络 ✅
   - API: 需要持续连接 ⚠️

### Q: 我可以用更好的模型吗？ (Claude/GPT-4)

**A**: 可以！但需要修改代码：

```python
# 修改 scripts/synthesize_notes.py
# 替换 Ollama 调用为 OpenAI API

import openai

def parse_annotation_openai(text, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": ...}]
    )
    return response.choices[0].message['content']
```

**权衡**:
- ✅ 质量更好 (GPT-4 > Claude > Mistral > qwen2.5)
- ❌ 成本更高 ($0.02-0.06 per annotation)
- ❌ 隐私顾虑 (数据上传)
- ❌ 需要 API key

**建议**: 保留 Ollama 默认，只在关键论文用 GPT-4

### Q: 处理一篇论文需要多长时间？

**A**: 取决于注释数量和模型：

| 注释数 | qwen2.5:0.5b | mistral:latest |
|--------|------------|-------------|
| 10 | ~15s | ~25s |
| 50 | ~45s | ~90s |
| 100 | ~90s | ~180s |

包括:
- 提取注释: ~5s
- 规则解析: ~2s per annotation
- LLM 生成: ~3-10s per annotation
- Notion 同步: ~5s
- 数据库写入: ~2s

---

## Data & Knowledge Management

### Q: 我的数据安全吗？

**A**: 完全安全！数据流：

```
你的电脑
  ├─ Zotero DB (SQLite, 本地)
  ├─ Ollama (本地 LLM, 无网络)
  └─ Notion (可选, 你的 token 控制)
```

**No external APIs** (除非你明确启用 Notion)

**最佳实践**:
1. Keep `NOTION_TOKEN` in `.env` (not in code)
2. Never commit `.env` to git
3. Use `.gitignore` to exclude sensitive files
4. Review Notion sharing settings periodically

### Q: 可以导出我的笔记吗？

**A**: 支持多种格式！

```bash
# Markdown
python scripts/export.py --format markdown --output ~/notes.md

# JSON (for data science)
python scripts/export.py --format json --output ~/notes.json

# CSV (for spreadsheet)
python scripts/export.py --format csv --output ~/notes.csv

# BibTeX (for LaTeX)
python scripts/export.py --format bibtex --output ~/thesis.bib

# Obsidian (for Obsidian vault)
python scripts/export.py --format obsidian --output ~/Obsidian/LitEngram
```

### Q: 如何处理新领域？ (非神经科学)

**A**: LitEngram 框架是通用的！

1. **修改 4 层结构** (如需要):
   ```bash
   # 编辑 references/annotation_guidelines.md
   # 改成你领域的术语
   ```

2. **添加领域检测** (自动):
   ```python
   # 修改 literature_analysis_framework.md
   # 添加你的领域 (物理/化学/社会学等)
   ```

3. **测试**:
   ```bash
   python scripts/synthesize_notes.py --paper-id "MyDomain2024" --parent-item-id 123
   ```

---

## Troubleshooting

### Q: "Zotero 数据库被锁定"

**A**: Zotero 还在使用数据库

**解决**:
```bash
# 强制关闭 Zotero
pkill -9 Zotero

# 清理锁文件
rm ~/Zotero/zotero.sqlite-journal

# 重试
python scripts/synthesize_notes.py ...
```

### Q: "Ollama 连接被拒绝"

**A**: Ollama 服务未运行

**解决**:
```bash
# 启动 Ollama
ollama serve &

# 等待启动
sleep 2

# 测试连接
curl http://localhost:11434/api/tags

# 重试
python scripts/synthesize_notes.py ...
```

### Q: "Notion token 无效"

**A**: Token 已过期或权限不足

**解决**:
1. 访问 https://www.notion.so/my-integrations
2. 重新生成 token (或创建新的)
3. 更新环境变量:
   ```bash
   export NOTION_TOKEN=ntn_new_token_here
   ```
4. 测试:
   ```bash
   python scripts/notion_sync.py --test
   ```

### Q: "LLM 输出不匹配 4 层结构"

**A**: 模型产生格式错误

**诊断**:
```python
# 检查 Ollama 日志
tail -f ~/.ollama/logs/ollama.log

# 尝试更好的模型
export OLLAMA_MODEL=mistral:latest
```

**临时修复**: 在 Zotero 中手动编辑注释
```
【定义】您的定义...
【本文角色】...
【论证关联】...
【延伸】...
```

---

## Advanced

### Q: 如何自定义 4 层结构？

**A**: 编辑解析规则：

```bash
# 打开框架文件
vim references/annotation_guidelines.md

# 修改正则表达式 (例如改成 [[ ]] 而不是 【 】)
# 修改层名称 (例如改成英文)
# 修改 LLM 提示词

# 重新运行
python scripts/synthesize_notes.py --paper-id "TestPaper" --parent-item-id 123
```

### Q: 可以与他人协作吗？

**A**: 可以！方式：

1. **共享 Notion Database** (推荐):
   - 在 Notion 中邀请协作者
   - 他们看到你的笔记 + 评论
   - 实时更新

2. **Git 分支** (代码贡献):
   - Fork 仓库
   - 创建分支
   - 提交 PR (见 CONTRIBUTING.md)

3. **共享导出**:
   ```bash
   # 导出为 JSON/CSV
   python scripts/export.py --format json --output ~/shared_notes.json
   # 分享文件给团队
   ```

### Q: 如何监控处理进度？

**A**: 启用详细日志：

```bash
# 增加日志级别
export DEBUG=true

# 运行
python scripts/synthesize_notes.py --paper-id "MyPaper" --verbose

# 输出示例:
# ✓ Connected to Zotero DB
# ✓ Found 52 annotations
# ✓ Annotation 1/52: parsing...
# ✓ Annotation 2/52: LLM generating...
# ...
# ✓ All 52 processed successfully
```

### Q: 能否与 Obsidian/Logseq 集成？

**A**: 可以！

```bash
# 导出为 Obsidian 格式
python scripts/export.py --format obsidian --output ~/Obsidian/LitEngram

# 或导出为 Logseq 格式
python scripts/export.py --format logseq --output ~/Logseq/journals
```

然后在 Obsidian/Logseq 中打开文件夹。

完整集成见 [INTEGRATIONS.md](INTEGRATIONS.md)

---

## Contributing & Support

### Q: 我如何报告 bug？

**A**: 提交 GitHub issue：

1. 访问 https://github.com/cyracaid/litengram/issues
2. 点击 "New issue"
3. 标题: `[BUG] 简短描述`
4. 描述:
   - 症状
   - 重现步骤
   - 预期 vs 实际
   - 环境 (OS, Python version, etc)

### Q: 我可以贡献新功能吗？

**A**: 欢迎！见 [CONTRIBUTING.md](../CONTRIBUTING.md)

---

更多问题？提交 GitHub Discussion 或发邮件至 [support email]
