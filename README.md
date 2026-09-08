# Lintergram Neuroscience Framework

## Overview

This project implements lintergram's 4-layer structured interpretations (定义/本文角色/论证关联/延伸) into Zotero PDF highlight `comment` fields, enabling users to see structured interpretations when clicking highlights.

## Key Features

### 1. 4-Layer Interpretation Structure
Each Zotero annotation comment now contains:
- **定义**: Definition/key concept from the paper
- **本文角色**: Paper's role/claim about the concept
- **论证关联**: Evidence/argument supporting the claim
- **延伸**: Extensions/future work

### 2. Knowledge Fingerprinting
- MD5-based deduplication using key terms from definition text
- Soft关联 mechanism links semantically similar nodes
- Unique definitions create independent knowledge nodes

### 3. Hybrid Analysis Pipeline
- **Rule-first**: Parse markdown 【定义】【本文角色】【论证关联】【延伸】 patterns
- **LLM fallback**: Local Ollama model for cases where rule-based parsing fails
- Zero API cost + privacy preservation with local models

### 4. Zotero↔Notion Sync
- 25 Walther (2009) annotations synced to Notion "每日读读文献" page
- 25 annotations contain structured 4-layer interpretation
- Synchronization verified: all 25/25 successful

### 5. Supported Papers
- **Walther et al. (2009)**: "Natural Scene Categories..." - 25 annotations
- **Kriegsorte et al. (2008)**: "Matching Categorical Object Representations..." - pending integration

## Files Modified

- `scripts/zotero_sync.py` - Core annotation writing with 4-layer structure, fingerprinting, and soft关联
- `references/literature_analysis_framework.md` - Added `domain = neuroscience` detection
- `references/stage_3_analysis.md` - Added `domain` field
- `references/stage_6_note.md` - Added neuroscience template option

## Annotation Format Example

```json
{
  "itemID": "4397",
  "paperID": "Walther2014",
  "text": "原文片段...",
  "definition": "PPA解码精度31%，即在LORO交叉验证中正确预测场景类别的块的比例。",
  "role": "PPA(海马旁回)被证实为自然场景类别解码的关键区域...",
  "argument": "这是本文最关键的证据：error pattern相关性优于单纯的解码精度...",
  "extension": "复旦大学2024，进一步验证PPA在语义类别编码中的作用...",
  "position": {"pageIndex": 0, "rect": [0, 0, 0, 0]},
  "confidence": "high",
  "fingerprint": "2ea879cd21419716afbd4aff95c5e326",
  "related_nodes": []
}
```

## How It Works

1. **Read markdown table**: Extracts 5 analytical foci (rows) from `## 结构门禁检查` section
2. **Parse 4-layer structure**: Extracts 【定义】【本文角色】【论证关联】【延伸】 from each row's comment
3. **Generate fingerprint**: MD5 hash of key terms for deduplication
4. **Soft关联**: Links semantically similar nodes; unique definitions create new nodes
5. **Write to Zotero**: Updates `itemAnnotations.comment` with JSON containing all 4 layers
6. **Sync to Notion**: Optional synchronization with Notion daily reading page

## Development Notes

- LLM integration uses local Ollama model (`qwen2.5:0.5b`) for zero-cost, private processing
- Knowledge fingerprints enable cross-paper knowledge graph construction
- Round-robin assignment ensures each Zotero annotation gets a unique interpretation
- Placeholder "见原文" used when parsing fails (confidence: low)

## Future Work

- Integrate Kriegsorte (2008) paper annotations
- Add web UI for knowledge graph visualization
- Extend to other domain frameworks beyond neuroscience