# LitEngram System Architecture

## Overview

LitEngram follows a **multi-stage pipeline architecture** designed for modularity and extensibility.

## Core Components

### 1. Zotero Integration Layer
- **Direct SQLite Access**: Read/write to `itemAnnotations` table
- **Transaction Management**: Atomic operations with `BEGIN IMMEDIATE`
- **Schema Validation**: PRAGMA integrity checks before processing
- **Concurrency Handling**: Database locking with 30s timeout

### 2. Parsing Pipeline

```
Input: Zotero Highlight
  ├─ Extract Text + Metadata
  ├─ Check for existing comment
  ├─ Validate coordinates/position
  └─ Store parent reference (parentItemID)
       ↓
Rule-First Parser
  ├─ Regex patterns for 【定义】【本文角色】【论证关联】【延伸】
  ├─ Confidence scoring (0-100)
  ├─ Handle edge cases (malformed markers, incomplete layers)
  └─ If success → proceed to Fingerprinting
       ↓ (if fail)
LLM Fallback (Ollama)
  ├─ Read full document context
  ├─ Generate missing layers
  ├─ Maintain 4-layer structure
  └─ Store confidence = "low"
       ↓
Output: Structured 4-Layer Comment
```

### 3. Knowledge Graph Layer

**Fingerprinting Algorithm**:
```python
def compute_fingerprint(definition_text):
    # Extract key terms from definition
    terms = extract_terms(definition_text)
    # Generate MD5 hash
    fingerprint = md5("|".join(sorted(terms))).hexdigest()
    return fingerprint
```

**Linking**:
- Same fingerprint → Same concept across papers
- Similar fingerprints → Related concepts (semantic similarity)
- Build transitive closures for concept families

### 4. Zotero Write-Back Layer

```sql
-- Critical update: MUST set authorName!
UPDATE itemAnnotations 
SET 
  comment = '<4-layer JSON>',
  authorName = 'Lintengram'
WHERE itemID = ?
```

**Why authorName?** Zotero UI skips rendering if `authorName IS NULL`

### 5. Optional Sync Layer (Notion)

- Uses Notion API (REST)
- Creates/updates database entries
- Maintains metadata (paper ID, annotation count, timestamp)
- Supports transactional rollback on failure

## Data Model

### itemAnnotations Schema (Zotero)

```sql
CREATE TABLE itemAnnotations (
  itemID INTEGER PRIMARY KEY,           -- Unique identifier
  parentItemID INT NOT NULL,            -- Reference to PDF attachment
  type INTEGER NOT NULL,                -- 1=highlight, 2=underline, 5=note
  authorName TEXT,                      -- ⚠️ CRITICAL: Must be set for UI rendering
  text TEXT,                            -- Original highlighted text
  comment TEXT,                         -- 4-layer structured comment (JSON-ish)
  color TEXT,                           -- Highlight color (e.g., #ffd400)
  pageLabel TEXT,                       -- Page number
  sortIndex TEXT,                       -- Sort order within page
  position TEXT,                        -- JSON: {"pageIndex": 0, "rects": [[...]]}
  isExternal INT NOT NULL,              -- 0=local, 1=external
  FOREIGN KEY (parentItemID) REFERENCES items(itemID)
);
```

### 4-Layer Comment Format

```json
{
  "1_definition": "Working memory (WM): short-term information storage and manipulation...",
  "2_role": "This paper extends WM research from 2-back to 1-6 load range",
  "3_argument": "This finding supports the inverted-U hypothesis of WM-activation",
  "4_extension": "Test this design in aging samples to understand lifespan trajectories",
  "confidence": "high",
  "fingerprint": "abc123def456",
  "metadata": {
    "llm_generated": false,
    "source": "rule-first",
    "timestamp": "2026-09-09T22:35:00Z"
  }
}
```

## Processing Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ 1. Initialize                                             │
├─────────────────────────────────────────────────────────┤
│ • Connect to Zotero SQLite                               │
│ • Close Zotero app (release DB lock)                     │
│ • Begin atomic transaction (BEGIN IMMEDIATE)             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Extraction                                             │
├─────────────────────────────────────────────────────────┤
│ • Query itemAnnotations WHERE parentItemID = ?           │
│ • Extract: text, position, color, pageLabel              │
│ • Check: existing comment status                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Parsing (Branching)                                   │
├─────────────────────────────────────────────────────────┤
│ For each annotation:                                     │
│  ├─ If has existing comment                              │
│  │  └─ Use existing (preserve user input)                │
│  ├─ Else try rule-first parser                           │
│  │  ├─ Regex extraction 【定义】【本文角色】etc         │
│  │  ├─ Confidence score                                  │
│  │  ├─ If confidence >= 0.8 → proceed                    │
│  │  └─ Else → fallthrough to LLM                         │
│  └─ Else (no comment, low confidence)                    │
│     └─ Use Ollama LLM                                    │
│         ├─ Read document context                         │
│         ├─ Generate all 4 layers                         │
│         └─ Mark as LLM-generated                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Knowledge Graph Generation                            │
├─────────────────────────────────────────────────────────┤
│ For each processed annotation:                           │
│  ├─ Extract key terms from【定义】                      │
│  ├─ Compute MD5 fingerprint                              │
│  ├─ Look up similar fingerprints                         │
│  ├─ Create/update concept node                           │
│  └─ Link to concept families                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Database Write-Back                                   │
├─────────────────────────────────────────────────────────┤
│ For each annotation:                                     │
│  • UPDATE itemAnnotations                                │
│    SET comment = <4-layer-json>                          │
│        authorName = 'Lintengram'                         │
│    WHERE itemID = ?                                      │
│  • Check rowcount == 1 (exactly one record updated)      │
│  • On error: ROLLBACK transaction                        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Commit & Verify                                       │
├─────────────────────────────────────────────────────────┤
│ • COMMIT transaction                                     │
│ • Verify PRAGMA integrity_check = 'ok'                   │
│ • Close connection                                       │
│ • Return status summary                                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Optional Notion Sync                                  │
├─────────────────────────────────────────────────────────┤
│ • Open Zotero (Notion sync only after DB release)        │
│ • POST to Notion API                                     │
│ • Create/update database entries                         │
│ • Log sync status                                        │
└─────────────────────────────────────────────────────────┘
```

## Error Handling

### Transaction Rollback Scenarios
1. **Database Lock** (> 30s timeout)
   - Action: ROLLBACK, return error status
   - User: Close Zotero manually, retry

2. **Integrity Violation** (PRIMARY KEY conflict)
   - Action: ROLLBACK, compute new itemID, RETRY (up to 20 attempts)
   - Reason: Concurrent writes during ADD

3. **Parse Failure** (malformed comment)
   - Action: Skip LLM, use placeholder "见原文"
   - Confidence: "low", manual review needed

4. **LLM Timeout** (Ollama > 60s)
   - Action: Fall back to empty comment, mark for manual review
   - Reason: Ollama service unavailable or overloaded

## Concurrency Model

**Problem**: Zotero client might still write while we're reading

**Solution**: 
```sql
-- Lock DB immediately, before any reads
BEGIN IMMEDIATE;  -- Wait until all writers release

-- Safe to read now
SELECT ... FROM itemAnnotations;

-- Safe to write now (exclusive lock held)
UPDATE itemAnnotations SET ...;

-- Release lock
COMMIT;  -- or ROLLBACK on error
```

**Timeout**: 30 seconds (configurable via `sqlite3.connect(timeout=30)`)

## Performance Considerations

### Bottlenecks
1. **LLM Inference** (~3-5s per annotation)
   - Solution: Batch processing, parallel requests
   
2. **Database Lock** (~0.1-1s per transaction)
   - Solution: Minimize lock duration, use connection pooling
   
3. **Notion API** (~1s per sync)
   - Solution: Batch API calls, async requests

### Optimization Strategies
- Use `batch_update_annotations()` instead of serial updates
- Disable Notion sync if not needed (`export NOTION_SYNC=false`)
- Use faster LLM model (qwen2.5:0.5b vs mistral)
- Pre-parse comments before calling Ollama

## Extensibility Points

1. **Custom Parsing Rules** 
   - Override regex in `annotation_guidelines.md`
   
2. **Alternative LLMs**
   - Replace Ollama with OpenAI/Claude/other in `synthesize_notes.py`
   
3. **Custom Sync Targets**
   - Add new sync backend (Obsidian, Logseq, etc.)
   - Implement interface: `def sync_to_custom(notes, config): ...`
   
4. **Domain-Specific Processing**
   - Add domain detector in `literature_analysis_framework.md`
   - Route to domain-specific processing pipeline

---

For implementation details, see [API_REFERENCE.md](API_REFERENCE.md)
