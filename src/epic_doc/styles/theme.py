"""Theme dataclass and registry for epic-doc."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CalloutColors:
    info_bg: str = "DBEAFE"
    info_border: str = "3B82F6"
    warning_bg: str = "FEF3C7"
    warning_border: str = "F59E0B"
    danger_bg: str = "FEE2E2"
    danger_border: str = "EF4444"
    success_bg: str = "D1FAE5"
    success_border: str = "10B981"


@dataclass
class Theme:
    """Complete visual definition for an epic-doc document."""

    # ── Identity ──────────────────────────────────────────────────────────────
    name: str = "professional"
    display_name: str = "Professional"
    description: str = "Clean and professional theme."

    # ── Typography ────────────────────────────────────────────────────────────
    # Legacy single-font fields (kept for backward compatibility). New code
    # should prefer the *_font_ascii / *_font_cjk fields below.
    heading_font: str = "Arial"
    body_font: str = "Arial"
    mono_font: str = "Consolas"

    # Explicit per-script fonts (used when writing OOXML w:rFonts).
    # - ascii/hAnsi: English/Latin
    # - eastAsia: CJK
    heading_font_ascii: Optional[str] = None
    body_font_ascii: Optional[str] = None
    mono_font_ascii: Optional[str] = None
    heading_font_cjk: Optional[str] = None
    body_font_cjk: Optional[str] = None
    mono_font_cjk: Optional[str] = None

    # Font sizes in points
    h1_size: int = 22
    h2_size: int = 16
    h3_size: int = 13
    h4_size: int = 12
    body_size: int = 11
    caption_size: int = 9
    code_size: int = 10

    # ── Primary Colors (hex without #) ────────────────────────────────────────
    primary: str = "1E3A5F"       # H1 text
    secondary: str = "2563EB"     # H2 text
    accent: str = "0EA5E9"        # H3 text, links, rule lines
    body_text: str = "1F2937"     # Normal body text
    light_text: str = "6B7280"    # Captions, secondary annotations

    # ── Table Colors ──────────────────────────────────────────────────────────
    table_header_bg: str = "1E3A5F"
    table_header_text: str = "FFFFFF"
    table_stripe_bg: str = "EFF6FF"    # Alternating row fill
    table_border: str = "BFDBFE"       # Outer/inner border
    table_grid: str = "DBEAFE"         # Grid lines

    # ── Page ──────────────────────────────────────────────────────────────────
    page_bg: str = "FFFFFF"

    # ── Code Block ────────────────────────────────────────────────────────────
    code_bg: str = "F1F5F9"
    code_text: str = "1E293B"
    code_border: str = "CBD5E1"

    # ── Callout Boxes ─────────────────────────────────────────────────────────
    callout: CalloutColors = field(default_factory=CalloutColors)

    # ── Chart Palette (hex with #, 7 colors) ─────────────────────────────────
    chart_palette: List[str] = field(default_factory=lambda: [
        "#2563EB", "#16A34A", "#DC2626", "#D97706",
        "#7C3AED", "#0891B2", "#DB2777",
    ])

    # ── Heading Style Flags ───────────────────────────────────────────────────
    h1_bold: bool = True
    h2_bold: bool = True
    h3_bold: bool = True
    h4_bold: bool = True
    h1_italic: bool = False
    h2_italic: bool = False
    h3_italic: bool = False
    h1_caps: bool = False
    h2_caps: bool = False
    h1_border: bool = True          # Bottom border under H1
    h1_border_color: Optional[str] = None  # None → uses accent

    # ── Heading Spacing (pt) ─────────────────────────────────────────────────
    h1_space_before: int = 18
    h1_space_after: int = 6
    h2_space_before: int = 14
    h2_space_after: int = 4
    h3_space_before: int = 10
    h3_space_after: int = 3
    h4_space_before: int = 8
    h4_space_after: int = 2

    # ── Body Spacing ─────────────────────────────────────────────────────────
    body_space_before: int = 0
    body_space_after: int = 8
    body_line_spacing: float = 1.15

    @property
    def h1_border_hex(self) -> str:
        return self.h1_border_color or self.accent

    def __post_init__(self) -> None:
        # Backfill new font fields from legacy ones when not provided.
        self.heading_font_ascii = self.heading_font_ascii or self.heading_font
        self.body_font_ascii = self.body_font_ascii or self.body_font
        # Requirement: English should default to Arial globally (including code blocks)
        # unless a theme explicitly overrides mono_font_ascii.
        self.mono_font_ascii = self.mono_font_ascii or "Arial"

        self.heading_font_cjk = self.heading_font_cjk or "等线"
        self.body_font_cjk = self.body_font_cjk or "等线"
        self.mono_font_cjk = self.mono_font_cjk or "等线"


# ── Registry ─────────────────────────────────────────────────────────────────

_REGISTRY: Dict[str, Theme] = {}


def register_theme(theme: Theme) -> Theme:
    _REGISTRY[theme.name] = theme
    return theme


def get_theme(name: str) -> Theme:
    if name not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")
    return _REGISTRY[name]


def list_themes() -> List[Theme]:
    return list(_REGISTRY.values())
