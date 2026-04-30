"""
Adviava ED AI Agent — AWS Deployment Architecture PDF
Generates: Adviava_ED_AI_Agent_AWS_Deployment.pdf
"""
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Polygon, Circle, Group,
)
from reportlab.lib.colors import HexColor

# ── Colour palette ─────────────────────────────────────────────────────────────
AWS_INK    = HexColor("#232F3E")   # AWS Squid Ink
AWS_ORG    = HexColor("#FF9900")   # AWS Orange
AWS_BLU    = HexColor("#4285F4")   # Internet / traffic
EC2_CLR    = HexColor("#F58534")   # EC2 compute
VPC_CLR    = HexColor("#8C4FFF")   # VPC purple
SG_CLR     = HexColor("#DD344C")   # Security group red
IGW_CLR    = HexColor("#1A9C3E")   # Internet gateway green
S3_CLR     = HexColor("#3F8624")   # Storage green

NAVY       = HexColor("#0D2B4E")   # Adviava navy
TEAL       = HexColor("#007C91")   # Adviava teal
GOLD       = HexColor("#D4A017")   # Adviava gold
MID_GREY   = HexColor("#4A5568")
LIGHT_BG   = HexColor("#F7FAFC")
RULE       = HexColor("#CBD5E0")
WHITE      = colors.white
BLACK      = colors.black

W, H = A4
MARGIN = 18 * mm
CW = W - 2 * MARGIN   # content width

# ── Styles ─────────────────────────────────────────────────────────────────────
def styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)
    return {
        "cover_eye":  S("ce", fontName="Helvetica", fontSize=10, textColor=HexColor("#90A8C8"),
                         letterSpacing=2, spaceBefore=0, spaceAfter=4, alignment=TA_LEFT),
        "cover_h1":   S("ch1", fontName="Helvetica-Bold", fontSize=32, textColor=WHITE,
                         leading=40, spaceAfter=6, alignment=TA_LEFT),
        "cover_sub":  S("cs", fontName="Helvetica", fontSize=14, textColor=HexColor("#B0C8D8"),
                         leading=20, spaceAfter=4, alignment=TA_LEFT),
        "cover_org":  S("co", fontName="Helvetica-Bold", fontSize=12, textColor=GOLD,
                         leading=16, alignment=TA_LEFT),
        "cover_date": S("cd", fontName="Helvetica", fontSize=9, textColor=HexColor("#90A8B8"),
                         alignment=TA_LEFT),
        "h1":   S("h1", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
                   spaceBefore=16, spaceAfter=6, leading=22),
        "h2":   S("h2", fontName="Helvetica-Bold", fontSize=12, textColor=TEAL,
                   spaceBefore=12, spaceAfter=4, leading=16),
        "h3":   S("h3", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
                   spaceBefore=8, spaceAfter=3, leading=14),
        "body": S("body", fontName="Helvetica", fontSize=9.5, textColor=MID_GREY,
                   leading=15, spaceAfter=4, alignment=TA_JUSTIFY),
        "mono": S("mono", fontName="Courier", fontSize=8.5, textColor=NAVY,
                   leading=13, spaceAfter=2, leftIndent=12, backColor=HexColor("#F0F4F8")),
        "bullet": S("bullet", fontName="Helvetica", fontSize=9.5, textColor=MID_GREY,
                     leading=15, leftIndent=14, bulletIndent=4, spaceAfter=2),
        "th":   S("th", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE,
                   alignment=TA_CENTER, leading=12),
        "td":   S("td", fontName="Helvetica", fontSize=8.5, textColor=MID_GREY,
                   alignment=TA_LEFT, leading=13),
        "td_b": S("td_b", fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY,
                   alignment=TA_LEFT, leading=13),
        "td_m": S("td_m", fontName="Courier", fontSize=8, textColor=TEAL,
                   alignment=TA_LEFT, leading=13),
        "cap":  S("cap", fontName="Helvetica-Oblique", fontSize=8, textColor=MID_GREY,
                   alignment=TA_CENTER, spaceAfter=8),
        "footer": S("ft", fontName="Helvetica", fontSize=7.5,
                     textColor=HexColor("#8090A0"), alignment=TA_CENTER),
        "callout": S("call", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
                      alignment=TA_CENTER, leading=15),
    }


# ── Page backgrounds ────────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AWS_INK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(AWS_ORG)
    canvas.rect(0, 0, W, 16*mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#1A2535"))
    canvas.rect(W - 60*mm, 0, 60*mm, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)
    canvas.setStrokeColor(HexColor("#2A3F55"))
    canvas.setLineWidth(0.4)
    for i in range(0, int(H) + 200, 36):
        canvas.line(W - 60*mm, i, W, i - 60*mm)
    canvas.restoreState()


def inner_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AWS_INK)
    canvas.rect(0, H - 14*mm, W, 14*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(HexColor("#90A8C8"))
    canvas.drawString(MARGIN, H - 9*mm, "ADVIAVA REGIONAL MEDICAL CENTER")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#607080"))
    canvas.drawRightString(W - MARGIN, H - 9*mm, "AWS Deployment Architecture")
    canvas.setFillColor(AWS_ORG)
    canvas.rect(0, 0, 3*mm, H - 14*mm, fill=1, stroke=0)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12*mm, W - MARGIN, 12*mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#8090A0"))
    canvas.drawString(MARGIN, 7*mm,
        "Adviava Regional Medical Center  |  ED AI Agent  |  AWS Deployment Reference")
    canvas.drawRightString(W - MARGIN, 7*mm, f"Page {doc.page}")
    canvas.restoreState()


def sp(n=6): return Spacer(1, n)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=4, spaceBefore=4)
def P(text, S, style="body"): return Paragraph(text, S[style])
def bul(text, S): return Paragraph(f"• {text}", S["bullet"])


def data_table(headers, rows, S, col_widths=None, header_color=None):
    hc = header_color or TEAL
    data = [[Paragraph(h, S["th"]) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), S["td_b"] if j == 0 else S["td"])
                     for j, c in enumerate(row)])
    if not col_widths:
        col_widths = [CW / len(headers)] * len(headers)
    ts = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  hc),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.2, hc),
    ])
    return Table(data, colWidths=col_widths, style=ts, hAlign="LEFT")


def mono_table(rows, S, col_widths=None):
    data = [[Paragraph(str(c), S["td_b"] if j == 0 else S["td_m"])
             for j, c in enumerate(row)]
            for row in rows]
    if not col_widths:
        col_widths = [CW * 0.38, CW * 0.62]
    ts = TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [HexColor("#F0F4F8"), WHITE]),
        ("GRID",           (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
        ("LEFTPADDING",    (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 7),
        ("LINEAFTER",      (0, 0), (0, -1), 1, RULE),
    ])
    return Table(data, colWidths=col_widths, style=ts, hAlign="LEFT")


# ═══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM DRAWABLES
# ═══════════════════════════════════════════════════════════════════════════════

class AwsBox(Flowable):
    """Generic AWS service box: rounded rect + icon label + title."""
    def __init__(self, title, subtitle="", color=TEAL, w=80, h=50, icon=""):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.color = color
        self.width = w
        self.height = h
        self.icon = icon

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        tw = c.stringWidth(self.title, "Helvetica-Bold", 8)
        c.drawString((self.width - tw) / 2, self.height / 2 - 2, self.title)
        if self.subtitle:
            c.setFont("Helvetica", 6.5)
            sw = c.stringWidth(self.subtitle, "Helvetica", 6.5)
            c.setFillColor(HexColor("#FFFFFF99") if True else WHITE)
            c.drawString((self.width - sw) / 2, self.height / 2 - 13, self.subtitle)


# ── Diagram 1: High-Level AWS Architecture ─────────────────────────────────────
def make_aws_arch(cw):
    dw, dh = cw, 200
    d = Drawing(dw, dh)

    def box(x, y, w, h, fill, label, sub="", lbl_size=8):
        d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=WHITE,
                   strokeWidth=1.2, rx=5, ry=5))
        tw = len(label) * lbl_size * 0.55
        d.add(String(x + w/2 - tw/2, y + h/2 + 3, label,
                     fontSize=lbl_size, fontName="Helvetica-Bold", fillColor=WHITE))
        if sub:
            sw = len(sub) * 6.5 * 0.55
            d.add(String(x + w/2 - sw/2, y + h/2 - 10, sub,
                         fontSize=6.5, fontName="Helvetica", fillColor=HexColor("#FFFFFF")))

    def arrow(x1, y1, x2, y2, color=HexColor("#607080")):
        d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.5))
        # arrowhead
        dx, dy = x2 - x1, y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        if length == 0: return
        ux, uy = dx/length, dy/length
        px, py = -uy, ux
        size = 6
        d.add(Polygon([x2, y2,
                        x2 - size*ux + size*0.4*px, y2 - size*uy + size*0.4*py,
                        x2 - size*ux - size*0.4*px, y2 - size*uy - size*0.4*py],
                       fillColor=color, strokeColor=color, strokeWidth=0))

    def label(x, y, text, size=7, color=MID_GREY, bold=False):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        tw = len(text) * size * 0.55
        d.add(String(x - tw/2, y, text, fontSize=size, fontName=fn, fillColor=color))

    # Internet cloud (left)
    d.add(Rect(2, 75, 72, 50, fillColor=AWS_BLU, strokeColor=WHITE,
               strokeWidth=1, rx=20, ry=20))
    d.add(String(38 - 25, 103, "Internet", fontSize=8.5, fontName="Helvetica-Bold",
                 fillColor=WHITE))
    d.add(String(38 - 30, 90, "User Browser", fontSize=7, fontName="Helvetica",
                 fillColor=HexColor("#DDEEFF")))

    # Arrow Internet → IGW
    arrow(74, 100, 108, 100, AWS_ORG)
    label(91, 106, "HTTP :8000", 6.5, AWS_ORG)

    # Internet Gateway box
    box(108, 78, 64, 44, IGW_CLR, "Internet", "Gateway", 7.5)

    # Arrow IGW → SG
    arrow(172, 100, 206, 100, AWS_ORG)

    # VPC outline
    d.add(Rect(200, 14, 290, 172, fillColor=HexColor("#F3EEFF"),
               strokeColor=VPC_CLR, strokeWidth=1.5, strokeDashArray=[4, 3],
               rx=8, ry=8))
    d.add(String(205, 178, "VPC  10.100.0.0/16  |  Region: us-east-2", fontSize=7,
                 fontName="Helvetica-Bold", fillColor=VPC_CLR))

    # Subnet outline
    d.add(Rect(210, 20, 270, 152, fillColor=HexColor("#EEF6FF"),
               strokeColor=HexColor("#4A90D9"), strokeWidth=1,
               strokeDashArray=[3, 2], rx=6, ry=6))
    d.add(String(215, 165, "Public Subnet  10.100.0.0/24  |  AZ: us-east-2a",
                 fontSize=6.5, fontName="Helvetica", fillColor=HexColor("#4A90D9")))

    # Security Group outline
    d.add(Rect(222, 26, 246, 132, fillColor=HexColor("#FFF5F5"),
               strokeColor=SG_CLR, strokeWidth=1, strokeDashArray=[2, 2],
               rx=5, ry=5))
    d.add(String(227, 152, "Security Group  sg-0e349182f9d8c8e03",
                 fontSize=6, fontName="Helvetica", fillColor=SG_CLR))

    # EC2 instance box
    box(238, 58, 214 - 12, 86, EC2_CLR, "EC2  t2.micro", "i-05cef553b3f5ffab7", 8)

    # App stack inside EC2
    app_layers = [
        (248, 110, 90, 14, HexColor("#1A3A2A"), "FastAPI :8000"),
        (248, 94,  90, 14, HexColor("#1A2A3A"), "Uvicorn ASGI"),
        (248, 78,  90, 14, HexColor("#0D2B4E"), "Python 3.11 venv"),
        (248, 62,  90, 14, HexColor("#2D3748"), "Amazon Linux 2023"),
    ]
    for ax, ay, aw, ah, ac, al in app_layers:
        d.add(Rect(ax, ay, aw, ah, fillColor=ac, strokeColor=WHITE,
                   strokeWidth=0.5, rx=2, ry=2))
        tw = len(al) * 6.5 * 0.55
        d.add(String(ax + aw/2 - tw/2, ay + 3, al,
                     fontSize=6.5, fontName="Helvetica", fillColor=WHITE))

    # SQLite DB box
    box(352, 58, 66, 40, HexColor("#1A6B2A"), "SQLite DB", "ed_database.db", 7)

    # Arrow EC2 → SQLite
    arrow(338, 80, 352, 80, HexColor("#2D7A3A"))
    label(345, 86, "SQL", 6.5, HexColor("#2D7A3A"))

    # systemd badge
    d.add(Rect(350, 108, 60, 18, fillColor=AWS_ORG, strokeColor=WHITE,
               strokeWidth=0, rx=4, ry=4))
    d.add(String(355, 115, "systemd service", fontSize=6.5, fontName="Helvetica-Bold",
                 fillColor=WHITE))

    # Port labels
    d.add(Rect(222, 150, 70, 10, fillColor=SG_CLR, strokeColor=WHITE,
               strokeWidth=0, rx=2, ry=2))
    d.add(String(225, 153, "TCP 22  TCP 8000  →  0.0.0.0/0",
                 fontSize=5.8, fontName="Helvetica", fillColor=WHITE))

    # Public IP badge
    d.add(Rect(338, 32, 74, 18, fillColor=NAVY, strokeColor=WHITE,
               strokeWidth=0, rx=4, ry=4))
    d.add(String(342, 39, "Public IP: 18.224.64.93",
                 fontSize=6.5, fontName="Helvetica-Bold", fillColor=GOLD))

    return d


# ── Diagram 2: Application Stack Layers ────────────────────────────────────────
def make_stack_diagram(cw):
    dw, dh = cw, 210
    d = Drawing(dw, dh)

    layers = [
        # (y, h, color, left_label, right_label)
        (186, 20, AWS_BLU,           "BROWSER",            "HTML / CSS / Vanilla JS"),
        (158, 24, IGW_CLR,           "INTERNET",           "HTTP TCP :8000  →  18.224.64.93"),
        (130, 24, SG_CLR,            "SECURITY GROUP",     "sg-0e349182f9d8c8e03  |  Port 8000 open"),
        (102, 24, EC2_CLR,           "EC2  t2.micro",      "1 vCPU · 1 GB RAM · 8 GB EBS · us-east-2a"),
        (74,  24, HexColor("#2D3748"),"AMAZON LINUX 2023", "ami-0cf8dce2cda56aa67"),
        (46,  24, NAVY,              "PYTHON 3.11 VENV",   "/home/ec2-user/pntdigappproj/.venv"),
        (18,  24, TEAL,              "UVICORN + FASTAPI",  "app.main:app  →  0.0.0.0:8000"),
        (0,   14, HexColor("#1A6B2A"),"MCP  +  SQLITE",    "mcp_server/server.py  |  data/ed_database.db"),
    ]

    bar_w = cw * 0.28

    for y, h, col, lbl, detail in layers:
        # coloured bar
        d.add(Rect(0, y, bar_w, h, fillColor=col, strokeColor=WHITE,
                   strokeWidth=0.8, rx=2, ry=2))
        tw = len(lbl) * 7.5 * 0.55
        d.add(String(bar_w/2 - tw/2, y + h/2 - 4, lbl,
                     fontSize=7.5, fontName="Helvetica-Bold", fillColor=WHITE))
        # detail text
        d.add(String(bar_w + 12, y + h/2 - 4, detail,
                     fontSize=8, fontName="Helvetica", fillColor=MID_GREY))
        # connector dot
        if y > 0:
            d.add(Line(bar_w/2, y, bar_w/2, y - 2,
                       strokeColor=HexColor("#CBD5E0"), strokeWidth=1))

    return d


# ── Diagram 3: Request Flow Sequence ───────────────────────────────────────────
def make_request_flow(cw):
    dw, dh = cw, 230
    d = Drawing(dw, dh)

    actors = [
        ("Browser",   16,  AWS_BLU),
        ("EC2\nFastAPI", 115, EC2_CLR),
        ("LangChain\nAgent", 210, NAVY),
        ("MCP\nServer", 305, TEAL),
        ("SQLite\nDB",  400, HexColor("#1A6B2A")),
    ]

    # Actor headers
    for name, x, col in actors:
        d.add(Rect(x - 34, 205, 68, 24, fillColor=col, strokeColor=WHITE,
                   strokeWidth=0.8, rx=4, ry=4))
        lines = name.split("\n")
        for i, ln in enumerate(lines):
            tw = len(ln) * 7 * 0.55
            d.add(String(x - tw/2, 218 - i*10, ln,
                         fontSize=7, fontName="Helvetica-Bold", fillColor=WHITE))
        # lifeline
        d.add(Line(x, 205, x, 0, strokeColor=HexColor("#CBD5E0"),
                   strokeWidth=0.6, strokeDashArray=[3, 2]))

    def msg(y, x1, x2, label, ret=False, col=MID_GREY):
        lx, rx = (x1, x2) if x1 < x2 else (x2, x1)
        if ret:
            d.add(Line(lx, y, rx, y, strokeColor=col, strokeWidth=1,
                       strokeDashArray=[4, 2]))
        else:
            d.add(Line(lx, y, rx, y, strokeColor=col, strokeWidth=1.2))
        # arrowhead
        if x1 < x2:
            ax, ay = rx, y
            d.add(Polygon([ax, ay, ax-7, ay+3, ax-7, ay-3],
                           fillColor=col, strokeColor=col, strokeWidth=0))
        else:
            ax, ay = lx, y
            d.add(Polygon([ax, ay, ax+7, ay+3, ax+7, ay-3],
                           fillColor=col, strokeColor=col, strokeWidth=0))
        tw = len(label) * 6.5 * 0.52
        mx = (x1 + x2) / 2
        d.add(String(mx - tw/2, y + 3, label,
                     fontSize=6.5, fontName="Helvetica", fillColor=col))

    # sequence
    msg(190,  16, 115, "POST /api/chat  {message}", col=AWS_BLU)
    msg(175, 115, 210, "agent_session() spawn")
    msg(160, 210, 305, "MCP connect (stdio)")
    msg(145, 305, 210, "tools registered", ret=True)
    msg(130, 210, 305, "tool call: get_critical_patients()")
    msg(115, 305, 400, "SELECT … FROM triage_records …")
    msg(100, 400, 305, "rows [ ]", ret=True, col=HexColor("#1A6B2A"))
    msg( 85, 305, 210, "JSON result", ret=True, col=TEAL)
    msg( 70, 210, 305, "tool call: execute_query(sql)")
    msg( 55, 305, 400, "SELECT … JOIN vital_signs …")
    msg( 40, 400, 305, "rows [ ]", ret=True, col=HexColor("#1A6B2A"))
    msg( 25, 305, 210, "JSON result", ret=True, col=TEAL)
    msg( 10, 210, 115, "final response text", ret=True, col=NAVY)
    msg( -4, 115,  16, "200 OK  {response, tool_calls}", ret=True, col=EC2_CLR)

    return d


# ── Diagram 4: CI/CD Deployment Workflow ───────────────────────────────────────
def make_cicd(cw):
    dw, dh = cw, 100
    d = Drawing(dw, dh)

    stages = [
        ("Local Dev\nWorkstation", 0,   NAVY),
        ("GitHub\nRepository",     130, HexColor("#24292E")),
        ("EC2 Instance\nus-east-2a", 260, EC2_CLR),
        ("Running App\n:8000",      390, TEAL),
    ]

    bw, bh = 100, 50
    for label, x, col in stages:
        d.add(Rect(x, 25, bw, bh, fillColor=col, strokeColor=WHITE,
                   strokeWidth=1, rx=6, ry=6))
        lines = label.split("\n")
        for i, ln in enumerate(lines):
            tw = len(ln) * 7.5 * 0.55
            d.add(String(x + bw/2 - tw/2, 57 - i*12, ln,
                         fontSize=7.5, fontName="Helvetica-Bold", fillColor=WHITE))

    arrows = [
        (100, 50, 130, 50, "git push", AWS_ORG),
        (230, 50, 260, 50, "git pull\nmain", IGW_CLR),
        (360, 50, 390, 50, "systemctl\nrestart", AWS_ORG),
    ]
    for x1, y1, x2, y2, lbl, col in arrows:
        d.add(Line(x1, y1, x2, y2, strokeColor=col, strokeWidth=1.8))
        d.add(Polygon([x2, y2, x2-8, y2+4, x2-8, y2-4],
                       fillColor=col, strokeColor=col, strokeWidth=0))
        lines = lbl.split("\n")
        for i, ln in enumerate(lines):
            tw = len(ln) * 6 * 0.55
            d.add(String((x1+x2)/2 - tw/2, 63 - i*9, ln,
                         fontSize=6, fontName="Helvetica-Bold", fillColor=col))

    return d


# ── Diagram 5: Future Architecture ─────────────────────────────────────────────
def make_future_arch(cw):
    dw, dh = cw, 170
    d = Drawing(dw, dh)

    def box(x, y, w, h, col, lbl, sub=""):
        d.add(Rect(x, y, w, h, fillColor=col, strokeColor=WHITE,
                   strokeWidth=1, rx=5, ry=5))
        tw = len(lbl) * 7.5 * 0.55
        d.add(String(x + w/2 - tw/2, y + h/2 + 2, lbl,
                     fontSize=7.5, fontName="Helvetica-Bold", fillColor=WHITE))
        if sub:
            sw = len(sub) * 6.5 * 0.55
            d.add(String(x + w/2 - sw/2, y + h/2 - 10, sub,
                         fontSize=6.5, fontName="Helvetica", fillColor=HexColor("#DDEEFF")))

    def arr(x1, y1, x2, y2, col=MID_GREY):
        d.add(Line(x1, y1, x2, y2, strokeColor=col, strokeWidth=1.4))
        dx, dy = x2-x1, y2-y1
        length = (dx**2+dy**2)**0.5 or 1
        ux, uy = dx/length, dy/length
        px, py = -uy*4, ux*4
        d.add(Polygon([x2, y2,
                        x2-7*ux+px, y2-7*uy+py,
                        x2-7*ux-px, y2-7*uy-py],
                       fillColor=col, strokeColor=col, strokeWidth=0))

    # Internet
    d.add(Rect(2, 65, 60, 40, fillColor=AWS_BLU, strokeColor=WHITE,
               strokeWidth=1, rx=18, ry=18))
    d.add(String(7, 87, "Internet", fontSize=8, fontName="Helvetica-Bold", fillColor=WHITE))
    d.add(String(7, 76, "HTTPS :443", fontSize=6.5, fontName="Helvetica", fillColor=HexColor("#DDEEFF")))

    arr(62, 85, 84, 85, AWS_ORG)

    # WAF + CloudFront
    box(84, 65, 64, 40, HexColor("#D63B1F"), "WAF", "CloudFront CDN")
    arr(148, 85, 170, 85, AWS_ORG)

    # ALB
    box(170, 65, 64, 40, HexColor("#E07A10"), "ALB", "HTTPS :443")
    arr(234, 85, 256, 85, AWS_ORG)

    # Auto Scaling Group
    d.add(Rect(252, 20, 138, 130, fillColor=HexColor("#FFF8F0"),
               strokeColor=AWS_ORG, strokeWidth=1.2,
               strokeDashArray=[5, 3], rx=6, ry=6))
    d.add(String(256, 144, "Auto Scaling Group", fontSize=7,
                 fontName="Helvetica-Bold", fillColor=AWS_ORG))
    box(260, 70, 60, 34, EC2_CLR, "EC2", "t3.small")
    box(330, 70, 60, 34, EC2_CLR, "EC2", "t3.small")
    d.add(String(265, 60, "AZ us-east-2a", fontSize=6, fontName="Helvetica", fillColor=MID_GREY))
    d.add(String(335, 60, "AZ us-east-2b", fontSize=6, fontName="Helvetica", fillColor=MID_GREY))

    arr(390, 85, 420, 85, AWS_ORG)

    # RDS
    box(420, 65, 64, 40, HexColor("#1A6B8A"), "RDS MySQL", "Multi-AZ")

    # Secrets Manager
    box(260, 28, 60, 26, HexColor("#8B3A6B"), "Secrets", "Manager")
    box(330, 28, 60, 26, HexColor("#2A6B3A"), "CloudWatch", "Logs+Alarms")

    return d


# ═══════════════════════════════════════════════════════════════════════════════
#  CONTENT PAGES
# ═══════════════════════════════════════════════════════════════════════════════

def page_cover(S):
    story = []
    story.append(Spacer(1, 58*mm))
    story.append(P("AWS Deployment Architecture", S, "cover_eye"))
    story.append(sp(6))
    story.append(P("ED AI Agent", S, "cover_h1"))
    story.append(P("Infrastructure & Operations Reference", S, "cover_sub"))
    story.append(sp(14))
    story.append(P("Adviava Regional Medical Center", S, "cover_org"))
    story.append(P("Emergency Department · Digital Health Platform", S, "cover_org"))
    story.append(sp(20))

    class CoverMeta(Flowable):
        def __init__(self, w=CW, h=52):
            super().__init__()
            self.width = w
            self.height = h

        def draw(self):
            c = self.canv
            metrics = [
                ("18.224.64.93", "Public IP"),
                ("us-east-2a",   "AWS Region / AZ"),
                ("t2.micro",     "Instance Type"),
                (":8000",        "Application Port"),
            ]
            n = len(metrics)
            cw = self.width / n
            c.setFillColor(HexColor("#0A2240"))
            c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
            for i, (val, lbl) in enumerate(metrics):
                x = i * cw
                if i > 0:
                    c.setStrokeColor(HexColor("#1A3D60"))
                    c.setLineWidth(0.5)
                    c.line(x, 8, x, self.height - 8)
                c.setFont("Helvetica-Bold", 14)
                c.setFillColor(AWS_ORG)
                c.drawCentredString(x + cw/2, 26, val)
                c.setFont("Helvetica", 6.5)
                c.setFillColor(HexColor("#90A8B8"))
                c.drawCentredString(x + cw/2, 12, lbl)

    story.append(CoverMeta(CW))
    story.append(sp(24))
    story.append(P(f"Generated: {datetime.now().strftime('%B %d, %Y')}  |  Confidential",
                   S, "cover_date"))
    story.append(PageBreak())
    return story


def page_overview(S):
    story = []
    story.append(P("1.  Deployment Overview", S, "h1"))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "The ED AI Agent is deployed as a single-instance application on <b>AWS EC2</b> in the "
        "<b>us-east-2 (Ohio)</b> region. The application runs under a <b>systemd service</b> "
        "(edaiagent) that starts automatically on boot, restarts on failure, and logs to the "
        "system journal. All patient data is stored in a SQLite database on the instance's EBS "
        "volume. The AI agent communicates with the Anthropic Claude API over HTTPS.",
        S, "body"))
    story.append(sp(10))

    # instance specs table
    story.append(P("1.1  EC2 Instance Specification", S, "h2"))
    story.append(data_table(
        ["Property", "Value"],
        [
            ("Instance ID",        "i-05cef553b3f5ffab7"),
            ("Instance Type",      "t2.micro  (1 vCPU · 1 GiB RAM)"),
            ("AMI",                "ami-0cf8dce2cda56aa67  —  Amazon Linux 2023"),
            ("Availability Zone",  "us-east-2a  (Ohio)"),
            ("Public IP",          "18.224.64.93  (static Elastic IP recommended)"),
            ("Private IP",         "10.100.0.29"),
            ("Root EBS Volume",    "8 GB  gp2  (2.3 GB used / 5.7 GB free)"),
            ("Security Group",     "sg-0e349182f9d8c8e03"),
            ("OS",                 "Amazon Linux 2023  (kernel 6.18.20)"),
            ("Runtime",            "Python 3.11.14  (virtualenv at ~/.venv)"),
        ],
        S, col_widths=[CW*0.34, CW*0.66], header_color=AWS_INK,
    ))
    story.append(sp(12))

    story.append(P("1.2  Application URLs", S, "h2"))
    story.append(data_table(
        ["Page", "URL", "Description"],
        [
            ("Dashboard",      "http://18.224.64.93:8000/",               "Live census — stats, ESI chart, patient table"),
            ("AI Chat",        "http://18.224.64.93:8000/chat",           "Conversational clinical query interface"),
            ("Patient Intake", "http://18.224.64.93:8000/intake",         "ED-001 patient registration form"),
            ("Business Case",  "http://18.224.64.93:8000/business-case",  "Value analysis and strategic roadmap"),
            ("API Docs",       "http://18.224.64.93:8000/docs",           "Swagger / OpenAPI interactive reference"),
        ],
        S, col_widths=[CW*0.22, CW*0.40, CW*0.38], header_color=TEAL,
    ))
    story.append(sp(10))
    story.append(P(
        "<b>Note:</b> The application currently runs over plain HTTP on port 8000. "
        "For production use, HTTPS via an Application Load Balancer with an ACM certificate "
        "is strongly recommended. See Section 7 for the future architecture roadmap.",
        S, "body"))
    story.append(PageBreak())
    return story


def page_arch_diagram(S):
    story = []
    story.append(P("2.  AWS High-Level Architecture", S, "h1"))
    story.append(hr())
    story.append(sp(8))
    story.append(P(
        "The diagram below shows the full network path from the user's browser to the SQLite "
        "database — traversing the Internet Gateway, VPC, public subnet, security group, and "
        "into the EC2 instance where the FastAPI application, AI agent, MCP server, and "
        "database all run as co-located processes.",
        S, "body"))
    story.append(sp(10))
    story.append(make_aws_arch(CW))
    story.append(sp(6))
    story.append(P(
        "Browser → Internet Gateway → VPC (us-east-2) → Public Subnet → "
        "Security Group → EC2 t2.micro → FastAPI → MCP subprocess → SQLite",
        S, "cap"))
    story.append(sp(12))

    # Network & Security table
    story.append(P("2.1  Security Group Rules", S, "h2"))
    story.append(data_table(
        ["Type", "Protocol", "Port", "Source", "Purpose"],
        [
            ("Inbound",  "TCP", "22",   "Your IP (recommended)", "SSH management access"),
            ("Inbound",  "TCP", "8000", "0.0.0.0/0",             "Application HTTP traffic"),
            ("Outbound", "All", "All",  "0.0.0.0/0",             "Internet access (Anthropic API, git, pip)"),
        ],
        S, col_widths=[CW*0.14, CW*0.15, CW*0.10, CW*0.30, CW*0.31],
        header_color=SG_CLR,
    ))
    story.append(sp(8))
    story.append(P(
        "<b>Security recommendation:</b> Restrict SSH (port 22) to your office IP range. "
        "Move port 8000 behind an ALB on port 443 (HTTPS) and close direct access "
        "to the instance once an ALB is in place.",
        S, "body"))
    story.append(PageBreak())
    return story


def page_stack(S):
    story = []
    story.append(P("3.  Application Stack on EC2", S, "h1"))
    story.append(hr())
    story.append(sp(8))
    story.append(P(
        "All application layers run as a single OS process managed by systemd. "
        "The stack from hardware to browser is shown below, with each layer's "
        "specific version and path on the instance.",
        S, "body"))
    story.append(sp(10))
    story.append(make_stack_diagram(CW))
    story.append(sp(8))
    story.append(P("Stack — bottom to top: OS → Python runtime → ASGI server → FastAPI routes → AI agent → MCP subprocess → SQLite", S, "cap"))
    story.append(sp(10))

    story.append(P("3.1  Installed Package Versions", S, "h2"))
    story.append(data_table(
        ["Package", "Version", "Role"],
        [
            ("fastapi",               "0.136.1",  "HTTP framework — routes, validation, static files"),
            ("uvicorn[standard]",     "0.46.0",   "ASGI server — event loop, request handling"),
            ("langchain",             "1.2.16",   "AI orchestration framework"),
            ("langchain-anthropic",   "1.4.2",    "Claude API integration"),
            ("langchain-mcp-adapters","0.2.2",    "MCP ↔ LangChain tool bridge"),
            ("langgraph",             "1.1.10",   "ReAct agent loop runtime"),
            ("mcp",                   "1.27.0",   "Model Context Protocol SDK (FastMCP)"),
            ("anthropic",             "0.97.0",   "Anthropic API client"),
            ("pydantic",              "2.13.3",   "Request/response data validation"),
            ("python-dotenv",         "1.2.2",    "Environment variable loading (.env)"),
        ],
        S, col_widths=[CW*0.33, CW*0.18, CW*0.49], header_color=NAVY,
    ))
    story.append(PageBreak())
    return story


def page_request_flow(S):
    story = []
    story.append(P("4.  Request Flow — AI Chat", S, "h1"))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "Each AI chat request follows the sequence below. The MCP server is spawned as a "
        "<b>child subprocess</b> for each request via stdio transport, executes the required "
        "database tool calls, and is cleanly terminated when the response is returned. "
        "Typical end-to-end latency is <b>5–10 seconds</b> depending on the number of "
        "tool calls the agent makes.",
        S, "body"))
    story.append(sp(10))
    story.append(make_request_flow(CW))
    story.append(sp(6))
    story.append(P(
        "Browser → POST /api/chat → agent_session() → LangChain ReAct loop → "
        "MCP tool calls → SQLite queries → response assembled → 200 OK",
        S, "cap"))
    story.append(sp(10))

    story.append(P("4.1  MCP Subprocess Lifecycle", S, "h2"))
    story.append(data_table(
        ["Phase", "Action", "Detail"],
        [
            ("1  Spawn",    "agent_session() entered",    "MultiServerMCPClient starts mcp_server/server.py via sys.executable"),
            ("2  Connect",  "stdio transport established", "client.session('ed_database') opens the MCP connection"),
            ("3  Discover", "load_mcp_tools(session)",    "9 tools introspected and wrapped as LangChain tools"),
            ("4  Execute",  "agent.ainvoke(messages)",    "ReAct loop: Reason → Tool call → Observe → Repeat"),
            ("5  Cleanup",  "context manager exits",      "MCP subprocess terminated, resources released"),
        ],
        S, col_widths=[CW*0.18, CW*0.28, CW*0.54], header_color=TEAL,
    ))
    story.append(PageBreak())
    return story


def page_cicd(S):
    story = []
    story.append(P("5.  CI/CD Deployment Workflow", S, "h1"))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "Deployments follow a simple git-based workflow. Code is developed locally, "
        "committed and pushed to GitHub, then pulled onto the EC2 instance and the "
        "systemd service is restarted. There is no automated CI pipeline in the current "
        "setup — all steps are manual SSH commands.",
        S, "body"))
    story.append(sp(10))
    story.append(make_cicd(CW))
    story.append(sp(6))
    story.append(P(
        "Local  →  git push  →  GitHub (arjakki/pntdigappproj)  →  git pull on EC2  →  systemctl restart edaiagent",
        S, "cap"))
    story.append(sp(12))

    story.append(P("5.1  Step-by-Step Deployment Commands", S, "h2"))
    story.append(sp(4))
    story.append(P("From your local machine — push a code change:", S, "body"))
    for cmd in [
        "git add <changed-files>",
        'git commit -m "your commit message"',
        "git push origin main",
    ]:
        story.append(Paragraph(cmd, S["mono"]))
        story.append(sp(2))

    story.append(sp(8))
    story.append(P("SSH into EC2 and deploy:", S, "body"))
    for cmd in [
        'ssh -i webapp.pem ec2-user@18.224.64.93',
        "cd ~/pntdigappproj",
        "git pull origin main",
        "sudo systemctl restart edaiagent",
        "sudo systemctl status edaiagent",
    ]:
        story.append(Paragraph(cmd, S["mono"]))
        story.append(sp(2))

    story.append(sp(10))
    story.append(P("5.2  systemd Service Configuration", S, "h2"))
    story.append(sp(4))
    story.append(mono_table([
        ("[Unit]",          ""),
        ("Description",     "ED AI Agent - Adviava Regional Medical Center"),
        ("After",           "network.target"),
        ("[Service]",       ""),
        ("Type",            "simple"),
        ("User",            "ec2-user"),
        ("WorkingDirectory","/home/ec2-user/pntdigappproj"),
        ("EnvironmentFile", "/home/ec2-user/pntdigappproj/.env"),
        ("ExecStart",       "/home/ec2-user/pntdigappproj/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"),
        ("Restart",         "on-failure"),
        ("RestartSec",      "5"),
        ("StandardOutput",  "journal"),
        ("StandardError",   "journal"),
        ("[Install]",       ""),
        ("WantedBy",        "multi-user.target"),
    ], S, col_widths=[CW*0.30, CW*0.70]))
    story.append(PageBreak())
    return story


def page_operations(S):
    story = []
    story.append(P("6.  Operations & Monitoring Reference", S, "h1"))
    story.append(hr())
    story.append(sp(8))

    story.append(P("6.1  Service Management Commands", S, "h2"))
    story.append(data_table(
        ["Command", "Purpose"],
        [
            ("sudo systemctl status edaiagent",          "Show service status, PID, memory, recent log lines"),
            ("sudo systemctl start edaiagent",           "Start the service"),
            ("sudo systemctl stop edaiagent",            "Stop the service"),
            ("sudo systemctl restart edaiagent",         "Restart (e.g. after code update or .env change)"),
            ("sudo systemctl enable edaiagent",          "Enable auto-start on boot"),
            ("sudo journalctl -u edaiagent -f",          "Stream live application logs"),
            ("sudo journalctl -u edaiagent --since '1h ago'", "Last hour of application logs"),
            ("sudo journalctl -u edaiagent -n 100",     "Last 100 log lines"),
        ],
        S, col_widths=[CW*0.55, CW*0.45], header_color=AWS_INK,
    ))
    story.append(sp(10))

    story.append(P("6.2  Instance Health Checks", S, "h2"))
    story.append(data_table(
        ["Check", "Command", "Expected"],
        [
            ("HTTP health",     "curl http://18.224.64.93:8000/api/stats", "200 OK + JSON body"),
            ("Process running", "pgrep -a python",                         "uvicorn process shown"),
            ("Port listening",  "ss -tlnp | grep 8000",                    "0.0.0.0:8000 LISTEN"),
            ("Disk space",      "df -h /",                                 "<80% used"),
            ("Memory",          "free -h",                                 "Swap not heavily used"),
            ("DB file",         "ls -lh ~/pntdigappproj/data/",            "ed_database.db present"),
        ],
        S, col_widths=[CW*0.22, CW*0.44, CW*0.34], header_color=TEAL,
    ))
    story.append(sp(10))

    story.append(P("6.3  Environment Configuration", S, "h2"))
    story.append(P(
        "Application configuration is loaded from <b>/home/ec2-user/pntdigappproj/.env</b> "
        "at service start. After editing the file, restart the service for changes to take effect.",
        S, "body"))
    story.append(sp(4))
    story.append(mono_table([
        ("ANTHROPIC_API_KEY", "sk-ant-...   (required for AI chat — 503 returned if missing)"),
        ("HOST",              "0.0.0.0      (bind all interfaces)"),
        ("PORT",              "8000         (application port)"),
    ], S, col_widths=[CW*0.30, CW*0.70]))
    story.append(sp(10))

    story.append(P("6.4  Log Interpretation", S, "h2"))
    story.append(data_table(
        ["Log Message", "Meaning"],
        [
            ("Application startup complete.",                     "Service started successfully — app is ready"),
            ("WARNING: ANTHROPIC_API_KEY not set",               "AI chat will return 503 — add key to .env"),
            ("INFO: … 200 GET /api/stats",                       "Dashboard stat fetch (normal)"),
            ("INFO: … 200 POST /api/chat",                       "Successful AI chat request"),
            ("INFO: … 503 POST /api/chat",                       "Missing API key — check .env"),
            ("INFO: … 500 POST /api/chat",                       "Agent error — check journal for traceback"),
            ("systemd: edaiagent.service: Main process exited",   "App crashed — systemd will auto-restart in 5s"),
        ],
        S, col_widths=[CW*0.52, CW*0.48], header_color=AWS_INK,
    ))
    story.append(PageBreak())
    return story


def page_future(S):
    story = []
    story.append(P("7.  Future Architecture Recommendations", S, "h1"))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "The current single-instance deployment is appropriate for a demonstration or pilot. "
        "Moving to production requires addressing availability, security, scalability, and "
        "data durability. The diagram and table below outline the recommended future state.",
        S, "body"))
    story.append(sp(10))
    story.append(make_future_arch(CW))
    story.append(sp(6))
    story.append(P(
        "Internet → WAF/CloudFront → ALB (HTTPS :443) → Auto Scaling Group (EC2) → RDS MySQL Multi-AZ",
        S, "cap"))
    story.append(sp(10))

    story.append(P("7.1  Recommended AWS Services", S, "h2"))
    story.append(data_table(
        ["Service", "Purpose", "Priority"],
        [
            ("ACM + ALB",            "HTTPS termination — TLS certificate via AWS Certificate Manager on an Application Load Balancer", "Immediate"),
            ("Route 53",             "Custom domain (e.g. ed-agent.adviava.com) with DNS failover",                                   "Immediate"),
            ("AWS WAF",              "Web Application Firewall — protect against OWASP top 10, rate limiting",                        "Immediate"),
            ("Elastic IP",           "Static public IP so DNS doesn't break on instance stop/start",                                  "Immediate"),
            ("RDS MySQL",            "Replace SQLite with managed MySQL — automated backups, Multi-AZ standby, point-in-time recovery","Short-term"),
            ("Secrets Manager",      "Store ANTHROPIC_API_KEY and DB credentials — rotation, audit log, no plaintext .env",           "Short-term"),
            ("CloudWatch",           "Logs, dashboards, alarms — CPU, memory, 5xx error rate, latency",                              "Short-term"),
            ("Auto Scaling Group",   "Scale EC2 fleet based on CPU/request load — minimum 2 instances across 2 AZs",                 "Medium-term"),
            ("S3",                   "Store generated PDFs and static assets — serve via CloudFront",                                 "Medium-term"),
            ("ECS Fargate",          "Containerise the app — eliminate OS patching, deploy via ECR image pipeline",                   "Long-term"),
            ("VPC Private Subnet",   "Move EC2/RDS to private subnet — access only via ALB, no public IP on instances",              "Long-term"),
            ("AWS Bedrock / VPC EP", "Call Claude via VPC endpoint — keep AI traffic off the public internet",                        "Long-term"),
        ],
        S, col_widths=[CW*0.25, CW*0.58, CW*0.17], header_color=NAVY,
    ))
    story.append(sp(10))

    story.append(P("7.2  Immediate Security Actions", S, "h2"))
    for item in [
        "<b>Restrict SSH access</b> — change security group inbound rule for port 22 from 0.0.0.0/0 to your office IP range",
        "<b>Enable HTTPS</b> — provision ACM certificate, create ALB listener on :443, redirect :80 → :443",
        "<b>Move API key to Secrets Manager</b> — remove ANTHROPIC_API_KEY from the .env file on disk",
        "<b>Enable CloudTrail</b> — audit all API calls to your AWS account",
        "<b>Enable EBS encryption</b> — encrypt the root volume containing the SQLite database",
    ]:
        story.append(bul(item, S))
    story.append(PageBreak())
    return story


def page_summary(S):
    story = []
    story.append(P("8.  Deployment Summary", S, "h1"))
    story.append(hr())
    story.append(sp(8))
    story.append(data_table(
        ["Component", "Detail"],
        [
            ("Application",       "ED AI Agent — Adviava Regional Medical Center"),
            ("Repository",        "https://github.com/arjakki/pntdigappproj"),
            ("Live URL",          "http://18.224.64.93:8000"),
            ("Cloud Provider",    "Amazon Web Services (AWS)"),
            ("Region",            "us-east-2  (Ohio)"),
            ("Instance",          "EC2 t2.micro  |  i-05cef553b3f5ffab7"),
            ("OS",                "Amazon Linux 2023  |  ami-0cf8dce2cda56aa67"),
            ("Runtime",           "Python 3.11.14  |  virtualenv"),
            ("Process Manager",   "systemd  |  edaiagent.service"),
            ("Web Framework",     "FastAPI 0.136.1  +  Uvicorn 0.46.0"),
            ("AI Stack",          "LangChain 1.2.16  +  LangGraph 1.1.10  +  Claude Sonnet 4.6"),
            ("Protocol",          "Model Context Protocol (MCP) 1.27.0  —  stdio transport"),
            ("Database",          "SQLite  |  /home/ec2-user/pntdigappproj/data/ed_database.db"),
            ("Security Group",    "sg-0e349182f9d8c8e03  |  TCP 22, TCP 8000 open"),
            ("Deployment Method", "git pull + systemctl restart  (manual)"),
            ("Auto-restart",      "systemd Restart=on-failure  |  RestartSec=5"),
            ("Boot auto-start",   "systemctl enable edaiagent"),
            ("Generated",         datetime.now().strftime("%B %d, %Y at %H:%M UTC")),
        ],
        S, col_widths=[CW*0.32, CW*0.68], header_color=AWS_INK,
    ))
    story.append(sp(16))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "<b>Adviava Regional Medical Center</b>  ·  ED AI Agent  ·  AWS Deployment Architecture  ·  "
        f"Version 1.0  ·  {datetime.now().strftime('%B %Y')}  ·  Confidential",
        S, "footer"))
    return story


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ═══════════════════════════════════════════════════════════════════════════════
def build_pdf(output_path: str):
    S = styles()

    cover_frame = Frame(MARGIN, 14*mm, CW, H - 28*mm,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)
    inner_frame = Frame(MARGIN + 4*mm, 16*mm, CW - 4*mm, H - 32*mm,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)

    doc = BaseDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=16*mm, bottomMargin=16*mm,
        title="ED AI Agent — AWS Deployment Architecture",
        author="Adviava Regional Medical Center",
        subject="AWS Infrastructure & Operations Reference",
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_bg),
        PageTemplate(id="inner", frames=[inner_frame], onPage=inner_bg),
    ])

    story = []
    story += page_cover(S)
    story.append(NextPageTemplate("inner"))
    story += page_overview(S)
    story += page_arch_diagram(S)
    story += page_stack(S)
    story += page_request_flow(S)
    story += page_cicd(S)
    story += page_operations(S)
    story += page_future(S)
    story += page_summary(S)

    doc.build(story)
    print(f"PDF saved: {output_path}")


if __name__ == "__main__":
    out = Path("Adviava_ED_AI_Agent_AWS_Deployment.pdf")
    build_pdf(str(out))
