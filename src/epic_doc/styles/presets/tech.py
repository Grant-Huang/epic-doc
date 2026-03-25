"""Tech — 极客深空：深色底调配青蓝荧光，IT 架构文档与技术报告的赛博美学。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

TECH = register_theme(Theme(
    name="tech",
    display_name="极客深空 Tech",
    description=(
        "深邃的暗色调配以科技感的青蓝荧光，赛博美学风格。"
        "适用于 IT 架构文档、技术报告、DevOps 文档。"
    ),

    heading_font="Arial",
    body_font="Arial",
    mono_font="Consolas",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="075985",
    secondary="0369A1",
    accent="06B6D4",
    body_text="0F172A",
    light_text="475569",

    table_header_bg="0F172A",
    table_header_text="22D3EE",
    table_stripe_bg="F0F9FF",
    table_border="38BDF8",
    table_grid="BAE6FD",

    code_bg="0F172A",
    code_text="22D3EE",
    code_border="0369A1",

    callout=CalloutColors(
        info_bg="E0F2FE", info_border="0284C7",
        warning_bg="FEF3C7", warning_border="B45309",
        danger_bg="FEE2E2", danger_border="B91C1C",
        success_bg="DCFCE7", success_border="15803D",
    ),

    chart_palette=[
        "#0F172A", "#075985", "#0369A1", "#06B6D4",
        "#22D3EE", "#7C3AED", "#8B5CF6",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="06B6D4",

    h1_space_before=18, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
