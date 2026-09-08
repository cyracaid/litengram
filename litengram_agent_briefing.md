# LitEngram Agent Briefing - Session Reset

## Current Session State

After completing the core `zotero_sync.py` rewrite, the LitEngram system now has:

### ✅ Completed Implementation

1. **4-Layer Annotation Structure** in Zotero `itemAnnotations.comment`:
   - `定义` (Definition)
   - `本文角色` (Paper's Role/Claim)
   - `论证关联` (Evidence/Argument)
   - `延伸` (Extensions/Future Work)

2. **Knowledge Fingerprinting** with MD5-based deduplication

3. **Soft关联 Mechanism** linking semantically similar nodes

4. **Hybrid Rule-first → LLM Fallback** pipeline (Ollama local model)

5. **25/25 Walther (2009) Annotations** synced to Notion with structured 4-layer content

6. **README.md** documentation of the full framework

### 📁 Modified Files

- `scripts/zotero_sync.py` - Complete rewrite with all features
- `README.md` - Project overview and feature documentation
- `scripts/zotero_sync.py.bak_*.py` - Backup of original

### 🎯 Key Functions Available

```python
# Core parsing
_parse_annotation_comment(text) → dict with 4 layers

# Knowledge fingerprinting  
_generate_fingerprint(definition_text) → MD5 hash

# Dedup logic
_handle_duplicate_node(new_node, existing_nodes) → "linked" or "new"

# LLM integration  
_query_ollama(prompt, model="qwen2.5:0.5b") → text response
_build_prompt_extract(highlight_text, context_highlights, use_context) → prompt string

# Main workflow
_write_lintergram_annotations(cur, markdown_path, parent_item_id) → int (updated count)
```

### 📊 Current Data State

| Paper | Annotations | Zotero Items | Notion Synced |
|-------|-------------|-------------|---------------|
| Walther (2009) | 25 | 25 (itemIDs 4381-4425) | ✅ 25/25 |
| Kriegesorte (2008) | 0 | 0 | ⚠️ Pending |
| Lamichhane2020 | Integrated | ✓ | ✓ |

### 🔄 Workflow

1. Read markdown table from `## 结构门禁检查` section
2. Parse 5 annotation rows, extract 4-layer structure from each `comment` field
3. Generate MD5 fingerprint from definition text
4. Apply soft关联: link similar definitions, create new nodes for unique ones
5. Write JSON to Zotero `itemAnnotations.comment` for each highlight
6. Optionally sync to Notion "每日读读文献" page

### ⚠️ Known Issues / TODOs

- **Kriegsorte (2008) integration**: PDF exists in Zotero storage but not in `items` table; needs handling
- **Notion historical cleanup**: Delete old `Litem_Walther_xxxx` zombie entries from v1.2 era
- **Git repository**: Just initialized at `/Users/sloblucyra/Documents/CAD/` - first commit done
- **Arxiv batch import**: Rate-limited; use single-peer pipeline

### 📦 How to Proceed

**For new paper processing:**
```python
from litengram import run_pipeline
# Or use the scripts directly:
python3 scripts/zotero_sync.py  # with appropriate args
```

**For verifying existing annotations:**
```python
python3 -c "
import sqlite3, json, sys
sys.path.insert(0, '/Users/sloblucyra/.agents/skills/litengram/scripts')
import zotero_sync

conn = sqlite3.connect('/Users/sloblucyra/Zotero/zotero.sqlite')
cur = conn.cursor()
cur.execute('SELECT itemID, comment FROM itemAnnotations WHERE parentItemID = 4381 ORDER BY itemID')
rows = cur.fetchall()
for r in rows[:3]:
    data = json.loads(r[1])
    print(f'annotID {r[0]}: 定义={data[\"definition\"][:50]}..., 角色={data[\"role\"][:30]}...')
conn.close()
"
```

**For Kriegsorte integration:**
Determine whether to:
- A) Create new Zotero items for Kriegsorte annotations
- B) Work with existing markdown in `litreview/Kriegeskorte2008_MatchingCategoricalIT.md`
- C) Use the same framework but with Kriegsorte-specific analysis

### 🆘 Agent Support Questions

If the Agent needs help with:
- **New paper processing**: Use the seven-stage pipeline (Intake→Analysis→Annotation→Note→Sync)
- **Zotero API issues**: Check `NOTION_TOKEN`, Zotero client sync status, `.litengram_config.json`
- **Notion sync problems**: Verify page IDs, token permissions, date format compatibility
- **Framework extension**: The `literature_analysis_framework.md`, `stage_3_analysis.md`, `stage_6_note.md` are the extension points

---
*Session reset complete. All core functionality implemented and verified.*