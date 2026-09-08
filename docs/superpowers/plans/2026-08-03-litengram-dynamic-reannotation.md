# LitEngram 动态标注重跑 — 打破一次性管线

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stage 4-5 运行时自行查询 Zotero annotation count 动态决定模式，不依赖 Stage 1-2 缓存；增加"重新标注"入口让用户划线后可单独重跑标注阶段。

**Architecture:** Stage 1-2 的 annotation_count 降级为"初步标记"；Stage 4-5 启动时通过 Zotero API 实时查询当前标注数量，自主判定 Mode A/B。新增 `/reannotate <paper>` 触发词，跳过 Stage 1-3 直接进入 4-5-6-7。

**Tech Stack:** Python + Zotero local API + SQLite + Markdown

---

### Task 1: stage_4-5_annotations.md — 运行时动态查询标注数

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_4-5_annotations.md`

- [ ] **Step 1: 在输入节之后、步骤 1 之前，增加"启动时查询标注"步骤**

找到文件中的 `## 步骤` → `### 1. 读参考文件`，在其之前插入：

```markdown
### 0. 启动时查询当前标注数（动态模式判定）

**不依赖 Stage 1-2 的 annotation_count**——运行时自行查询 Zotero API：

```bash
curl -s "http://127.0.0.1:23119/api/users/0/items/{attachmentKey}/children?itemType=annotation"
```

- `count > 0` → 模式 A（混合）：标注已有 annotation + AI 补充嵌入笔记
- `count === 0` → 模式 B（纯 AI）：全部 AI 标注嵌入笔记

同时通过 SQLite 查询已有 annotation 的 itemID 和当前 comment 状态：

```sql
SELECT ia.itemID, i.key, ia.type, ia.comment, ia.text 
FROM itemAnnotations ia 
JOIN items i ON ia.itemID = i.itemID 
WHERE ia.parentItemID = {attachmentItemID}
```

- `comment 为空或仅含 [AI] 前缀` → 需要写入/覆盖
- `comment 已有有意义内容` → 跳过（保留用户/之前的注释）
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/references/stage_4-5_annotations.md
git commit -m "feat: stage_4-5 queries annotation count at runtime, not from Stage 1-2 cache"
```

---

### Task 2: stage_1-2_intake.md — 标注数降级为初步标记

**Files:**
- Modify: `~/.agents/skills/litengram/references/stage_1-2_intake.md`

- [ ] **Step 1: 修改"获取全文 + 已有标注"步骤**

找到文件中的这段：

```markdown
### 2. 获取全文 + 已有标注

通过 Zotero 定位论文并提取 PDF，检查已有标注数量：
- `annotations > 0` → 模式 A（混合标注）
- `annotations === 0` → 模式 B（AI 智能标注）
```

改为：

```markdown
### 2. 获取全文 + 已有标注

通过 Zotero 定位论文并提取 PDF，检查已有标注数量作为初步标记：
- `annotations > 0` → 初步标记为"有划线"（最终模式由 Stage 4-5 运行时动态判定）
- `annotations === 0` → 初步标记为"无划线"

> **注**：此标记仅供 Stage 3 分析时了解上下文。Stage 4-5 启动时会重新查询当前标注数，
> 因此用户在 Stage 1-3 期间新增的划线不会被遗漏。
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/references/stage_1-2_intake.md
git commit -m "docs: downgrade annotation count in stage_1-2 to preliminary marker"
```

---

### Task 3: SKILL.md — 添加"重新标注"入口和独立触发

**Files:**
- Modify: `~/.agents/skills/litengram/SKILL.md`

- [ ] **Step 1: 在调度表之后、"各阶段 Prompt 模板"之前，添加重新标注入口**

在 `## 调度表` 节和 `## 各阶段 Prompt 模板` 节之间插入：

```markdown
## 局部重跑入口

用户可随时对已完成论文单独重跑标注阶段（Stage 4-5-6-7）：

**触发词**: "重新标注" / "reannotate" / "处理划线" / "加标注" / "标注这篇" + 论文标识

**流程**:
```
1. 从 Zotero 获取论文 itemKey / attachmentKey / parentItemID
2. Stage 4-5: 运行时查询当前标注数 → 动态判定模式 → 生成标注
3. Stage 6: 更新笔记中 📌 关键标注 节
4. Stage 7: 同步 Zotero 子笔记 + 本地 .md + Notion
```

**跳过**: Stage 1-2（无需重新判定优先级）和 Stage 3（已有分析文本复用）。
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/SKILL.md
git commit -m "feat: add re-annotate entry point — user can reprocess highlights after the fact"
```

---

### Task 4: SKILL.md — Stage 4-5 的 task prompt 中传入当前标注查询指令

**Files:**
- Modify: `~/.agents/skills/litengram/SKILL.md`

- [ ] **Step 1: 更新 Stage 4-5 Prompt 模板节**

找到：

```markdown
### Stage 4-5: Cognitive Annotation + Reviewer
```

在其下的描述中，确保说明 Stage 4-5 的 task prompt 接收的输入包含 `attachmentKey` 用于实时查询标注。

将：

```markdown
执行 prompt 在 `references/stage_4-5_annotations.md`，须先读：
- `references/annotation_guidelines.md`
- `references/concept_excavation.md`
- `references/reviewer_protocol.md`
```

改为：

```markdown
执行 prompt 在 `references/stage_4-5_annotations.md`。主 agent 传入 `attachmentKey` + `attachmentItemID`，
Stage 4-5 启动时自行查询 Zotero API 获取当前标注数，动态判定模式。

须先读：
- `references/annotation_guidelines.md`
- `references/concept_excavation.md`
- `references/reviewer_protocol.md`
```

- [ ] **Step 2: 提交**

```bash
git add ~/.agents/skills/litengram/SKILL.md
git commit -m "docs: ensure stage_4-5 receives attachmentKey for runtime annotation query"
```

---

### Task 5: 验证 — 对 Dhamala 2023 模拟"用户后加划线"场景

**Files:**
- 只读: Zotero SQLite（检查当前标注数）
- 修改: 无（纯验证）

- [ ] **Step 1: 检查当前标注数**

```bash
curl -s "http://127.0.0.1:23119/api/users/11261922/items/KEFDT4YT/children?itemType=annotation" | python3 -c "
import json,sys
a=json.load(sys.stdin)
print(f'Current annotations: {len(a)}')
for x in a:
    print(f'  itemID(needs SQLite): key={x[\"key\"]}, text={x[\"data\"].get(\"annotationText\",\"\")[:50]}, comment={x[\"data\"].get(\"annotationComment\",\"\")[:30]}')
"
```

- [ ] **Step 2: 如果 count > 0，按 Stage 4-5 新流程跑 Mode A**

生成 UPDATE SQL 更新每条已有 annotation 的 comment，同时保持 📌 关键标注表格。

- [ ] **Step 3: 确认 Zotero 不卡死 + 注释出现在 PDF 中**

重启 Zotero，打开 PDF，确认每条划线旁有注释。

- [ ] **Step 4: 提交（如有改动）**

```bash
git add litreview/Dhamala2023_BrainPredictiveModeling.md
git commit -m "verify: mode A re-annotation works with runtime annotation query"
```
