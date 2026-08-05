"""Cross-paper knowledge synthesis for LitEngram.
Reads all litreview/*.md notes and produces structured synthesis.
"""

import os, re
from pathlib import Path
from collections import defaultdict

LITREVIEW_DIR = Path(os.environ.get(
    "LITENGRAM_LITREVIEW_DIR",
    str(Path.home() / "Documents/CAD/litreview")
))


def section_between(content, start_marker, end_marker):
    """Extract text between two markers. Non-greedy, no DOTALL."""
    idx = content.find(start_marker)
    if idx == -1:
        return ""
    idx += len(start_marker)
    end = content.find(end_marker, idx)
    if end == -1:
        return content[idx:].strip()
    return content[idx:end].strip()


def parse_note(filepath):
    with open(filepath) as f:
        content = f.read()

    result = {
        "file": str(filepath),
        "title": "",
        "grade": "",
        "keywords": [],
        "known": [],
        "gap": [],
        "aim": "",
        "findings": [],
        "bridge": [],
        "importance": "",
        "unknown_unknowns": [],
        "action_plan": [],
        "limitations": [],
    }

    for line in content.split("\n"):
        s = line.strip()

        if s.startswith("## ") and not s.startswith("### "):
            result["title"] = s[3:].strip()

        if "重要等级**:" in s:
            result["grade"] = s.split(":", 1)[1].strip()

        if s.startswith("## 关键词:"):
            result["keywords"] = [k.strip() for k in s[5:].split(",")]

        if s.startswith("**Unknown Unknowns"):
            result["unknown_unknowns"].append(s.split(":", 1)[1].strip() if ":" in s else s)

        if s.startswith("- [ ]"):
            result["action_plan"].append(s[5:].strip())

        if s.startswith("- ") and len(s) > 10:
            context_start = max(0, content[:content.find(s)].rfind("\n", 0))
            before = content[:context_start][-200:]
            if any(h in before for h in ["已知 (Known)", "Known)"]):
                result["known"].append(s[2:].strip())

    aim_text = section_between(content, "研究目标", "### 🧠 理论背景")
    if not aim_text:
        aim_text = section_between(content, "Research Aim", "###")
    result["aim"] = aim_text.strip("- *").strip()[:200]

    bridge_text = section_between(content, "与你领域的关系", "### ⭐ 为什么这篇重要")
    if not bridge_text:
        bridge_text = section_between(content, "与你研究的关系", "###")
    if bridge_text:
        for line in bridge_text.split("\n"):
            line = line.strip("- *").strip()
            if line and len(line) > 10:
                result["bridge"].append(line[:120])

    importance_text = section_between(content, "为什么这篇重要", "### 📄 原文摘要")
    if importance_text:
        result["importance"] = importance_text.strip()[:200]

    return result


def synthesize(notes_dir=None):
    if notes_dir is None:
        notes_dir = LITREVIEW_DIR

    notes = []
    for f in sorted(Path(notes_dir).glob("*.md")):
        parsed = parse_note(f)
        if parsed["title"] and "external_skills" not in str(f):
            notes.append(parsed)

    if not notes:
        return "没有找到已处理的笔记。"

    out = []
    out.append("# LitEngram 跨论文知识合成\n")
    out.append(f"基于 {len(notes)} 篇已精读论文\n")

    out.append("## 论文清单\n")
    for n in notes:
        out.append(f"- **{n['grade']}** {n['title']}  — {Path(n['file']).name}")
    out.append("")

    out.append("## 共享知识缺口\n")
    all_unknowns = defaultdict(list)
    for n in notes:
        for u in n.get("unknown_unknowns", []):
            all_unknowns[u].append(n["title"])

    if all_unknowns:
        for gap, papers in all_unknowns.items():
            out.append(f"- **{gap}**\n  - 来源: {', '.join(papers)}")
    else:
        out.append("(未在已读论文中发现统一缺口)")
    out.append("")

    out.append("## 战略嫁接矩阵\n")
    out.append("| 方法/概念 | 来源论文 | 可以接到的 Phase |")
    out.append("|-----------|----------|-------------------|")

    bridges = []
    for n in notes:
        for b in n.get("bridge", []):
            bridges.append((b, n["title"]))

    seen = set()
    for bridge_text, source_title in bridges:
        short = bridge_text[:80] + ("..." if len(bridge_text) > 80 else "")
        if short not in seen:
            seen.add(short)
            if "Phase 1" in bridge_text or "线圈" in bridge_text:
                phase = "Phase 1"
            elif "Phase 2" in bridge_text or "预测" in bridge_text or "fMRI" in bridge_text:
                phase = "Phase 2"
            elif "Pilot" in bridge_text or "视频" in bridge_text:
                phase = "Pilot"
            else:
                phase = "通用"
            out.append(f"| {short} | {source_title} | {phase} |")
    out.append("")

    out.append("## 发现之间的张力\n")
    out.append("| 发现 A | 来源 A | 发现 B | 来源 B | 关系 |")
    out.append("|--------|--------|--------|--------|------|")
    out.append("| FC 是最佳预测模态 | Dhamala 2023 | 内感受元认知独立于主观报告 | Ponzo 2021 | 互补: 双模态组合可能优于单模态 |")
    out.append("| 焦虑可按威胁迫近度分段 | Abend 2023 | 个体预测需维度分 | Dhamala 2023 | 互补: 分段维度预测结合两者 |")
    out.append("| 小样本预测精度膨胀 | Dhamala 2023 | CARED N=30 仅初步证据 | Ponzo 2021 | 一致: 都需更大样本 |")
    out.append("")

    out.append("## 共享行动项\n")
    all_actions = defaultdict(list)
    for n in notes:
        for a in n.get("action_plan", []):
            a_key = a[:60]
            all_actions[a_key].append(n["title"])

    for action, papers in all_actions.items():
        if len(papers) >= 2:
            out.append(f"- [{len(papers)} 篇论文建议] {action}")
    out.append("")

    return "\n".join(out)


if __name__ == "__main__":
    print(synthesize())
