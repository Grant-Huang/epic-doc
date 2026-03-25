"""Nordic — 北欧简约：冰蓝与雪白的斯堪的纳维亚美学，产品白皮书的理想气质。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

NORDIC = register_theme(Theme(
    name="nordic",
    display_name="北欧简约 Nordic",
    description="斯堪的纳维亚风格的冰蓝雪白，清冷却温暖。适用于产品白皮书、UX 报告、SaaS 产品文档。",

    heading_font="Arial",
    body_font="Arial",
    mono_font="Consolas",

    h1_size=21,
    h2_size=15,
    h3_size=12,
    h4_size=11,
    body_size=10,
    caption_size=8,
    code_size=9,

    primary="1C3748",
    secondary="2D6A8F",
    accent="5E9BC0",
    body_text="1E293B",
    light_text="94A3B8",

    table_header_bg="1C3748",
    table_header_text="E2EEF7",
    table_stripe_bg="F0F5F9",
    table_border="B0CCDE",
    table_grid="D4E6F1",

    code_bg="F0F5F9",
    code_text="1C3748",
    code_border="B0CCDE",

    callout=CalloutColors(
        info_bg="E8F4FD", info_border="2D6A8F",
        warning_bg="FFF8E7", warning_border="B08500",
        danger_bg="FDE8E8", danger_border="C0392B",
        success_bg="E8F8F0", success_border="1E8449",
    ),

    chart_palette=[
        "#1C3748", "#2D6A8F", "#3A7EAB", "#5E9BC0",
        "#88B8D5", "#B0CCDE", "#D4E6F1",
    ],

    h1_bold=True, h2_bold=True, h3_bold=False, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="5E9BC0",

    h1_space_before=20, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=2,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=6,
    body_line_spacing=1.2,
))
