# ruff: noqa: UP045

"""pandoc-based DOCX -> HTML/PDF conversion.

This module keeps conversions bytes-level for easy integration with HTTP responses.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import Optional

from epic_doc.utils.tempfiles import TempFileManager


def _require_pandoc(pandoc_path: str = "pandoc") -> str:
    """Return pandoc executable path or raise a helpful error."""
    # Prefer explicit path if provided, but still validate it.
    if pandoc_path != "pandoc":
        if os.path.isfile(pandoc_path):
            return pandoc_path
        raise ImportError(
            "pandoc executable not found at the provided path: "
            f"{pandoc_path}. Please install pandoc and ensure the binary is available."
        )

    found = shutil.which("pandoc")
    if not found:
        raise ImportError(
            "pandoc is required for DOCX -> HTML/PDF conversion. "
            "Install it first: https://pandoc.org/installing.html"
        )
    return found


def docx_bytes_to_html_bytes(
    docx_bytes: bytes,
    *,
    title: Optional[str] = None,
    pandoc_path: str = "pandoc",
    extra_args: Optional[list[str]] = None,
) -> bytes:
    """Convert DOCX bytes into standalone HTML bytes using pandoc."""
    pandoc_bin = _require_pandoc(pandoc_path)
    extra_args = extra_args or []

    tmgr = TempFileManager()
    try:
        in_path = tmgr.new_tempfile(suffix=".docx")
        with open(in_path, "wb") as f:
            f.write(docx_bytes)

        out_path = tmgr.new_tempfile(suffix=".html")

        cmd: list[str] = [
            pandoc_bin,
            in_path,
            "-f",
            "docx",
            "-t",
            "html",
            "-s",
            "--standalone",
            "--wrap=none",
            "-o",
            out_path,
        ]
        if title:
            cmd.extend(["--metadata", f"title={title}"])
        cmd.extend(extra_args)

        proc = subprocess.run(
            cmd,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="ignore")
            raise RuntimeError(f"pandoc HTML conversion failed: {stderr}")

        with open(out_path, "rb") as f:
            return f.read()
    finally:
        tmgr.cleanup()


def docx_bytes_to_pdf_bytes(
    docx_bytes: bytes,
    *,
    pandoc_path: str = "pandoc",
    extra_args: Optional[list[str]] = None,
) -> bytes:
    """Convert DOCX bytes into PDF bytes using pandoc."""
    pandoc_bin = _require_pandoc(pandoc_path)
    extra_args = extra_args or []

    tmgr = TempFileManager()
    try:
        in_path = tmgr.new_tempfile(suffix=".docx")
        with open(in_path, "wb") as f:
            f.write(docx_bytes)

        out_path = tmgr.new_tempfile(suffix=".pdf")

        cmd: list[str] = [
            pandoc_bin,
            in_path,
            "-f",
            "docx",
            "-t",
            "pdf",
            "-s",
            "-o",
            out_path,
        ]
        cmd.extend(extra_args)

        proc = subprocess.run(
            cmd,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", errors="ignore")
            raise RuntimeError(f"pandoc PDF conversion failed: {stderr}")

        with open(out_path, "rb") as f:
            return f.read()
    finally:
        tmgr.cleanup()

