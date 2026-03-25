from __future__ import annotations

# ruff: noqa: UP045
import json
import sys
from pathlib import Path
from typing import Any, Optional

import streamlit as st

# Make sure `epic_doc` can be imported when running from repo root:
#   streamlit run web/streamlit_app.py
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS_DIR = ROOT / "docs"
try:
    from epic_doc import list_themes
    from epic_doc.converters.pandoc import (
        docx_bytes_to_html_bytes,
        docx_bytes_to_pdf_bytes,
    )
    from epic_doc.schema import build_from_dict
except ModuleNotFoundError:
    sys.path.insert(0, str(SRC))
    from epic_doc import list_themes
    from epic_doc.converters.pandoc import (
        docx_bytes_to_html_bytes,
        docx_bytes_to_pdf_bytes,
    )
    from epic_doc.schema import build_from_dict


def _list_docs_md() -> list[Path]:
    if not DOCS_DIR.exists():
        return []
    return sorted([p for p in DOCS_DIR.glob("*.md") if p.is_file()], key=lambda p: p.name)


def _read_md(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_default_json() -> str:
    candidate = ROOT / "examples" / "web_demo_config_example.json"
    if candidate.exists():
        return candidate.read_text(encoding="utf-8")
    # Fallback to existing sample.
    fallback = ROOT / "examples" / "json_config_example.json"
    if fallback.exists():
        return fallback.read_text(encoding="utf-8")
    return json.dumps({"theme": "minimal", "blocks": []}, ensure_ascii=False, indent=2)


def _best_effort_title(defn: dict[str, Any]) -> Optional[str]:
    meta = defn.get("meta") or {}
    if isinstance(meta, dict):
        title = meta.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()
    return None


st.set_page_config(page_title="epic-doc 文档生成", layout="wide")
st.title("epic-doc 文档生成与预览")

tab_build, tab_docs = st.tabs(["生成/预览", "帮助文档"])

with tab_docs:
    st.subheader("帮助文档")
    docs = _list_docs_md()
    if not docs:
        st.info("未找到 docs/*.md 文档。")
    else:
        names = [p.name for p in docs]
        default_idx = names.index("index.md") if "index.md" in names else 0
        selected = st.selectbox("选择文档", names, index=default_idx)
        md_path = DOCS_DIR / selected
        try:
            st.markdown(_read_md(md_path))
        except Exception as exc:
            st.error(f"读取文档失败：{exc}")

with tab_build:
    themes = list_themes()
    theme_names = [t.name for t in themes]

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1) 选择主题")
        default_theme_idx = (
            theme_names.index("professional") if "professional" in theme_names else 0
        )
        selected_theme = st.selectbox("Theme", theme_names, index=default_theme_idx)

        st.subheader("2) 编辑 JSON 配置")
        default_json = _load_default_json()
        json_text = st.text_area(
            "DOC 定义（与 `epic-doc generate config.json` 等价）",
            value=default_json,
            height=520,
        )

        generate = st.button("生成 DOCX + HTML 预览 + PDF（需要 pandoc）", type="primary")

    with col_right:
        st.subheader("输出")
        st.caption("DOCX 始终生成；HTML/PDF 需要系统安装 pandoc。")

        out_docx = st.empty()
        out_html = st.empty()
        out_pdf = st.empty()


if "generate" in locals() and generate:
    try:
        definition = json.loads(json_text)
    except json.JSONDecodeError as exc:
        st.error(f"JSON 解析失败：{exc}")
        st.stop()

    if not isinstance(definition, dict):
        st.error("JSON 顶层必须是对象（dict）。")
        st.stop()

    # Force selected theme (keeps UI predictable).
    definition["theme"] = selected_theme
    title = _best_effort_title(definition)

    with st.spinner("正在生成 DOCX..."):
        doc = build_from_dict(definition)
        docx_bytes = doc.to_bytes()

    out_docx.download_button(
        label="下载 DOCX",
        data=docx_bytes,
        file_name="report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # HTML preview
    try:
        with st.spinner("正在使用 pandoc 转换为 HTML 预览..."):
            html_bytes = docx_bytes_to_html_bytes(docx_bytes, title=title)
            html_str = html_bytes.decode("utf-8", errors="ignore")
        out_html.subheader("HTML 预览（pandoc）")
        out_html.components.v1.html(html_str, height=900, scrolling=True)
    except ImportError as exc:
        st.warning(str(exc))
    except RuntimeError as exc:
        st.error(f"HTML 转换失败：{exc}")

    # PDF download
    try:
        with st.spinner("正在转换为 PDF..."):
            pdf_bytes = docx_bytes_to_pdf_bytes(docx_bytes)
        out_pdf.download_button(
            label="下载 PDF",
            data=pdf_bytes,
            file_name="report.pdf",
            mime="application/pdf",
        )
    except ImportError as exc:
        st.warning(str(exc))
    except RuntimeError as exc:
        st.error(f"PDF 转换失败：{exc}")

