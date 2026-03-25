import io
import zipfile

from epic_doc import EpicDoc


def _read_document_xml(docx_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as zf:
        raw = zf.read("word/document.xml")
    return raw.decode("utf-8", errors="ignore")


def test_toc_depth_respected():
    for depth in (1, 2, 3, 4):
        doc = EpicDoc(theme="minimal")
        doc.add_toc(depth=depth)
        xml = _read_document_xml(doc.to_bytes())
        assert f'\\o "1-{depth}"' in xml

