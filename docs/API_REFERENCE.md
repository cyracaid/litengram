# API Reference — LitEngram

Complete function documentation for LitEngram scripts and modules.

---

## Core Modules

### `scripts/zotero_sync.py`

Main module for Zotero database interaction.

#### `class ZoteroDB`

```python
from scripts.zotero_sync import ZoteroDB

db = ZoteroDB(db_path="~/Zotero/zotero.sqlite")
```

**Methods**:

##### `connect()`
```python
def connect(timeout=30) -> sqlite3.Connection
```
- Opens connection to Zotero SQLite database
- **Args**: 
  - `timeout` (int): Connection timeout in seconds (default: 30)
- **Returns**: sqlite3.Connection object
- **Raises**: `FileNotFoundError` if DB path invalid
- **Example**:
  ```python
  db.connect()
  print("✓ Connected to Zotero")
  ```

##### `close()`
```python
def close()
```
- Safely closes database connection
- Commits any pending transactions
- **Example**:
  ```python
  db.close()
  ```

##### `get_annotations(parent_item_id: int) -> List[Dict]`
```python
annotations = db.get_annotations(parent_item_id=4429)
```
- Retrieves all annotations for a specific PDF
- **Args**: 
  - `parent_item_id` (int): PDF itemID in Zotero
- **Returns**: List of annotation dicts with keys:
  - `itemID`: Unique annotation ID
  - `text`: Highlighted text
  - `comment`: Existing comment (if any)
  - `color`: Highlight color hex
  - `pageLabel`: Page number
  - `position`: JSON with coordinates
- **Example**:
  ```python
  for ann in annotations:
      print(f"Page {ann['pageLabel']}: {ann['text'][:50]}...")
  ```

##### `update_annotation(item_id: int, comment: str, author_name: str = "Lintengram") -> Dict`
```python
result = db.update_annotation(
    item_id=4431, 
    comment="【定义】...",
    author_name="Lintengram"
)
```
- Updates single annotation's comment and author
- **Args**:
  - `item_id` (int): Annotation itemID
  - `comment` (str): New comment text (≤ 65536 chars)
  - `author_name` (str): Author name (default: "Lintengram")
- **Returns**: 
  ```python
  {
    "status": "✅" or "❌",
    "itemID": 4431,
    "rows_affected": 1,
    "message": "Updated successfully"
  }
  ```
- **Raises**: `sqlite3.IntegrityError` if itemID not found

##### `batch_update_annotations(updates: List[Tuple]) -> Dict`
```python
updates = [
    (4431, "【定义】Definition 1..."),
    (4432, "【定义】Definition 2..."),
]
result = db.batch_update_annotations(updates)
```
- Updates multiple annotations in atomic transaction
- **Args**:
  - `updates` (List[Tuple]): List of (itemID, comment) tuples
- **Returns**:
  ```python
  {
    "status": "✅",
    "total": 52,
    "success": 51,
    "failed": 1,
    "errors": ["itemID 4500: not found"]
  }
  ```
- **Performance**: ~50ms per annotation (vs 100ms serial)

##### `verify_annotations(parent_item_id: int) -> Dict`
```python
report = db.verify_annotations(parent_item_id=4429)
```
- Validates all annotations have authorName and comment
- **Returns**:
  ```python
  {
    "total": 52,
    "valid": 51,
    "invalid": 1,
    "missing_authorName": ["itemID 4500"],
    "missing_comment": []
  }
  ```

---

### `scripts/synthesize_notes.py`

High-level orchestration for processing papers.

#### `def process_paper(paper_id: str, parent_item_id: int, llm_model: str = "qwen2.5:0.5b") -> Dict`

```python
from scripts.synthesize_notes import process_paper

result = process_paper(
    paper_id="Lamichhane2020_Nback",
    parent_item_id=4429,
    llm_model="qwen2.5:0.5b"
)
```

- Main entry point for processing a complete paper
- **Args**:
  - `paper_id` (str): Unique paper identifier
  - `parent_item_id` (int): Zotero PDF itemID
  - `llm_model` (str): Ollama model name
- **Returns**:
  ```python
  {
    "paper_id": "Lamichhane2020_Nback",
    "status": "✅ completed",
    "annotations_processed": 52,
    "annotations_parsed": 48,
    "annotations_llm_generated": 4,
    "knowledge_fingerprints": 47,
    "notion_synced": True,
    "duration_seconds": 45.3,
    "errors": []
  }
  ```
- **Time**: ~30-60s for 50 annotations (depending on LLM)

#### `def parse_annotation(text: str, highlight_text: str, model: str) -> Dict`

```python
comment = parse_annotation(
    text="Working memory is...",
    highlight_text="Working memory",
    model="qwen2.5:0.5b"
)
```

- Extracts 4-layer structure from text
- **Returns**:
  ```python
  {
    "layer_1_definition": "Working memory (WM): ...",
    "layer_2_role": "This paper extends WM to...",
    "layer_3_argument": "Supports inverted-U hypothesis...",
    "layer_4_extension": "Test in aging populations...",
    "confidence": "high" | "medium" | "low",
    "source": "rule-first" | "llm"
  }
  ```

---

### `scripts/notion_sync.py`

Optional integration with Notion.

#### `def sync_to_notion(paper_key: str, annotations_json: Dict, notion_token: str) -> Dict`

```python
from scripts.notion_sync import sync_to_notion

result = sync_to_notion(
    paper_key="NIY96UDQ",
    annotations_json={"layers": [...]},
    notion_token=os.environ['NOTION_TOKEN']
)
```

- Syncs structured notes to Notion database
- **Args**:
  - `paper_key` (str): Zotero paper citation key
  - `annotations_json` (Dict): Processed annotations
  - `notion_token` (str): Notion integration token
- **Returns**:
  ```python
  {
    "status": "✅ synced",
    "notion_page_id": "abc123...",
    "properties_updated": 8,
    "blocks_created": 1
  }
  ```
- **Requires**: `NOTION_DATABASE_ID` environment variable

---

## Utility Functions

### `scripts/_markdown_blocks.py`

Markdown parsing utilities.

#### `def extract_markdown_blocks(text: str, marker_prefix: str = "【") -> Dict[str, str]`

```python
blocks = extract_markdown_blocks(
    text="【定义】...\n【本文角色】...",
    marker_prefix="【"
)
# Returns: {"定义": "...", "本文角色": "..."}
```

- Extracts Chinese-style markdown blocks
- **Markers**: `【定义】`, `【本文角色】`, `【论证关联】`, `【延伸】`
- **Returns**: Dict mapping marker names to content

---

## Configuration

### Environment Variables

```bash
# Required
export ZOTERO_DB_PATH=~/Zotero/zotero.sqlite

# Optional
export OLLAMA_MODEL=qwen2.5:0.5b
export OLLAMA_HOST=http://localhost:11434
export NOTION_TOKEN=ntn_xxxxx
export NOTION_DATABASE_ID=xxxxx
export DEBUG=false
export NOTION_SYNC=true
```

---

## Error Handling

### Common Exceptions

```python
# Database locked (Zotero still running)
try:
    db.connect()
except sqlite3.OperationalError as e:
    print("Close Zotero first!")
    
# Invalid paper ID
try:
    result = process_paper("InvalidID", parent_item_id=9999)
except ValueError as e:
    print("Paper ID not found in Zotero")

# Ollama not responding
try:
    comment = parse_annotation(text, highlight, "qwen2.5:0.5b")
except ConnectionError as e:
    print("Ollama service unavailable - run: ollama serve")
```

---

## Usage Examples

### Example 1: Simple Annotation Update

```python
from scripts.zotero_sync import ZoteroDB

db = ZoteroDB()
db.connect()

# Get all annotations for a paper
annotations = db.get_annotations(parent_item_id=4429)
print(f"Found {len(annotations)} annotations")

# Update first annotation
db.update_annotation(
    item_id=annotations[0]['itemID'],
    comment="【定义】Working memory is...",
    author_name="Lintengram"
)

db.close()
```

### Example 2: Batch Processing with LLM

```python
from scripts.synthesize_notes import process_paper

result = process_paper(
    paper_id="MyPaper2024",
    parent_item_id=4429,
    llm_model="qwen2.5:0.5b"
)

print(f"✓ Processed {result['annotations_processed']} annotations")
print(f"✓ LLM generated {result['annotations_llm_generated']} comments")
print(f"✓ Completed in {result['duration_seconds']:.1f} seconds")
```

### Example 3: With Notion Sync

```python
import os
from scripts.synthesize_notes import process_paper
from scripts.notion_sync import sync_to_notion

# Process paper
result = process_paper(
    paper_id="Lamichhane2020_Nback",
    parent_item_id=4429
)

# Sync to Notion
if result['status'].startswith('✅'):
    notion_result = sync_to_notion(
        paper_key="NIY96UDQ",
        annotations_json=result['annotations'],
        notion_token=os.environ['NOTION_TOKEN']
    )
    print(f"✓ Synced to Notion: {notion_result['notion_page_id']}")
```

---

## Performance Tips

- **Batch operations**: Use `batch_update_annotations()` instead of loop
- **LLM selection**: qwen2.5:0.5b (~3s) vs mistral (~10s)
- **Notion sync**: Disable if not needed with `export NOTION_SYNC=false`
- **Database**: Close Zotero before processing to avoid lock timeout

---

For more info, see [ARCHITECTURE.md](ARCHITECTURE.md)
