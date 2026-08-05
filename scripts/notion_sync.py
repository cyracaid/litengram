"""Notion sync for LitEngram v1.2 — write notes to "每日读读文献" page."""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

from notion_client import Client

CONFIG_PATH = Path(os.environ.get("LITENGRAM_CONFIG_PATH", str(Path.home() / "Documents/CAD/.litengram_config.json")))
DAILY_PAGE_NAME = "每日读读文献"
MAX_APPEND = 100
MAX_DEPTH = 2


class NotionSync:
    def __init__(self):
        self.token = os.environ.get("NOTION_TOKEN")
        self.client = None
        self.daily_page_id = None
        self.status = {}

    def _load_cache(self):
        if CONFIG_PATH.exists():
            try:
                return json.loads(CONFIG_PATH.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save_cache(self, data):
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def resolve_page_id(self):
        cache = self._load_cache()
        if cache.get("notion_daily_page_id"):
            self.daily_page_id = cache["notion_daily_page_id"]
            return True

        if not self.client:
            return False

        try:
            results = self.client.search(
                query=DAILY_PAGE_NAME,
                filter={"property": "object", "value": "page"},
            ).get("results", [])

            for r in results:
                # Find the property with type "title" (key may be "Title" / "title" / "Name")
                page_title = ""
                for prop in r.get("properties", {}).values():
                    if prop.get("type") == "title" and prop.get("title"):
                        page_title = prop["title"][0].get("plain_text", "")
                        break
                if page_title == DAILY_PAGE_NAME:
                    self.daily_page_id = r["id"]
                    self._save_cache({"notion_daily_page_id": self.daily_page_id})
                    return True

            print(f"Notion: ❌ 页「{DAILY_PAGE_NAME}」未找到，请确认已分享给 integration")
            return False

        except Exception as e:
            print(f"Notion: ❌ Search API 报错: {e}")
            return False

    def _get_toggle_id(self, parent_id, target_title):
        """Find or create a toggle block with exact title under parent_id."""
        children = []
        cursor = None
        while True:
            resp = self.client.blocks.children.list(
                block_id=parent_id,
                start_cursor=cursor,
                page_size=100,
            )
            children.extend(resp.get("results", []))
            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")

        for child in children:
            if child["type"] == "toggle":
                text = ""
                for rt in child["toggle"]["rich_text"]:
                    text += rt.get("plain_text", "")
                if text.strip() == target_title:
                    return child["id"], False  # existed

        new = self.client.blocks.children.append(
            block_id=parent_id,
            children=[
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": target_title},
                            }
                        ]
                    },
                }
            ],
        )
        new_id = new["results"][0]["id"]
        return new_id, True  # created

    def _find_paper_toggle(self, parent_id, paper_title):
        """Check if paper toggle already exists under parent toggle."""
        try:
            children = self.client.blocks.children.list(
                block_id=parent_id, page_size=100
            ).get("results", [])

            for child in children:
                if child["type"] == "toggle":
                    text = "".join(
                        rt.get("plain_text", "")
                        for rt in child["toggle"]["rich_text"]
                    )
                    if paper_title in text:
                        return child["id"]
        except Exception:
            pass
        return None

    def _md_to_notion_blocks(self, md_text, depth=0):
        """Convert markdown note to Notion blocks up to MAX_DEPTH nesting."""
        blocks = []
        lines = md_text.strip().split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # heading_3: ### ...
            if stripped.startswith("### "):
                blocks.append(self._text_block("heading_3", stripped[4:]))
                i += 1
                continue

            # heading_2: ## ... (skip — used as toggle title)
            if stripped.startswith("## "):
                i += 1
                continue

            # heading_1: # ... (skip)
            if stripped.startswith("# "):
                i += 1
                continue

            # blockquote — merge consecutive > lines into one block
            if stripped.startswith(">"):
                quote_lines = []
                while i < len(lines):
                    ls = lines[i].strip()
                    if ls.startswith(">"):
                        text = ls[1:].strip()
                        if text:
                            quote_lines.append(text)
                        i += 1
                    else:
                        break
                if quote_lines:
                    merged = "\n".join(quote_lines)
                    blocks.append(self._text_block("quote", merged))
                continue

            # bullet list: - or * or 1.
            if stripped.startswith("- ") or stripped.startswith("* "):
                lis = []
                while i < len(lines):
                    ls = lines[i].strip()
                    if ls.startswith("- ") or ls.startswith("* "):
                        lis.append(ls[2:])
                        i += 1
                    else:
                        break
                for item in lis:
                    blocks.append(self._text_block("bulleted_list_item", item))
                continue

            if re.match(r"^\d+\. ", stripped):
                lis = []
                while i < len(lines):
                    ls = lines[i].strip()
                    m = re.match(r"^\d+\.\s*(.*)", ls)
                    if m:
                        lis.append(m.group(1))
                        i += 1
                    else:
                        break
                for item in lis:
                    blocks.append(self._text_block("bulleted_list_item", item))
                continue

            # table detection (simple |...|...|)
            if "|" in stripped and stripped.count("|") >= 3:
                table = self._parse_table(lines, i)
                if table:
                    blocks.append(table)
                    i += len(table.get("table", {}).get("children", [])) + 1
                    continue

            # default: paragraph
            blocks.append(self._text_block("paragraph", stripped))
            i += 1

        return blocks

    def _parse_table(self, lines, start):
        """Parse a simple markdown table into Notion table blocks."""
        rows = []
        i = start
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.split("|")[1:-1]]
                # Skip separator row (all cells are --- or similar)
                if cells and all(re.match(r"^-+$", c) for c in cells):
                    i += 1
                    continue
                if cells:
                    rows.append(cells)
            else:
                break
            i += 1

        if len(rows) < 2:
            return None

        table_children = []
        for idx, row in enumerate(rows):
            cells_list = []
            for cell in row:
                cells_list.append(
                    [
                        {
                            "type": "text",
                            "text": {"content": cell},
                            "annotations": {"bold": idx == 0},
                        }
                    ]
                )
            table_children.append(
                {
                    "type": "table_row",
                    "table_row": {"cells": cells_list},
                }
            )

        return {
            "type": "table",
            "table": {
                "table_width": len(rows[0]),
                "has_column_header": True,
                "children": table_children,
            },
        }

    def _text_block(self, block_type, text):
        """Create a Notion block with bold/italic annotations from markdown."""
        rich_text = self._parse_rich_text(text)
        if block_type in ("toggle",):
            return {"type": block_type, block_type: {"rich_text": rich_text}}
        return {"type": block_type, block_type: {"rich_text": rich_text}}

    def _parse_rich_text(self, text):
        """Parse markdown bold/italic into Notion rich_text annotations."""
        parts = []
        # Simple bold: **text** and italic: *text*
        pattern = re.compile(r"(\*\*(.+?)\*\*|\*(.+?)\*)")
        last_end = 0
        for m in pattern.finditer(text):
            if m.start() > last_end:
                parts.append(
                    {
                        "type": "text",
                        "text": {"content": text[last_end : m.start()]},
                    }
                )
            if m.group(2):  # bold
                parts.append(
                    {
                        "type": "text",
                        "text": {"content": m.group(2)},
                        "annotations": {"bold": True},
                    }
                )
            else:  # italic
                parts.append(
                    {
                        "type": "text",
                        "text": {"content": m.group(3)},
                        "annotations": {"italic": True},
                    }
                )
            last_end = m.end()

        if last_end < len(text):
            parts.append(
                {"type": "text", "text": {"content": text[last_end:]}}
            )

        if not parts:
            parts = [{"type": "text", "text": {"content": text}}]

        # Truncate rich_text entries to 2000 chars
        truncated = []
        for p in parts:
            content = p["text"]["content"]
            while len(content) > 2000:
                truncated.append(
                    {"type": "text", "text": {"content": content[:2000]}, **{k: v for k, v in p.items() if k != "text"}}
                )
                content = content[2000:]
            if content:
                truncated.append(
                    {"type": "text", "text": {"content": content}, **{k: v for k, v in p.items() if k != "text"}}
                )
        return truncated

    def _clear_children(self, block_id):
        """Archive all children of a block (delete them)."""
        cursor = None
        while True:
            resp = self.client.blocks.children.list(
                block_id=block_id, page_size=100, start_cursor=cursor
            )
            for child in resp.get("results", []):
                try:
                    self.client.blocks.update(block_id=child["id"], archived=True)
                except Exception:
                    pass
            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")

    def _append_blocks(self, block_id, blocks, retries=2):
        """Append blocks with 100-at-a-time batching and retry on 429."""
        for batch_start in range(0, len(blocks), MAX_APPEND):
            batch = blocks[batch_start : batch_start + MAX_APPEND]
            for attempt in range(retries + 1):
                try:
                    self.client.blocks.children.append(
                        block_id=block_id, children=batch
                    )
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < retries:
                        time.sleep(2 ** (attempt + 1))
                        continue
                    raise e

    def sync_note(self, title, markdown_content, date_str=None, skip_if_exists=True):
        """Sync a note to Notion under today's date toggle.

        If skip_if_exists=True: skip if paper already exists (no-op).
        If skip_if_exists=False: update existing paper content in-place.
        Never deletes other papers under the same date toggle.

        Returns: "✅", "✅(已更新)", or "❌(reason)"
        """
        if not self.token:
            return "❌(NOTION_TOKEN 未设置)"

        self.client = Client(auth=self.token)

        if not self.resolve_page_id():
            return "❌(找不到「每日读读文献」页)"

        date_str = date_str or datetime.now().strftime("%Y-%m-%d")

        try:
            # Step 1: find or create date toggle (never delete existing date toggles)
            date_toggle_id, is_new = self._get_toggle_id(
                self.daily_page_id, date_str
            )

            # Step 2: parse markdown into blocks
            blocks = self._md_to_notion_blocks(markdown_content)

            # Step 3: check if paper toggle already exists
            existing_id = self._find_paper_toggle(date_toggle_id, title)
            if existing_id:
                if skip_if_exists:
                    return "✅(已存在，跳过)"
                else:
                    # UPDATE mode: clear old children, re-append
                    self._clear_children(existing_id)
                    self._append_blocks(existing_id, blocks)
                    return "✅(已更新)"

            # Step 4: create paper toggle (first time)
            paper_toggle = {
                "type": "toggle",
                "toggle": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": title},
                        }
                    ]
                },
            }
            created = self.client.blocks.children.append(
                block_id=date_toggle_id,
                children=[paper_toggle],
            )
            paper_id = created["results"][0]["id"]

            # Step 5: append content blocks inside the paper toggle
            self._append_blocks(paper_id, blocks)

            return "✅"

        except Exception as e:
            return f"❌({e})"

    def sync_annotations_only(self, title, annotations_markdown, date_str=None):
        """只更新笔记中 📌 关键标注 节，不动其他内容。

        用于 re-annotation 场景：论文分析不变，只多了标注。
        当前实现简化：退化为完整 sync_note（可靠但慢）。
        未来优化：块级 diff，仅替换 📌 标注相关 blocks。
        """
        return self.sync_note(
            title=title,
            markdown_content=annotations_markdown,
            date_str=date_str,
            skip_if_exists=False,
        )
