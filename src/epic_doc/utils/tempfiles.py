"""Temporary file manager for chart and diagram images."""
from __future__ import annotations

import os
import tempfile
from typing import List


class TempFileManager:
    """Tracks temporary files created during document build and cleans them up."""

    def __init__(self) -> None:
        self._paths: List[str] = []

    def new_png(self) -> str:
        """Create a new temporary PNG file and return its path."""
        fd, path = tempfile.mkstemp(suffix=".png", prefix="epic_doc_")
        os.close(fd)
        self._paths.append(path)
        return path

    def cleanup(self) -> None:
        """Delete all tracked temporary files."""
        for path in self._paths:
            try:
                os.unlink(path)
            except OSError:
                pass
        self._paths.clear()

    def __enter__(self) -> "TempFileManager":
        return self

    def __exit__(self, *_: object) -> None:
        self.cleanup()
