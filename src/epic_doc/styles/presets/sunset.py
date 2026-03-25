"""Sunset — 暖橙日落：热情活力的橙红色系，营销报告、创意方案的视觉冲击力担当。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

SUNSET = register_theme(Theme(
    name="sunset",
    display_name="暖橙日落 Sunset",
    description="日落时分的橙红渐变，热情而充满活力。适用于营销报告、创意提案、消费品行业分析。",

    heading_font="Calibri",
    body_font="Calibri",
    mono_font="Courier New",

    h1_size=23,
    h2_size=17,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="7C2D12",
    secondary="C2410C",
    accent="EA580C",
    body_text="1C0A00",
    light_text="78716C",

    table_header_bg="7C2D12",
    table_header_text="FFFFFF",
    table_stripe_bg="FFF7ED",
    table_border="FED7AA",
    table_grid="FDBA74",

    code_bg="FFF7ED",
    code_text="431407",
    code_border="FB923C",

    callout=CalloutColors(
        info_bg="FFF7ED", info_border="EA580C",
        warning_bg="FFFBEB", warning_border="D97706",
        danger_bg="FEF2F2", danger_border="DC2626",
        success_bg="ECFDF5", success_border="059669",
    ),

    chart_palette=[
        "#7C2D12", "#9A3412", "#C2410C", "#EA580C",
        "#F97316", "#FB923C", "#FDBA74",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="EA580C",

    h1_space_before=18, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
