"""Theme system for epic-doc."""
# Trigger registration of all built-in themes
import epic_doc.styles.presets  # noqa: F401, E402
from epic_doc.styles.theme import Theme, get_theme, list_themes, register_theme

__all__ = ["Theme", "get_theme", "list_themes", "register_theme"]
