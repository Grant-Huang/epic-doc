# epic-doc 设计文档

## 项目定位

**epic-doc** 是一个 Python 库，用于以编程方式生成复杂精美的 `.docx` 文档。设计目标：

- 供其他 Python 项目 `import` 调用，也可通过 CLI 使用
- 提供流式构建器 API，调用直觉化
- 支持 JSON/dict 配置驱动生成（适合模板化场景）
- 内置 11 套精心设计的主题，开箱即美
- 支持加载自定义 `.docx` 模板（企业品牌场景）
- 支持 DOCX -> HTML/PDF（通过 pandoc，可选能力）
- 提供 Streamlit Web 示例，方便快速体验与演示

---

## 架构概览

```
EpicDoc (builder.py)
    │
    ├── Theme System (styles/)
    │   ├── Theme dataclass      ← 颜色/字体/间距规范
    │   └── Presets (10 套)      ← 内置主题实例
    │
    ├── Elements (elements/)
    │   ├── text.py              ← 标题、段落、列表、超链接、代码块
    │   ├── table.py             ← 复杂表格（合并/底纹/边框/嵌套）
    │   ├── image.py             ← 图片插入（尺寸/对齐/标题）
    │   ├── chart.py             ← matplotlib 图表 → PNG → 嵌入
    │   ├── diagram.py           ← graphviz 流程图 → PNG → 嵌入
    │   └── layout.py            ← 页眉/页脚/目录/分页/分节
    │
    ├── Schema (schema.py)       ← JSON dict → builder 调用
    ├── CLI (cli.py)             ← click CLI，调用 schema.py
    ├── Converters (converters/) ← DOCX -> HTML/PDF（pandoc，可选）
    │
    └── Utils (utils/)
        ├── xml_helpers.py       ← python-docx 底层 XML 操作封装
        └── tempfiles.py         ← 临时图片文件管理（context manager）
```

---

## 核心 API

### 初始化

```python
from epic_doc import EpicDoc

doc = EpicDoc(theme='professional')        # 内置主题
doc = EpicDoc(theme='ocean')               # 其他内置主题
doc = EpicDoc(template='my_brand.docx')    # 自定义 .docx 模板
```

### 文本元素

```python
doc.add_heading('年度报告', level=1)
doc.add_heading('执行摘要', level=2)

doc.add_paragraph('正文内容...')
doc.add_paragraph('加粗段落', bold=True)
doc.add_paragraph('红色内容', color='#DC2626')
doc.add_paragraph('居中对齐', align='center')   # left|center|right|justify

doc.add_list(['项目一', '项目二', '项目三'], style='bullet')   # 无序
doc.add_list(['步骤一', '步骤二'], style='numbered')            # 有序
doc.add_list(                                                    # 嵌套列表
    ['步骤一', ['子步骤A', '子步骤B'], '步骤二'],
    style='numbered'
)

doc.add_hyperlink('点击查看文档', url='https://example.com')
doc.add_code_block('SELECT * FROM users WHERE id = 1;', language='sql')
doc.add_callout('重要提示：这是一个高亮提示框', style='info')   # info|warning|danger|success
```

### 表格

```python
doc.add_table(
    data=[
        ['部门',  'Q1',  'Q2',  'Q3',  '合计'],
        ['销售',  100,   200,   150,   450  ],
        ['研发',  80,    90,    110,   280  ],
        ['市场',  60,    70,    90,    220  ],
    ],
    headers=True,              # 首行为表头（深色背景）
    style='striped',           # striped|grid|minimal|bordered|dark
    col_widths=[3, 1.2, 1.2, 1.2, 1.5],  # 英寸，None 则等宽
    merge=[                    # 合并单元格 [(起始行, 起始列, 结束行, 结束列), ...]
        (0, 0, 0, 0),
    ],
    caption='表 1：季度收益对比',
    align='center',            # 表格整体水平对齐
    font_size=10,
)
```

### 图表（matplotlib）

```python
doc.add_chart(
    chart_type='bar',          # bar|hbar|line|pie|area|scatter|combo
    data={'Q1': 100, 'Q2': 200, 'Q3': 150, 'Q4': 220},
    title='季度营收（万元）',
    xlabel='季度',
    ylabel='金额（万）',
    width=5.5,                 # 英寸
    height=3.0,
    colors=None,               # None → 使用主题配色盘
    caption='图 1：季度营收趋势',
    show_values=True,          # 在柱子上显示数值
    show_grid=True,
)

# 多系列折线图
doc.add_chart(
    chart_type='line',
    data={
        '销售额': {'Q1': 100, 'Q2': 120, 'Q3': 150},
        '利润':   {'Q1': 30,  'Q2': 40,  'Q3': 55 },
    },
    title='收入与利润对比',
)
```

### 流程图（graphviz）

```python
doc.add_flowchart(
    nodes={
        'start':   {'label': '开始',     'shape': 'oval',    'color': None},
        'input':   {'label': '接收请求', 'shape': 'box'},
        'check':   {'label': '数据校验', 'shape': 'diamond'},
        'process': {'label': '业务处理', 'shape': 'box'},
        'error':   {'label': '返回错误', 'shape': 'box',     'color': 'red'},
        'end':     {'label': '返回结果', 'shape': 'oval'},
    },
    edges=[
        ('start',   'input'),
        ('input',   'check'),
        ('check',   'process', {'label': '通过'}),
        ('check',   'error',   {'label': '失败'}),
        ('process', 'end'),
        ('error',   'end'),
    ],
    direction='TB',            # TB|LR|RL|BT
    width=5.0,
    caption='图 2：请求处理流程',
)
```

### 图片插入

```python
doc.add_image('path/to/image.png', width=4.0, caption='图 3：架构图')
doc.add_image(bytes_data, width=3.5, align='center')
```

### 布局控制

```python
doc.set_metadata(title='年度报告', author='Grant', subject='Business Report')
doc.add_toc(title='目录', depth=3)
doc.set_header('机密文档 | 2026 年度', align='right')
doc.set_footer(text='© 2026 Grant Inc.', page_number=True, align='center')
doc.add_page_break()
doc.add_section_break()        # 分节（可设置不同页眉页脚）
doc.add_horizontal_rule()      # 水平分隔线
```

### 输出

```python
doc.save('output.docx')
data: bytes = doc.to_bytes()   # 适合 HTTP 响应 / 内存传递

# 可选：通过 pandoc 导出 HTML/PDF（需要系统安装 pandoc）
html_bytes: bytes = doc.to_html_bytes()
pdf_bytes: bytes = doc.to_pdf_bytes()
```

---

## 主题系统

### Theme 数据结构

每个主题是一个 `Theme` dataclass 实例，包含以下字段组：

| 字段组 | 内容 |
|--------|------|
| **Typography** | 标题/正文/等宽字体族，H1~H4/正文/标题的字号 |
| **Colors** | primary/secondary/accent/body_text/light_text |
| **Table** | 表头背景色、表头文字色、斑马纹色、边框色 |
| **Chart** | 6~8 色配色盘列表 |
| **Heading Style** | 粗体/斜体/下划线/全大写/段前段后间距/H1 底部边框 |
| **Code Block** | 背景色、文字色 |
| **Callout** | info/warning/danger/success 四种底色 |

### 内置主题一览

| ID | 名称 | 风格定位 | 主色 | 字体 |
|----|------|---------|------|------|
| `professional` | 商务深蓝 | 企业年报、商业提案 | `#1E3A5F` | Calibri |
| `minimal` | 极简墨白 | 技术文档、API 文档 | `#111827` | Arial |
| `ocean` | 海洋深邃 | 科研报告、数据分析 | `#0C4A6E` | Calibri |
| `forest` | 自然绿意 | 环保/可持续报告 | `#14532D` | Georgia |
| `sunset` | 暖橙日落 | 营销报告、创意方案 | `#7C2D12` | Calibri |
| `elegant` | 优雅紫金 | 高端提案、奢侈品牌 | `#3B0764` | Times New Roman |
| `tech` | 极客深空 | 技术架构文档、IT报告 | `#0F172A` | Calibri |
| `academic` | 学术棕米 | 学术论文、研究报告 | `#44403C` | Times New Roman |
| `cherry` | 樱花雅粉 | 品牌手册、活动策划 | `#881337` | Calibri |
| `nordic` | 北欧简约 | 产品白皮书、UX报告 | `#1C3748` | Arial |

---

## JSON Schema（CLI / from_dict 用）

```json
{
  "$schema": "https://epic-doc.dev/schema/v1.json",
  "theme": "professional",
  "template": null,
  "meta": {
    "title": "文档标题",
    "author": "作者",
    "subject": "主题"
  },
  "header": { "text": "页眉文字", "align": "right" },
  "footer": { "text": "页脚文字", "page_number": true, "align": "center" },
  "blocks": [
    { "type": "toc", "title": "目录", "depth": 3 },
    { "type": "heading", "text": "标题", "level": 1 },
    { "type": "paragraph", "text": "段落内容", "bold": false, "align": "justify" },
    { "type": "list", "items": ["项目1", "项目2"], "style": "bullet" },
    { "type": "code", "code": "print('hello')", "language": "python" },
    { "type": "callout", "text": "注意事项", "style": "warning" },
    {
      "type": "table",
      "data": [["列1", "列2"], ["值1", "值2"]],
      "headers": true,
      "style": "striped",
      "caption": "表格标题"
    },
    {
      "type": "chart",
      "chart_type": "bar",
      "data": { "A": 10, "B": 20 },
      "title": "图表标题",
      "caption": "图表说明"
    },
    {
      "type": "flowchart",
      "nodes": { "a": { "label": "开始" }, "b": { "label": "结束" } },
      "edges": [["a", "b"]],
      "direction": "TB",
      "caption": "流程图说明"
    },
    { "type": "image", "path": "image.png", "width": 4.0, "caption": "图片说明" },
    { "type": "page_break" },
    { "type": "hr" }
  ]
}
```

---

## CLI 设计

```bash
# 从 JSON 配置生成文档
epic-doc generate config.json -o output.docx

# 同时导出 HTML/PDF（需要 pandoc）
epic-doc generate config.json -o output.docx --also-html --also-pdf

# 验证 JSON 配置（不生成文档）
epic-doc validate config.json

# 列出所有可用主题及描述
epic-doc themes

# 输出 JSON Schema 定义（可导入编辑器做补全）
epic-doc schema

# 从主题生成预览文档（用于选主题）
epic-doc preview professional -o preview.docx
epic-doc preview --all -o /tmp/previews/
```

---

## 依赖说明

| 包 | 版本 | 用途 |
|----|------|------|
| `python-docx` | ≥1.1 | 核心 DOCX 构建 |
| `matplotlib` | ≥3.8 | 图表生成 |
| `graphviz` | ≥0.20 | 流程图生成（需系统安装 graphviz 可执行文件） |
| `click` | ≥8.0 | CLI 框架 |
| `lxml` | ≥5.0 | XML 操作（python-docx 依赖，直接使用） |
| `Pillow` | ≥10.0 | 图片处理 |
| `pandoc` | — | DOCX -> HTML/PDF（系统依赖，可选） |

> **注意**：`graphviz` Python 包需要系统安装 graphviz 可执行文件（`brew install graphviz` / `apt install graphviz`）。若未安装，调用 `add_flowchart()` 时会抛出明确的 `ImportError` 提示，不影响其他功能。

---

## 开发计划

### Phase 1 — 核心基础（当前）
- [x] 项目骨架：目录结构、pyproject.toml、.gitignore
- [x] DESIGN.md 设计文档
- [x] 主题系统：Theme dataclass + 11 套主题
- [x] 工具层：xml_helpers + tempfiles
- [x] 文本元素：标题/段落/列表/超链接/代码块/callout/hr
- [x] 核心 Builder 类

### Phase 2 — 表格与图表
- [x] 复杂表格：合并单元格、斑马纹、边框自定义、5 种样式预设
- [x] matplotlib 图表：bar/hbar/line/pie/area/scatter/combo
- [x] graphviz 流程图：多形状、多方向、彩色节点

### Phase 3 — 布局与模板
- [x] 页眉/页脚/分页/分节
- [x] 目录（TOC）
- [ ] 自定义 .docx 模板支持（保留为扩展项）
- [x] 图片插入（含标题）
- [x] callout 提示框

### Phase 3.5 — 导出与演示（可选能力）
- [x] DOCX -> HTML/PDF（pandoc）
- [x] Streamlit Web 示例（演示与预览）

### Phase 4 — Schema + CLI
- [x] JSON Schema 解析器
- [x] click CLI 实现
- [x] 主题预览命令

### Phase 5 — 示例与测试
- [x] 5 个完整示例文件
- [x] 单元测试覆盖核心逻辑
- [x] README 完善

---

## 关键设计决策

### 1. 图表以图片嵌入
matplotlib / graphviz 渲染为临时 PNG，通过 python-docx 的 `add_picture()` 嵌入。
临时文件通过 `TempFileManager` context manager 自动清理，`save()` 和 `to_bytes()` 完成后触发。

### 2. graphviz 可选
`graphviz` 系统二进制是可选依赖。若不存在，调用 `add_flowchart()` 时抛出带安装指引的 `EpicDocDependencyError`，其余功能不受影响。

### 2.1 pandoc 可选
`pandoc` 是可选系统依赖。若不存在，导出 HTML/PDF 会抛出带安装指引的 `ImportError`，DOCX 主流程不受影响。

### 3. 主题与模板的关系
- 使用内置主题时：从空白 Document 创建，通过修改 docx styles 应用主题
- 使用自定义模板时：从 `.docx` 模板加载（保留其 styles），内置主题仅覆盖配色变量，字体/间距从模板继承

### 4. 返回 self 实现链式调用
所有 `add_*` 方法均返回 `self`，支持：
```python
doc.add_heading('报告').add_paragraph('内容').add_table(data).save('out.docx')
```

### 5. to_bytes() 用于集成场景
```python
# FastAPI
return StreamingResponse(io.BytesIO(doc.to_bytes()), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# Django
response = HttpResponse(doc.to_bytes(), content_type='application/...')
response['Content-Disposition'] = 'attachment; filename="report.docx"'
```
