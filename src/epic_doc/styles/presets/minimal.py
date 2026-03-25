"""Minimal — 极简墨白：纯净排版，技术文档、API 文档的理想选择。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

MINIMAL = register_theme(Theme(
    name="minimal",
    display_name="极简墨白 Minimal",
    description="去除装饰，只保留内容本身。纯黑白灰配色，适用于技术文档、API 文档、开发规范。",

    heading_font="Arial",
    body_font="Arial",
    mono_font="Consolas",

    h1_size=20,
    h2_size=15,
    h3_size=12,
    h4_size=11,
    body_size=10,
    caption_size=8,
    code_size=9,

    primary="111827",
    secondary="374151",
    accent="4B5563",
    body_text="1F2937",
    light_text="9CA3AF",

    table_header_bg="1F2937",
    table_header_text="FFFFFF",
    table_stripe_bg="F9FAFB",
    table_border="D1D5DB",
    table_grid="E5E7EB",

    code_bg="F3F4F6",
    code_text="111827",
    code_border="D1D5DB",

    callout=CalloutColors(
        info_bg="F3F4F6", info_border="6B7280",
        warning_bg="FFFBEB", warning_border="9CA3AF",
        danger_bg="FEF2F2", danger_border="6B7280",
        success_bg="F0FDF4", success_border="6B7280",
    ),

    chart_palette=[
        "#111827", "#374151", "#6B7280", "#9CA3AF",
        "#D1D5DB", "#1F2937", "#4B5563",
    ],

    h1_bold=True, h2_bold=True, h3_bold=False, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="D1D5DB",

    h1_space_before=20, h1_space_after=8,
    h2_space_before=16, h2_space_after=4,
    h3_space_before=12, h3_space_after=2,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=6,
    body_line_spacing=1.2,
))
