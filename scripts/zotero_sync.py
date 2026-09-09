"""Zotero sync for LitEngram v1.2 — write notes as Zotero-safe HTML.

NOTE: SQLite inserts create items with synced=0. The Zotero client uploads
them on the next sync, so run a sync (or ask the user to) after writing.
Keys are generated as 8-char [2-9A-NP-Z] — Zotero rejects 0/1/O and
lowercase hex keys (server 400 'not a valid item key').
"""

import random
import re
import sqlite3
import os
from pathlib import Path

from _markdown_blocks import parse_blocks, parse_inline_spans

ZOTERO_DB = Path(os.environ.get("ZOTERO_DB_PATH", str(Path.home() / "Zotero/zotero.sqlite")))
LIBRARY_ID = int(os.environ.get("LITENGRAM_LIBRARY_ID", "1"))

# Zotero's allowed key charset: digits 2-9 + A-Z minus O (no 0, 1, O)
_KEY_CHARS = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"


def zotero_key(cur=None):
    """Generate a valid 8-char Zotero item key.

    If a DB cursor is given, retries on collision against existing keys
    in this library. A collision is astronomically unlikely with a
    random 8-char key, but it was previously entirely unhandled and
    would have surfaced as a raw sqlite UNIQUE-constraint error.
    """
    for _ in range(20):
        key = "".join(random.choice(_KEY_CHARS) for _ in range(8))
        if cur is None:
            return key
        cur.execute("SELECT 1 FROM items WHERE key=? AND libraryID=?", (key, LIBRARY_ID))
        if not cur.fetchone():
            return key
    raise RuntimeError("zotero_key: failed to generate a unique key after 20 attempts")


def _esc(text):
    """Escape HTML special chars."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _inline(text):
    """Convert inline **bold**, *italic*, `code` spans to Zotero-safe HTML."""
    out = []
    for kind, content in parse_inline_spans(text):
        escaped = _esc(content)
        if kind == "code":
            out.append(f"<code>{escaped}</code>")
        elif kind == "bold":
            out.append(f"<b>{escaped}</b>")
        elif kind == "italic":
            out.append(f"<i>{escaped}</i>")
        else:
            out.append(escaped)
    return "".join(out)


_HEADING_TAGS = {1: "h1", 2: "h2", 3: "h3", 4: "h4"}


def md_to_zotero_html(md_text):
    """Convert clean Markdown to Zotero-safe XHTML.

    Zotero 7 renders a subset of XHTML in notes. This converter
    targets that subset: headers, bold, italic, lists, tables,
    blockquotes, code — with no raw HTML in the source Markdown.

    Block-level splitting is shared with notion_sync.py via
    _markdown_blocks.py, so the two sync targets can't silently drift
    on what counts as a table / numbered list / heading.
    """
    out = []
    for block in parse_blocks(md_text):
        btype = block["type"]

        if btype == "heading":
            tag = _HEADING_TAGS[block["level"]]
            out.append(f"<{tag}>{_inline(block['text'])}</{tag}>")

        elif btype == "paragraph":
            out.append(f"<p>{_inline(block['text'])}</p>")

        elif btype == "blockquote":
            parts = [_inline(line) for line in block["lines"]]
            out.append("<blockquote><p>" + "</p><p>".join(parts) + "</p></blockquote>")

        elif btype == "bullet_list":
            items = "\n".join(f"<li>{_inline(item)}</li>" for item in block["items"])
            out.append(f"<ul>\n{items}\n</ul>")

        elif btype == "numbered_list":
            items = "\n".join(f"<li>{_inline(item)}</li>" for item in block["items"])
            out.append(f"<ol>\n{items}\n</ol>")

        elif btype == "table":
            rows = block["rows"]
            table_html = "<table>\n"
            for idx, row in enumerate(rows):
                tag = "th" if idx == 0 else "td"
                table_html += "<tr>" + "".join(f"<{tag}>{_inline(cell)}</{tag}>" for cell in row) + "</tr>\n"
            table_html += "</table>"
            out.append(table_html)

        elif btype == "hr":
            out.append("<hr/>")

    body = "\n".join(out)
    return f'<div class="zotero-note znv1">\n{body}\n</div>'


def _find_child_note(cur, parent_item_id):
    """Find existing, non-trashed child note for parent. Returns itemID or None.

    Excludes items in Zotero's trash (deletedItems): without this, a note
    the user deliberately deleted in the Zotero client (but hasn't
    emptied from trash yet) could be "found" here and silently reused/
    overwritten on the next sync. When more than one match exists (e.g.
    from a note created before this dedup logic existed), prefers the
    most recently created one instead of an arbitrary row.
    """
    cur.execute(
        "SELECT itemID FROM items WHERE "
        "itemTypeID=28 AND libraryID=? AND "
        "itemID IN (SELECT itemID FROM itemNotes WHERE parentItemID=?) "
        "AND itemID NOT IN (SELECT itemID FROM deletedItems) "
        "ORDER BY itemID DESC",
        (LIBRARY_ID, parent_item_id),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _delete_old_note(cur, item_id):
    """Delete a note entry given its itemID."""
    cur.execute("DELETE FROM itemNotes WHERE itemID=?", (item_id,))
    cur.execute("DELETE FROM items WHERE itemID=?", (item_id,))


def _validate_parent(cur, parent_item_id):
    """Confirm parent_item_id refers to a real, non-note, non-trashed item.

    Real-world evidence this is needed: a caller-side bug (or a corrupted
    upstream itemID, e.g. from the _create_note race this module also
    fixes) can pass an itemID that is missing, already trashed, or itself
    a note/attachment rather than the paper item. Silently proceeding
    then attaches — or self-attaches — a note to nothing meaningful, and
    the failure is invisible until someone goes looking for the note in
    Zotero/Notion and can't find it. Returns None if valid, else an error
    string describing what's wrong.
    """
    cur.execute(
        "SELECT itemTypeID FROM items WHERE itemID=? AND libraryID=?",
        (parent_item_id, LIBRARY_ID),
    )
    row = cur.fetchone()
    if row is None:
        return f"parent_item_id {parent_item_id} 在 Zotero 库中不存在"

    cur.execute("SELECT 1 FROM deletedItems WHERE itemID=?", (parent_item_id,))
    if cur.fetchone():
        return f"parent_item_id {parent_item_id} 已在 Zotero 回收站中"

    item_type_id = row[0]
    if item_type_id in (28, 3):
        kind = "note" if item_type_id == 28 else "attachment"
        return (
            f"parent_item_id {parent_item_id} 本身是一个 {kind}（itemTypeID={item_type_id}），"
            "不是论文条目 —— 传入的 parent_item_id 很可能是错的"
        )
    return None


def _create_note(cur, parent_item_id, html_content):
    """Create a new child note for parent.

    itemID is allocated as MAX(itemID)+1 — Zotero's schema doesn't expose
    a safer public way to do this. Real-world evidence: this collided
    with a concurrent write to the same database (most likely Zotero's
    own client not having fully quit despite close_zotero_first()) —
    the computed new_id matched an itemID something else was writing at
    almost the same instant, producing a corrupted note whose itemID
    equaled its own parentItemID, attached to neither a real note nor
    the actual paper. The INSERT is now retried on a genuine PRIMARY KEY
    collision (IntegrityError) with a freshly recomputed id, instead of
    only computing MAX+1 once and trusting it.
    """
    key = zotero_key(cur)
    for _ in range(20):
        cur.execute("SELECT MAX(itemID) FROM items")
        max_id = cur.fetchone()[0] or 0
        new_id = max_id + 1
        try:
            cur.execute(
                "INSERT INTO items (itemID, itemTypeID, key, dateAdded, dateModified, libraryID) "
                "VALUES (?, 28, ?, datetime('now'), datetime('now'), ?)",
                (new_id, key, LIBRARY_ID),
            )
            break
        except sqlite3.IntegrityError:
            continue
    else:
        raise RuntimeError("_create_note: failed to allocate a free itemID after 20 attempts")

    cur.execute(
        "INSERT INTO itemNotes (itemID, parentItemID, note) VALUES (?, ?, ?)",
        (new_id, parent_item_id, html_content),
    )
    return new_id, key


def sync_note(markdown_path, parent_item_id):
    """Convert Markdown to Zotero-safe HTML and write to Zotero SQLite.

    Args:
        markdown_path: Path to the .md note file.
        parent_item_id: Zotero itemID of the parent paper entry.

    Returns:
        dict with status, itemID, key, html_len.
    """
    if not ZOTERO_DB.exists():
        return {"status": "❌", "error": f"Zotero DB not found: {ZOTERO_DB}"}

    # Read and strip gate section
    with open(markdown_path) as f:
        content = f.read()

    parts = re.split(r"\n---\n\s*## 结构门禁检查", content)
    md_body = parts[0].strip()

    # Convert to Zotero-safe HTML
    html = md_to_zotero_html(md_body)

    # Write to SQLite
    close_zotero_first()
    conn = sqlite3.connect(str(ZOTERO_DB))
    try:
        cur = conn.cursor()

        parent_error = _validate_parent(cur, parent_item_id)
        if parent_error:
            return {"status": "❌", "error": f"父条目校验失败: {parent_error}"}

        existing_id = _find_child_note(cur, parent_item_id)
        if existing_id:
            # UPDATE existing note
            cur.execute("UPDATE itemNotes SET note=? WHERE itemID=?", (html, existing_id))
            cur.execute(
                "UPDATE items SET dateModified=datetime('now') WHERE itemID=?",
                (existing_id,),
            )
            conn.commit()
            result = {
                "status": "✅",
                "itemID": existing_id,
                "html_len": len(html),
                "mode": "updated",
            }
        else:
            # CREATE new note
            new_id, key = _create_note(cur, parent_item_id, html)
            conn.commit()
            result = {
                "status": "✅",
                "itemID": new_id,
                "key": key,
                "html_len": len(html),
                "mode": "created",
            }

        return result
    finally:
        # Always release the connection, even if a write above raised —
        # previously an exception mid-transaction left the connection open.
        conn.close()


def close_zotero_first():
    """Politely ask Zotero to close, so SQLite is not locked.

    If Zotero refuses or the DB stays locked, the caller
    will see a clear message and can close it manually.
    """
    import subprocess
    import time

    # If Zotero isn't running, nothing to do.
    ret = subprocess.run(
        ["pgrep", "-x", "Zotero"],
        capture_output=True,
    )
    if ret.returncode != 0:
        return

    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Zotero" to quit'],
            capture_output=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        pass

    # Give Zotero a moment to flush and release the lock.
    for _ in range(10):
        time.sleep(0.5)
        ret = subprocess.run(
            ["pgrep", "-x", "Zotero"],
            capture_output=True,
        )
        if ret.returncode != 0:
            return

    # If Zotero still refuses, try once more with SIGTERM.
    try:
        subprocess.run(
            ["osascript", "-e",
             'tell application "Zotero" to quit saving yes'],
            capture_output=True,
            timeout=3,
        )
    except Exception:
        pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python zotero_sync.py <markdown_path> <parent_item_id>")
        sys.exit(1)

    result = sync_note(sys.argv[1], int(sys.argv[2]))
    print(result)
