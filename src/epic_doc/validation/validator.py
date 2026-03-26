"""Definition validation with JSONPath-like error locations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ValidationError:
    path: str
    message: str
    code: Optional[str] = None

    def format(self) -> str:
        return f"{self.path}: {self.message}"


_VALID_BLOCK_TYPES = {
    "heading",
    "paragraph",
    "list",
    "code",
    "code_block",
    "callout",
    "hyperlink",
    "hr",
    "page_break",
    "section_break",
    "toc",
    "table",
    "chart",
    "flowchart",
    "image",
}


def _jp(parent: str, key: str) -> str:
    return f"{parent}.{key}"


def _jpi(parent: str, idx: int) -> str:
    return f"{parent}[{idx}]"


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _jsonpath_from_parts(parts: list[Any]) -> str:
    path = "$"
    for p in parts:
        if isinstance(p, int):
            path += f"[{p}]"
        elif isinstance(p, str) and p.isidentifier():
            path += f".{p}"
        else:
            # Fallback for unusual keys
            path += f"[{p!r}]"
    return path


def _try_jsonschema_validate(defn: Any) -> list[ValidationError]:
    """Best-effort JSON Schema structural validation (soft dependency)."""
    try:
        import jsonschema  # type: ignore
    except Exception:
        return []

    try:
        from epic_doc.validation.schema_v1 import build_schema_v1

        schema = build_schema_v1()
    except Exception:
        return []

    errors: list[ValidationError] = []
    try:
        Validator = getattr(jsonschema, "Draft202012Validator", None)
        if Validator is None:
            # Older jsonschema versions: fallback to validate() with first error only.
            jsonschema.validate(instance=defn, schema=schema)
            return []

        validator = Validator(schema)
        for err in sorted(validator.iter_errors(defn), key=lambda e: list(e.absolute_path)):
            parts = list(err.absolute_path)
            path = _jsonpath_from_parts(parts)
            errors.append(ValidationError(path, err.message, code="schema"))
    except Exception:
        # If jsonschema itself fails unexpectedly, never break validate; just fall back.
        return []

    return errors


def _validate_meta_source(meta: Any, path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if meta is None:
        return errs
    if not isinstance(meta, dict):
        errs.append(ValidationError(path, "meta must be an object", code="type"))
        return errs
    source = meta.get("source")
    if source is None:
        return errs
    sp = _jp(path, "source")
    if not isinstance(source, dict):
        errs.append(ValidationError(sp, "meta.source must be an object", code="type"))
        return errs

    if "doc" in source and not isinstance(source.get("doc"), str):
        errs.append(ValidationError(_jp(sp, "doc"), "must be a string", code="type"))
    if "chunk" in source and not isinstance(source.get("chunk"), (str, int)):
        errs.append(ValidationError(_jp(sp, "chunk"), "must be string or integer", code="type"))
    if "offset" in source:
        off = source.get("offset")
        op = _jp(sp, "offset")
        if off is None:
            return errs
        if isinstance(off, int):
            return errs
        if isinstance(off, list) and len(off) == 2 and all(isinstance(i, int) for i in off):
            return errs
        errs.append(ValidationError(op, "must be int, [int,int], or null", code="type"))
    return errs


def _validate_table_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "data" not in block:
        errs.append(ValidationError(_jp(path, "data"), "missing required field", code="required"))
        return errs
    data = block.get("data")
    dp = _jp(path, "data")
    if not isinstance(data, list) or not data:
        errs.append(ValidationError(dp, "must be a non-empty array", code="type"))
        return errs
    n_rows = len(data)
    row0 = data[0] if data else []
    if not isinstance(row0, list) or not row0:
        errs.append(
            ValidationError(_jpi(dp, 0), "first row must be a non-empty array", code="type")
        )
        return errs
    n_cols = len(row0)
    for r_idx, row in enumerate(data):
        if not isinstance(row, list):
            errs.append(ValidationError(_jpi(dp, r_idx), "row must be an array", code="type"))
            continue
        if len(row) != n_cols:
            errs.append(
                ValidationError(
                    _jpi(dp, r_idx),
                    f"row has {len(row)} columns, expected {n_cols}",
                    code="shape",
                )
            )

    col_widths = block.get("col_widths")
    if col_widths is not None:
        cwp = _jp(path, "col_widths")
        if not isinstance(col_widths, list) or not all(_is_number(x) for x in col_widths):
            errs.append(ValidationError(cwp, "must be an array of numbers", code="type"))
        else:
            if len(col_widths) != n_cols:
                errs.append(
                    ValidationError(
                        cwp,
                        f"expected {n_cols} column widths, got {len(col_widths)}",
                        code="shape",
                    )
                )

    merge = block.get("merge")
    if merge is not None:
        mp = _jp(path, "merge")
        if not isinstance(merge, list):
            errs.append(ValidationError(mp, "must be an array", code="type"))
        else:
            for i, item in enumerate(merge):
                ip = _jpi(mp, i)
                if (
                    not isinstance(item, (list, tuple))
                    or len(item) != 4
                    or not all(isinstance(x, int) for x in item)
                ):
                    errs.append(ValidationError(ip, "must be [sr, sc, er, ec] ints", code="type"))
                    continue
                sr, sc, er, ec = (int(x) for x in item)
                if sr < 0 or sc < 0 or er < 0 or ec < 0:
                    errs.append(ValidationError(ip, "indices must be >= 0", code="range"))
                if sr > er or sc > ec:
                    errs.append(ValidationError(ip, "must satisfy sr<=er and sc<=ec", code="range"))
                if er >= n_rows:
                    errs.append(
                        ValidationError(ip, f"er out of range (rows={n_rows})", code="range")
                    )
                if ec >= n_cols:
                    errs.append(
                        ValidationError(ip, f"ec out of range (cols={n_cols})", code="range")
                    )

    return errs


def _validate_heading_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "text" not in block:
        errs.append(ValidationError(_jp(path, "text"), "missing required field", code="required"))
    elif not isinstance(block.get("text"), str):
        errs.append(ValidationError(_jp(path, "text"), "must be a string", code="type"))

    if "level" in block:
        level = block.get("level")
        lp = _jp(path, "level")
        if not isinstance(level, int):
            errs.append(ValidationError(lp, "must be an integer", code="type"))
        elif not (1 <= level <= 4):
            errs.append(ValidationError(lp, "must be between 1 and 4", code="range"))
    return errs


def _validate_paragraph_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "text" not in block:
        errs.append(ValidationError(_jp(path, "text"), "missing required field", code="required"))
    elif not isinstance(block.get("text"), str):
        errs.append(ValidationError(_jp(path, "text"), "must be a string", code="type"))
    if "font_size" in block and block.get("font_size") is not None:
        fs = block.get("font_size")
        if not isinstance(fs, int):
            errs.append(ValidationError(_jp(path, "font_size"), "must be an integer", code="type"))
        elif fs < 6 or fs > 72:
            errs.append(
                ValidationError(_jp(path, "font_size"), "must be between 6 and 72", code="range")
            )
    return errs


def _validate_list_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "items" not in block:
        errs.append(ValidationError(_jp(path, "items"), "missing required field", code="required"))
        return errs
    items = block.get("items")
    if not isinstance(items, list):
        errs.append(ValidationError(_jp(path, "items"), "must be an array", code="type"))
    return errs


def _validate_code_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "code" not in block:
        errs.append(ValidationError(_jp(path, "code"), "missing required field", code="required"))
    elif not isinstance(block.get("code"), str):
        errs.append(ValidationError(_jp(path, "code"), "must be a string", code="type"))
    return errs


def _validate_callout_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "text" not in block:
        errs.append(ValidationError(_jp(path, "text"), "missing required field", code="required"))
    elif not isinstance(block.get("text"), str):
        errs.append(ValidationError(_jp(path, "text"), "must be a string", code="type"))
    style = block.get("style")
    if style is not None and style not in ("info", "warning", "danger", "success"):
        errs.append(ValidationError(_jp(path, "style"), "invalid style", code="enum"))
    return errs


def _validate_hyperlink_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "text" not in block:
        errs.append(ValidationError(_jp(path, "text"), "missing required field", code="required"))
    if "url" not in block:
        errs.append(ValidationError(_jp(path, "url"), "missing required field", code="required"))
    if "url" in block and not isinstance(block.get("url"), str):
        errs.append(ValidationError(_jp(path, "url"), "must be a string", code="type"))
    return errs


def _validate_toc_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "depth" in block:
        depth = block.get("depth")
        if not isinstance(depth, int):
            errs.append(ValidationError(_jp(path, "depth"), "must be an integer", code="type"))
        elif depth < 1 or depth > 9:
            errs.append(
                ValidationError(_jp(path, "depth"), "must be between 1 and 9", code="range")
            )
    return errs


def _validate_chart_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "data" not in block:
        errs.append(ValidationError(_jp(path, "data"), "missing required field", code="required"))
    elif not isinstance(block.get("data"), dict):
        errs.append(ValidationError(_jp(path, "data"), "must be an object", code="type"))
    return errs


def _validate_flowchart_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "nodes" not in block:
        errs.append(ValidationError(_jp(path, "nodes"), "missing required field", code="required"))
    elif not isinstance(block.get("nodes"), dict):
        errs.append(ValidationError(_jp(path, "nodes"), "must be an object", code="type"))
    if "edges" not in block:
        errs.append(ValidationError(_jp(path, "edges"), "missing required field", code="required"))
    else:
        edges = block.get("edges")
        ep = _jp(path, "edges")
        if not isinstance(edges, list):
            errs.append(ValidationError(ep, "must be an array", code="type"))
        else:
            for i, e in enumerate(edges):
                if not isinstance(e, (list, tuple)):
                    errs.append(ValidationError(_jpi(ep, i), "edge must be an array", code="type"))
                    continue
                if len(e) not in (2, 3):
                    errs.append(
                        ValidationError(_jpi(ep, i), "edge must have 2 or 3 items", code="shape")
                    )
    return errs


def _validate_image_block(block: dict[str, Any], path: str) -> list[ValidationError]:
    errs: list[ValidationError] = []
    if "path" not in block:
        errs.append(ValidationError(_jp(path, "path"), "missing required field", code="required"))
    elif not isinstance(block.get("path"), str):
        errs.append(ValidationError(_jp(path, "path"), "must be a string", code="type"))
    for dim in ("width", "height"):
        if dim in block and block.get(dim) is not None and not _is_number(block.get(dim)):
            errs.append(ValidationError(_jp(path, dim), "must be a number", code="type"))
    return errs


def validate_definition(defn: Any) -> list[ValidationError]:
    """Validate a full config definition. Returns a list of errors."""
    errs: list[ValidationError] = []

    # Soft-dependency accelerator: if jsonschema is installed, use it for
    # structural validation (required fields/types/oneOf) with precise paths.
    errs.extend(_try_jsonschema_validate(defn))

    if not isinstance(defn, dict):
        return [ValidationError("$", "definition must be an object", code="type")]

    blocks = defn.get("blocks")
    if blocks is None:
        errs.append(ValidationError("$.blocks", "missing required field", code="required"))
        return errs
    if not isinstance(blocks, list):
        errs.append(ValidationError("$.blocks", "must be an array", code="type"))
        return errs

    for i, block in enumerate(blocks):
        bp = f"$.blocks[{i}]"
        if not isinstance(block, dict):
            errs.append(ValidationError(bp, "block must be an object", code="type"))
            continue

        errs.extend(_validate_meta_source(block.get("meta"), _jp(bp, "meta")))

        btype = block.get("type")
        tp = _jp(bp, "type")
        if not isinstance(btype, str) or not btype:
            errs.append(ValidationError(tp, "missing or invalid type", code="required"))
            continue
        btype = btype.lower()
        if btype not in _VALID_BLOCK_TYPES:
            errs.append(ValidationError(tp, f"unknown type '{btype}'", code="enum"))
            continue

        if btype == "heading":
            errs.extend(_validate_heading_block(block, bp))
        elif btype == "paragraph":
            errs.extend(_validate_paragraph_block(block, bp))
        elif btype == "list":
            errs.extend(_validate_list_block(block, bp))
        elif btype in ("code", "code_block"):
            errs.extend(_validate_code_block(block, bp))
        elif btype == "callout":
            errs.extend(_validate_callout_block(block, bp))
        elif btype == "hyperlink":
            errs.extend(_validate_hyperlink_block(block, bp))
        elif btype == "toc":
            errs.extend(_validate_toc_block(block, bp))
        elif btype == "table":
            errs.extend(_validate_table_block(block, bp))
        elif btype == "chart":
            errs.extend(_validate_chart_block(block, bp))
        elif btype == "flowchart":
            errs.extend(_validate_flowchart_block(block, bp))
        elif btype == "image":
            errs.extend(_validate_image_block(block, bp))
        else:
            # hr/page_break/section_break: currently no extra validation
            pass

    return errs

