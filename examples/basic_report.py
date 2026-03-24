"""Example: Basic business report using the 'professional' theme."""
from epic_doc import EpicDoc

doc = EpicDoc(theme="professional")

doc.set_metadata(title="2026 年度业务报告", author="Grant Huang", subject="Business Report")
doc.set_header("2026 年度业务报告  |  机密", align="right")
doc.set_footer(text="© 2026 Grant Inc.", page_number=True)

doc.add_toc(title="目录", depth=3)
doc.add_page_break()

# ── Executive Summary ─────────────────────────────────────────────────────────
doc.add_heading("执行摘要", level=1)
doc.add_paragraph(
    "2026 年度，公司整体营收同比增长 24%，达到 1.38 亿元人民币。各业务线均取得阶段性突破，"
    "研发投入占比提升至 18%，用户规模突破 500 万。本报告将对全年业务进行系统性复盘，"
    "并对未来一年的战略方向提出建议。",
    align="justify",
)

doc.add_callout(
    "本报告中所有数据均为模拟示例，仅用于展示 epic-doc 的文档生成能力。",
    style="warning",
    title="免责声明",
)

# ── Key Metrics ───────────────────────────────────────────────────────────────
doc.add_heading("核心指标", level=2)
doc.add_table(
    data=[
        ["指标",         "2025 年",   "2026 年",   "同比增长"],
        ["总营收（万元）", "11,200",    "13,800",    "+23.2%"],
        ["净利润（万元）", "1,680",     "2,208",     "+31.4%"],
        ["活跃用户（万）", "320",       "500",       "+56.3%"],
        ["员工总数",      "1,240",     "1,680",     "+35.5%"],
        ["研发投入占比",  "14%",       "18%",       "+4 pp"],
    ],
    headers=True,
    style="striped",
    col_widths=[3.2, 1.4, 1.4, 1.2],
    caption="表 1：2026 年度核心指标对比",
)

# ── Business Lines ────────────────────────────────────────────────────────────
doc.add_heading("业务线概述", level=1)

doc.add_heading("SaaS 平台", level=2)
doc.add_paragraph(
    "SaaS 平台全年 ARR 突破 8,000 万元，付费客户数量增至 12,400 家。"
    "产品在企业级市场获得广泛认可，NPS 评分达到 72 分。"
)
doc.add_list(
    [
        "新增核心功能 47 项，产品迭代周期压缩至 2 周",
        "企业客户平均合同价值（ACV）同比提升 18%",
        "客户留存率维持在 94% 的历史高位",
        "移动端 DAU 增长 120%",
    ],
    style="bullet",
)

doc.add_heading("数据服务", level=2)
doc.add_paragraph(
    "数据服务业务线实现营收 3,200 万元，较上年增长 38%。"
    "依托自研数据中台，平均数据处理延迟降低至 85ms。"
)

doc.add_heading("咨询与实施", level=2)
doc.add_paragraph(
    "咨询业务完成大型实施项目 34 个，平均项目周期从 6 个月缩短至 4.2 个月，"
    "客户满意度评分为 4.7/5.0。"
)

# ── Financials ────────────────────────────────────────────────────────────────
doc.add_page_break()
doc.add_heading("财务数据", level=1)

doc.add_heading("季度营收", level=2)
doc.add_table(
    data=[
        ["业务线",    "Q1",    "Q2",    "Q3",    "Q4",    "全年合计"],
        ["SaaS 平台", 1800,    1950,    2100,    2150,    8000   ],
        ["数据服务",  650,     760,     840,     950,     3200   ],
        ["咨询实施",  480,     560,     620,     640,     2300   ],
        ["其他",      60,      70,      80,      90,      300    ],
        ["合计",      2990,    3340,    3640,    3830,    13800  ],
    ],
    headers=True,
    style="grid",
    merge=[(5, 0, 5, 0)],
    col_widths=[2.2, 1.0, 1.0, 1.0, 1.0, 1.2],
    caption="表 2：各业务线季度营收（万元）",
)

doc.add_heading("费用结构", level=2)
doc.add_table(
    data=[
        ["费用类别",  "金额（万元）", "占营收比"],
        ["销售费用",  2,346,         "17.0%"],
        ["研发投入",  2,484,         "18.0%"],
        ["管理费用",  828,           "6.0%"],
        ["市场推广",  1,104,         "8.0%"],
        ["其他费用",  829,           "6.0%"],
    ],
    headers=True,
    style="bordered",
    caption="表 3：2026 年度费用结构",
)

# ── Outlook ───────────────────────────────────────────────────────────────────
doc.add_heading("2027 年展望", level=1)
doc.add_paragraph(
    "展望 2027 年，公司将继续聚焦核心产品打磨与市场渗透，"
    "预计全年营收目标为 1.8 亿元，同比增长 30%。",
    align="justify",
)
doc.add_list(
    [
        "完成 B 轮融资，目标融资规模 5,000 万美元",
        "进入东南亚市场，建立本地化运营团队",
        "推出 AI 原生产品线，抢占智能化转型市场",
        "完善数据安全合规体系，通过 ISO 27001 认证",
    ],
    style="numbered",
)

doc.add_callout(
    "上述预测基于当前市场环境及公司内部规划，实际结果可能因市场变化而存在差异。",
    style="info",
)

doc.save("output_basic_report.docx")
print("✓ output_basic_report.docx")
