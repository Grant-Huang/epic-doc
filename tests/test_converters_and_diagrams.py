import io
import shutil

import pytest
from PIL import Image

from epic_doc import EpicDoc
from epic_doc.converters.pandoc import docx_bytes_to_html_bytes, docx_bytes_to_pdf_bytes


def _has_pandoc() -> bool:
    return shutil.which("pandoc") is not None


def _readable_html(html_bytes: bytes) -> str:
    return html_bytes.decode("utf-8", errors="ignore")


def test_image_smoke_insert_bytes():
    # Ensure image insertion works without system dependencies.
    doc = EpicDoc(theme="minimal")

    img = Image.new("RGB", (16, 16), (255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    doc.add_image(img_bytes, width=2.0, caption="test image")
    data = doc.to_bytes()
    assert data[:2] == b"PK"


def test_flowchart_smoke_with_graphviz():
    # Graphviz needs both python package + system binary ("dot").
    if shutil.which("dot") is None:
        pytest.skip("graphviz binary 'dot' not found in PATH")

    doc = EpicDoc(theme="tech")
    doc.add_heading("Flowchart Test", level=1)
    doc.add_flowchart(
        nodes={
            "start": "开始",
            "process": {"label": "处理", "shape": "box"},
            "end": "结束",
        },
        edges=[
            ("start", "process"),
            ("process", "end"),
        ],
        caption="flowchart smoke",
        direction="TB",
    )
    data = doc.to_bytes()
    assert data[:2] == b"PK"


@pytest.mark.skipif(not _has_pandoc(), reason="pandoc not installed")
def test_docx_to_html_bytes():
    doc = EpicDoc(theme="ocean")
    doc.add_heading("Hello", level=1)
    doc.add_paragraph("World")
    docx_bytes = doc.to_bytes()

    html_bytes = docx_bytes_to_html_bytes(docx_bytes, title="Hello")
    html = _readable_html(html_bytes)
    assert "<html" in html.lower()
    assert "Hello" in html


@pytest.mark.skipif(not _has_pandoc(), reason="pandoc not installed")
def test_docx_to_pdf_bytes_smoke():
    doc = EpicDoc(theme="minimal")
    doc.add_heading("PDF Smoke", level=1)
    doc.add_paragraph("If you see this, pdf conversion works.")
    docx_bytes = doc.to_bytes()

    try:
        pdf_bytes = docx_bytes_to_pdf_bytes(docx_bytes)
    except RuntimeError as exc:
        # Common case: pandoc pdf needs a TeX engine.
        msg = str(exc).lower()
        if any(k in msg for k in ("xelatex", "pdflatex", "latex", "tectonic")):
            pytest.skip("PDF conversion requires a LaTeX engine (not available).")
        raise

    assert pdf_bytes[:4] == b"%PDF"

