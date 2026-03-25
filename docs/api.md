---
title: epic-doc API 使用说明
---

## 1. 安装

```bash
pip install epic-doc
```

开发模式：

```bash
pip install -e ".[dev]"
```

## 2. 核心对象：EpicDoc

```python
from epic_doc import EpicDoc

doc = EpicDoc(theme="professional")
```

### 2.1 元数据与布局

```python
doc.set_metadata(title="报告", author="Alice")
doc.set_header("机密 | 2026", align="right")
doc.set_footer(text="epic-doc", page_number=True, align="center")

doc.add_toc(title="目录", depth=3)
doc.add_page_break()
doc.add_section_break(break_type="next_page")
```

说明：

- `add_toc(depth=...)` 会插入 TOC field code（需要 Word/LibreOffice 刷新目录）
- `depth` 会映射到 `\\o "1-{depth}"`，控制目录级别范围

### 2.2 文本能力

```python
doc.add_heading("执行摘要", level=1)
doc.add_paragraph("正文...", align="justify")
doc.add_list(["A", "B", ["B-1", "B-2"], "C"], style="bullet")
doc.add_hyperlink("链接", url="https://example.com")
doc.add_code_block("print('hello')", language="python")
doc.add_callout("重要提示", style="warning", title="注意")
doc.add_horizontal_rule()
```

### 2.3 表格

```python
doc.add_table(
    data=[
        ["Name", "Q1", "Q2"],
        ["A", 1, 2],
        ["B", 3, 4],
    ],
    headers=True,
    style="striped",  # striped|grid|minimal|bordered|dark
    col_widths=[2.5, 1.0, 1.0],
    merge=[(0, 0, 0, 1)],
    caption="表 1：示例",
    align="center",
    cell_align="center",
    font_size=10,
)
```

### 2.4 图表（matplotlib -> PNG -> DOCX）

```python
doc.add_chart(
    chart_type="bar",
    data={"Q1": 100, "Q2": 200, "Q3": 150},
    title="季度营收",
    ylabel="金额",
    show_values=True,
    caption="图 1：柱状图",
)
```

### 2.5 流程图（graphviz -> PNG -> DOCX）

```python
doc.add_flowchart(
    nodes={"a": "开始", "b": {"label": "处理", "shape": "box"}, "c": "结束"},
    edges=[("a", "b"), ("b", "c")],
    direction="TB",
    caption="图 2：流程图",
)
```

依赖说明：

- 需要 `pip install graphviz`
- 还需要系统安装 graphviz 二进制（`dot` 在 PATH）

### 2.6 图片插入

```python
doc.add_image("path/to/image.png", width=4.0, caption="图：示例")

png_bytes = b"..."
doc.add_image(png_bytes, width=3.0, align="center")
```

## 3. 输出（DOCX/HTML/PDF）

### 3.1 DOCX

```python
doc.save("out.docx")
data = doc.to_bytes()
```

### 3.2 HTML/PDF（pandoc，可选）

```python
html_bytes = doc.to_html_bytes()
pdf_bytes = doc.to_pdf_bytes()
```

注意：

- 需要系统安装 `pandoc`
- `pandoc -> PDF` 常常需要 LaTeX 引擎（缺失会抛出运行时错误）

## 4. Schema：从 dict/JSON 生成

```python
from epic_doc.schema import build_from_dict

definition = {
  "theme": "minimal",
  "meta": {"title": "API 接口文档"},
  "blocks": [
    {"type": "heading", "text": "标题", "level": 1},
    {"type": "paragraph", "text": "段落"},
  ],
}

doc = build_from_dict(definition)
doc.save("from_dict.docx")
```

## 5. Web 集成（示例）

FastAPI（返回 DOCX bytes）：

```python
import io
from fastapi.responses import StreamingResponse
from epic_doc import EpicDoc

def report():
    doc = EpicDoc(theme="professional").add_heading("动态报告", level=1)
    return StreamingResponse(
        io.BytesIO(doc.to_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=report.docx"},
    )
```

