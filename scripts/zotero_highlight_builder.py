"""Zotero PDF highlight builder — legal-position annotation injection via PyMuPDF.

v1.6: refutes the old "SQLite cannot build valid annotation position" claim.
Zotero's position y-axis origin is at the page bottom (PDF native coordinates);
PyMuPDF's y-axis origin is at the top. They satisfy `zotero_y = pageH - pymupdf_y`.
Calibrated against real annotations already in the library (sum ≈ pageH).

Usage:
    python zotero_highlight_builder.py <note_md> <attachment_item_id> [--pdf <path>] [--dry-run]

Reads the 📌 关键标注 (AI Annotation Highlights) table from a LitEngram note .md,
locates each quote in the PDF via char-level core matching (tolerates hyphens,
line-break splitting, punctuation), and INSERTs legal annotation rows.

NOTE: 必须 Zotero 关闭时运行（否则 database is locked）。
"""

import json
import os
import random
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF

_KEY_CHARS = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
DB = Path(os.environ.get("ZOTERO_DB_PATH", str(Path.home() / "Zotero/zotero.sqlite")))


def zotero_key():
    return "".join(random.choice(_KEY_CHARS) for _ in range(8))


def close_zotero_first():
    import subprocess
    import time

    ret = subprocess.run(["pgrep", "-x", "Zotero"], capture_output=True)
    if ret.returncode != 0:
        return
    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Zotero" to quit'],
            capture_output=True, timeout=5,
        )
    except subprocess.TimeoutExpired:
        pass
    for _ in range(10):
        time.sleep(0.5)
        ret = subprocess.run(["pgrep", "-x", "Zotero"], capture_output=True)
        if ret.returncode != 0:
            return
    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Zotero" to quit saving yes'],
            capture_output=True, timeout=3,
        )
    except Exception:
        pass


def locate_core(pdf_path, term):
    """Return {"page": int, "rects": [[...], ...]} in Zotero coordinate space."""
    def core(s):
        return "".join(c for c in unicodedata.normalize("NFKC", s) if c.isalnum()).lower()

    tcore = core(term)
    doc = fitz.open(pdf_path)
    for p in range(len(doc)):
        d = doc[p].get_text("dict")
        chars = []
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for sp in line.get("spans", []):
                    txt = sp.get("text", "")
                    if not txt.strip():
                        continue
                    ntxt = unicodedata.normalize("NFKC", txt)
                    x0, y0, x1, y1 = sp["bbox"]
                    xw = max(1e-6, (x1 - x0) / max(1, len(ntxt)))
                    for ci, ch in enumerate(ntxt):
                        if ch.isalnum():
                            chars.append((x0 + ci * xw, sp["bbox"], ch.lower()))
        ctext = "".join(c[2] for c in chars)
        pos = ctext.find(tcore)
        if pos >= 0:
            matched = chars[pos : pos + len(tcore)]
            pageH = doc[p].rect.height
            groups = {}  # (y0, y1) -> x list
            for x, bbox, ch in matched:
                groups.setdefault((bbox[1], bbox[3]), []).append(x)
            rects = [
                [round(min(xs), 3), round(pageH - sy1, 3),
                 round(max(xs), 3), round(pageH - sy0, 3)]
                for (sy0, sy1), xs in groups.items()
            ]
            rects.sort(key=lambda r: r[1])
            doc.close()
            return {"page": p, "rects": rects}
    doc.close()
    return None


def parse_annotation_table(md_path):
    rows = []
    in_section = False
    for line in open(md_path):
        s = line.strip()
        if s.startswith("### 📌 关键标注"):
            in_section = True
            continue
        if in_section and s.startswith("### "):
            break
        if in_section and s.startswith("|") and "|" in s[1:]:
            cells = [c.strip() for c in s.split("|")[1:-1]]
            if len(cells) >= 4 and cells[0].isdigit():
                rows.append({"num": cells[0], "orig": cells[1],
                             "region": cells[2], "comment": cells[3]})
    return rows


def build(pdf_path, attachment_item_id, rows):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    inserted, failed = 0, []
    for r in rows:
        term = r["orig"].strip().strip('"')
        comment = r["comment"].strip()
        if not term or not comment:
            failed.append((r["num"], "empty"))
            continue
        res = locate_core(pdf_path, term)
        if not res:
            failed.append((r["num"], "not-located"))
            continue
        pos = json.dumps({"pageIndex": res["page"], "rects": res["rects"]}, ensure_ascii=False)
        page_label = str(res["page"] + 1)
        sort_index = f"{res['page']:05d}|{700000 - int(res['rects'][0][1]):06d}|00001" if res["rects"] else f"{res['page']:05d}|000000|00001"
        key = zotero_key()
        cur.execute(
            "INSERT INTO items (itemTypeID, dateAdded, dateModified, clientDateModified, "
            "libraryID, key, version, synced, clientVersion) "
            "VALUES (1, datetime('now'), datetime('now'), datetime('now'), 1, ?, "
            "(SELECT COALESCE(MAX(version),0)+1 FROM items), 0, 0)",
            (key,),
        )
        nid = cur.lastrowid
        cur.execute(
            "INSERT INTO itemAnnotations (itemID, parentItemID, type, authorName, text, "
            "comment, color, pageLabel, sortIndex, position, isExternal) "
            "VALUES (?, ?, 1, 'Lintergram', ?, ?, '#ffd400', ?, ?, ?, 0)",
            (nid, attachment_item_id, term, comment, page_label, sort_index, pos),
        )
        inserted += 1
    conn.commit()
    conn.close()
    return inserted, failed


def main():
    if len(sys.argv) < 3:
        print("Usage: zotero_highlight_builder.py <note_md> <attachment_item_id> [--pdf <path>] [--dry-run]")
        sys.exit(1)
    md_path = sys.argv[1]
    att_id = int(sys.argv[2])
    pdf_path = None
    dry = "--dry-run" in sys.argv
    if "--pdf" in sys.argv:
        pdf_path = sys.argv[sys.argv.index("--pdf") + 1]
    # resolve attachment storage path from DB if not given
    if not pdf_path:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        row = cur.execute(
            "SELECT path FROM itemAttachments WHERE itemID=?", (att_id,)
        ).fetchone()
        conn.close()
        if not row or not row[0] or not row[0].startswith("storage:"):
            print("❌ attachment storage path not resolvable; pass --pdf manually")
            sys.exit(1)
        rel = row[0].split(":", 1)[1].split("/", 1)
        pdf_path = os.path.expanduser(f"~/Zotero/storage/{rel[0]}/{rel[1]}" if len(rel) > 1 else f"~/Zotero/storage/{rel[0]}")
        if not os.path.exists(pdf_path):
            print(f"❌ PDF not found: {pdf_path}")
            sys.exit(1)
    print(f"PDF: {pdf_path}")

    if not dry:
        close_zotero_first()
    rows = parse_annotation_table(md_path)
    print(f"annotation rows: {len(rows)}")
    inserted, failed = build(pdf_path, att_id, rows) if not dry else (len(rows), [])
    print(f"inserted: {inserted}")
    if failed:
        for n, why in failed:
            print(f"  FAIL #{n}: {why}")
    if dry:
        print("dry-run: no DB writes")


if __name__ == "__main__":
    main()