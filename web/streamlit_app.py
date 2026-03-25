from __future__ import annotations

# ruff: noqa: UP045
import json
import sys
from pathlib import Path
from typing import Any, Optional

import streamlit as st
import streamlit.components.v1 as components

# Make sure `epic_doc` can be imported when running from repo root:
#   streamlit run web/streamlit_app.py
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS_DIR = ROOT / "docs"
USER_THEMES_DIR = ROOT / "themes"
try:
    from epic_doc import list_themes
    from epic_doc.converters.pandoc import (
        docx_bytes_to_html_bytes,
        docx_bytes_to_pdf_bytes,
    )
    from epic_doc.schema import build_from_dict
    from epic_doc.styles.theme import Theme, register_theme
except ModuleNotFoundError:
    sys.path.insert(0, str(SRC))
    from epic_doc import list_themes
    from epic_doc.converters.pandoc import (
        docx_bytes_to_html_bytes,
        docx_bytes_to_pdf_bytes,
    )
    from epic_doc.schema import build_from_dict
    from epic_doc.styles.theme import Theme, register_theme


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


def _list_example_json() -> list[Path]:
    examples_dir = ROOT / "examples"
    if not examples_dir.exists():
        return []
    return sorted([p for p in examples_dir.glob("*.json") if p.is_file()], key=lambda p: p.name)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _theme_to_dict(theme: Theme) -> dict[str, Any]:
    return theme.__dict__.copy()


def _filter_theme_fields(data: dict[str, Any]) -> dict[str, Any]:
    allowed = set(Theme.__dataclass_fields__.keys())
    return {k: v for k, v in data.items() if k in allowed}


def _list_user_theme_json() -> list[Path]:
    if not USER_THEMES_DIR.exists():
        return []
    return sorted([p for p in USER_THEMES_DIR.glob("*.json") if p.is_file()], key=lambda p: p.name)


def _load_user_themes() -> None:
    # Best-effort: register all themes under themes/*.json
    for p in _list_user_theme_json():
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                continue
            payload = _filter_theme_fields(raw)
            if not isinstance(payload.get("name"), str) or not payload["name"].strip():
                continue
            register_theme(Theme(**payload))
        except Exception:
            # Ignore broken user themes; keep app usable.
            continue


def _best_effort_title(defn: dict[str, Any]) -> Optional[str]:
    meta = defn.get("meta") or {}
    if isinstance(meta, dict):
        title = meta.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()
    return None


st.set_page_config(page_title="epic-doc 文档生成", layout="wide")
st.title("epic-doc 文档生成与预览")

_load_user_themes()

st.markdown(
    """
<style>
  /* Hide Streamlit toolbar + menu (best-effort; may change with Streamlit versions) */
  [data-testid="stToolbar"] { display: none !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


def _get_query_params() -> dict[str, str]:
    try:
        # New API (Streamlit >= 1.30)
        qp = dict(st.query_params)
        return {k: str(v) for k, v in qp.items()}
    except Exception:
        try:
            qp = st.experimental_get_query_params()
            return {k: (v[0] if isinstance(v, list) and v else str(v)) for k, v in qp.items()}
        except Exception:
            return {}


def _set_query_params(**params: str) -> None:
    try:
        st.query_params.clear()
        for k, v in params.items():
            st.query_params[k] = v
    except Exception:
        st.experimental_set_query_params(**params)


qp = _get_query_params()
default_view = qp.get("view", "build")
view = st.sidebar.radio(
    "导航",
    ["build", "docs"],
    index=0 if default_view != "docs" else 1,
    format_func=lambda x: "生成/预览" if x == "build" else "帮助文档",
)
if view != default_view:
    # Keep doc selection if switching views.
    doc = qp.get("doc", "index.md")
    _set_query_params(view=view, doc=doc)

if view == "docs":
    st.subheader("帮助文档")
    docs = _list_docs_md()
    if not docs:
        st.info("未找到 docs/*.md 文档。")
    else:
        names = [p.name for p in docs]
        default_doc = qp.get("doc", "index.md")
        default_idx = names.index(default_doc) if default_doc in names else (
            names.index("index.md") if "index.md" in names else 0
        )
        selected = st.selectbox("选择文档", names, index=default_idx)
        if selected != default_doc:
            _set_query_params(view="docs", doc=selected)
        md_path = DOCS_DIR / selected
        try:
            st.markdown(_read_md(md_path))
        except Exception as exc:
            st.error(f"读取文档失败：{exc}")

if view == "build":
    themes = list_themes()
    theme_names = [t.name for t in themes]

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1) 选择主题")
        default_theme_idx = (
            theme_names.index("professional") if "professional" in theme_names else 0
        )
        selected_theme = st.selectbox("Theme", theme_names, index=default_theme_idx)

        st.subheader("主题设定（保存为新主题）")
        with st.expander("打开主题编辑器", expanded=False):
            base_theme_name = st.selectbox(
                "基准主题",
                theme_names,
                index=theme_names.index(selected_theme) if selected_theme in theme_names else 0,
                key="theme_editor_base",
            )
            base_theme = next((t for t in themes if t.name == base_theme_name), themes[0])
            base_dict = _theme_to_dict(base_theme)

            st.caption("字体（英文/中文/代码）")
            col_f1, col_f2 = st.columns([1, 1])
            with col_f1:
                heading_ascii = st.text_input(
                    "标题英文(ASCII)字体",
                    value=str(base_dict.get("heading_font_ascii") or "Arial"),
                )
                body_ascii = st.text_input(
                    "正文英文(ASCII)字体",
                    value=str(base_dict.get("body_font_ascii") or "Arial"),
                )
                mono_ascii = st.text_input(
                    "代码英文(ASCII)字体",
                    value=str(base_dict.get("mono_font_ascii") or "Arial"),
                )
            with col_f2:
                heading_cjk = st.text_input(
                    "标题中文(CJK)字体",
                    value=str(base_dict.get("heading_font_cjk") or "等线"),
                )
                body_cjk = st.text_input(
                    "正文中文(CJK)字体",
                    value=str(base_dict.get("body_font_cjk") or "等线"),
                )
                mono_cjk = st.text_input(
                    "代码中文(CJK)字体",
                    value=str(base_dict.get("mono_font_cjk") or "等线"),
                )

            st.caption("字号（pt）")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                h1_size = st.number_input(
                    "H1",
                    min_value=8,
                    max_value=64,
                    value=int(base_dict.get("h1_size", 22)),
                )
                h2_size = st.number_input(
                    "H2",
                    min_value=8,
                    max_value=64,
                    value=int(base_dict.get("h2_size", 16)),
                )
                h3_size = st.number_input(
                    "H3",
                    min_value=8,
                    max_value=64,
                    value=int(base_dict.get("h3_size", 13)),
                )
            with col_s2:
                h4_size = st.number_input(
                    "H4",
                    min_value=8,
                    max_value=64,
                    value=int(base_dict.get("h4_size", 12)),
                )
                body_size = st.number_input(
                    "正文",
                    min_value=8,
                    max_value=32,
                    value=int(base_dict.get("body_size", 11)),
                )
                caption_size = st.number_input(
                    "Caption",
                    min_value=6,
                    max_value=24,
                    value=int(base_dict.get("caption_size", 9)),
                )
            with col_s3:
                code_size = st.number_input(
                    "代码",
                    min_value=6,
                    max_value=24,
                    value=int(base_dict.get("code_size", 10)),
                )

            st.caption("颜色（hex，无 #）")
            col_c1, col_c2 = st.columns([1, 1])
            with col_c1:
                primary = st.text_input(
                    "primary(H1)",
                    value=str(base_dict.get("primary", "1E3A5F")),
                )
                secondary = st.text_input(
                    "secondary(H2)",
                    value=str(base_dict.get("secondary", "2563EB")),
                )
                accent = st.text_input(
                    "accent(H3/链接)",
                    value=str(base_dict.get("accent", "0EA5E9")),
                )
                body_text = st.text_input(
                    "body_text",
                    value=str(base_dict.get("body_text", "1F2937")),
                )
                light_text = st.text_input(
                    "light_text",
                    value=str(base_dict.get("light_text", "6B7280")),
                )
            with col_c2:
                table_header_bg = st.text_input(
                    "table_header_bg",
                    value=str(base_dict.get("table_header_bg", "1E3A5F")),
                )
                table_header_text = st.text_input(
                    "table_header_text",
                    value=str(base_dict.get("table_header_text", "FFFFFF")),
                )
                table_stripe_bg = st.text_input(
                    "table_stripe_bg",
                    value=str(base_dict.get("table_stripe_bg", "EFF6FF")),
                )
                table_border = st.text_input(
                    "table_border",
                    value=str(base_dict.get("table_border", "BFDBFE")),
                )

            st.caption("保存")
            new_name = st.text_input(
                "新主题 ID（name）",
                value=f"{base_theme.name}_custom",
            )
            new_display_name = st.text_input(
                "显示名（display_name）",
                value=f"{base_theme.display_name}（自定义）",
            )
            new_desc = st.text_input(
                "描述（description）",
                value="User customized theme.",
            )

            if st.button("保存主题到 themes/*.json 并立即启用"):
                USER_THEMES_DIR.mkdir(parents=True, exist_ok=True)
                payload = _filter_theme_fields({
                    **base_dict,
                    "name": new_name.strip(),
                    "display_name": new_display_name.strip(),
                    "description": new_desc.strip(),
                    "heading_font_ascii": heading_ascii.strip(),
                    "body_font_ascii": body_ascii.strip(),
                    "mono_font_ascii": mono_ascii.strip(),
                    "heading_font_cjk": heading_cjk.strip(),
                    "body_font_cjk": body_cjk.strip(),
                    "mono_font_cjk": mono_cjk.strip(),
                    "h1_size": int(h1_size),
                    "h2_size": int(h2_size),
                    "h3_size": int(h3_size),
                    "h4_size": int(h4_size),
                    "body_size": int(body_size),
                    "caption_size": int(caption_size),
                    "code_size": int(code_size),
                    "primary": primary.strip(),
                    "secondary": secondary.strip(),
                    "accent": accent.strip(),
                    "body_text": body_text.strip(),
                    "light_text": light_text.strip(),
                    "table_header_bg": table_header_bg.strip(),
                    "table_header_text": table_header_text.strip(),
                    "table_stripe_bg": table_stripe_bg.strip(),
                    "table_border": table_border.strip(),
                })
                if not payload.get("name"):
                    st.error("新主题 ID 不能为空。")
                else:
                    out_path = USER_THEMES_DIR / f"{payload['name']}.json"
                    out_path.write_text(
                        json.dumps(payload, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    register_theme(Theme(**payload))
                    st.success(f"已保存并启用：{out_path.name}")
                    st.rerun()

        st.subheader("2) 选择示例模板（可选）")
        examples = _list_example_json()
        if examples:
            ex_names = [p.name for p in examples]
            default_ex = "web_demo_config_example.json"
            default_ex_idx = ex_names.index(default_ex) if default_ex in ex_names else 0
            selected_ex = st.selectbox("示例模板", ex_names, index=default_ex_idx)
            if st.button("加载示例到编辑器"):
                st.session_state["doc_json_text"] = _read_text(ROOT / "examples" / selected_ex)

        st.subheader("3) 编辑 JSON 配置")
        if "doc_json_text" not in st.session_state:
            st.session_state["doc_json_text"] = _load_default_json()
        json_text = st.text_area(
            "DOC 定义（与 `epic-doc generate config.json` 等价）",
            key="doc_json_text",
            value=st.session_state["doc_json_text"],
            height=520,
        )

        generate = st.button("生成 DOCX + HTML 预览 + PDF（需要 pandoc）", type="primary")

    with col_right:
        st.subheader("输出")
        st.caption("DOCX 始终生成；HTML/PDF 需要系统安装 pandoc。")

        out_docx = st.empty()
        out_html = st.empty()
        out_pdf = st.empty()


if view == "build" and "generate" in locals() and generate:
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
        with out_html:
            components.html(html_str, height=900, scrolling=True)
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

