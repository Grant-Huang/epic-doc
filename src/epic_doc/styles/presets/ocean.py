"""Ocean — 海洋深邃：蓝绿渐变色系，科研报告、数据分析的视觉利器。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

OCEAN = register_theme(Theme(
    name="ocean",
    display_name="海洋深邃 Ocean",
    description="深邃的蓝绿色系，层次感强。适用于科研报告、数据分析报告、金融报告。",

    heading_font="Calibri",
    body_font="Calibri",
    mono_font="Courier New",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="0C4A6E",
    secondary="0369A1",
    accent="0891B2",
    body_text="164E63",
    light_text="6B7280",

    table_header_bg="0C4A6E",
    table_header_text="FFFFFF",
    table_stripe_bg="F0F9FF",
    table_border="7DD3FC",
    table_grid="BAE6FD",

    code_bg="ECFEFF",
    code_text="0C4A6E",
    code_border="67E8F9",

    callout=CalloutColors(
        info_bg="E0F2FE", info_border="0369A1",
        warning_bg="FEF9C3", warning_border="CA8A04",
        danger_bg="FEE2E2", danger_border="DC2626",
        success_bg="DCFCE7", success_border="15803D",
    ),

    chart_palette=[
        "#0C4A6E", "#0369A1", "#0891B2", "#06B6D4",
        "#22D3EE", "#155E75", "#0E7490",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="0891B2",

    h1_space_before=18, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
