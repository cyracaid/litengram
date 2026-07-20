# Stage 4-5: Cognitive Annotation + Reviewer

> 由 LitEngram meta-skill 调度。生成混合标注并写入 Zotero，执行审稿人自审。

## 输入

从主 agent 处接收：
- 分析结果（Stage 3 产出）
- 论文全文
- 已有标注清单

## 步骤

### 1. 读参考文件

- `references/annotation_guidelines.md` — 4 层标注结构 + 混合标注规则
- `references/concept_excavation.md` — 9 层深挖规格（标注中嵌深挖）
- `references/reviewer_protocol.md` — 7 维度审稿人自审

### 2. 生成标注

按模式 A（用户已划线）或模式 B（纯 AI）执行。每条标注含 4 层批注 + 概念溯源。

写入 Zotero SQLite：关 → 写 → 开。

### 3. 审稿人自审

⛰️ 级强制，⚔️ 级可选，📌/🌫️ 跳过。
用敌对视角审视笔记初稿，输出 7 维度评估 + 攻击点。

## 输出

```json
{
  "annotations": {"user": 0, "ai": 0, "total": 0},
  "annotation_coverage": ["Intro", "Methods", "Results", "Discussion"],
  "reviewer": {
    "performed": true,
    "weakest_claim": "",
    "challenges": []
  }
}
```
