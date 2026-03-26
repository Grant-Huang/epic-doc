import json

from epic_doc.validation.schema_v1 import build_schema_v1


def test_schema_v1_has_blocks_oneof_variants():
    schema = build_schema_v1()
    assert schema["type"] == "object"
    assert "blocks" in schema["properties"]
    items = schema["properties"]["blocks"]["items"]
    assert "oneOf" in items
    one_of = items["oneOf"]
    assert isinstance(one_of, list)
    # Ensure it is more than just a type enum.
    assert len(one_of) >= 10


def test_schema_v1_is_json_serializable():
    schema = build_schema_v1()
    json.dumps(schema, ensure_ascii=False)

