from epic_doc.validation.validator import validate_definition


def test_validate_reports_precise_path_for_heading_level():
    definition = {
        "theme": "minimal",
        "blocks": [
            {"type": "heading", "text": "T", "level": 99},
        ],
    }
    errors = validate_definition(definition)
    msgs = [e.format() for e in errors]
    assert any(m.startswith("$.blocks[0].level:") for m in msgs)


def test_validate_reports_precise_path_for_table_col_widths_and_merge():
    definition = {
        "theme": "minimal",
        "blocks": [
            {
                "type": "table",
                "data": [
                    ["A", "B"],
                    [1, 2],
                ],
                "col_widths": [1.0],
                "merge": [[0, 0, 99, 1]],
            }
        ],
    }
    errors = validate_definition(definition)
    msgs = [e.format() for e in errors]
    assert any(m.startswith("$.blocks[0].col_widths:") for m in msgs)
    assert any(m.startswith("$.blocks[0].merge[0]:") for m in msgs)


def test_validate_accepts_meta_source_shape():
    definition = {
        "theme": "minimal",
        "blocks": [
            {
                "type": "paragraph",
                "text": "x",
                "meta": {"source": {"doc": "a.md", "chunk": "c1", "offset": [10, 20]}},
            }
        ],
    }
    errors = validate_definition(definition)
    assert errors == []


def test_validate_uses_jsonschema_when_available(monkeypatch):
    import sys
    from types import ModuleType

    calls: list[tuple[object, object]] = []

    class FakeErr:
        def __init__(self):
            self.absolute_path = ["blocks", 0, "text"]
            self.message = "is a required property"

    class FakeValidator:
        def __init__(self, schema):
            self.schema = schema

        def iter_errors(self, instance):
            calls.append((instance, self.schema))
            yield FakeErr()

    fake = ModuleType("jsonschema")
    fake.Draft202012Validator = FakeValidator  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "jsonschema", fake)

    definition = {"blocks": [{"type": "heading"}]}
    errors = validate_definition(definition)
    assert calls, "expected jsonschema validator to be invoked"
    assert any(e.path == "$.blocks[0].text" for e in errors)

