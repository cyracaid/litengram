# Complete Workflow Example

Step-by-step guide showing real usage of LitEngram.

---

## Scenario: Analyzing a Neuroscience Paper

**Paper**: Lamichhane et al. (2020) - "Exploring brain-behavior relationships..."  
**Goal**: Extract structured knowledge and prepare for thesis writing

---

### Day 1: Initial Reading & Highlighting

**Step 1**: Open PDF in Zotero
```
File: ~/Zotero/storage/ABC123/paper.pdf
Zotero Library: Research Notes → Neuroscience → Working Memory
```

**Step 2**: First pass - Skim for understanding
```
Read:
- Abstract (2 min) → understand scope
- Figures (3 min) → visual overview
- Methods (5 min) → what they did
```

**Step 3**: Second pass - Highlight key points
```
Highlight 1: "working memory capacity limited to 7±2 items"
  → This is a KEY DEFINITION
  
Highlight 2: "inverted-U relationship between load and fMRI activation"
  → This is the MAIN FINDING
  
Highlight 3: "fMRI data from 25 subjects (mean age 24±3)"
  → This is METHODOLOGY
```

**Step 4**: Add manual comments (optional but recommended)
```
Right-click highlight 1 → "Add comment" →

【定义】
Working memory (WM): short-term storage and manipulation of information,
Baddeley & Hitch (1974), capacity limit approximately 7±2 items

【本文角色】
This paper extends WM research from standard 2-back task to full 1-6 load range

【论证关联】
Finding of inverted-U (peak at load 4) supports the compensation hypothesis

【延伸】
- Could aging affect the peak load? Might shift from 4 to 3 or 5
- Compare with working memory capacity measures (OSPAN, CCPT)
```

**Result after Day 1**:
- 52 highlights added to paper
- 2-3 manual comments added
- Time spent: ~40 minutes
- Next: Let LitEngram do the heavy lifting

---

### Day 2: LitEngram Processing

**Step 1**: Prepare environment
```bash
# Make sure Zotero is CLOSED
pkill -9 Zotero

# Check environment
echo $ZOTERO_DB_PATH
echo $OLLAMA_MODEL

# Output:
# ~/Zotero/zotero.sqlite
# qwen2.5:0.5b
```

**Step 2**: Run LitEngram
```bash
# Get parent_item_id from Zotero
# Method: Right-click PDF → "Show in Library" → Note the ID (e.g., 4429)

python scripts/synthesize_notes.py \
  --paper-id "Lamichhane2020_Nback" \
  --parent-item-id 4429 \
  --verbose

# Output:
# ✓ Connected to Zotero DB
# ✓ Found 52 annotations
# ✓ Processing: 1/52 (rule parser) ✓ 15ms
# ✓ Processing: 2/52 (rule parser) ✓ 12ms
# ✓ Processing: 3/52 (LLM) ✓ 3500ms
# ... (more)
# ✓ All 52 processed successfully
# ✓ Synced to Notion (optional)
# ✓ Duration: 45.3 seconds
```

**Step 3**: Verify in Zotero
```
Open Zotero
→ Find paper
→ Click first highlight
→ See: 4-layer comment now appears!

【定义】Working memory (WM): short-term storage...
【本文角色】This paper extends WM research...
【论证关联】Finding supports the compensation hypothesis...
【延伸】Consider testing in aging populations...
```

**Result after Day 2**:
- All 52 annotations have structured comments
- Knowledge fingerprints generated
- Synced to Notion (if enabled)
- Time spent: ~1 minute (mostly waiting for LLM)

---

### Day 3: Review in Notion (Optional)

**Step 1**: Open Notion
```
Visit: notion.so → LitEngram database
See: New entry for Lamichhane2020_Nback
```

**Step 2**: Review annotations
```
Expand toggle for this paper:
- Annotation 1: 【定义】...
- Annotation 2: 【本文角色】...
- ... (50 more)
```

**Step 3**: Add your own thoughts
```
In Notion, add comment:
"This finding contradicts Smith et al (2019) who found linear relationship.
Need to investigate why. Possible confound: age difference?"
```

**Result after Day 3**:
- Organized knowledge in Notion
- Can see connections to other papers
- Ready to cite when writing
- Time spent: ~15 minutes

---

### Week 1: Writing Integration

**Step 1**: Search Notion for related papers
```
Query: "working memory" + "fMRI"
Results: 
- Lamichhane2020 (52 annotations)
- Walther2009 (25 annotations)
- Kriegeskorte2008 (15 annotations)
```

**Step 2**: Use fingerprints to find related concepts
```
Search for fingerprint of "inverted-U relationship"
Results: Same concept appears in:
- Lamichhane2020 (original paper)
- Smith2019 (mentions inverted-U)
- Kaplan2018 (similar pattern in executive function)
```

**Step 3**: Write with confidence
```
Draft paragraph:
"Multiple studies demonstrate an inverted-U relationship between 
cognitive load and neural activation (Lamichhane et al., 2020; 
Smith, 2019; Kaplan, 2018). This pattern suggests a mechanism 
of compensation where..."

Now you KNOW you have the context right because:
✓ You read all 3 papers
✓ LitEngram extracted the key points
✓ You have full 4-layer understanding
✓ Notes are organized in Notion
```

**Result after Week 1**:
- Ready to cite 3 papers accurately
- Understand the conceptual landscape
- Can write with confidence
- Time saved: ~2 hours vs manual note-taking

---

### Week 4: Concept Synthesis

**Step 1**: Export to Markdown
```bash
python scripts/export.py \
  --format markdown \
  --output ~/thesis_notes/neuroscience.md
```

**Step 2**: Use in thesis writing
```bash
# Now you have a markdown file with:
# - All papers
# - All annotations
# - All 4-layer structure
# - Ready to incorporate into thesis

cat ~/thesis_notes/neuroscience.md | head -50

# Output:
# # Neuroscience Papers
#
# ## Lamichhane et al. (2020)
# ### Annotation 1: Definition
# Working memory (WM): short-term storage...
# ### Annotation 2: Role
# This paper extends WM research...
# ... (many more)
```

**Step 3**: Update thesis bibliography
```bash
python scripts/export.py \
  --format bibtex \
  --output ~/thesis.bib

# In LaTeX:
\bibliography{thesis}
```

**Result after Week 4**:
- Thesis has proper citations
- All notes exported
- Ready to submit
- Total time spent on this paper: ~2 hours (vs 6+ hours without LitEngram)

---

## Time Comparison

### Without LitEngram
```
Read paper:           45 min
Manual note-taking:   60 min
Organize in notes:    30 min
Search for citations: 30 min
Write + verify:       45 min
─────────────────────────────
TOTAL:               210 minutes (3.5 hours)
```

### With LitEngram
```
Read paper:           45 min
Highlight key points: 10 min
Run LitEngram:        2 min (1 min waiting)
Review in Notion:     15 min
Use in writing:       20 min
─────────────────────────────
TOTAL:               92 minutes (1.5 hours)
```

**Time saved: ~2 hours per paper** (or 55% faster)

---

## Key Takeaways

1. **Active reading is essential** - LitEngram automates the boring part, but you still need to highlight thoughtfully

2. **Manual comments help** - Even 2-3 carefully written comments make LitEngram's output much better

3. **Notion dashboard is optional** - But helpful for linking concepts across papers

4. **Writing is faster** - With organized, fingerprinted notes, citing is much quicker and more accurate

5. **Knowledge compounds** - The more papers you process, the more connections emerge

---

Next: Try this workflow on your own paper! See [BEST_PRACTICES.md](../BEST_PRACTICES.md) for more tips.
