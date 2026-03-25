# epic-doc

> 以编程方式生成复杂精美的 `.docx` 文档。

**epic-doc** 是一个 Python 库，提供流式构建器 API，支持 11 套内置精美主题，可生成包含复杂表格、多种图表和流程图的专业 Word 文档。

## 特性

- **11 套精美主题** — 商务深蓝、极简墨白、海洋深邃、自然绿意、暖橙日落、优雅紫金、极客深空、学术棕米、樱花雅粉、北欧简约、宝石红金
- **流式构建器 API** — 链式调用，开发体验直觉化
- **复杂表格** — 合并单元格、斑马纹、边框自定义、5 种样式预设
- **7 种图表** — 柱状图、水平柱状图、折线图、面积图、饼图、散点图、Combo 图（matplotlib 渲染）
- **流程图** — 多形状、多方向、彩色节点（graphviz 渲染）
- **callout 提示框** — info / warning / danger / success 四种
- **完整布局控制** — 页眉、页脚、目录、分页、分节
- **JSON/CLI 驱动** — 支持配置文件生成，适合批量场景
- **to_bytes()** — 适配 FastAPI / Flask / Django HTTP 响应

## 安装

```bash
pip install epic-doc
```

生成流程图还需要系统安装 graphviz：

```bash
# macOS
brew install graphviz
# Ubuntu/Debian
sudo apt install graphviz
```

## 快速开始

```python
from epic_doc import EpicDoc

doc = EpicDoc(theme="professional")

doc.set_metadata(title="2026 年度报告", author="Grant")
doc.set_header("年度报告  |  机密", align="right")
doc.set_footer(text="© 2026 Grant Inc.", page_number=True)

doc.add_heading("执行摘要", level=1)
doc.add_paragraph("2026 年度营收同比增长 24%，达到 1.38 亿元。")

doc.add_table(
    data=[
        ["部门", "Q1", "Q2", "Q3", "Q4"],
        ["销售", 300, 350, 380, 420],
        ["研发", 200, 220, 240, 260],
    ],
    headers=True,
    style="striped",
    caption="表 1：季度数据",
)

doc.add_chart(
    chart_type="bar",
    data={"Q1": 300, "Q2": 350, "Q3": 380, "Q4": 420},
    title="季度营收",
    show_values=True,
    caption="图 1：柱状图示例",
)

doc.add_flowchart(
    nodes={
        "start":   "开始",
        "process": {"label": "处理数据", "shape": "box"},
        "check":   {"label": "校验结果", "shape": "diamond"},
        "end":     "完成",
    },
    edges=[
        ("start", "process"),
        ("process", "check"),
        ("check", "end", {"label": "通过"}),
        ("check", "process", {"label": "重试", "style": "dashed"}),
    ],
    direction="TB",
    caption="图 2：处理流程",
)

doc.save("report.docx")
```

## 内置主题

| 主题 ID | 名称 | 适用场景 |
|---------|------|---------|
| `professional` | 商务深蓝 | 企业年报、商业提案 |
| `minimal` | 极简墨白 | 技术文档、API 文档 |
| `ocean` | 海洋深邃 | 科研报告、数据分析 |
| `forest` | 自然绿意 | 环保/可持续报告 |
| `sunset` | 暖橙日落 | 营销报告、创意方案 |
| `elegant` | 优雅紫金 | 高端提案、奢侈品牌 |
| `tech` | 极客深空 | IT 架构、技术报告 |
| `academic` | 学术棕米 | 学术论文、研究报告 |
| `cherry` | 樱花雅粉 | 品牌手册、活动策划 |
| `nordic` | 北欧简约 | 产品白皮书、UX 报告 |
| `ruby` | 宝石红金 | 法律合规、金融年报 |

## CLI

```bash
# 从 JSON 生成文档
epic-doc generate config.json -o output.docx

# 验证配置
epic-doc validate config.json

# 列出主题
epic-doc themes

# 生成主题预览
epic-doc preview professional -o preview.docx
epic-doc preview --all --outdir ./previews/

# 输出 JSON Schema
epic-doc schema
```

## API 参考

| 方法 | 说明 |
|------|------|
| `add_heading(text, level, align)` | 标题 H1–H4 |
| `add_paragraph(text, bold, italic, underline, color, align, font_size)` | 段落 |
| `add_list(items, style)` | 列表，支持嵌套 |
| `add_hyperlink(text, url)` | 超链接 |
| `add_code_block(code, language)` | 代码块 |
| `add_callout(text, style, title)` | 提示框 info/warning/danger/success |
| `add_horizontal_rule()` | 水平分隔线 |
| `add_table(data, headers, style, col_widths, merge, caption, ...)` | 表格 |
| `add_chart(chart_type, data, title, ...)` | matplotlib 图表 |
| `add_flowchart(nodes, edges, direction, ...)` | graphviz 流程图 |
| `add_image(source, width, height, align, caption)` | 图片 |
| `add_toc(title, depth)` | 目录 |
| `set_header(text, align)` | 页眉 |
| `set_footer(text, page_number, align)` | 页脚 |
| `add_page_break()` | 分页 |
| `set_metadata(title, author, subject, description)` | 文档属性 |
| `save(path)` | 保存文件 |
| `to_bytes()` | 返回 bytes |

## 集成示例

### FastAPI

```python
from fastapi.responses import StreamingResponse
import io
from epic_doc import EpicDoc

@app.get("/report")
def report():
    doc = EpicDoc(theme="professional")
    doc.add_heading("动态报告", level=1)
    return StreamingResponse(
        io.BytesIO(doc.to_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=report.docx"},
    )
```

## 开发

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
