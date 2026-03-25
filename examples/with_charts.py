"""Example: Data analysis report with multiple chart types — 'ocean' theme."""
from epic_doc import EpicDoc

doc = EpicDoc(theme="ocean")

doc.set_metadata(title="市场数据分析报告 Q4 2026", author="Data Team")
doc.set_header("市场数据分析报告 Q4 2026", align="center")
doc.set_footer(page_number=True)

doc.add_heading("市场数据分析报告", level=1)
doc.add_heading("2026 年第四季度", level=2)
doc.add_paragraph("本报告基于 2026 年 Q4 真实业务数据，涵盖收入、用户增长、市场份额等核心维度。")

doc.add_horizontal_rule()

# ── Revenue bar chart ─────────────────────────────────────────────────────────
doc.add_heading("营收表现", level=2)
doc.add_chart(
    chart_type="bar",
    data={"1月": 420, "2月": 380, "3月": 510, "4月": 480, "5月": 560, "6月": 620,
          "7月": 590, "8月": 680, "9月": 720, "10月": 810, "11月": 890, "12月": 950},
    title="2026 年各月营收（万元）",
    ylabel="营收（万元）",
    show_values=False,
    show_grid=True,
    width=6.0,
    height=3.2,
    caption="图 1：2026 全年月度营收走势",
)

# ── Multi-series line chart ───────────────────────────────────────────────────
doc.add_heading("收入与利润对比", level=2)
doc.add_chart(
    chart_type="line",
    data={
        "营收（万元）": {"Q1": 1310, "Q2": 1660, "Q3": 1990, "Q4": 2650},
        "利润（万元）": {"Q1": 393,  "Q2": 498,  "Q3": 597,  "Q4": 795 },
        "研发投入（万元）": {"Q1": 236, "Q2": 299, "Q3": 358, "Q4": 477},
    },
    title="季度收入 / 利润 / 研发投入趋势",
    ylabel="金额（万元）",
    legend=True,
    width=6.0,
    height=3.2,
    caption="图 2：多指标季度趋势对比",
)

doc.add_page_break()

# ── Pie chart ─────────────────────────────────────────────────────────────────
doc.add_heading("市场份额分布", level=2)
doc.add_chart(
    chart_type="pie",
    data={
        "我司":   35.2,
        "竞争对手A": 28.6,
        "竞争对手B": 18.4,
        "竞争对手C": 11.3,
        "其他":   6.5,
    },
    title="Q4 2026 市场份额占比",
    width=4.5,
    height=3.5,
    caption="图 3：行业市场份额分布",
)

# ── Area chart ────────────────────────────────────────────────────────────────
doc.add_heading("用户增长趋势", level=2)
doc.add_chart(
    chart_type="area",
    data={
        "活跃用户（万）":   {"Q1 23": 180, "Q2 23": 210, "Q3 23": 248, "Q4 23": 290,
                            "Q1 24": 320, "Q2 24": 368, "Q3 24": 415, "Q4 24": 500},
        "付费用户（万）":   {"Q1 23": 54,  "Q2 23": 67,  "Q3 23": 82,  "Q4 23": 98,
                            "Q1 24": 112, "Q2 24": 134, "Q3 24": 156, "Q4 24": 186},
    },
    title="用户规模双年增长趋势",
    ylabel="用户数（万）",
    width=6.0,
    height=3.0,
    caption="图 4：2023–2024 年用户增长面积图",
)

# ── Horizontal bar ────────────────────────────────────────────────────────────
doc.add_heading("地区营收排名", level=2)
doc.add_chart(
    chart_type="hbar",
    data={
        "华东大区": 4200,
        "华南大区": 3100,
        "华北大区": 2800,
        "西南大区": 1600,
        "西北大区": 900,
        "海外":     1200,
    },
    title="2026 年各大区营收（万元）",
    xlabel="营收（万元）",
    show_values=True,
    width=5.5,
    height=3.0,
    caption="图 5：区域营收水平对比",
)

# ── Combo chart ───────────────────────────────────────────────────────────────
doc.add_page_break()
doc.add_heading("营收与增速组合图", level=2)
doc.add_chart(
    chart_type="combo",
    data={
        "营收（万元）": {"Q1": 1310, "Q2": 1660, "Q3": 1990, "Q4": 2650},
        "同比增速（%）": {"Q1": 18.2, "Q2": 22.5, "Q3": 26.8, "Q4": 33.2},
    },
    title="季度营收（柱）与增速（线）组合",
    caption="图 6：Combo 图 — 柱状图+折线图叠加",
    width=6.0,
    height=3.2,
)

doc.add_heading("数据摘要", level=2)
doc.add_table(
    data=[
        ["维度",     "Q1",    "Q2",    "Q3",    "Q4",    "全年"],
        ["营收（万）", 1310,    1660,    1990,    2650,    7610 ],
        ["利润（万）", 393,     498,     597,     795,     2283 ],
        ["利润率",   "30%",   "30%",   "30%",   "30%",   "30%"],
        ["用户（万）", 320,     368,     415,     500,     "-"  ],
        ["增速",     "18.2%", "22.5%", "26.8%", "33.2%", "26.2%"],
    ],
    headers=True,
    style="striped",
    caption="表 1：2026 全年季度数据汇总",
)

doc.save("output_with_charts.docx")
print("✓ output_with_charts.docx")
