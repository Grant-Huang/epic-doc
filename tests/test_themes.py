"""Tests for the theme system."""
import pytest

from epic_doc.styles import get_theme, list_themes
from epic_doc.styles.theme import Theme

EXPECTED_THEMES = [
    "professional", "minimal", "ocean", "forest", "sunset",
    "elegant", "tech", "academic", "cherry", "nordic", "ruby",
]


def test_all_themes_registered():
    names = [t.name for t in list_themes()]
    for expected in EXPECTED_THEMES:
        assert expected in names, f"Theme '{expected}' not registered"


def test_theme_count():
    assert len(list_themes()) >= 10


def test_get_theme_returns_theme():
    t = get_theme("professional")
    assert isinstance(t, Theme)
    assert t.name == "professional"


def test_get_theme_unknown_raises():
    with pytest.raises(ValueError, match="Unknown theme"):
        get_theme("does_not_exist")


def test_all_themes_have_required_fields():
    for theme in list_themes():
        assert theme.name, "Theme missing name"
        assert theme.display_name, f"Theme '{theme.name}' missing display_name"
        assert theme.description, f"Theme '{theme.name}' missing description"
        assert theme.primary, f"Theme '{theme.name}' missing primary color"
        assert theme.heading_font, f"Theme '{theme.name}' missing heading_font"
        assert theme.body_font, f"Theme '{theme.name}' missing body_font"
        assert len(theme.chart_palette) >= 5, \
            f"Theme '{theme.name}' chart_palette too short"


def test_theme_colors_are_valid_hex():
    import re
    hex6 = re.compile(r"^[0-9A-Fa-f]{6}$")
    for theme in list_themes():
        for field in ("primary", "secondary", "accent", "body_text",
                      "table_header_bg", "table_header_text"):
            val = getattr(theme, field)
            assert hex6.match(val), \
                f"Theme '{theme.name}'.{field} = '{val}' is not a valid 6-char hex"


def test_theme_font_sizes_positive():
    for theme in list_themes():
        assert theme.h1_size > theme.h2_size >= theme.h3_size >= theme.body_size > 0, \
            f"Theme '{theme.name}' has inconsistent font sizes"


def test_h1_border_hex_falls_back_to_accent():
    t = get_theme("academic")
    assert not t.h1_border  # academic has no H1 border
    t2 = get_theme("professional")
    assert t2.h1_border
    assert t2.h1_border_hex == t2.h1_border_color or t2.h1_border_hex == t2.accent
