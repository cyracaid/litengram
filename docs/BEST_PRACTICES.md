# Best Practices — LitEngram

How to use LitEngram effectively for maximum knowledge retention and productivity.

---

## 📖 Reading & Annotation Workflow

### 1. Active Reading Strategy

**Goal**: Extract maximum value from each paper in minimum time

**Process**:
```
First Pass (Skim)
├─ Read abstract + intro → understand paper scope
├─ Skim headings + figures → get visual overview
└─ Time: 5-10 minutes

Second Pass (Focused)
├─ Read methods + results carefully
├─ Highlight key definitions: "working memory", "fMRI", etc
├─ Highlight key findings: "inverted-U relationship", etc
├─ Highlight surprises: contradictions to expectations
└─ Time: 20-30 minutes

Third Pass (Synthesis)
├─ Re-read introduction (now you understand context)
├─ Note how findings connect to larger field
├─ Think about gaps/future directions
├─ Mark 2-3 most important concepts for deep annotation
└─ Time: 10-15 minutes
```

**Result**: 35-55 minutes/paper, but much better understanding

### 2. Highlighting Strategy

**What to highlight**:
- ✅ Key definitions (mark as "定义" in comment)
- ✅ Core findings (mark as "论证关联")
- ✅ Methodology details (mark as "本文角色")
- ✅ Surprising results (mark as "延伸")

**What NOT to highlight**:
- ❌ General background (too common)
- ❌ Literature reviews (just references)
- ❌ Full sentences (extract key phrases)
- ❌ Redundant information

**Good example**:
```
✅ Highlight: "inverted-U relationship between WM load and activation"
❌ NOT: "Many studies have shown that working memory capacity varies
        with age and task difficulty, and the relationship between
        working memory load and neural activation is complex..."
```

### 3. Annotation Comment Format

**Before running LitEngram, add manual comments in Zotero**:

```
【定义】
Working memory (WM): short-term storage and manipulation of information,
Baddeley & Hitch (1974), capacity limit ~7±2 items

【本文角色】
This paper extends classical 2-back WM task to 1-6 load range,
examining how fMRI activation changes with load

【论证关联】
Finding supports inverted-U hypothesis: 
activation increases 1-3 load, peaks at 4, then plateaus/decreases 5-6

【延伸】
(Your own ideas)
- Test in aging: expect delayed peak (5 instead of 4)
- Compare with working memory capacity measures (OSPAN)
- Reconcile with cognitive control literature
```

**LitEngram will**:
- ✅ Parse existing comments (preserve your work)
- ✅ Fill missing layers via LLM (save you time)
- ✅ Generate fingerprints (link to other papers)
- ✅ Sync to Notion (build knowledge graph)

---

## 🔧 Processing Strategy

### Batch vs Serial Processing

**Batch (Recommended)**:
```python
# Process 52 annotations in ~45 seconds (atomic transaction)
result = process_paper(
    paper_id="Lamichhane2020_Nback",
    parent_item_id=4429
)
```
- ✅ Faster (1 connection, 1 transaction)
- ✅ Safer (all-or-nothing commit)
- ✅ Progress bar (see status in real-time)

**Serial (Debug only)**:
```python
# Update each annotation individually (52 × 100ms = 5.2s DB time)
for ann in annotations:
    db.update_annotation(ann['itemID'], comment)
```
- ❌ Slower (52 separate connections)
- ❌ Risky (partial failure scenario)
- ✅ Useful: inspect each result

### LLM Model Selection

| Model | Speed | Quality | Memory | Best For |
|-------|-------|---------|--------|----------|
| **qwen2.5:0.5b** | 🚀 3-5s | ⭐⭐⭐⭐ | 500MB | DEFAULT (recommended) |
| **mistral:latest** | 🐢 8-12s | ⭐⭐⭐⭐⭐ | 7GB | Complex reasoning |
| **neural-chat** | 🚀 4-7s | ⭐⭐⭐⭐ | 4GB | Balanced |
| **llama2** | 🐢 10-15s | ⭐⭐⭐ | 5GB | Lightweight alt |

**Recommendation**: Start with `qwen2.5:0.5b` (default), upgrade to `mistral` if output quality poor

```bash
# Switch model
export OLLAMA_MODEL=mistral:latest
python scripts/synthesize_notes.py --paper-id "MyPaper2024" --parent-item-id 4429
```

---

## 🧠 Knowledge Management

### Building Your Knowledge Graph

**Goal**: Link similar concepts across papers

**Example**:
```
Paper 1 (Walther 2009):
  【定义】Scene categories: natural scenes grouped by semantic meaning
  Fingerprint: abc123...

Paper 2 (Kriegeskorte 2008):
  【定义】Visual categorization: grouping stimuli by perceptual similarity
  Fingerprint: abc123... ← Same fingerprint!
  
→ LitEngram automatically links these as "same concept"
```

**How to leverage**:
1. Run LitEngram on multiple papers in same domain
2. Check Notion dashboard for "linked concepts"
3. See how understanding evolves across papers
4. Use for writing: "As seen in [Paper1] and [Paper2]..."

### Concept Excavation (9 Layers)

When you need deep understanding, explore the **9-layer model** in [references/concept_excavation.md](../references/concept_excavation.md):

1. **Etymology**: Where does the term come from?
2. **Formal Definition**: How do scientists define it?
3. **Historical Context**: How has understanding evolved?
4. **Current State**: What do we know now?
5. **Applications**: Where is it used?
6. **Limitations**: What are the boundaries?
7. **Related Concepts**: What concepts are adjacent?
8. **Open Questions**: What don't we know?
9. **Future Directions**: Where is research heading?

**Example**: Understanding "Working Memory"
```
1. Etymology: "Working" = temporary, "Memory" = storage
2. Definition: Baddeley's component model (phonological loop, etc)
3. History: Miller (1956) magic number 7 → 1974 Baddeley & Hitch
4. Current: fMRI reveals frontal/parietal networks (this paper!)
5. Applications: ADHD assessment, cognitive training
6. Limitations: Culture-dependent?, species-specific?
7. Related: attention, executive function, processing speed
8. Open: How does WM relate to long-term memory consolidation?
9. Future: Real-time neurofeedback training?
```

### Periodic Review (Spaced Repetition)

**Strategy**: Revisit papers on a schedule to reinforce memory

```
Timeline:
Day 1:   Read paper → Create highlights → Run LitEngram
Week 1:  Review Notion notes → Write 1-page summary
Week 2:  Look for connections to other papers
Week 4:  Use in your writing (thesis/grant/blog)
Month 2: Cite in new work → Confirm understanding still strong
```

**Benefits**:
- ✅ Exponentially better retention (Ebbinghaus curve)
- ✅ Ideas gestate → new insights emerge
- ✅ Connections become clear across papers
- ✅ Ready to cite accurately when needed

---

## 📝 Writing & Citing

### Using Annotated Notes in Writing

**Before**:
```
I remember reading something about working memory...
(30 min search through papers)
```

**After LitEngram**:
```
# Query Notion: "working memory + fMRI"
# Result: 12 annotations across 3 papers with full 4-layer structure
# Write: "As shown by Lamichhane et al. (2020), the inverted-U..."
# (2 min - full context available)
```

### Creating Paper Outlines

**Method 1: Concept-First (Recommended)**
```
1. Define key concepts (from annotations)
2. Group by concept (linked fingerprints)
3. Order by logical flow
4. Fill gaps with new reading
```

**Method 2: Chronological**
```
1. Start with oldest papers
2. Trace how understanding evolved
3. Highlight paradigm shifts
4. Show your contribution
```

### Preventing Over-Citation

**Problem**: "I have 50 annotations, which ones matter?"

**Solution**:
1. Filter annotations by confidence > "high"
2. Look for fingerprints with 3+ papers (strong evidence)
3. Use 【论证关联】layer to prioritize (closest to your argument)
4. Aim for 1 cite per major point

**Rule of thumb**: If citing > 3 times per paragraph, consolidate or summarize instead

---

## 🔐 Organization & Backup

### Folder Structure

```
~/litengram-workspace/
├── zotero-exports/           # Backup of Zotero notes
│   ├── 2024-09-01.json
│   ├── 2024-09-08.json       # Weekly backups
│   └── 2024-09-15.json
├── papers-processed/         # Markdown export of processed papers
│   ├── Walther2009.md
│   ├── Lamichhane2020.md
│   └── ...
├── knowledge-graph/          # Notion exports (monthly)
│   ├── concepts.csv
│   ├── links.csv
│   └── ...
└── notion-backups/           # Notion page backups
    └── LitEngram-2024-09-09.html
```

### Backup Strategy

**Daily**: 
- ✅ Zotero auto-syncs (if Zotero account enabled)

**Weekly**:
- ✅ Export Notion as HTML: Settings → Export → HTML

**Monthly**:
- ✅ Export Notion DB as CSV: Database → Export → CSV

```bash
# Automated weekly backup script
crontab -e
# Add: 0 22 * * 0 python ~/litengram/scripts/backup_notion.py
```

---

## ⚡ Performance Optimization

### Faster Processing

**Technique 1: Disable Notion Sync**
```bash
export NOTION_SYNC=false
# Time: 45s → 40s (10% faster)
```

**Technique 2: Use Faster LLM**
```bash
export OLLAMA_MODEL=qwen2.5:0.5b  # vs mistral
# Time: 60s → 45s (25% faster)
```

**Technique 3: Batch Updates**
```python
# Batch (good)
db.batch_update_annotations(updates)  # 45s for 52 items

# Serial (bad)
for item_id, comment in updates:
    db.update_annotation(item_id, comment)  # 90+ seconds
```

### Memory Efficiency

**Problem**: Ollama eats 200MB during processing

**Solutions**:
1. Close other apps (free up system memory)
2. Use smaller model (qwen2.5:0.5b not mistral)
3. Limit concurrent Ollama calls (batch mode already does this)

---

## 🐛 Troubleshooting

### Issue: "Database is locked"

**Symptoms**: Script hangs for 30s then fails

**Diagnosis**: Zotero is still running/using DB

**Fix**:
```bash
pkill -f Zotero                      # Force kill Zotero
rm ~/Zotero/zotero.sqlite-journal   # Clean up lock file
python scripts/synthesize_notes.py  # Try again
```

### Issue: "Ollama connection refused"

**Symptoms**: "ConnectionError: Cannot reach Ollama"

**Diagnosis**: Ollama service not running

**Fix**:
```bash
ollama serve &                  # Start in background
sleep 2                         # Wait for startup
python scripts/synthesize_notes.py
```

### Issue: "LLM output doesn't match 4-layer structure"

**Symptoms**: Comments missing 【延伸】 or malformed

**Diagnosis**: Model having trouble with prompt

**Fix**:
```bash
# Switch to better model
export OLLAMA_MODEL=mistral:latest

# Or manually edit the comment in Zotero
# LitEngram respects existing comments
```

---

## 💡 Tips & Tricks

### Tip 1: Use Consistent Highlighting Color

```
🟨 Yellow (default) = Key definition
🟥 Red = Surprising finding
🟦 Blue = Methodology detail
🟩 Green = Future direction
```

Then you can filter by color in Notion dashboard.

### Tip 2: Leverage "Batch Add" in Zotero

```
Instead of:
1. Open PDF → Read → Highlight → Comment → Repeat 52x

Try:
1. First pass: Highlight everything (no comments)
2. Run LitEngram
3. Review in Notion (with 4 layers now!)
4. Manual comment only on complex items
```

**Time saved**: 2 hours → 30 minutes per paper

### Tip 3: Cross-Cite Using Fingerprints

When writing, query Notion by fingerprint to find all papers discussing same concept:

```sql
-- Notion filter: fingerprint = "abc123def456"
-- Result: This concept appears in papers A, B, C
-- Write: "Multiple studies confirm this..." + cite all 3
```

### Tip 4: Export for Thesis/Publication

```bash
# Export processed papers as BibTeX + annotations
python scripts/export.py --format bibtex --output thesis.bib

# Now you have:
# - Organized citations
# - Structured annotations
# - Ready to integrate into thesis
```

---

## 📊 Measuring Your Progress

### Metrics to Track

- **Papers processed**: Cumulative count
- **Annotations created**: Total highlights
- **Concepts linked**: Cross-paper fingerprints
- **Reading speed**: Words/minute (should improve over time)
- **Retention**: How much you remember 1 month later (test yourself!)

### Sample Tracking

```
Week 1:  3 papers, 47 annotations, 8 linked concepts
Week 2:  2 papers, 34 annotations, 12 linked concepts (↑50%)
Week 3:  4 papers, 98 annotations, 24 linked concepts (↑100%)
```

**Trend**: More linked concepts = better integration of knowledge

---

## 🎓 Advanced: Domain-Specific Tips

### For Neuroscience Papers

See [references/literature_analysis_framework.md](../references/literature_analysis_framework.md) for:
- Specific 4-layer prompts for fMRI/EEG
- Key concepts to track (nodes, networks, oscillations)
- Common pitfalls (reverse inference, overfitting)

### For Psychology Papers

- Focus on **operationalization**: How did they measure constructs?
- Mark **effect sizes** prominently (not just p-values!)
- Annotate **sample characteristics** (age, culture, demographics)

### For Computer Science Papers

- Extract **algorithm complexity**: O(n), O(n log n), etc
- Note **implementation details**: important for reproduction
- Mark **assumptions**: what does this assume about input?

---

For API details, see [API_REFERENCE.md](API_REFERENCE.md)  
For architecture, see [ARCHITECTURE.md](ARCHITECTURE.md)
