"""Command-line interface for epic-doc."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import click

from epic_doc.styles import list_themes


@click.group()
@click.version_option(package_name="epic-doc")
def main() -> None:
    """epic-doc — generate complex, beautiful DOCX documents."""


@main.command("generate")
@click.argument("config", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", default=None, help="Output .docx file path.")
@click.option("--theme", default=None, help="Override the theme in the config.")
@click.option("--also-pdf", is_flag=True, help="Also generate output PDF via pandoc.")
@click.option("--also-html", is_flag=True, help="Also generate output HTML via pandoc.")
def generate(
    config: str,
    output: Optional[str],
    theme: Optional[str],
    also_pdf: bool,
    also_html: bool,
) -> None:
    """Generate a DOCX document from a JSON config file.

    \b
    Example:
        epic-doc generate report.json -o report.docx
    """
    from epic_doc.schema import build_from_dict

    cfg_path = Path(config)
    try:
        with cfg_path.open(encoding="utf-8") as f:
            definition = json.load(f)
    except json.JSONDecodeError as exc:
        click.echo(f"[error] Invalid JSON in {config}: {exc}", err=True)
        sys.exit(1)

    if theme:
        definition["theme"] = theme

    out_path = Path(output or cfg_path.with_suffix(".docx").name)

    try:
        doc = build_from_dict(definition)
        doc.save(str(out_path))
        click.echo(f"[ok] Saved → {out_path}")

        if also_pdf:
            pdf_bytes = doc.to_pdf_bytes()
            pdf_path = out_path.with_suffix(".pdf")
            pdf_path.write_bytes(pdf_bytes)
            click.echo(f"[ok] Saved → {pdf_path}")

        if also_html:
            html_bytes = doc.to_html_bytes()
            html_path = out_path.with_suffix(".html")
            html_path.write_bytes(html_bytes)
            click.echo(f"[ok] Saved → {html_path}")
    except Exception as exc:
        click.echo(f"[error] {exc}", err=True)
        sys.exit(1)


@main.command("validate")
@click.argument("config", type=click.Path(exists=True, dir_okay=False))
def validate(config: str) -> None:
    """Validate a JSON config file without generating the document.

    \b
    Example:
        epic-doc validate report.json
    """

    cfg_path = Path(config)
    try:
        with cfg_path.open(encoding="utf-8") as f:
            definition = json.load(f)
    except json.JSONDecodeError as exc:
        click.echo(f"[error] Invalid JSON: {exc}", err=True)
        sys.exit(1)

    errors: list[str] = []

    # Check theme
    theme_name = definition.get("theme", "professional")
    try:
        from epic_doc.styles import get_theme
        get_theme(theme_name)
    except ValueError as exc:
        errors.append(str(exc))

    # Check block types
    valid_types = {
        "heading", "paragraph", "list", "code", "code_block", "callout",
        "hyperlink", "hr", "page_break", "section_break", "toc",
        "table", "chart", "flowchart", "image",
    }
    for i, block in enumerate(definition.get("blocks", [])):
        btype = block.get("type", "")
        if btype not in valid_types:
            errors.append(f"Block #{i}: unknown type '{btype}'")
        if btype == "table" and "data" not in block:
            errors.append(f"Block #{i} (table): missing required field 'data'")
        if btype in ("chart",) and "data" not in block:
            errors.append(f"Block #{i} (chart): missing required field 'data'")
        if btype == "flowchart":
            if "nodes" not in block:
                errors.append(f"Block #{i} (flowchart): missing required field 'nodes'")
            if "edges" not in block:
                errors.append(f"Block #{i} (flowchart): missing required field 'edges'")
        if btype == "image" and "path" not in block:
            errors.append(f"Block #{i} (image): missing required field 'path'")

    if errors:
        click.echo("[fail] Validation errors:", err=True)
        for e in errors:
            click.echo(f"  • {e}", err=True)
        sys.exit(1)
    else:
        click.echo(f"[ok] {config} is valid ({len(definition.get('blocks', []))} blocks)")


@main.command("themes")
def themes() -> None:
    """List all available themes with descriptions."""
    all_themes = list_themes()
    click.echo(f"\n{'ID':<16} {'Display Name':<28} Description")
    click.echo("─" * 78)
    for t in all_themes:
        click.echo(f"  {t.name:<14} {t.display_name:<28} {t.description[:38]}")
    click.echo()


@main.command("preview")
@click.argument("theme_name", default="professional")
@click.option("-o", "--output", default=None, help="Output .docx path.")
@click.option("--all", "all_themes", is_flag=True,
              help="Generate previews for all themes.")
@click.option("--outdir", default=".", help="Output directory for --all previews.")
def preview(
    theme_name: str,
    output: Optional[str],
    all_themes: bool,
    outdir: str,
) -> None:
    """Generate a theme preview document.

    \b
    Examples:
        epic-doc preview professional -o preview.docx
        epic-doc preview --all --outdir ./previews
    """
    from epic_doc.styles import get_theme

    if all_themes:
        import os
        os.makedirs(outdir, exist_ok=True)
        for t in list_themes():
            out_path = str(Path(outdir) / f"preview_{t.name}.docx")
            _generate_preview(t.name, out_path)
            click.echo(f"[ok] {t.name} → {out_path}")
    else:
        try:
            get_theme(theme_name)
        except ValueError as exc:
            click.echo(f"[error] {exc}", err=True)
            sys.exit(1)
        out_path = output or f"preview_{theme_name}.docx"
        _generate_preview(theme_name, out_path)
        click.echo(f"[ok] Preview saved → {out_path}")


@main.command("schema")
def schema() -> None:
    """Print the JSON schema for config files to stdout."""
    schema_def = {
        "$schema": "https://epic-doc.dev/schema/v1.json",
        "type": "object",
        "properties": {
            "theme": {"type": "string", "description": "Theme ID (see: epic-doc themes)"},
            "template": {"type": ["string", "null"], "description": "Path to .docx template"},
            "meta": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "header": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "align": {"type": "string", "enum": ["left", "center", "right"]},
                        },
                    },
                ]
            },
            "footer": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "page_number": {"type": "boolean"},
                    "align": {"type": "string", "enum": ["left", "center", "right"]},
                },
            },
            "blocks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["type"],
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "heading", "paragraph", "list", "code", "callout",
                                "hyperlink", "hr", "page_break", "section_break",
                                "toc", "table", "chart", "flowchart", "image",
                            ],
                        },
                    },
                },
            },
        },
    }
    click.echo(json.dumps(schema_def, indent=2, ensure_ascii=False))


def _generate_preview(theme_name: str, out_path: str) -> None:
    """Generate a comprehensive preview document for a theme."""
    from epic_doc import EpicDoc

    doc = EpicDoc(theme=theme_name)
    t = doc._theme

    doc.set_metadata(title=f"Preview — {t.display_name}", author="epic-doc")
    doc.set_header(f"{t.display_name}  |  epic-doc 主题预览", align="right")
    doc.set_footer(text="epic-doc", page_number=True)

    doc.add_heading(f"{t.display_name}", level=1)
    doc.add_paragraph(t.description)
    doc.add_paragraph(
        f"字体：标题 {t.heading_font} / 正文 {t.body_font} / 等宽 {t.mono_font}  |  "
        f"主色 #{t.primary} / 副色 #{t.secondary} / 强调色 #{t.accent}"
    )

    doc.add_horizontal_rule()
    doc.add_heading("文字排版", level=2)
    doc.add_paragraph("这是一段标准正文内容，展示字体、行间距与段落间距效果。文字应清晰可读，适合长篇阅读。")
    doc.add_paragraph("加粗文字示例", bold=True)
    doc.add_paragraph("斜体文字示例", italic=True)
    doc.add_paragraph("带下划线的文字", underline=True)

    doc.add_heading("三级标题示例", level=3)
    doc.add_paragraph("三级标题下的段落内容，层次清晰。")

    doc.add_heading("四级标题示例", level=4)
    doc.add_paragraph("四级标题适合最细粒度的内容分层。")

    doc.add_heading("列表", level=2)
    doc.add_list(
        ["无序列表项目一", "无序列表项目二", ["嵌套子项目A", "嵌套子项目B"], "无序列表项目三"]
    )
    doc.add_list(["步骤一：准备工作", "步骤二：执行操作", "步骤三：验证结果"], style="numbered")

    doc.add_heading("代码块", level=2)
    doc.add_code_block(
        'from epic_doc import EpicDoc\n\ndoc = EpicDoc(theme="' + theme_name + '")\n'
        'doc.add_heading("Hello World", level=1)\ndoc.save("output.docx")',
        language="python",
    )

    doc.add_heading("提示框", level=2)
    doc.add_callout("这是一条信息提示，用于展示中性内容。", style="info", title="信息")
    doc.add_callout("注意：此操作需要管理员权限。", style="warning", title="警告")
    doc.add_callout("操作成功完成！", style="success", title="成功")
    doc.add_callout("发生错误，请检查日志。", style="danger", title="错误")

    doc.add_page_break()

    doc.add_heading("表格", level=2)
    doc.add_table(
        data=[
            ["部门", "Q1", "Q2", "Q3", "Q4", "合计"],
            ["销售部", 1200, 1450, 1380, 1600, 5630],
            ["研发部", 800,  820,  900,  950,  3470],
            ["市场部", 600,  700,  650,  720,  2670],
            ["运营部", 400,  420,  440,  460,  1720],
        ],
        headers=True,
        style="striped",
        col_widths=[2.2, 1.0, 1.0, 1.0, 1.0, 1.0],
        caption="表 1：各部门季度数据（万元）",
    )

    doc.add_heading("网格样式表格", level=3)
    doc.add_table(
        data=[
            ["特性", "支持情况", "备注"],
            ["多级标题", "✅ 完整", "Heading 1–4"],
            ["复杂表格", "✅ 完整", "合并/底纹/边框"],
            ["matplotlib 图表", "✅ 完整", "7 种图表类型"],
            ["graphviz 流程图", "✅ 完整", "需安装 graphviz"],
        ],
        headers=True,
        style="grid",
        caption="表 2：功能支持情况（grid 样式）",
    )

    doc.add_heading("图表", level=2)
    doc.add_chart(
        chart_type="bar",
        data={"Q1": 1200, "Q2": 1450, "Q3": 1380, "Q4": 1600},
        title="季度营收（万元）",
        ylabel="营收（万）",
        show_values=True,
        caption=f"图 1：柱状图示例（{t.display_name} 主题配色）",
    )

    doc.add_chart(
        chart_type="line",
        data={
            "销售额": {"Q1": 1200, "Q2": 1450, "Q3": 1380, "Q4": 1600},
            "利润":   {"Q1": 360,  "Q2": 435,  "Q3": 414,  "Q4": 480},
        },
        title="收入与利润趋势",
        legend=True,
        caption="图 2：多系列折线图示例",
    )

    doc.add_chart(
        chart_type="pie",
        data={"销售部": 5630, "研发部": 3470, "市场部": 2670, "运营部": 1720},
        title="部门支出占比",
        caption="图 3：饼图示例",
    )

    doc.save(out_path)
