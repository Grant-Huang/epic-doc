"""Forest — 自然绿意：沉稳的绿色系，环保报告、可持续发展主题的绝配。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

FOREST = register_theme(Theme(
    name="forest",
    display_name="自然绿意 Forest",
    description="自然森林的绿色层次，沉稳而充满生命力。适用于环保报告、可持续发展年报、农业/林业报告。",

    heading_font="Georgia",
    body_font="Georgia",
    mono_font="Courier New",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="14532D",
    secondary="166534",
    accent="15803D",
    body_text="1C3829",
    light_text="6B7280",

    table_header_bg="14532D",
    table_header_text="FFFFFF",
    table_stripe_bg="F0FDF4",
    table_border="86EFAC",
    table_grid="BBF7D0",

    code_bg="F0FDF4",
    code_text="14532D",
    code_border="86EFAC",

    callout=CalloutColors(
        info_bg="DCFCE7", info_border="15803D",
        warning_bg="FEF9C3", warning_border="92400E",
        danger_bg="FEE2E2", danger_border="991B1B",
        success_bg="D1FAE5", success_border="065F46",
    ),

    chart_palette=[
        "#14532D", "#166534", "#15803D", "#16A34A",
        "#22C55E", "#4ADE80", "#86EFAC",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="15803D",

    h1_space_before=20, h1_space_after=8,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.2,
))
