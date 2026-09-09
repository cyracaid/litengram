# Integrations — LitEngram

Connect LitEngram with other tools in your knowledge management workflow.

---

## Obsidian Integration

Export LitEngram notes to Obsidian vault:

```bash
python scripts/export.py --format obsidian --output ~/Obsidian/LitEngram
```

Result:
- Notes organized by paper
- Wikilinks between concepts (via fingerprints)
- Full 4-layer structure preserved
- Ready for graph view

---

## Logseq Integration

Export to Logseq journal format:

```bash
python scripts/export.py --format logseq --output ~/Logseq/journals
```

Result:
- Daily entries per paper processed
- Nested blocks preserve 4-layer structure
- Tags auto-generated
- Ready for Logseq DB

---

## Roam Research

Export as JSON for Roam:

```bash
python scripts/export.py --format json --output ~/notes.json
```

Then in Roam:
1. Tools → Import JSON
2. Select exported file
3. Maps to Roam blocks automatically

---

## LaTeX / Overleaf

Export BibTeX + annotations:

```bash
python scripts/export.py --format bibtex --output ~/thesis.bib
```

Result:
- thesis.bib: All papers with metadata
- thesis-annotations.md: Notes per paper

In Overleaf:
1. Upload .bib file to project
2. Reference in main.tex: \bibliography{thesis}
3. Use \cite{AuthorYear} to cite

---

## Zotero Sync (Native)

LitEngram works directly with Zotero DB:
- No export needed
- Changes appear instantly in Zotero UI
- Comments visible on highlights

Native sync enabled by default.

---

## Notion API

Already integrated! Enable with:

```bash
export NOTION_TOKEN=ntn_xxxxx
export NOTION_DATABASE_ID=xxxxx
export NOTION_SYNC=true

python scripts/synthesize_notes.py --paper-id "MyPaper" --parent-item-id 123
```

---

For more details on each integration, see docs/examples/
