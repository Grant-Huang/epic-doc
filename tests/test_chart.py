"""Tests for the chart element (matplotlib rendering)."""
import pytest

from epic_doc import EpicDoc


def _doc(theme="ocean") -> EpicDoc:
    return EpicDoc(theme=theme)


# ── Single-series charts ──────────────────────────────────────────────────────

SINGLE = {"Q1": 100, "Q2": 200, "Q3": 150, "Q4": 250}


def test_bar_chart():
    doc = _doc()
    doc.add_chart(chart_type="bar", data=SINGLE, title="Bar Chart")
    assert doc.to_bytes()[:2] == b"PK"


def test_hbar_chart():
    doc = _doc()
    doc.add_chart(chart_type="hbar", data=SINGLE, title="Horizontal Bar")
    assert doc.to_bytes()[:2] == b"PK"


def test_line_chart():
    doc = _doc()
    doc.add_chart(chart_type="line", data=SINGLE, title="Line Chart")
    assert doc.to_bytes()[:2] == b"PK"


def test_area_chart():
    doc = _doc()
    doc.add_chart(chart_type="area", data=SINGLE, title="Area Chart")
    assert doc.to_bytes()[:2] == b"PK"


def test_pie_chart():
    doc = _doc()
    doc.add_chart(chart_type="pie", data=SINGLE, title="Pie Chart")
    assert doc.to_bytes()[:2] == b"PK"


def test_scatter_chart():
    doc = _doc()
    doc.add_chart(chart_type="scatter", data=SINGLE, title="Scatter")
    assert doc.to_bytes()[:2] == b"PK"


# ── Multi-series charts ───────────────────────────────────────────────────────

MULTI = {
    "Sales":  {"Q1": 100, "Q2": 150, "Q3": 130, "Q4": 200},
    "Profit": {"Q1": 30,  "Q2": 45,  "Q3": 39,  "Q4": 60},
}


def test_bar_multiseries():
    doc = _doc()
    doc.add_chart(chart_type="bar", data=MULTI, title="Multi-series Bar")
    assert doc.to_bytes()[:2] == b"PK"


def test_line_multiseries():
    doc = _doc()
    doc.add_chart(chart_type="line", data=MULTI, title="Multi-series Line", legend=True)
    assert doc.to_bytes()[:2] == b"PK"


def test_area_multiseries():
    doc = _doc()
    doc.add_chart(chart_type="area", data=MULTI, title="Multi-series Area")
    assert doc.to_bytes()[:2] == b"PK"


def test_hbar_multiseries():
    doc = _doc()
    doc.add_chart(chart_type="hbar", data=MULTI, title="Multi-series HBar")
    assert doc.to_bytes()[:2] == b"PK"


def test_combo_chart():
    doc = _doc()
    doc.add_chart(chart_type="combo", data=MULTI, title="Combo Chart")
    assert doc.to_bytes()[:2] == b"PK"


# ── Chart options ─────────────────────────────────────────────────────────────

def test_chart_with_caption():
    doc = _doc()
    doc.add_chart(chart_type="bar", data=SINGLE, caption="图 1：季度营收")
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_show_values():
    doc = _doc()
    doc.add_chart(chart_type="bar", data=SINGLE, show_values=True)
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_custom_size():
    doc = _doc()
    doc.add_chart(chart_type="line", data=SINGLE, width=4.0, height=2.0)
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_custom_colors():
    doc = _doc()
    doc.add_chart(
        chart_type="bar",
        data=SINGLE,
        colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"],
    )
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_axis_labels():
    doc = _doc()
    doc.add_chart(
        chart_type="bar",
        data=SINGLE,
        title="季度数据",
        xlabel="季度",
        ylabel="金额（万）",
    )
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_no_grid():
    doc = _doc()
    doc.add_chart(chart_type="bar", data=SINGLE, show_grid=False)
    assert doc.to_bytes()[:2] == b"PK"


def test_chart_empty_data():
    doc = _doc()
    # Empty data should produce a valid (blank-ish) chart without crashing
    doc.add_chart(chart_type="bar", data={})
    assert doc.to_bytes()[:2] == b"PK"


def test_invalid_chart_type():
    doc = _doc()
    with pytest.raises(ValueError, match="Unknown chart_type"):
        doc.add_chart(chart_type="radar", data=SINGLE)


# ── All themes produce valid charts ──────────────────────────────────────────

def test_chart_all_themes():
    from epic_doc import list_themes
    for theme in list_themes():
        doc = EpicDoc(theme=theme.name)
        doc.add_chart(chart_type="bar", data=SINGLE, title=theme.display_name)
        data = doc.to_bytes()
        assert data[:2] == b"PK", f"Chart with theme '{theme.name}' failed"


# ── Temp file cleanup ─────────────────────────────────────────────────────────

def test_temp_files_cleaned_after_save(tmp_path):
    import os

    doc = _doc()
    doc.add_chart(chart_type="bar", data=SINGLE)

    # Before save, temp files should exist
    assert len(doc._tmgr._paths) > 0
    paths_before = list(doc._tmgr._paths)

    out = str(tmp_path / "out.docx")
    doc.save(out)

    # After save, all temp files removed
    assert len(doc._tmgr._paths) == 0
    for p in paths_before:
        assert not os.path.exists(p), f"Temp file not cleaned: {p}"


def test_temp_files_cleaned_after_to_bytes():
    import os

    doc = _doc()
    doc.add_chart(chart_type="pie", data=SINGLE)
    paths_before = list(doc._tmgr._paths)

    _ = doc.to_bytes()

    assert len(doc._tmgr._paths) == 0
    for p in paths_before:
        assert not os.path.exists(p), f"Temp file not cleaned: {p}"
