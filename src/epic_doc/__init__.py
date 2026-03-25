"""epic-doc — generate complex, beautiful DOCX documents programmatically."""
from epic_doc.builder import EpicDoc
from epic_doc.styles import get_theme, list_themes
from epic_doc.styles.theme import Theme

__version__ = "0.1.0"
__all__ = ["EpicDoc", "Theme", "get_theme", "list_themes"]
