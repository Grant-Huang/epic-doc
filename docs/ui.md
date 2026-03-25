---
title: epic-doc 界面使用说明（Streamlit）
---

## 1. 目的

Streamlit 示例用于：

- **快速展示 epic-doc 的完整能力**（主题、表格、图表、导出）
- 让使用者在浏览器中**编辑 JSON**，一键生成 DOCX，并可选导出 HTML/PDF

入口文件：`web/streamlit_app.py`

## 2. 运行前准备

### 2.1 安装 Python 依赖

在项目根目录：

```bash
pip install -e ".[dev]"
pip install streamlit
```

### 2.2 安装 pandoc（用于 HTML/PDF）

如果你只需要下载 DOCX，可以不装 pandoc；但 HTML 预览与 PDF 导出需要它。

- macOS：`brew install pandoc`
- Ubuntu/Debian：`sudo apt install pandoc`
- Windows：从 pandoc 官网安装并确保 `pandoc` 在 PATH 中

> 提示：pandoc 转 PDF 常常还需要 LaTeX 引擎（例如 xelatex/pdflatex/tectonic）。如果没装，页面会提示 PDF 转换失败。

## 3. 启动界面

在项目根目录运行：

```bash
streamlit run web/streamlit_app.py
```

## 4. 界面功能说明

### 4.1 选择主题

页面左侧会列出所有内置主题 ID（来自 `epic_doc.styles.list_themes()`）。

选择后会覆盖 JSON 里的 `theme` 字段（以保证页面行为可预测）。

### 4.2 编辑 JSON 配置

页面默认会加载：

- 优先：`examples/web_demo_config_example.json`
- 其次：`examples/json_config_example.json`

你可以直接编辑 JSON，常见块类型：

- 文本：`heading`/`paragraph`/`list`/`code`/`callout`/`hr`
- 结构：`toc`/`page_break`/`section_break`
- 复杂元素：`table`/`chart`/`flowchart`/`image`

### 4.3 生成与下载

点击按钮后会执行：

- 生成 DOCX（一定可用）
  - 提供“下载 DOCX”
- 若系统安装了 pandoc：
  - DOCX -> HTML：在右侧展示预览
  - DOCX -> PDF：提供“下载 PDF”

## 5. 常见问题（FAQ）

### 5.1 HTML/PDF 按钮可见但转换失败

可能原因：

- `pandoc` 未安装或不在 PATH
- PDF 导出需要 LaTeX 引擎（常见报错含 `xelatex/pdflatex`）

### 5.2 流程图不显示/报错

流程图需要系统安装 graphviz（二进制 `dot`）：

- macOS：`brew install graphviz`
- Ubuntu/Debian：`sudo apt install graphviz`
- Windows：安装 graphviz 并确保 `dot` 在 PATH

