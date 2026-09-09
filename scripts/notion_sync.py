"""Notion sync for LitEngram v1.2 — write notes to "每日读读文献" page."""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from notion_client import Client

from _markdown_blocks import parse_blocks, parse_inline_spans

CONFIG_PATH = Path(os.environ.get("LITENGRAM_CONFIG_PATH", str(Path.home() / "Documents/litengram/.litengram_config.json")))
DAILY_PAGE_NAME = "每日读读文献"
MAX_APPEND = 100


class NotionSync:
    def __init__(self):
        self.token = os.environ.get("NOTION_TOKEN")
        # Create the client up front (not just inside sync_note) so the
        # documented standalone usage in SKILL.md — `ns = NotionSync();
        # ns.resolve_page_id()` — actually works on a cold cache instead
        # of silently returning False because no client existed yet.
        self.client = Client(auth=self.token) if self.token else None
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
        cached_id = cache.get("notion_daily_page_id")

        if cached_id:
            if self.client:
                # Verify the cached page still exists / is still shared
                # with the integration before trusting it — previously a
                # renamed, deleted, or unshared page would only surface
                # as a confusing raw exception deep inside sync_note,
                # with no way to refresh the cache short of hand-editing
                # the config file.
                try:
                    self.client.pages.retrieve(page_id=cached_id)
                    self.daily_page_id = cached_id
                    return True
                except Exception:
                    pass  # stale cache — fall through and re-resolve below
            else:
                # No client to verify with; trust the cache optimistically.
                self.daily_page_id = cached_id
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

    def _get_toggle_id(self, parent_id, target_title, cache_key=None):
        """Find or create a toggle block with exact title under parent_id.

        If cache_key is given (used for the per-date toggle), checks/updates
        a persisted id cache first. Without this, every single sync call —
        even to append one more paper under today's date — had to page
        through *every* child of the root page to relocate today's toggle,
        an ever-growing linear scan as months of reading history pile up.
        """
        if cache_key:
            cache = self._load_cache()
            cached_id = cache.get("notion_toggle_ids", {}).get(cache_key)
            if cached_id:
                try:
                    self.client.blocks.retrieve(block_id=cached_id)
                    return cached_id, False
                except Exception:
                    pass  # stale — fall through to full search/create below

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
                    if cache_key:
                        self._cache_toggle_id(cache_key, child["id"])
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
        if cache_key:
            self._cache_toggle_id(cache_key, new_id)
        return new_id, True  # created

    def _cache_toggle_id(self, date_str, toggle_id):
        cache = self._load_cache()
        toggle_map = cache.get("notion_toggle_ids", {})
        toggle_map[date_str] = toggle_id
        cache["notion_toggle_ids"] = toggle_map
        self._save_cache(cache)

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

    def _md_to_notion_blocks(self, md_text):
        """Convert a Markdown note into Notion blocks.

        Block splitting is shared with zotero_sync.py via
        _markdown_blocks.py (see that module's docstring for why —
        the two converters used to be separate copies that had already
        started drifting). `#`/`##` headings are skipped since they're
        used as toggle titles elsewhere; `###` and `####` both map to
        Notion's heading_3, since Notion has no heading_4.
        """
        blocks = []
        for block in parse_blocks(md_text):
            btype = block["type"]

            if btype == "heading":
                if block["level"] in (1, 2):
                    continue
                blocks.append(self._text_block("heading_3", block["text"]))

            elif btype == "paragraph":
                blocks.append(self._text_block("paragraph", block["text"]))

            elif btype == "blockquote":
                blocks.append(self._text_block("quote", "\n".join(block["lines"])))

            elif btype == "bullet_list":
                for item in block["items"]:
                    blocks.append(self._text_block("bulleted_list_item", item))

            elif btype == "numbered_list":
                # Previously these were rendered as bulleted_list_item,
                # which silently discarded the ordering. Notion has its
                # own numbered_list_item block type for this.
                for item in block["items"]:
                    blocks.append(self._text_block("numbered_list_item", item))

            elif btype == "table":
                table = self._table_block(block["rows"])
                if table:
                    blocks.append(table)

            elif btype == "hr":
                # Notion's native divider block — previously "---" fell
                # through to the default paragraph case and showed up
                # as a literal "---" line of text.
                blocks.append({"type": "divider", "divider": {}})

        return blocks

    def _table_block(self, rows):
        """Build a Notion table block from parsed rows (rows[0] is the header)."""
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
        """Parse markdown bold/italic/code into Notion rich_text annotations.

        Uses the shared inline-span parser (_markdown_blocks.py). This
        also picks up `code` spans, which the old hand-rolled bold/italic
        regex here never recognized — inline `code` used to reach Notion
        as literal backtick characters instead of a code-formatted span.
        """
        parts = []
        for kind, content in parse_inline_spans(text):
            entry = {"type": "text", "text": {"content": content}}
            if kind == "bold":
                entry["annotations"] = {"bold": True}
            elif kind == "italic":
                entry["annotations"] = {"italic": True}
            elif kind == "code":
                entry["annotations"] = {"code": True}
            parts.append(entry)

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

    def _clear_children(self, block_id, retries=2):
        """Archive all children of a block (delete them).

        Returns the list of child block IDs that could not be archived.
        Previously any failure here (most commonly a 429 rate limit) was
        swallowed silently with no retry, so an update could leave stale
        old content mixed in with the freshly appended new content with
        no error surfaced anywhere.
        """
        cursor = None
        failed = []
        while True:
            resp = self.client.blocks.children.list(
                block_id=block_id, page_size=100, start_cursor=cursor
            )
            for child in resp.get("results", []):
                for attempt in range(retries + 1):
                    try:
                        self.client.blocks.update(block_id=child["id"], archived=True)
                        break
                    except Exception as e:
                        if "429" in str(e) and attempt < retries:
                            time.sleep(2 ** (attempt + 1))
                            continue
                        failed.append(child["id"])
                        break
            if not resp.get("has_more"):
                break
            cursor = resp.get("next_cursor")
        return failed

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

        if not self.client:
            self.client = Client(auth=self.token)

        if not self.resolve_page_id():
            return "❌(找不到「每日读读文献」页)"

        date_str = date_str or datetime.now().strftime("%Y-%m-%d")

        try:
            # Step 1: find or create date toggle (never delete existing date
            # toggles). cache_key=date_str avoids re-listing every child of
            # the root page on every single sync call.
            date_toggle_id, is_new = self._get_toggle_id(
                self.daily_page_id, date_str, cache_key=date_str
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
                    failed = self._clear_children(existing_id)
                    self._append_blocks(existing_id, blocks)
                    if failed:
                        return f"✅(已更新，但 {len(failed)} 个旧块未能清除，可能有残留内容)"
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
