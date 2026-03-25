"""Tests for EpicDoc builder core functionality."""
import pytest

from epic_doc import EpicDoc


def test_epicdoc_default_init():
    doc = EpicDoc()
    assert doc._theme.name == "professional"


def test_epicdoc_custom_theme():
    doc = EpicDoc(theme="ocean")
    assert doc._theme.name == "ocean"


def test_epicdoc_repr():
    doc = EpicDoc(theme="minimal")
    assert "minimal" in repr(doc)


def test_epicdoc_invalid_theme():
    with pytest.raises(ValueError):
        EpicDoc(theme="nonexistent_theme_xyz")


def test_to_bytes_returns_bytes():
    doc = EpicDoc(theme="minimal")
    doc.add_heading("Test", level=1)
    data = doc.to_bytes()
    assert isinstance(data, bytes)
    assert len(data) > 0
    # DOCX magic bytes: PK (zip)
    assert data[:2] == b"PK"


def test_save_creates_file(tmp_path):
    path = str(tmp_path / "test.docx")
    doc = EpicDoc(theme="professional")
    doc.add_heading("Hello World", level=1)
    doc.add_paragraph("This is a test document.")
    doc.save(path)
    import os
    assert os.path.exists(path)
    assert os.path.getsize(path) > 1000


def test_method_chaining():
    doc = EpicDoc(theme="minimal")
    result = (
        doc
        .add_heading("Title", level=1)
        .add_paragraph("Body text")
        .add_list(["A", "B", "C"])
        .add_horizontal_rule()
    )
    assert result is doc


def test_add_heading_levels():
    doc = EpicDoc(theme="professional")
    for lvl in range(1, 5):
        doc.add_heading(f"Level {lvl} heading", level=lvl)
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_paragraph_formatting():
    doc = EpicDoc(theme="professional")
    doc.add_paragraph("Normal text")
    doc.add_paragraph("Bold text", bold=True)
    doc.add_paragraph("Italic text", italic=True)
    doc.add_paragraph("Underlined", underline=True)
    doc.add_paragraph("Red text", color="#DC2626")
    doc.add_paragraph("Centered", align="center")
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_list_bullet():
    doc = EpicDoc(theme="forest")
    doc.add_list(["Item 1", "Item 2", "Item 3"], style="bullet")
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_list_numbered():
    doc = EpicDoc(theme="forest")
    doc.add_list(["Step 1", "Step 2", "Step 3"], style="numbered")
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_code_block():
    doc = EpicDoc(theme="tech")
    doc.add_code_block("print('hello world')", language="python")
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_callout_styles():
    doc = EpicDoc(theme="professional")
    for style in ("info", "warning", "danger", "success"):
        doc.add_callout(f"A {style} message", style=style, title=style.upper())
    data = doc.to_bytes()
    assert len(data) > 0


def test_set_header_footer():
    doc = EpicDoc(theme="nordic")
    doc.set_header("Test Header", align="right")
    doc.set_footer(text="Test Footer", page_number=True)
    data = doc.to_bytes()
    assert len(data) > 0


def test_set_metadata():
    doc = EpicDoc(theme="elegant")
    doc.set_metadata(title="Test Doc", author="Test Author", subject="Testing")
    data = doc.to_bytes()
    assert len(data) > 0


def test_add_page_break():
    doc = EpicDoc(theme="professional")
    doc.add_paragraph("Page 1")
    doc.add_page_break()
    doc.add_paragraph("Page 2")
    data = doc.to_bytes()
    assert len(data) > 0


def test_context_manager():
    with EpicDoc(theme="minimal") as doc:
        doc.add_heading("Context Manager Test", level=1)
        data = doc.to_bytes()
    assert isinstance(data, bytes)


def test_all_themes_produce_valid_docx():
    from epic_doc import list_themes
    for theme in list_themes():
        doc = EpicDoc(theme=theme.name)
        doc.add_heading(f"{theme.display_name}", level=1)
        doc.add_paragraph(theme.description)
        data = doc.to_bytes()
        assert data[:2] == b"PK", f"Theme '{theme.name}' produced invalid DOCX"
