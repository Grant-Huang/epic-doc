"""Elegant — 优雅紫金：紫色与金色的高贵组合，高端提案与奢侈品牌的专属格调。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

ELEGANT = register_theme(Theme(
    name="elegant",
    display_name="优雅紫金 Elegant",
    description="深紫与金色的奢华搭配，高贵典雅。适用于高端商业提案、奢侈品牌报告、VIP 客户文档。",

    heading_font="Arial",
    body_font="Arial",
    mono_font="Courier New",

    h1_size=24,
    h2_size=17,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="3B0764",
    secondary="6B21A8",
    accent="A855F7",
    body_text="1C0038",
    light_text="7E22CE",

    table_header_bg="3B0764",
    table_header_text="F5D060",
    table_stripe_bg="FAF5FF",
    table_border="D8B4FE",
    table_grid="E9D5FF",

    code_bg="FAF5FF",
    code_text="3B0764",
    code_border="C084FC",

    callout=CalloutColors(
        info_bg="FAF5FF", info_border="7E22CE",
        warning_bg="FFFBEB", warning_border="B45309",
        danger_bg="FFF1F2", danger_border="BE185D",
        success_bg="F0FDF4", success_border="15803D",
    ),

    chart_palette=[
        "#3B0764", "#6B21A8", "#7E22CE", "#A855F7",
        "#B45309", "#D97706", "#F59E0B",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=True, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="B45309",

    h1_space_before=22, h1_space_after=8,
    h2_space_before=16, h2_space_after=5,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=9,
    body_line_spacing=1.25,
))
