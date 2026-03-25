---
title: epic-doc CLI 使用说明
---

## 1. 安装与准备

安装库：

```bash
pip install epic-doc
```

从源码开发（项目根目录）：

```bash
pip install -e ".[dev]"
```

可选系统依赖：

- **graphviz**（仅流程图需要）
- **pandoc**（仅导出 HTML/PDF 需要）

## 2. CLI 总览

入口命令：`epic-doc`

### 2.1 generate：从 JSON 生成文档

基础用法（只生成 DOCX）：

```bash
epic-doc generate examples/json_config_example.json -o output.docx
```

同时导出 HTML/PDF（需要安装 pandoc）：

```bash
epic-doc generate examples/json_config_example.json -o output.docx --also-html --also-pdf
```

覆盖主题（以 CLI 参数为准）：

```bash
epic-doc generate config.json --theme professional -o report.docx
```

输出规则：

- `-o/--output` 指定 DOCX 输出路径
- `--also-html` 会在同目录生成同名 `.html`
- `--also-pdf` 会在同目录生成同名 `.pdf`

### 2.2 validate：校验 JSON 配置

```bash
epic-doc validate examples/json_config_example.json
```

校验内容（当前实现）：

- theme 是否存在
- blocks 中 type 是否是已知类型
- 关键字段是否存在（例如 table 的 data、image 的 path）

### 2.3 themes：列出主题

```bash
epic-doc themes
```

### 2.4 preview：生成主题预览

单个主题：

```bash
epic-doc preview professional -o preview_professional.docx
```

全部主题：

```bash
epic-doc preview --all --outdir ./previews
```

### 2.5 schema：输出 JSON Schema（基础版）

```bash
epic-doc schema
```

## 3. 常见问题

### 3.1 生成 HTML/PDF 报错

- 确认 `pandoc` 已安装并在 PATH 中
- PDF 导出常常需要 LaTeX 引擎（例如 xelatex/pdflatex/tectonic）

### 3.2 生成流程图报错

需要系统安装 graphviz（`dot` 可执行文件在 PATH 中）。

