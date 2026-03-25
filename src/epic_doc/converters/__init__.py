"""Converters: optional output formats (pandoc, etc.)."""

from epic_doc.converters.pandoc import docx_bytes_to_html_bytes, docx_bytes_to_pdf_bytes

__all__ = ["docx_bytes_to_html_bytes", "docx_bytes_to_pdf_bytes"]

