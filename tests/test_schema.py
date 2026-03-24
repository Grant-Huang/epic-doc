"""Tests for the JSON schema parser."""
import pytest

from epic_doc.schema import build_from_dict


def _minimal_def(**kwargs):
    base = {"theme": "minimal", "blocks": []}
    base.update(kwargs)
    return base


def test_empty_blocks():
    doc = build_from_dict(_minimal_def())
    data = doc.to_bytes()
    assert data[:2] == b"PK"


def test_heading_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "heading", "text": "Test", "level": 1},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_paragraph_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "paragraph", "text": "Hello world", "bold": True},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_list_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "list", "items": ["A", "B", "C"], "style": "bullet"},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_code_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "code", "code": "print('hello')", "language": "python"},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_callout_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "callout", "text": "Watch out!", "style": "warning"},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_table_block():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "table", "data": [["A", "B"], [1, 2]], "headers": True},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_hr_and_page_break():
    doc = build_from_dict(_minimal_def(blocks=[
        {"type": "paragraph", "text": "Before"},
        {"type": "hr"},
        {"type": "page_break"},
        {"type": "paragraph", "text": "After"},
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_meta_block():
    doc = build_from_dict({
        "theme": "professional",
        "meta": {"title": "Schema Test", "author": "Tester"},
        "blocks": [],
    })
    data = doc.to_bytes()
    assert len(data) > 0


def test_header_footer_string():
    doc = build_from_dict({
        "theme": "ocean",
        "header": "My Header",
        "footer": {"page_number": True},
        "blocks": [],
    })
    data = doc.to_bytes()
    assert len(data) > 0


def test_unknown_block_type_raises():
    with pytest.raises(ValueError, match="Unknown block type"):
        build_from_dict(_minimal_def(blocks=[
            {"type": "unknown_xyz"},
        ]))


def test_table_merge_from_list():
    doc = build_from_dict(_minimal_def(blocks=[
        {
            "type": "table",
            "data": [["A", "B", "C"], [1, 2, 3]],
            "merge": [[0, 0, 0, 1]],
        },
    ]))
    data = doc.to_bytes()
    assert len(data) > 0


def test_full_definition():
    definition = {
        "theme": "nordic",
        "meta": {"title": "Full Test", "author": "Test"},
        "header": {"text": "Test Header", "align": "right"},
        "footer": {"text": "Footer", "page_number": True},
        "blocks": [
            {"type": "heading", "text": "Full Document Test", "level": 1},
            {"type": "paragraph", "text": "Intro paragraph."},
            {"type": "list", "items": ["A", "B"], "style": "bullet"},
            {"type": "hr"},
            {"type": "table", "data": [["X", "Y"], [1, 2]], "headers": True},
            {"type": "code", "code": "x = 1", "language": "python"},
            {"type": "callout", "text": "Note", "style": "info"},
            {"type": "page_break"},
            {"type": "paragraph", "text": "Page 2 content."},
        ],
    }
    doc = build_from_dict(definition)
    data = doc.to_bytes()
    assert data[:2] == b"PK"
