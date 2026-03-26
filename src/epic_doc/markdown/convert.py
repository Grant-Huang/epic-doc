"""Minimal Markdown -> epic-doc blocks converter.

Goal: reduce maintenance cost by using Markdown as the source-of-truth.

This converter is intentionally conservative and uses only the stdlib.
Supported (v0):
- Headings: # .. ####
- HR: ---
- Fenced code blocks: ```lang ... ```
- Bullet lists: - item
- Numbered lists: 1. item
- Pipe tables (GitHub style)
- Paragraphs
"""

from __future__ import annotations

import re
from typing import Any, Optional

_RE_HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
_RE_BULLET = re.compile(r"^\s*-\s+(.*)$")
_RE_NUMBER = re.compile(r"^\s*\d+\.\s+(.*)$")
_RE_FENCE = re.compile(r"^```(\w+)?\s*$")


def markdown_to_blocks(md: str) -> list[dict[str, Any]]:
    lines = md.splitlines()
    i = 0
    blocks: list[dict[str, Any]] = []

    def _flush_paragraph(buf: list[str]) -> None:
        text = "\n".join([s.rstrip() for s in buf]).strip()
        if text:
            blocks.append({"type": "paragraph", "text": text})
        buf.clear()

    para_buf: list[str] = []

    def _consume_list(start_idx: int) -> tuple[int, Optional[str], list[str]]:
        j = start_idx
        items: list[str] = []
        style: Optional[str] = None
        while j < len(lines):
            m_b = _RE_BULLET.match(lines[j])
            m_n = _RE_NUMBER.match(lines[j])
            if m_b:
                style = style or "bullet"
                if style != "bullet":
                    break
                items.append(m_b.group(1).strip())
                j += 1
                continue
            if m_n:
                style = style or "numbered"
                if style != "numbered":
                    break
                items.append(m_n.group(1).strip())
                j += 1
                continue
            break
        return j, style, items

    def _is_table_separator(row: list[str]) -> bool:
        if not row:
            return False
        # like: | --- | :---: |
        for cell in row:
            c = cell.strip()
            if not c:
                return False
            c = c.strip(":")
            if not c or any(ch != "-" for ch in c):
                return False
        return True

    def _split_pipe_row(s: str) -> list[str]:
        raw = s.strip()
        if raw.startswith("|"):
            raw = raw[1:]
        if raw.endswith("|"):
            raw = raw[:-1]
        parts = [p.strip() for p in raw.split("|")]
        return parts

    while i < len(lines):
        line = lines[i]

        # fenced code block
        m_f = _RE_FENCE.match(line)
        if m_f:
            _flush_paragraph(para_buf)
            lang = (m_f.group(1) or None)
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not _RE_FENCE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines) and _RE_FENCE.match(lines[i]):
                i += 1
            blocks.append({"type": "code", "language": lang, "code": "\n".join(code_lines)})
            continue

        # hr
        if line.strip() == "---":
            _flush_paragraph(para_buf)
            blocks.append({"type": "hr"})
            i += 1
            continue

        # heading
        m_h = _RE_HEADING.match(line)
        if m_h:
            _flush_paragraph(para_buf)
            level = len(m_h.group(1))
            text = m_h.group(2).strip()
            blocks.append({"type": "heading", "text": text, "level": level})
            i += 1
            continue

        # table (very small heuristic: a pipe row + separator row)
        if "|" in line:
            row1 = _split_pipe_row(line)
            if i + 1 < len(lines) and "|" in lines[i + 1]:
                row2 = _split_pipe_row(lines[i + 1])
                if len(row1) == len(row2) and _is_table_separator(row2):
                    _flush_paragraph(para_buf)
                    headers = row1
                    i += 2
                    data: list[list[Any]] = [headers]
                    while i < len(lines) and "|" in lines[i]:
                        r = _split_pipe_row(lines[i])
                        if len(r) != len(headers):
                            break
                        data.append(r)
                        i += 1
                    blocks.append(
                        {"type": "table", "headers": True, "style": "striped", "data": data}
                    )
                    continue

        # list
        if _RE_BULLET.match(line) or _RE_NUMBER.match(line):
            _flush_paragraph(para_buf)
            j, style, items = _consume_list(i)
            if items:
                blocks.append({"type": "list", "style": style or "bullet", "items": items})
                i = j
                continue

        # blank line splits paragraphs
        if not line.strip():
            _flush_paragraph(para_buf)
            i += 1
            continue

        para_buf.append(line)
        i += 1

    _flush_paragraph(para_buf)
    return blocks

