"""Low-level python-docx XML helpers."""

# ruff: noqa: UP045

from __future__ import annotations

from typing import Optional

from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_run_fonts(
    run,
    *,
    ascii_font: str,
    cjk_font: str,
    hansi_font: Optional[str] = None,
) -> None:
    """Set a run's font for both Latin and CJK scripts via OOXML.

    Word uses w:rFonts to pick fonts by script. Setting only run.font.name is
    often insufficient for CJK (eastAsia).
    """
    hansi_font = hansi_font or ascii_font
    try:
        run.font.name = ascii_font
    except Exception:
        pass

    r = run._r
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)

    rFonts.set(qn("w:ascii"), ascii_font)
    rFonts.set(qn("w:hAnsi"), hansi_font)
    rFonts.set(qn("w:cs"), ascii_font)
    rFonts.set(qn("w:eastAsia"), cjk_font)


def set_cell_bg(cell, hex_color: str) -> None:
    """Set a table cell's background/shading color (hex without #)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.upper().lstrip("#"))
    existing = tcPr.find(qn("w:shd"))
    if existing is not None:
        tcPr.remove(existing)
    tcPr.append(shd)


def set_cell_borders(
    cell,
    top: Optional[str] = None,
    bottom: Optional[str] = None,
    left: Optional[str] = None,
    right: Optional[str] = None,
    color: str = "000000",
    size: str = "4",
    val: str = "single",
) -> None:
    """Set individual cell borders. Pass hex color without #."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders_el = tcPr.find(qn("w:tcBorders"))
    if borders_el is None:
        borders_el = OxmlElement("w:tcBorders")
        tcPr.append(borders_el)

    sides = {"top": top, "bottom": bottom, "left": left, "right": right}
    for side, enable in sides.items():
        if enable is not None:
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:val"), val if enable else "nil")
            el.set(qn("w:sz"), size)
            el.set(qn("w:color"), color.upper().lstrip("#"))
            existing = borders_el.find(qn(f"w:{side}"))
            if existing is not None:
                borders_el.remove(existing)
            borders_el.append(el)


def set_table_borders(table, color: str = "000000", size: str = "4") -> None:
    """Apply uniform borders to all cells in a table."""
    hex_color = color.upper().lstrip("#")
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)

    tblBorders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), size)
        el.set(qn("w:color"), hex_color)
        tblBorders.append(el)

    existing = tblPr.find(qn("w:tblBorders"))
    if existing is not None:
        tblPr.remove(existing)
    tblPr.append(tblBorders)


def set_table_no_borders(table) -> None:
    """Remove all visible borders from a table."""
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)

    tblBorders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:color"), "FFFFFF")
        tblBorders.append(el)

    existing = tblPr.find(qn("w:tblBorders"))
    if existing is not None:
        tblPr.remove(existing)
    tblPr.append(tblBorders)


def _twips_from_inches(inches: float) -> int:
    # 1 inch = 1440 twips
    return int(round(float(inches) * 1440))


def set_table_column_widths(table, widths_in: list[float]) -> None:
    """Set table column widths robustly (tblGrid + tcW).

    python-docx's high-level width assignment is often overridden by Word's autofit.
    This helper writes OOXML widths so col_widths is much more likely to stick.
    """
    tbl = table._tbl

    # --- tblGrid ---
    grid = tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        # Insert after tblPr if present, otherwise prepend
        tblPr = tbl.find(qn("w:tblPr"))
        if tblPr is not None:
            tbl.insert(1, grid)
        else:
            tbl.insert(0, grid)

    # Clear existing gridCols
    for child in list(grid):
        grid.remove(child)

    for w_in in widths_in:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(_twips_from_inches(w_in)))
        grid.append(gc)

    # --- tcW for each cell ---
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            if idx >= len(widths_in):
                break
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:type"), "dxa")
            tcW.set(qn("w:w"), str(_twips_from_inches(widths_in[idx])))


def add_paragraph_border_bottom(paragraph, color: str, size: str = "4") -> None:
    """Add a bottom border to a paragraph (used for H1 decorative line)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color.upper().lstrip("#"))
    pBdr.append(bottom)

    existing = pPr.find(qn("w:pBdr"))
    if existing is not None:
        pPr.remove(existing)
    pPr.append(pBdr)


def set_cell_vertical_alignment(cell, alignment: str = "center") -> None:
    """Set vertical text alignment in a cell: top | center | bottom."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = OxmlElement("w:vAlign")
    vAlign.set(qn("w:val"), alignment)
    existing = tcPr.find(qn("w:vAlign"))
    if existing is not None:
        tcPr.remove(existing)
    tcPr.append(vAlign)


def make_hyperlink(paragraph, text: str, url: str, color: str = "2563EB") -> None:
    """Insert a hyperlink run into an existing paragraph."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    rStyle = OxmlElement("w:rStyle")
    rStyle.set(qn("w:val"), "Hyperlink")
    rPr.append(rStyle)

    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), color.upper().lstrip("#"))
    rPr.append(color_el)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(underline)

    new_run.append(rPr)
    text_el = OxmlElement("w:t")
    text_el.text = text
    text_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    new_run.append(text_el)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_toc_field(document, depth: int = 3) -> None:
    """Insert a TOC field instruction into the document.

    Note: TOC depth is controlled via the TOC field instruction:
    ``TOC \\o "1-{depth}"``.
    """
    depth = int(depth)
    # Word 的目录级别通常是 1-9，这里做一个保守夹取。
    depth = max(1, min(depth, 9))
    paragraph = document.add_paragraph()
    p = paragraph._p

    # Apply TOC Heading style
    pPr = p.get_or_add_pPr()
    pStyle = OxmlElement("w:pStyle")
    pStyle.set(qn("w:val"), "TOCHeading")
    pPr.insert(0, pStyle)

    fldChar_begin = OxmlElement("w:fldChar")
    fldChar_begin.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.text = f' TOC \\o "1-{depth}" \\h \\z \\u '
    instrText.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    fldChar_sep = OxmlElement("w:fldChar")
    fldChar_sep.set(qn("w:fldCharType"), "separate")

    fldChar_end = OxmlElement("w:fldChar")
    fldChar_end.set(qn("w:fldCharType"), "end")

    run = OxmlElement("w:r")
    run.append(fldChar_begin)
    p.append(run)

    run2 = OxmlElement("w:r")
    run2.append(instrText)
    p.append(run2)

    run3 = OxmlElement("w:r")
    run3.append(fldChar_sep)
    p.append(run3)

    placeholder_run = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "（请在 Word 中按 Ctrl+A, F9 更新目录）"
    placeholder_run.append(t)
    p.append(placeholder_run)

    run4 = OxmlElement("w:r")
    run4.append(fldChar_end)
    p.append(run4)

    return paragraph
