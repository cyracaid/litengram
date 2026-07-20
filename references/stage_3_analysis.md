# Stage 3: Deep Analysis — 5 维度解剖

> 由 LitEngram meta-skill 调度。对论文做 5 维度分析，收集概念深挖素材。

## 输入

从主 agent 处接收：
- 论文全文摘要
- 优先级信息
- 研究上下文

## 步骤

### 1. 读参考文件

- `references/literature_analysis_framework.md` — 5 维度分析范式、三层拆解、质量检查
- `references/concept_excavation.md` — 了解概念深挖素材收集标准（9 层规格）

### 2. 执行三遍读法

按框架执行三遍读法 → 5 维度解剖 → 统计完整性检查。

### 3. 收集概念深挖素材

遇到关键术语（方法、概念、理论）时记录：
- 术语名称 + 类别
- 出现位置
- 是否需要深挖（简单定义 / 标准 9 层 / 对比辨析）

## 输出

返回以下结构给主 agent：

```json
{
  "dimension_1": {"known": [], "gap": [], "aim": ""},
  "dimension_2": {
    "layer_1": "操作描述",
    "layer_2": {"whys": [], "stats_checklist": {}},
    "layer_3": "方法局限"
  },
  "dimension_3": {"findings": []},
  "dimension_4": {"strategy": ""},
  "dimension_5": {"importance": ""},
  "concept_targets": [
    {"term": "gPPI", "category": "method", "depth": "standard"}
  ],
  "analysis_text": "完整分析文本（供下游 Stage 6 消费）"
}
```
