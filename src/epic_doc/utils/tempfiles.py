"""Temporary file manager for chart and diagram images."""
from __future__ import annotations

import os
import tempfile


class TempFileManager:
    """Tracks temporary files created during document build and cleans them up."""

    def __init__(self) -> None:
        self._paths: list[str] = []

    def new_tempfile(self, *, suffix: str = ".tmp", prefix: str = "epic_doc_") -> str:
        """Create a new tracked temporary file path and return its path.

        The file is created (via ``mkstemp``) and will be deleted on ``cleanup()``.
        """
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(fd)
        self._paths.append(path)
        return path

    def new_png(self) -> str:
        """Create a new temporary PNG file and return its path."""
        return self.new_tempfile(suffix=".png", prefix="epic_doc_")

    def cleanup(self) -> None:
        """Delete all tracked temporary files."""
        for path in self._paths:
            try:
                os.unlink(path)
            except OSError:
                pass
        self._paths.clear()

    def __enter__(self) -> TempFileManager:
        return self

    def __exit__(self, *_: object) -> None:
        self.cleanup()
