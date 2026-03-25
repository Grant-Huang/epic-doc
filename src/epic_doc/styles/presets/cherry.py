"""Cherry — 樱花雅粉：日系清新粉红，品牌手册与活动策划的柔美之选。"""
from epic_doc.styles.theme import CalloutColors, Theme, register_theme

CHERRY = register_theme(Theme(
    name="cherry",
    display_name="樱花雅粉 Cherry",
    description="日系樱花般的粉红色系，清新而不失精致。适用于品牌手册、活动策划、时尚/美妆行业报告。",

    heading_font="Arial",
    body_font="Arial",
    mono_font="Courier New",

    h1_size=22,
    h2_size=16,
    h3_size=13,
    h4_size=12,
    body_size=11,
    caption_size=9,
    code_size=10,

    primary="881337",
    secondary="BE185D",
    accent="E11D48",
    body_text="1C0010",
    light_text="9F1239",

    table_header_bg="881337",
    table_header_text="FFE4E6",
    table_stripe_bg="FFF1F2",
    table_border="FDA4AF",
    table_grid="FECDD3",

    code_bg="FFF1F2",
    code_text="881337",
    code_border="FB7185",

    callout=CalloutColors(
        info_bg="FFF1F2", info_border="E11D48",
        warning_bg="FFFBEB", warning_border="D97706",
        danger_bg="FEE2E2", danger_border="DC2626",
        success_bg="F0FDF4", success_border="15803D",
    ),

    chart_palette=[
        "#881337", "#9F1239", "#BE185D", "#DB2777",
        "#EC4899", "#F472B6", "#FBCFE8",
    ],

    h1_bold=True, h2_bold=True, h3_bold=True, h4_bold=False,
    h1_italic=False, h2_italic=False, h3_italic=False,
    h1_caps=False, h2_caps=False,
    h1_border=True, h1_border_color="FB7185",

    h1_space_before=18, h1_space_after=6,
    h2_space_before=14, h2_space_after=4,
    h3_space_before=10, h3_space_after=3,
    h4_space_before=8,  h4_space_after=2,
    body_space_before=0, body_space_after=8,
    body_line_spacing=1.15,
))
