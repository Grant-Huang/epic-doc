"""Tests for the table element."""
from epic_doc import EpicDoc

SAMPLE_DATA = [
    ["Name", "Q1", "Q2", "Q3"],
    ["Product A", 100, 200, 150],
    ["Product B", 80, 90, 110],
]


def _make_doc() -> EpicDoc:
    return EpicDoc(theme="professional")


def test_basic_table():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, headers=True, style="striped")
    data = doc.to_bytes()
    assert data[:2] == b"PK"


def test_table_styles():
    for style in ("striped", "grid", "minimal", "bordered", "dark", "card"):
        doc = _make_doc()
        doc.add_table(data=SAMPLE_DATA, headers=True, style=style)
        data = doc.to_bytes()
        assert data[:2] == b"PK", f"Style '{style}' failed"


def test_table_with_caption():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, caption="表 1：测试表格")
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_with_col_widths():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, col_widths=[2.5, 1.0, 1.0, 1.0])
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_merge_cells():
    doc = _make_doc()
    doc.add_table(
        data=[
            ["Region", "Q1", "Q2"],
            ["APAC",   100,  200],
            ["EMEA",   80,   90],
        ],
        merge=[(0, 0, 0, 0)],
    )
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_without_headers():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, headers=False)
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_with_alignment():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, align="center", cell_align="center")
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_custom_font_size():
    doc = _make_doc()
    doc.add_table(data=SAMPLE_DATA, font_size=9)
    data = doc.to_bytes()
    assert len(data) > 0


def test_empty_table_does_not_crash():
    doc = _make_doc()
    doc.add_table(data=[])  # should silently do nothing
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_single_row():
    doc = _make_doc()
    doc.add_table(data=[["Only", "One", "Row"]], headers=True)
    data = doc.to_bytes()
    assert len(data) > 0


def test_large_table():
    doc = _make_doc()
    header = ["#", "Name", "Value", "Status"]
    rows = [[i, f"Item {i}", i * 10, "OK"] for i in range(1, 51)]
    doc.add_table(data=[header] + rows, headers=True, style="striped")
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_with_all_themes():
    from epic_doc import list_themes
    for theme in list_themes():
        doc = EpicDoc(theme=theme.name)
        doc.add_table(data=SAMPLE_DATA, headers=True)
        data = doc.to_bytes()
        assert data[:2] == b"PK", f"Table with theme '{theme.name}' failed"
