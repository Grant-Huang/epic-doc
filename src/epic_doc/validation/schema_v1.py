"""JSON Schema v1 generator for epic-doc config definitions.

This schema is intended to be:
- Human-readable (for docs/tools)
- Machine-usable (for JSON schema validators)

It focuses on structural validation. Some semantic constraints (e.g. table merge
bounds) are validated in Python in `validator.py`.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _meta_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "source": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "doc": {"type": "string"},
                    "chunk": {"type": ["string", "integer"]},
                    "offset": {
                        "oneOf": [
                            {"type": "integer"},
                            {
                                "type": "array",
                                "items": {"type": "integer"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            {"type": "null"},
                        ]
                    },
                },
            }
        },
    }


def _block_base_properties() -> Dict[str, Any]:
    return {
        "meta": _meta_schema(),
    }


def _block_schema_heading() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "text"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "heading"},
            "text": {"type": "string"},
            "level": {"type": "integer", "minimum": 1, "maximum": 4},
            "align": {"type": "string", "enum": ["left", "center", "right", "justify"]},
        },
    }


def _block_schema_paragraph() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "text"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "paragraph"},
            "text": {"type": "string"},
            "bold": {"type": "boolean"},
            "italic": {"type": "boolean"},
            "underline": {"type": "boolean"},
            "color": {"type": ["string", "null"]},
            "align": {"type": "string", "enum": ["left", "center", "right", "justify"]},
            "font_size": {"type": ["integer", "null"], "minimum": 6, "maximum": 72},
            "style": {"type": ["string", "null"]},
        },
    }


def _block_schema_list() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "items"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "list"},
            "items": {"type": "array"},
            "style": {"type": "string", "enum": ["bullet", "numbered"]},
        },
    }


def _block_schema_code() -> Dict[str, Any]:
    # Accept both "code" and "code_block" for compatibility.
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "code"],
        "properties": {
            **_block_base_properties(),
            "type": {"type": "string", "enum": ["code", "code_block"]},
            "code": {"type": "string"},
            "language": {"type": ["string", "null"]},
        },
    }


def _block_schema_callout() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "text"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "callout"},
            "text": {"type": "string"},
            "style": {"type": "string", "enum": ["info", "warning", "danger", "success"]},
            "title": {"type": ["string", "null"]},
        },
    }


def _block_schema_hyperlink() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "text", "url"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "hyperlink"},
            "text": {"type": "string"},
            "url": {"type": "string"},
        },
    }


def _block_schema_hr() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "hr"},
        },
    }


def _block_schema_page_break() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "page_break"},
        },
    }


def _block_schema_section_break() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "section_break"},
            "break_type": {
                "type": "string",
                "enum": ["next_page", "even_page", "odd_page", "continuous"],
            },
        },
    }


def _block_schema_toc() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "toc"},
            "title": {"type": "string"},
            "depth": {"type": "integer", "minimum": 1, "maximum": 9},
        },
    }


def _block_schema_table() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "data"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "table"},
            "data": {"type": "array"},
            "headers": {"type": "boolean"},
            "style": {
                "type": "string",
                "enum": ["striped", "grid", "minimal", "bordered", "dark", "card"],
            },
            "col_widths": {"type": ["array", "null"], "items": {"type": "number"}},
            "merge": {
                "type": ["array", "null"],
                "items": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "minItems": 4,
                    "maxItems": 4,
                },
            },
            "caption": {"type": ["string", "null"]},
            "align": {"type": "string", "enum": ["left", "center", "right"]},
            "font_size": {"type": ["integer", "null"], "minimum": 6, "maximum": 72},
            "cell_align": {"type": "string", "enum": ["left", "center", "right"]},
        },
    }


def _block_schema_chart() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "data"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "chart"},
            "chart_type": {
                "type": "string",
                "enum": ["bar", "hbar", "line", "area", "pie", "scatter", "combo"],
            },
            "data": {"type": "object"},
            "title": {"type": ["string", "null"]},
            "xlabel": {"type": ["string", "null"]},
            "ylabel": {"type": ["string", "null"]},
            "width": {"type": "number"},
            "height": {"type": "number"},
            "colors": {"type": ["array", "null"], "items": {"type": "string"}},
            "caption": {"type": ["string", "null"]},
            "show_values": {"type": "boolean"},
            "show_grid": {"type": "boolean"},
            "legend": {"type": "boolean"},
        },
    }


def _block_schema_flowchart() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "nodes", "edges"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "flowchart"},
            "nodes": {"type": "object"},
            "edges": {"type": "array"},
            "direction": {"type": "string", "enum": ["TB", "LR", "RL", "BT"]},
            "width": {"type": "number"},
            "caption": {"type": ["string", "null"]},
            "graph_attrs": {"type": ["object", "null"]},
        },
    }


def _block_schema_image() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "path"],
        "properties": {
            **_block_base_properties(),
            "type": {"const": "image"},
            "path": {"type": "string"},
            "width": {"type": ["number", "null"]},
            "height": {"type": ["number", "null"]},
            "align": {"type": "string", "enum": ["left", "center", "right"]},
            "caption": {"type": ["string", "null"]},
        },
    }


def _blocks_oneof() -> List[Dict[str, Any]]:
    return [
        _block_schema_heading(),
        _block_schema_paragraph(),
        _block_schema_list(),
        _block_schema_code(),
        _block_schema_callout(),
        _block_schema_hyperlink(),
        _block_schema_hr(),
        _block_schema_page_break(),
        _block_schema_section_break(),
        _block_schema_toc(),
        _block_schema_table(),
        _block_schema_chart(),
        _block_schema_flowchart(),
        _block_schema_image(),
    ]


def build_schema_v1() -> Dict[str, Any]:
    """Return JSON Schema (dict) for epic-doc config files."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://epic-doc.dev/schema/v1.json",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "theme": {"type": "string", "description": "Theme ID (see: epic-doc themes)"},
            "template": {"type": ["string", "null"], "description": "Path to .docx template"},
            "meta": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
            "header": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "text": {"type": "string"},
                            "align": {"type": "string", "enum": ["left", "center", "right"]},
                            "include_title": {"type": "boolean"},
                        },
                    },
                ]
            },
            "footer": {
                "oneOf": [
                    {"type": "boolean"},
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "text": {"type": ["string", "null"]},
                            "page_number": {"type": "boolean"},
                            "align": {"type": "string", "enum": ["left", "center", "right"]},
                        },
                    },
                ]
            },
            "audit": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "enabled": {"type": "boolean"},
                    "title": {"type": "string"},
                },
            },
            "blocks": {
                "type": "array",
                "items": {"oneOf": _blocks_oneof()},
            },
        },
        "required": ["blocks"],
    }

