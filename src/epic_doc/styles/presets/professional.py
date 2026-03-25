"""Professional — 商务深蓝：企业年报、商业提案的首选。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

PROFESSIONAL = register_theme(Theme(
    name="professional",
    display_name="商务深蓝 Professional",
    description="经典深海蓝配色，适用于企业年报、商业提案、投资分析等正式场合。",

    heading_font="Arial",
    body_font="Arial",
    mono_font="Courier New",
    heading_font_cjk="楷体",
    body_font_cjk="楷体",
    mono_font_cjk="楷体",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="1E3A5F",
    secondary="1D4ED8",
    accent="0369A1",
    body_text="1F2937",
    light_text="6B7280",

    table_header_bg="1E3A5F",
    table_header_text="FFFFFF",
    table_stripe_bg="EFF6FF",
    table_border="93C5FD",
    table_grid="BFDBFE",

    code_bg="F1F5F9",
    code_text="0F172A",
    code_border="94A3B8",

    callout=CalloutColors(
        info_bg="DBEAFE", info_border="2563EB",
        warning_bg="FEF3C7", warning_border="D97706",
        danger_bg="FEE2E2", danger_border="DC2626",
        success_bg="DCFCE7", success_border="16A34A",
    ),

    chart_palette=[
        "#1D4ED8", "#0369A1", "#0891B2", "#0E7490",
        "#1E40AF", "#1E3A5F", "#64748B",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=True,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="0369A1",

    h1_space_before=18, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
