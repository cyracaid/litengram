"""Zotero annotation comment sync — write 4-layer comments to PDF annotations.

FIX (2026-09-09): All annotations must have authorName set, otherwise Zotero UI
cannot render them even if comment data exists. This script ensures every
annotation has both comment + authorName before syncing.

TODO: Update annotations with comment + authorName in a single atomic operation.
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Dict, Tuple

ZOTERO_DB = Path(os.environ.get("ZOTERO_DB_PATH", str(Path.home() / "Zotero/zotero.sqlite")))
AUTHOR_NAME = "Lintergram"  # All AI-generated annotations use this author


def close_zotero_first():
    """Politely ask Zotero to close, so SQLite is not locked."""
    import subprocess
    import time

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

    for _ in range(10):
        time.sleep(0.5)
        ret = subprocess.run(
            ["pgrep", "-x", "Zotero"],
            capture_output=True,
        )
        if ret.returncode != 0:
            return

    try:
        subprocess.run(
            ["osascript", "-e", 'tell application "Zotero" to quit saving yes'],
            capture_output=True,
            timeout=3,
        )
    except Exception:
        pass


def update_annotation_comment(
    parent_item_id: int,
    annotation_id: int,
    comment: str,
    author_name: Optional[str] = None,
) -> Dict:
    """Update a single annotation's comment + authorName fields.
    
    Args:
        parent_item_id: itemID of the PDF attachment
        annotation_id: itemID of the annotation
        comment: 4-layer comment text (or empty string to skip)
        author_name: Author name (defaults to AUTHOR_NAME)
    
    Returns:
        {"status": "✓" | "✗", "annotation_id": ..., "comment_len": ..., "error": ...}
        
    IMPORTANT: Does NOT modify position/sortIndex/pageLabel — only comment + authorName.
    """
    if not ZOTERO_DB.exists():
        return {"status": "✗", "error": f"Zotero DB not found: {ZOTERO_DB}"}

    author = author_name or AUTHOR_NAME
    
    close_zotero_first()
    conn = sqlite3.connect(str(ZOTERO_DB), timeout=30)
    conn.isolation_level = None
    
    try:
        cur = conn.cursor()
        cur.execute("BEGIN IMMEDIATE")
        
        # Verify annotation exists
        cur.execute(
            "SELECT itemID, parentItemID FROM itemAnnotations WHERE itemID=? AND parentItemID=?",
            (annotation_id, parent_item_id),
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return {
                "status": "✗",
                "error": f"Annotation itemID={annotation_id} not found under PDF itemID={parent_item_id}",
            }
        
        # Update comment + authorName (ONLY these two fields)
        cur.execute(
            "UPDATE itemAnnotations SET comment=?, authorName=? WHERE itemID=?",
            (comment, author, annotation_id),
        )
        
        conn.commit()
        return {
            "status": "✓",
            "annotation_id": annotation_id,
            "comment_len": len(comment) if comment else 0,
            "author_name": author,
        }
    
    except sqlite3.OperationalError as e:
        conn.rollback()
        return {
            "status": "✗",
            "error": f"Database locked or write failed: {e}",
        }
    except Exception as e:
        conn.rollback()
        return {
            "status": "✗",
            "error": f"Error updating annotation: {e}",
        }
    finally:
        conn.close()


def batch_update_annotations(
    parent_item_id: int,
    updates: List[Tuple[int, str]],
    author_name: Optional[str] = None,
) -> Dict:
    """Update multiple annotations in a single transaction.
    
    Args:
        parent_item_id: itemID of the PDF attachment
        updates: List of (annotation_id, comment) tuples
        author_name: Author name (defaults to AUTHOR_NAME)
    
    Returns:
        {"status": "✓" | "✗", "updated": N, "errors": [...]}
    """
    if not ZOTERO_DB.exists():
        return {"status": "✗", "error": f"Zotero DB not found: {ZOTERO_DB}"}

    author = author_name or AUTHOR_NAME
    
    close_zotero_first()
    conn = sqlite3.connect(str(ZOTERO_DB), timeout=30)
    conn.isolation_level = None
    
    errors = []
    updated_count = 0
    
    try:
        cur = conn.cursor()
        cur.execute("BEGIN IMMEDIATE")
        
        for annotation_id, comment in updates:
            # Verify annotation exists
            cur.execute(
                "SELECT itemID FROM itemAnnotations WHERE itemID=? AND parentItemID=?",
                (annotation_id, parent_item_id),
            )
            if not cur.fetchone():
                errors.append(f"Annotation {annotation_id} not found")
                continue
            
            # Update comment + authorName
            cur.execute(
                "UPDATE itemAnnotations SET comment=?, authorName=? WHERE itemID=?",
                (comment, author, annotation_id),
            )
            updated_count += 1
        
        conn.commit()
        return {
            "status": "✓" if updated_count > 0 else "⚠",
            "updated": updated_count,
            "errors": errors if errors else None,
        }
    
    except sqlite3.OperationalError as e:
        conn.rollback()
        return {
            "status": "✗",
            "error": f"Database locked or write failed: {e}",
        }
    except Exception as e:
        conn.rollback()
        return {
            "status": "✗",
            "error": f"Batch update failed: {e}",
        }
    finally:
        conn.close()


def verify_annotations(parent_item_id: int) -> Dict:
    """Verify all annotations under a PDF have non-NULL comment + authorName.
    
    Returns:
        {
            "total": N,
            "with_comment": M,
            "with_author": K,
            "missing": [{"id": ..., "has_comment": ..., "has_author": ...}, ...],
        }
    """
    if not ZOTERO_DB.exists():
        return {"status": "✗", "error": f"Zotero DB not found: {ZOTERO_DB}"}
    
    close_zotero_first()
    conn = sqlite3.connect(str(ZOTERO_DB), timeout=30)
    
    try:
        cur = conn.cursor()
        
        # Get all annotations for this PDF
        cur.execute(
            "SELECT itemID, comment, authorName FROM itemAnnotations WHERE parentItemID=? ORDER BY itemID",
            (parent_item_id,),
        )
        rows = cur.fetchall()
        
        total = len(rows)
        with_comment = sum(1 for _, c, _ in rows if c and c.strip())
        with_author = sum(1 for _, _, a in rows if a)
        
        missing = []
        for item_id, comment, author in rows:
            has_comment = bool(comment and comment.strip())
            has_author = bool(author)
            if not (has_comment and has_author):
                missing.append({
                    "id": item_id,
                    "has_comment": has_comment,
                    "has_author": has_author,
                })
        
        return {
            "status": "✓",
            "total": total,
            "with_comment": with_comment,
            "with_author": with_author,
            "missing": missing,
        }
    
    except Exception as e:
        return {
            "status": "✗",
            "error": f"Verification failed: {e}",
        }
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python zotero_annotation_sync.py verify <parent_item_id>")
        print("  python zotero_annotation_sync.py update <parent_item_id> <annotation_id> '<comment>'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "verify":
        parent_id = int(sys.argv[2])
        result = verify_annotations(parent_id)
        print(result)
    
    elif command == "update":
        parent_id = int(sys.argv[2])
        annot_id = int(sys.argv[3])
        comment = sys.argv[4] if len(sys.argv) > 4 else ""
        result = update_annotation_comment(parent_id, annot_id, comment)
        print(result)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
