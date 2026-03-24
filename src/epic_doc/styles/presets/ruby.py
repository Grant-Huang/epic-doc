"""Ruby — 宝石红金：深红与暗金交织，法律合规文档与金融报告的权威气场。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

RUBY = register_theme(Theme(
    name="ruby",
    display_name="宝石红金 Ruby",
    description="深红与暗金色调的权威组合，尊贵且富有力量感。适用于法律合规文档、金融年报、政府报告。",

    heading_font="Times New Roman",
    body_font="Calibri",
    mono_font="Courier New",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="7F1D1D",
    secondary="991B1B",
    accent="B91C1C",
    body_text="1C0606",
    light_text="78716C",

    table_header_bg="7F1D1D",
    table_header_text="FEF2F2",
    table_stripe_bg="FEF2F2",
    table_border="FECACA",
    table_grid="FEE2E2",

    code_bg="FEF2F2",
    code_text="450A0A",
    code_border="FCA5A5",

    callout=CalloutColors(
        info_bg="FEF2F2", info_border="B91C1C",
        warning_bg="FFFBEB", warning_border="B45309",
        danger_bg="FEE2E2", danger_border="7F1D1D",
        success_bg="F0FDF4", success_border="166534",
    ),

    chart_palette=[
        "#7F1D1D", "#991B1B", "#B91C1C", "#DC2626",
        "#B45309", "#D97706", "#F59E0B",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=True, h2_caps=False,
    h1_border=True, h1_border_color="B91C1C",

    h1_space_before=20, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
