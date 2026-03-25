"""Example: Technical architecture document with flowcharts — 'tech' theme."""
from epic_doc import EpicDoc

doc = EpicDoc(theme="tech")

doc.set_metadata(title="系统架构设计文档 v2.0", author="Architecture Team")
doc.set_header("系统架构设计文档 v2.0  |  内部机密", align="right")
doc.set_footer(text="Architecture Team", page_number=True)

doc.add_heading("系统架构设计文档", level=1)
doc.add_heading("版本 2.0  |  2026-03", level=2)

doc.add_callout(
    "本文档描述平台核心服务的架构设计，包含请求处理流程、数据流向及关键决策节点。",
    style="info",
    title="文档说明",
)

# ── Request processing flow ───────────────────────────────────────────────────
doc.add_heading("请求处理流程", level=2)
doc.add_paragraph("所有 API 请求经过统一网关层后，按照以下流程进行处理：")

doc.add_flowchart(
    nodes={
        "client":    {"label": "客户端请求",   "shape": "oval"},
        "gateway":   {"label": "API Gateway", "shape": "box"},
        "auth":      {"label": "认证授权",     "shape": "diamond"},
        "ratelimit": {"label": "限流检查",     "shape": "diamond"},
        "router":    {"label": "路由分发",     "shape": "box"},
        "service_a": {"label": "用户服务",     "shape": "box"},
        "service_b": {"label": "数据服务",     "shape": "box"},
        "service_c": {"label": "消息服务",     "shape": "box"},
        "cache":     {"label": "Redis 缓存",   "shape": "cylinder"},
        "db":        {"label": "数据库集群",   "shape": "cylinder"},
        "response":  {"label": "返回响应",     "shape": "oval"},
        "reject":    {"label": "拒绝请求",     "shape": "oval", "color": "DC2626"},
    },
    edges=[
        ("client",    "gateway"),
        ("gateway",   "auth"),
        ("auth",      "ratelimit", {"label": "通过"}),
        ("auth",      "reject",    {"label": "未授权", "style": "dashed"}),
        ("ratelimit", "router",    {"label": "通过"}),
        ("ratelimit", "reject",    {"label": "超限", "style": "dashed"}),
        ("router",    "service_a", {"label": "/user/*"}),
        ("router",    "service_b", {"label": "/data/*"}),
        ("router",    "service_c", {"label": "/msg/*"}),
        ("service_a", "cache"),
        ("service_b", "db"),
        ("cache",     "response"),
        ("db",        "response"),
        ("service_c", "response"),
    ],
    direction="TB",
    width=5.5,
    caption="图 1：API 请求处理全流程",
)

doc.add_page_break()

# ── Data pipeline flow ────────────────────────────────────────────────────────
doc.add_heading("数据处理管道", level=2)
doc.add_paragraph("实时数据从采集到入库的完整处理链路如下：")

doc.add_flowchart(
    nodes={
        "source":   {"label": "数据源\n(IoT/日志/API)", "shape": "oval"},
        "ingest":   {"label": "数据采集层\nKafka",       "shape": "box"},
        "validate": {"label": "数据校验",               "shape": "diamond"},
        "enrich":   {"label": "数据清洗增强",            "shape": "box"},
        "stream":   {"label": "实时计算\nFlink",         "shape": "box"},
        "batch":    {"label": "批量处理\nSpark",         "shape": "box"},
        "dw":       {"label": "数据仓库\nClickHouse",    "shape": "cylinder"},
        "datalake": {"label": "数据湖\nHDFS/S3",         "shape": "cylinder"},
        "api":      {"label": "查询 API 层",             "shape": "box"},
        "discard":  {"label": "数据丢弃\n+告警",          "shape": "box", "color": "DC2626"},
        "bi":       {"label": "BI 分析平台",             "shape": "oval"},
    },
    edges=[
        ("source",   "ingest"),
        ("ingest",   "validate"),
        ("validate", "enrich",  {"label": "有效"}),
        ("validate", "discard", {"label": "无效", "style": "dashed"}),
        ("enrich",   "stream"),
        ("enrich",   "batch"),
        ("stream",   "dw"),
        ("batch",    "datalake"),
        ("dw",       "api"),
        ("datalake", "api"),
        ("api",      "bi"),
    ],
    direction="LR",
    width=6.2,
    caption="图 2：实时数据处理管道（从左至右）",
)

# ── Deployment topology ───────────────────────────────────────────────────────
doc.add_heading("部署拓扑", level=2)
doc.add_paragraph("生产环境采用多可用区（AZ）部署，实现高可用和故障容错：")

doc.add_flowchart(
    nodes={
        "lb":      {"label": "负载均衡\nNGINX",    "shape": "box"},
        "az1":     {"label": "可用区 A",            "shape": "box"},
        "az2":     {"label": "可用区 B",            "shape": "box"},
        "az3":     {"label": "可用区 C",            "shape": "box"},
        "pod1a":   {"label": "Pod×3\nAPI Server",  "shape": "box"},
        "pod1b":   {"label": "Pod×2\nWorker",      "shape": "box"},
        "pod2a":   {"label": "Pod×3\nAPI Server",  "shape": "box"},
        "pod2b":   {"label": "Pod×2\nWorker",      "shape": "box"},
        "pod3a":   {"label": "Pod×3\nAPI Server",  "shape": "box"},
        "db_m":    {"label": "DB 主节点",           "shape": "cylinder"},
        "db_s1":   {"label": "DB 从节点 1",         "shape": "cylinder"},
        "db_s2":   {"label": "DB 从节点 2",         "shape": "cylinder"},
    },
    edges=[
        ("lb",   "az1"),
        ("lb",   "az2"),
        ("lb",   "az3"),
        ("az1",  "pod1a"),
        ("az1",  "pod1b"),
        ("az2",  "pod2a"),
        ("az2",  "pod2b"),
        ("az3",  "pod3a"),
        ("pod1a", "db_m"),
        ("pod2a", "db_m"),
        ("pod3a", "db_m"),
        ("db_m",  "db_s1", {"label": "主从同步"}),
        ("db_m",  "db_s2", {"label": "主从同步"}),
    ],
    direction="TB",
    width=5.5,
    caption="图 3：多可用区部署拓扑",
)

# ── Tech stack table ──────────────────────────────────────────────────────────
doc.add_page_break()
doc.add_heading("技术栈总览", level=2)
doc.add_table(
    data=[
        ["层级",     "组件",              "版本",    "用途"],
        ["接入层",   "NGINX",             "1.24",   "负载均衡 / SSL 卸载"],
        ["API 层",   "FastAPI",           "0.111",  "RESTful API / WebSocket"],
        ["缓存",     "Redis Cluster",     "7.2",    "热数据缓存 / 会话"],
        ["消息队列", "Apache Kafka",      "3.6",    "异步消息 / 事件驱动"],
        ["数据库",   "PostgreSQL",        "16",     "主业务数据"],
        ["数据仓库", "ClickHouse",        "24.1",   "OLAP 分析查询"],
        ["流计算",   "Apache Flink",      "1.18",   "实时数据处理"],
        ["搜索",     "Elasticsearch",     "8.12",   "全文检索 / 日志"],
        ["容器编排", "Kubernetes",        "1.29",   "服务部署 / 弹性伸缩"],
        ["监控",     "Prometheus+Grafana","latest", "指标监控 / 告警"],
    ],
    headers=True,
    style="striped",
    col_widths=[1.4, 1.8, 1.0, 2.5],
    caption="表 1：技术栈组件清单",
)

doc.add_heading("核心 API 示例", level=2)
doc.add_code_block(
    """# 创建文档 API
POST /api/v2/documents
Authorization: Bearer <token>
Content-Type: application/json

{
  "theme": "tech",
  "meta": {"title": "架构报告"},
  "blocks": [
    {"type": "heading", "text": "系统架构", "level": 1},
    {"type": "flowchart",
     "nodes": {"a": "开始", "b": "处理", "c": "结束"},
     "edges": [["a","b"],["b","c"]]}
  ]
}""",
    language="http",
)

doc.save("output_with_flowchart.docx")
print("✓ output_with_flowchart.docx")
