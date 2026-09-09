"""Shared Markdown parsing for LitEngram's sync targets.

Both zotero_sync.py (Markdown -> Zotero XHTML) and notion_sync.py
(Markdown -> Notion API blocks) used to carry their own copies of the
same block-level splitter (headings / paragraphs / lists / tables /
blockquotes / hr) and the same inline **bold** / *italic* / `code`
parsing. Two copies meant they could drift — e.g. the table-detection
heuristic ended up different between the two, and numbered lists were
only rendered correctly on one side. Parsing lives here once; each
target only does the last step of turning blocks/spans into its own
output format.
"""

import re

_HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)")
_BULLET_RE = None  # bullets are matched by plain str.startswith below
_NUMBERED_RE = re.compile(r"^\d+\.\s*(.*)")
_HR_RE = re.compile(r"^-{3,}$")
_SEPARATOR_CELL_RE = re.compile(r"^-+$")
_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_ITALIC_RE = re.compile(r"(\*\*(.+?)\*\*|\*(.+?)\*)")


def parse_blocks(md_text):
    """Split Markdown text into a list of block dicts.

    Each block is one of:
      {"type": "heading", "level": 1-4, "text": str}
      {"type": "paragraph", "text": str}
      {"type": "blockquote", "lines": [str, ...]}
      {"type": "bullet_list", "items": [str, ...]}
      {"type": "numbered_list", "items": [str, ...]}
      {"type": "table", "rows": [[str, ...], ...]}   # rows[0] is the header row
      {"type": "hr"}
    """
    lines = md_text.strip().split("\n")
    blocks = []
    para = []
    i = 0

    def flush_para():
        if para:
            merged = " ".join(para).strip()
            if merged:
                blocks.append({"type": "paragraph", "text": merged})
            para.clear()

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        if not s:
            flush_para()
            i += 1
            continue

        heading_match = _HEADING_RE.match(s)
        if heading_match:
            flush_para()
            blocks.append(
                {"type": "heading", "level": len(heading_match.group(1)), "text": heading_match.group(2)}
            )
            i += 1
            continue

        if s.startswith(">"):
            flush_para()
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
                blocks.append({"type": "blockquote", "lines": quote_lines})
            continue

        if s.startswith("- ") or s.startswith("* "):
            flush_para()
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith("- ") or ls.startswith("* "):
                    items.append(ls[2:])
                    i += 1
                else:
                    break
            blocks.append({"type": "bullet_list", "items": items})
            continue

        m = _NUMBERED_RE.match(s)
        if m:
            flush_para()
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                mm = _NUMBERED_RE.match(ls)
                if mm:
                    items.append(mm.group(1))
                    i += 1
                else:
                    break
            blocks.append({"type": "numbered_list", "items": items})
            continue

        # Table: require a real "|...|" row (not just "3+ pipes anywhere in
        # the line") so sentences using "|" for conditional-probability
        # notation etc. aren't misdetected as tables.
        if s.startswith("|") and s.endswith("|") and s.count("|") >= 3:
            flush_para()
            rows = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith("|") and ls.endswith("|"):
                    cells = [c.strip() for c in ls.split("|")[1:-1]]
                    # Skip separator rows (|---|---|)
                    if cells and all(_SEPARATOR_CELL_RE.match(c) for c in cells):
                        i += 1
                        continue
                    if cells:
                        rows.append(cells)
                else:
                    break
                i += 1
            if len(rows) >= 2:
                blocks.append({"type": "table", "rows": rows})
            continue

        if _HR_RE.match(s):
            flush_para()
            blocks.append({"type": "hr"})
            i += 1
            continue

        para.append(s)
        i += 1

    flush_para()
    return blocks


def parse_inline_spans(text):
    """Split inline text into (kind, content) spans.

    kind is one of "text" / "bold" / "italic" / "code". Code spans are
    pulled out first so `**`/`*` characters inside backticks are never
    treated as bold/italic markers.
    """
    segments = []
    pos = 0
    for m in _CODE_RE.finditer(text):
        if m.start() > pos:
            segments.append(("text", text[pos : m.start()]))
        segments.append(("code", m.group(1)))
        pos = m.end()
    if pos < len(text):
        segments.append(("text", text[pos:]))
    if not segments:
        segments = [("text", text)]

    spans = []
    for kind, seg in segments:
        if kind == "code":
            spans.append(("code", seg))
            continue
        last_end = 0
        for m in _BOLD_ITALIC_RE.finditer(seg):
            if m.start() > last_end:
                spans.append(("text", seg[last_end : m.start()]))
            if m.group(2) is not None:
                spans.append(("bold", m.group(2)))
            else:
                spans.append(("italic", m.group(3)))
            last_end = m.end()
        if last_end < len(seg):
            spans.append(("text", seg[last_end:]))

    return spans or [("text", text)]
