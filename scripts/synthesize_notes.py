"""Cross-paper knowledge synthesis for LitEngram (v2.0).

Reads all litreview/*.md notes and produces a structured synthesis.
v2.0: notes use the 8-anchor skeleton (基本信息 / 这篇在讲什么 / 核心论证 /
作者论证与证据 / 局限与批判 / 我的疑问 / 待验证 / 和我的研究的关系 / 原文摘要).
This script parses those anchors; it tolerates older notes (falls back to
title+grade only) without crashing.
"""

import os, re
from pathlib import Path
from collections import defaultdict

LITREVIEW_DIR = Path(os.environ.get(
    "LITENGRAM_LITREVIEW_DIR",
    str(Path.home() / "Documents/litengram/litreview")
))

# v2.0 anchor headings (frozen — see literature_note_template.md)
ANCHORS = [
    "基本信息",
    "这篇在讲什么",
    "核心论证",
    "作者论证与证据",
    "局限与批判",
    "我的疑问",
    "待验证",
    "和我的研究的关系",
    "原文摘要",
]

# Older headings we still map, for backward tolerance
LEGACY_MAP = {
    "与你领域的关系": "和我的研究的关系",
    "与你研究的关系": "和我的研究的关系",
}

GRADE_SYMBOLS = ["⛰️", "⚔️", "📌", "🌫️"]


def _split_sections(content):
    """Return {heading: body_text} by '## ' headings. Body excludes nested '### '."""
    sections = {}
    current = None
    buf = []
    for line in content.split("\n"):
        if line.startswith("## ") and not line.startswith("### "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            if current is not None:
                buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def _norm_heading(h):
    h = h.strip()
    for old, new in LEGACY_MAP.items():
        if old in h:
            return new
    for a in ANCHORS:
        if h.startswith(a) or a in h:
            return a
    return h


def parse_note(filepath):
    content = Path(filepath).read_text()
    lines = content.split("\n")

    # title: first '# ' line, cleaned of emoji / boilerplate
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    title = re.sub(r"^[\U0001F000-\U0001FAFF\u2190-\u27BF\u2600-\u26FF\s]+", "", title)
    title = re.sub(r"文献精读\s*[—\-–]?\s*", "", title)
    title = re.sub(r"\s*[—\-–]\s*\d{4}-\d{2}-\d{2}.*$", "", title)
    title = re.sub(r"^产物\s*\d+[:：].*", "", title).strip() or title
    title = title.strip(" —-·")
    if not title:
        title = Path(filepath).stem

    # grade: first grade symbol in the header (first ~12 lines)
    grade = ""
    for line in lines[:12]:
        for sym in GRADE_SYMBOLS:
            if sym in line:
                grade = sym
                break
        if grade:
            break

    raw = _split_sections(content)
    sections = {}
    for h, body in raw.items():
        sections[_norm_heading(h)] = body

    def bullets(key):
        body = sections.get(key, "")
        out = []
        for line in body.split("\n"):
            s = line.strip()
            if s.startswith("- ") and len(s) > 3:
                out.append(s[2:].strip())
        return out

    return {
        "file": str(filepath),
        "title": title,
        "grade": grade,
        "sections": sections,
        "relations": bullets("和我的研究的关系"),
        "pending": bullets("待验证"),
        "questions": bullets("我的疑问"),
    }


def synthesize(notes_dir=None):
    if notes_dir is None:
        notes_dir = LITREVIEW_DIR

    notes = []
    for f in sorted(Path(notes_dir).glob("*.md")):
        if f.name.startswith("_"):          # skip _synthesis_*.md etc.
            continue
        try:
            parsed = parse_note(f)
        except Exception:
            continue
        if parsed["title"] and "external_skills" not in str(f):
            notes.append(parsed)

    if not notes:
        return "没有找到可合成的笔记。"

    out = []
    out.append("# LitEngram 跨论文知识合成 (v2.0)\n")
    out.append(f"基于 {len(notes)} 篇已精读论文\n")

    out.append("## 论文清单\n")
    for n in notes:
        g = n["grade"] or "·"
        out.append(f"- {g} {n['title']}  — {Path(n['file']).name}")
    out.append("")

    # 战略嫁接矩阵: from 和我的研究的关系
    out.append("## 战略嫁接矩阵\n")
    out.append("| 来源论文 | 可以接到的点 |")
    out.append("|-----------|--------------|")
    any_bridge = False
    for n in notes:
        for b in n["relations"]:
            any_bridge = True
            short = b[:100] + ("..." if len(b) > 100 else "")
            out.append(f"| {n['title'][:40]} | {short} |")
    if not any_bridge:
        out.append("| (无) | 笔记里没有列出具体的嫁接点 |")
    out.append("")

    # 共享行动项: from 待验证
    out.append("## 共享行动项（来自各篇「待验证」）\n")
    actions = defaultdict(list)
    for n in notes:
        for a in n["pending"]:
            actions[a[:70]].append(n["title"])
    if actions:
        for a, papers in actions.items():
            out.append(f"- {a}  — 来源: {', '.join(p[:30] for p in papers)}")
    else:
        out.append("(各篇未列「待验证」条目)")
    out.append("")

    # 悬而未决的问题: from 我的疑问
    out.append("## 悬而未决的问题（来自各篇「我的疑问」）\n")
    qcount = 0
    for n in notes:
        for q in n["questions"]:
            qcount += 1
            out.append(f"- {q[:100]}  — {n['title'][:40]}")
    if qcount == 0:
        out.append("(各篇未列「我的疑问」条目)")
    out.append("")

    out.append("> 说明：跨论文的「共享缺口」与「发现张力」需要语义判断，脚本不臆造——")
    out.append("> 请由 agent/用户基于上面各篇的「核心论证」「局限与批判」「和我的研究的关系」人工归纳。")
    out.append("")

    return "\n".join(out)


if __name__ == "__main__":
    print(synthesize())
