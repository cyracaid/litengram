"""Zotero sync for LitEngram v1.2 — write notes as Zotero-safe HTML."""

import re
import secrets
import sqlite3
import os
from pathlib import Path

ZOTERO_DB = Path.home() / "Zotero/zotero.sqlite"
LIBRARY_ID = 1


def md_to_zotero_html(md_text):
    """Convert clean Markdown to Zotero-safe XHTML.

    Zotero 7 renders a subset of XHTML in notes. This converter
    targets that subset: headers, bold, italic, lists, tables,
    blockquotes, code — with no raw HTML in the source Markdown.
    """
    lines = md_text.strip().split("\n")
    out = []
    i = 0

    def esc(text):
        """Escape HTML special chars."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def inline(text):
        """Convert inline **bold**, *italic*, `code` to Zotero-safe HTML."""
        text = esc(text)
        # code backtick first (so ** inside `` is not parsed)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        # italic
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
        return text

    def flush_para(para_lines):
        """Flush accumulated paragraph lines as <p>."""
        if not para_lines:
            return
        merged = " ".join(para_lines).strip()
        if merged:
            out.append(f"<p>{inline(merged)}</p>")

    para = []

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        if not s:
            # Blank line → flush paragraph
            flush_para(para)
            para = []
            i += 1
            continue

        # # heading 1
        if s.startswith("# ") and not s.startswith("## "):
            flush_para(para)
            para = []
            out.append(f"<h1>{inline(s[2:])}</h1>")
            i += 1
            continue

        # ## heading 2
        if s.startswith("## ") and not s.startswith("### "):
            flush_para(para)
            para = []
            out.append(f"<h2>{inline(s[3:])}</h2>")
            i += 1
            continue

        # ### heading 3
        if s.startswith("### ") and not s.startswith("#### "):
            flush_para(para)
            para = []
            out.append(f"<h3>{inline(s[4:])}</h3>")
            i += 1
            continue

        # #### heading 4
        if s.startswith("#### "):
            flush_para(para)
            para = []
            out.append(f"<h4>{inline(s[5:])}</h4>")
            i += 1
            continue

        # Blockquote: merge consecutive > lines
        if s.startswith(">"):
            flush_para(para)
            para = []
            quote_parts = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith(">"):
                    text = ls[1:].strip()
                    if text:
                        quote_parts.append(inline(text))
                    i += 1
                else:
                    break
            if quote_parts:
                out.append("<blockquote><p>" + "</p><p>".join(quote_parts) + "</p></blockquote>")
            continue

        # Bullet list: - or *
        if s.startswith("- ") or s.startswith("* "):
            flush_para(para)
            para = []
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith("- ") or ls.startswith("* "):
                    items.append(inline(ls[2:]))
                    i += 1
                else:
                    break
            out.append("<ul>\n" + "\n".join(f"<li>{item}</li>" for item in items) + "\n</ul>")
            continue

        # Numbered list
        m = re.match(r"^\d+\.\s*(.*)", s)
        if m:
            flush_para(para)
            para = []
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                mm = re.match(r"^\d+\.\s*(.*)", ls)
                if mm:
                    items.append(inline(mm.group(1)))
                    i += 1
                else:
                    break
            out.append("<ol>\n" + "\n".join(f"<li>{item}</li>" for item in items) + "\n</ol>")
            continue

        # Table: |...|...|
        if s.startswith("|") and s.endswith("|") and s.count("|") >= 3:
            flush_para(para)
            para = []
            rows = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith("|") and ls.endswith("|"):
                    cells = [c.strip() for c in ls.split("|")[1:-1]]
                    # Skip separator rows
                    if cells and all(re.match(r"^-+$", c) for c in cells):
                        i += 1
                        continue
                    if cells:
                        rows.append(cells)
                else:
                    break
                i += 1
            if len(rows) >= 2:
                table_html = "<table>\n"
                for idx, row in enumerate(rows):
                    tag = "th" if idx == 0 else "td"
                    table_html += "<tr>" + "".join(f"<{tag}>{inline(cell)}</{tag}>" for cell in row) + "</tr>\n"
                table_html += "</table>"
                out.append(table_html)
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$", s):
            flush_para(para)
            para = []
            out.append("<hr/>")
            i += 1
            continue

        # Default: accumulate paragraph
        para.append(s)
        i += 1

    # Flush last paragraph
    flush_para(para)

    body = "\n".join(out)
    return f'<div class="zotero-note znv1">\n{body}\n</div>'


def _find_child_note(cur, parent_item_id):
    """Find existing child note for parent. Returns itemID or None."""
    cur.execute(
        "SELECT itemID FROM items WHERE "
        "itemTypeID=28 AND libraryID=? AND "
        "itemID IN (SELECT itemID FROM itemNotes WHERE parentItemID=?)",
        (LIBRARY_ID, parent_item_id),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _delete_old_note(cur, item_id):
    """Delete a note entry given its itemID."""
    cur.execute("DELETE FROM itemNotes WHERE itemID=?", (item_id,))
    cur.execute("DELETE FROM items WHERE itemID=?", (item_id,))


def _create_note(cur, parent_item_id, html_content):
    """Create a new child note for parent."""
    cur.execute("SELECT MAX(itemID) FROM items")
    max_id = cur.fetchone()[0] or 0
    new_id = max_id + 1
    key = secrets.token_hex(6)

    cur.execute(
        "INSERT INTO items (itemID, itemTypeID, key, dateAdded, dateModified, libraryID) "
        "VALUES (?, 28, ?, datetime('now'), datetime('now'), ?)",
        (new_id, key, LIBRARY_ID),
    )
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
    cur = conn.cursor()

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

    conn.close()
    return result


def close_zotero_first():
    """Try to close Zotero so SQLite is not locked."""
    import subprocess

    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Zotero" to quit'],
            capture_output=True,
            timeout=5,
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
