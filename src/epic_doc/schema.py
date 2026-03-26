"""JSON/dict schema parser — converts a document definition dict into EpicDoc calls."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from epic_doc.builder import EpicDoc


def build_from_dict(definition: Dict[str, Any]) -> EpicDoc:
    """Build an EpicDoc instance from a definition dictionary.

    The dict structure mirrors the JSON schema documented in DESIGN.md.

    Example::

        doc = build_from_dict({
            "theme": "professional",
            "meta": {"title": "Report", "author": "Alice"},
            "header": {"text": "Confidential", "align": "right"},
            "footer": {"page_number": True},
            "blocks": [
                {"type": "heading", "text": "Introduction", "level": 1},
                {"type": "paragraph", "text": "This report covers..."},
                {"type": "table", "data": [["A", "B"], [1, 2]], "headers": True},
            ]
        })
        doc.save("output.docx")
    """
    theme    = definition.get("theme", "professional")
    template = definition.get("template")

    doc = EpicDoc(theme=theme, template=template)

    # Metadata
    meta = definition.get("meta", {})
    if meta:
        doc.set_metadata(
            title=meta.get("title"),
            author=meta.get("author"),
            subject=meta.get("subject"),
            description=meta.get("description"),
        )

    # Header
    header = definition.get("header")
    if header:
        if isinstance(header, str):
            doc.set_header(header)
        else:
            doc.set_header(
                text=header.get("text", ""),
                align=header.get("align", "right"),
            )

    # Footer
    footer = definition.get("footer")
    if footer:
        if isinstance(footer, bool) and footer:
            doc.set_footer(page_number=True)
        else:
            doc.set_footer(
                text=footer.get("text"),
                page_number=footer.get("page_number", True),
                align=footer.get("align", "center"),
            )

    # Blocks
    blocks = definition.get("blocks", [])
    for block in blocks:
        _process_block(doc, block)

    audit = definition.get("audit") or {}
    if isinstance(audit, dict) and audit.get("enabled"):
        title = audit.get("title") if isinstance(audit.get("title"), str) else "引用/追溯表"
        _append_audit_trail(doc, title=title, blocks=blocks)

    return doc


def _process_block(doc: EpicDoc, block: Dict[str, Any]) -> None:
    btype = block.get("type", "").lower()

    if btype == "heading":
        doc.add_heading(
            text=block["text"],
            level=block.get("level", 1),
            align=block.get("align", "left"),
        )

    elif btype == "paragraph":
        doc.add_paragraph(
            text=block["text"],
            bold=block.get("bold", False),
            italic=block.get("italic", False),
            underline=block.get("underline", False),
            color=block.get("color"),
            align=block.get("align", "left"),
            font_size=block.get("font_size"),
        )

    elif btype == "list":
        doc.add_list(
            items=block["items"],
            style=block.get("style", "bullet"),
        )

    elif btype in ("code", "code_block"):
        doc.add_code_block(
            code=block["code"],
            language=block.get("language"),
        )

    elif btype == "callout":
        doc.add_callout(
            text=block["text"],
            style=block.get("style", "info"),
            title=block.get("title"),
        )

    elif btype == "hyperlink":
        doc.add_hyperlink(
            text=block["text"],
            url=block["url"],
        )

    elif btype == "hr":
        doc.add_horizontal_rule()

    elif btype == "page_break":
        doc.add_page_break()

    elif btype == "section_break":
        doc.add_section_break(break_type=block.get("break_type", "next_page"))

    elif btype == "toc":
        doc.add_toc(
            title=block.get("title", "目录"),
            depth=block.get("depth", 3),
        )

    elif btype == "table":
        doc.add_table(
            data=block["data"],
            headers=block.get("headers", True),
            style=block.get("style", "striped"),
            col_widths=block.get("col_widths"),
            merge=_parse_merge(block.get("merge")),
            caption=block.get("caption"),
            align=block.get("align", "left"),
            font_size=block.get("font_size"),
            cell_align=block.get("cell_align", "left"),
        )

    elif btype == "chart":
        doc.add_chart(
            chart_type=block.get("chart_type", "bar"),
            data=block.get("data", {}),
            title=block.get("title"),
            xlabel=block.get("xlabel"),
            ylabel=block.get("ylabel"),
            width=block.get("width", 5.5),
            height=block.get("height", 3.2),
            colors=block.get("colors"),
            caption=block.get("caption"),
            show_values=block.get("show_values", False),
            show_grid=block.get("show_grid", True),
            legend=block.get("legend", True),
        )

    elif btype == "flowchart":
        nodes_raw = block.get("nodes", {})
        edges_raw = block.get("edges", [])
        # edges may come as lists (from JSON) — convert to tuples
        edges = [tuple(e) for e in edges_raw]
        doc.add_flowchart(
            nodes=nodes_raw,
            edges=edges,
            direction=block.get("direction", "TB"),
            width=block.get("width", 5.0),
            caption=block.get("caption"),
        )

    elif btype == "image":
        doc.add_image(
            source=block["path"],
            width=block.get("width"),
            height=block.get("height"),
            align=block.get("align", "center"),
            caption=block.get("caption"),
        )

    else:
        raise ValueError(
            f"Unknown block type '{btype}'. "
            "Valid types: heading, paragraph, list, code, callout, hyperlink, "
            "hr, page_break, section_break, toc, table, chart, flowchart, image"
        )


def _parse_merge(merge_raw: Optional[Any]) -> Optional[List]:
    """Normalise merge spec — lists of 4-element lists/tuples."""
    if not merge_raw:
        return None
    result = []
    for item in merge_raw:
        if isinstance(item, (list, tuple)) and len(item) == 4:
            result.append(tuple(int(x) for x in item))
    return result or None


def _append_audit_trail(doc: EpicDoc, *, title: str, blocks: list[Any]) -> None:
    rows: list[list[Any]] = [["BlockIndex", "Type", "Source.doc", "Source.chunk", "Source.offset"]]
    for idx, block in enumerate(blocks):
        if not isinstance(block, dict):
            rows.append([idx, "", "", "", ""])
            continue
        btype = str(block.get("type", "") or "")
        meta = block.get("meta") if isinstance(block.get("meta"), dict) else {}
        source = meta.get("source") if isinstance(meta.get("source"), dict) else {}
        rows.append([
            idx,
            btype,
            source.get("doc", ""),
            source.get("chunk", ""),
            source.get("offset", ""),
        ])

    doc.add_page_break()
    doc.add_heading(title, level=1)
    doc.add_paragraph("下表用于审计/追溯：从生成块定位回源 Markdown/文档分片。", font_size=10)
    doc.add_table(
        data=rows,
        headers=True,
        style="grid",
        col_widths=[0.9, 1.1, 1.8, 1.2, 1.0],
        font_size=9,
    )
