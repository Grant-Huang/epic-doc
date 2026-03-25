"""Academic — 学术棕米：温暖的大地色调，学术论文与研究报告的庄重之选。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

ACADEMIC = register_theme(Theme(
    name="academic",
    display_name="学术棕米 Academic",
    description="温暖的棕色与米色基调，庄重而不失温度。适用于学术论文、研究报告、白皮书、行业调研。",

    heading_font="Times New Roman",
    body_font="Times New Roman",
    mono_font="Courier New",

    h1_size=20,
    h2_size=15,
    h3_size=12,
    h4_size=11,
    body_size=12,
    caption_size=10,
    code_size=10,

    primary="44403C",
    secondary="78716C",
    accent="B45309",
    body_text="1C1917",
    light_text="A8A29E",

    table_header_bg="44403C",
    table_header_text="FAFAF9",
    table_stripe_bg="FAFAF9",
    table_border="D6D3D1",
    table_grid="E7E5E4",

    code_bg="FAFAF9",
    code_text="292524",
    code_border="D6D3D1",

    callout=CalloutColors(
        info_bg="FEF3C7", info_border="B45309",
        warning_bg="FFFBEB", warning_border="D97706",
        danger_bg="FEF2F2", danger_border="991B1B",
        success_bg="ECFDF5", success_border="065F46",
    ),

    chart_palette=[
        "#44403C", "#78716C", "#B45309", "#D97706",
        "#78350F", "#92400E", "#A8A29E",
    ],

    h1_bold=True, h2_bold=True, h3_bold=False, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=True,
    h1_caps=False, h2_caps=False,
    h1_border=False, h1_border_color=None,

    h1_space_before=24, h1_space_after=8,
    h2_space_before=18, h2_space_after=6,
    h3_space_before=12, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=10,
    body_line_spacing=1.5,
))
