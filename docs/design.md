---
title: epic-doc 设计文档（完整）
---

## 1. 项目定位

**epic-doc** 是一个 Python 工具库，目标是**以编程方式生成复杂精美的 DOCX**，并能在“工具项目”形态下被其他项目调用：

- **库（Library）**：`import epic_doc` 直接构建/输出
- **CLI**：从 JSON 配置批量生成文档
- **Web 示例（Streamlit）**：可视化编辑 JSON、生成 DOCX，并在浏览器中预览（HTML）与导出（PDF）

## 2. 范围与非目标

### 2.1 范围（支持）

- **DOCX 生成（核心）**
  - 标题/段落/列表/超链接
  - 代码块（以 1×1 表格实现背景底纹）
  - Callout 提示框（以 1×1 表格实现底色与边框）
  - 分页/分节/页眉/页脚/目录（TOC field）
  - 复杂表格（合并、底纹、边框、5 种预设样式）
  - 图表（matplotlib 渲染成 PNG 再嵌入）
  - 流程图（graphviz 渲染成 PNG 再嵌入）
  - 图片插入（支持 bytes 或路径）

- **导出能力（可选）**
  - DOCX -> HTML（pandoc）
  - DOCX -> PDF（pandoc；通常需要 LaTeX 引擎）

### 2.2 非目标（当前不做/不保证）

- 在 DOCX 内生成**可编辑**的 Word 原生矢量绘图对象（SmartArt、DrawingML shapes、内嵌 Excel 图表 OLE 等）
- 读取/解析任意 DOCX 并保留其全部排版语义（本项目当前主要定位为“生成器”）

## 3. 架构总览

代码结构（与仓库实际一致）：

```
src/epic_doc/
├── __init__.py
├── builder.py                 # EpicDoc fluent builder
├── schema.py                  # JSON/dict -> builder 调用
├── cli.py                     # click CLI
├── converters/
│   └── pandoc.py              # DOCX -> HTML/PDF (optional)
├── elements/
│   ├── text.py                # headings/paragraph/list/hyperlink/code/callout/hr
│   ├── table.py               # complex tables
│   ├── chart.py               # matplotlib charts -> PNG
│   ├── diagram.py             # graphviz flowcharts -> PNG
│   ├── image.py               # image insertion
│   └── layout.py              # header/footer/toc/page_break/section_break
├── styles/
│   ├── theme.py               # Theme dataclass + registry
│   └── presets/               # 11 themes
└── utils/
    ├── xml_helpers.py         # OOXML helpers for python-docx
    └── tempfiles.py           # temp file tracking & cleanup
```

## 4. 核心设计决策

### 4.1 图表/流程图以图片嵌入

原因：

- `python-docx` 对 Word 原生图表/SmartArt 等封装有限
- 生成可编辑矢量对象需要大量手写 OOXML，复杂且脆弱

实现策略：

- 图表：`matplotlib` 输出 PNG
- 流程图：`graphviz` 输出 PNG
- 临时文件：统一由 `TempFileManager` 跟踪并在 `save()/to_bytes()` 结束后清理

### 4.2 目录（TOC）使用 Field Code（占位）

DOCX 的目录通常由 Word/LibreOffice 在打开文档后刷新生成（例如 Ctrl+A 然后 F9）。

- `add_toc(title, depth)` 插入 TOC field code
- `depth` 通过 field instruction 中的 `\\o "1-{depth}"` 控制目录级别

### 4.3 Fluent API 与 Schema/CLI 的关系

- 业务能力统一由 `EpicDoc` 提供（单一入口）
- `schema.py` 只做“JSON 结构 -> EpicDoc 调用”的映射
- `cli.py` 只做“读取 JSON -> 调用 schema -> 写文件”的胶水逻辑

这样可以避免逻辑重复，并确保：

- API/CLI/Web 示例使用同一套实现
- 新增能力只需扩展 builder/element，再给 schema/cli 增加映射即可

## 5. 数据模型（Schema）

顶层：

- `theme`: 主题 ID
- `template`: 可选 DOCX 模板路径
- `meta`: 文档属性
- `header/footer`: 页眉页脚
- `blocks`: 内容块数组（顺序渲染）

block 典型类型：

- `heading`, `paragraph`, `list`, `hyperlink`, `code`, `callout`, `hr`
- `table`, `chart`, `flowchart`, `image`
- `toc`, `page_break`, `section_break`

`schema.py` 对应的映射实现：`build_from_dict()` + `_process_block()`

## 6. 依赖与可选依赖

### 6.1 Python 依赖

- `python-docx`: DOCX 生成基础
- `lxml`: XML 操作（也用于 python-docx）
- `Pillow`: 图片处理/兼容（测试与图片插入）
- `matplotlib`: 图表渲染
- `graphviz`: 流程图渲染（Python 包）
- `click`: CLI

### 6.2 系统依赖（可选）

- `graphviz` 二进制（`dot`）：只有在调用 `add_flowchart()` 时需要
- `pandoc`：只有在导出 HTML/PDF 或 Web 示例预览/导出时需要
- LaTeX 引擎（pdf 导出常见需要，如 `xelatex`/`pdflatex`/`tectonic`）：pandoc -> PDF 时可能需要

## 7. 错误处理与兼容策略

- 对可选能力（graphviz/pandoc）：缺失时抛出带安装提示的 `ImportError` 或 `RuntimeError`，不影响 DOCX 主流程
- 测试：对可选依赖采用 `pytest.skip`（避免 CI/开发环境没有系统依赖时全红）

## 8. 扩展点（后续路线）

- **更强的模板机制**：从企业模板继承样式 + 主题变量覆盖
- **更多图表类型**：雷达图、箱线图、热力图等（仍以图片嵌入）
- **更丰富的表格能力**：单元格内嵌表格、复杂表头布局、自动分页拆分
- **导出增强**：HTML 导出时引入统一 CSS，提升浏览器预览体验

