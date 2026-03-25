import io
import zipfile

from epic_doc import EpicDoc


def _read_document_xml(docx_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as zf:
        raw = zf.read("word/document.xml")
    return raw.decode("utf-8", errors="ignore")


def test_professional_cjk_is_kaiti_english_is_arial_globally():
    doc = EpicDoc(theme="professional")
    doc.set_header("Header 页眉 English 中文")
    doc.set_footer("Footer 页脚 English 中文", page_number=True)

    doc.add_heading("标题 Heading 中文 English", level=1)
    doc.add_paragraph("正文 Paragraph 中文 English", font_size=10)
    doc.add_list(["列表 item 1 中文 English", "列表 item 2 中文 English"])
    doc.add_callout("Callout 正文 中文 English", style="info", title="提示 Title 中文 English")
    doc.add_code_block("print('hello')\n# 注释 中文\n")
    doc.add_table(
        data=[
            ["字段 Field", "值 Value"],
            ["名称 Name", "奥托精密 Otto"],
        ],
        headers=True,
        style="grid",
        col_widths=[2.0, 4.0],
        font_size=9,
    )

    xml = _read_document_xml(doc.to_bytes())
    assert 'w:ascii="Arial"' in xml
    assert 'w:hAnsi="Arial"' in xml
    assert 'w:eastAsia="楷体"' in xml


def test_non_professional_defaults_cjk_dengxian_english_arial():
    doc = EpicDoc(theme="minimal")
    doc.add_heading("测试 Test 中文", level=2)
    doc.add_paragraph("段落 Paragraph 中文 English", font_size=10)
    doc.add_code_block("echo hello\n# 中文注释\n")

    xml = _read_document_xml(doc.to_bytes())
    assert 'w:ascii="Arial"' in xml
    assert 'w:hAnsi="Arial"' in xml
    assert 'w:eastAsia="等线"' in xml

