# Zotero 联动工作流

See `CAD/_zotero_workflow.md` for the complete Zotero technical workflow including:
- Core principles and startup flow
- Note template (deprecated — see `literature_note_template.md`)
- File storage structure
- Technical reference (API endpoints, SQLite tables)
- Annotation batch writing standards (kept here for historical reference)

## Quick Reference

### API (Read)
```
GET  /api/users/0/items/{itemKey}
GET  /api/users/0/items/{itemKey}/children
GET  /api/users/0/items?q={query}
```

### SQLite (Write)
Database: `~/Zotero/zotero.sqlite`

Kill → Write → Restart:
```bash
osascript -e 'quit app "Zotero"'
sqlite3 ~/Zotero/zotero.sqlite "UPDATE ..."
open -a Zotero
```

### Key Tables
- `items`: itemID, itemTypeID (1=annotation, 2=attachment, 14=note), key, parentItemID
- `itemAnnotations`: itemID, parentItemID, type, comment, text
- `itemNotes`: itemID, parentItemID, note (HTML)
- `itemAttachments`: itemID, parentItemID, path
- `collections` / `collectionItems`: collection membership
