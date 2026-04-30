"""
Generate Adviava ED AI Agent — Business Case PDF
"""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.lib.colors import HexColor

# ── Brand palette ─────────────────────────────────────────────────────────────
NAVY      = HexColor("#0D2B4E")   # primary dark
TEAL      = HexColor("#007C91")   # accent
TEAL_LITE = HexColor("#E0F4F7")   # table header bg
MID_GREY  = HexColor("#4A5568")   # body text
LIGHT_BG  = HexColor("#F7FAFC")   # alternating row
RED       = HexColor("#C8341F")   # alert / critical
GOLD      = HexColor("#D4A017")   # highlight
WHITE     = colors.white
BLACK     = colors.black

W, H = A4  # 595.28 x 841.89 pt

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "cover_title": S("cover_title",
            fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
            leading=36, alignment=TA_LEFT, spaceAfter=8),
        "cover_sub": S("cover_sub",
            fontName="Helvetica", fontSize=14, textColor=HexColor("#B0C8D8"),
            leading=20, alignment=TA_LEFT, spaceAfter=6),
        "cover_org": S("cover_org",
            fontName="Helvetica-Bold", fontSize=12, textColor=GOLD,
            leading=16, alignment=TA_LEFT),
        "cover_date": S("cover_date",
            fontName="Helvetica", fontSize=10, textColor=HexColor("#90A8B8"),
            alignment=TA_LEFT),
        "h1": S("h1",
            fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
            spaceBefore=18, spaceAfter=6, leading=22,
            borderPadding=(0, 0, 4, 0)),
        "h2": S("h2",
            fontName="Helvetica-Bold", fontSize=12, textColor=TEAL,
            spaceBefore=14, spaceAfter=4, leading=16),
        "h3": S("h3",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            spaceBefore=10, spaceAfter=3, leading=14),
        "body": S("body",
            fontName="Helvetica", fontSize=9.5, textColor=MID_GREY,
            leading=15, alignment=TA_JUSTIFY, spaceAfter=4),
        "bullet": S("bullet",
            fontName="Helvetica", fontSize=9.5, textColor=MID_GREY,
            leading=15, leftIndent=14, bulletIndent=4,
            spaceAfter=2),
        "bold_bullet": S("bold_bullet",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
            leading=15, leftIndent=14, bulletIndent=4, spaceAfter=2),
        "th": S("th",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE,
            alignment=TA_CENTER, leading=12),
        "td": S("td",
            fontName="Helvetica", fontSize=8.5, textColor=MID_GREY,
            alignment=TA_LEFT, leading=13),
        "td_bold": S("td_bold",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY,
            alignment=TA_LEFT, leading=13),
        "italic": S("italic",
            fontName="Helvetica-Oblique", fontSize=9, textColor=MID_GREY,
            leading=14, alignment=TA_CENTER),
        "callout": S("callout",
            fontName="Helvetica-Bold", fontSize=10.5, textColor=NAVY,
            leading=16, alignment=TA_CENTER),
        "footer": S("footer",
            fontName="Helvetica", fontSize=7.5, textColor=HexColor("#8090A0"),
            alignment=TA_CENTER),
        "tag": S("tag",
            fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
            alignment=TA_CENTER),
    }


# ── Page templates ─────────────────────────────────────────────────────────────
MARGIN = 18 * mm
CONTENT_W = W - 2 * MARGIN

def cover_background(canvas, doc):
    canvas.saveState()
    # full navy background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # teal accent bar bottom
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, W, 18 * mm, fill=1, stroke=0)
    # decorative right stripe
    canvas.setFillColor(HexColor("#0A2240"))
    canvas.rect(W - 55 * mm, 0, 55 * mm, H, fill=1, stroke=0)
    # gold top accent bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 4 * mm, W, 4 * mm, fill=1, stroke=0)
    # light diagonal watermark lines
    canvas.setStrokeColor(HexColor("#1A3D60"))
    canvas.setLineWidth(0.5)
    for i in range(0, int(H) + 200, 40):
        canvas.line(W - 55 * mm, i, W, i - 55 * mm)
    canvas.restoreState()


def inner_background(canvas, doc):
    canvas.saveState()
    # top navy header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 14 * mm, W, 14 * mm, fill=1, stroke=0)
    # header text
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(HexColor("#90A8C8"))
    canvas.drawString(MARGIN, H - 9 * mm, "ADVIAVA REGIONAL MEDICAL CENTER")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#607080"))
    canvas.drawRightString(W - MARGIN, H - 9 * mm, "ED AI Agent — Business Case & Value Analysis")
    # teal left margin accent
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 3 * mm, H - 14 * mm, fill=1, stroke=0)
    # footer line
    canvas.setStrokeColor(HexColor("#CBD5E0"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, W - MARGIN, 12 * mm)
    # footer text
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#8090A0"))
    canvas.drawString(MARGIN, 7 * mm, "Adviava Regional Medical Center  |  Confidential — For Internal Use Only")
    canvas.drawRightString(W - MARGIN, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


# ── Helpers ────────────────────────────────────────────────────────────────────
def sp(n=6):
    return Spacer(1, n)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor("#CBD5E0"),
                      spaceAfter=4, spaceBefore=4)

def P(text, style):
    return Paragraph(text, style)

def bullet(text, S, bold=False):
    key = "bold_bullet" if bold else "bullet"
    return Paragraph(f"• {text}", S[key])


def styled_table(headers, rows, S, col_widths=None):
    th_style = S["th"]
    td_style = S["td"]

    data = [[Paragraph(h, th_style) for h in headers]]
    for i, row in enumerate(rows):
        styled_row = []
        for j, cell in enumerate(row):
            is_bold = j == 0
            st = S["td_bold"] if is_bold else td_style
            styled_row.append(Paragraph(str(cell), st))
        data.append(styled_row)

    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)

    ts = TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID",         (0, 0), (-1, -1), 0.4, HexColor("#CBD5E0")),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW",    (0, 0), (-1, 0),  1.2, TEAL),
    ])
    return Table(data, colWidths=col_widths, style=ts, hAlign="LEFT")


class TagBox(Flowable):
    """Coloured pill badge."""
    def __init__(self, text, bg=TEAL, fg=WHITE, width=90, height=16):
        super().__init__()
        self.text = text
        self.bg = bg
        self.fg = fg
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        self.canv.setFont("Helvetica-Bold", 7.5)
        self.canv.setFillColor(self.fg)
        self.canv.drawCentredString(self.width / 2, 4.5, self.text)


class MetricBlock(Flowable):
    """Three-column stat block used on cover and exec summary."""
    def __init__(self, metrics, width=None):
        super().__init__()
        self.metrics = metrics   # list of (value, label)
        self.width = width or CONTENT_W
        self.height = 42

    def draw(self):
        n = len(self.metrics)
        cell_w = self.width / n
        for i, (val, lbl) in enumerate(self.metrics):
            x = i * cell_w
            # divider
            if i > 0:
                self.canv.setStrokeColor(HexColor("#CBD5E0"))
                self.canv.setLineWidth(0.5)
                self.canv.line(x, 4, x, self.height - 4)
            self.canv.setFont("Helvetica-Bold", 18)
            self.canv.setFillColor(TEAL)
            self.canv.drawCentredString(x + cell_w / 2, 22, val)
            self.canv.setFont("Helvetica", 7.5)
            self.canv.setFillColor(MID_GREY)
            self.canv.drawCentredString(x + cell_w / 2, 10, lbl)


# ── Cover page ─────────────────────────────────────────────────────────────────
def make_cover(S):
    story = []

    story.append(Spacer(1, 62 * mm))
    story.append(P("Business Case", S["cover_sub"]))
    story.append(sp(4))
    story.append(P("ED AI Agent", S["cover_title"]))
    story.append(P("Clinical Decision Support System", S["cover_title"]))
    story.append(sp(12))
    story.append(P("Adviava Regional Medical Center", S["cover_org"]))
    story.append(P("Emergency Department", S["cover_org"]))
    story.append(sp(20))

    # metric bar on cover
    cover_metrics = [
        ("145M", "Annual US ED Visits"),
        ("35%", "Shift Time Lost to EHR Navigation"),
        ("62%", "ED Physician Burnout Rate"),
        ("$361K", "Est. Annual Savings / Department"),
    ]

    class CoverMetrics(Flowable):
        def __init__(self, metrics, w, h=52):
            super().__init__()
            self.metrics = metrics
            self.width = w
            self.height = h

        def draw(self):
            n = len(self.metrics)
            cw = self.width / n
            self.canv.setFillColor(HexColor("#0A2240"))
            self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
            for i, (val, lbl) in enumerate(self.metrics):
                x = i * cw
                if i > 0:
                    self.canv.setStrokeColor(HexColor("#1A3D60"))
                    self.canv.setLineWidth(0.5)
                    self.canv.line(x, 8, x, self.height - 8)
                self.canv.setFont("Helvetica-Bold", 16)
                self.canv.setFillColor(GOLD)
                self.canv.drawCentredString(x + cw / 2, 26, val)
                self.canv.setFont("Helvetica", 7)
                self.canv.setFillColor(HexColor("#90A8B8"))
                self.canv.drawCentredString(x + cw / 2, 12, lbl)

    story.append(CoverMetrics(cover_metrics, CONTENT_W))
    story.append(sp(24))
    story.append(P("April 2026  |  Confidential", S["cover_date"]))
    story.append(PageBreak())
    return story


# ── Executive Summary ─────────────────────────────────────────────────────────
def make_exec_summary(S):
    story = []
    story.append(P("Executive Summary", S["h1"]))
    story.append(hr())
    story.append(sp(4))
    story.append(P(
        "Emergency Departments are the most time-critical, highest-risk, and operationally "
        "complex environments in modern healthcare. Every minute of delay in accessing patient "
        "information, every missed allergy flag, and every avoidable triage error carries "
        "life-or-death consequences — and significant financial liability.",
        S["body"]))
    story.append(sp(6))
    story.append(P(
        "The <b>ED AI Agent</b> is an AI-powered clinical decision support platform that gives "
        "emergency medicine staff <b>instant, natural-language access</b> to patient records, "
        "triage data, medication histories, and critical alerts — connected in real time to the "
        "hospital's patient database via the <b>Model Context Protocol (MCP)</b>.",
        S["body"]))
    story.append(sp(6))
    story.append(P(
        "This document outlines the business problem, the solution's measurable value, and "
        "why this technology is not just relevant today but will become foundational infrastructure "
        "for every hospital department over the next decade.",
        S["body"]))
    story.append(sp(10))

    story.append(MetricBlock([
        ("145M", "Annual US ED Visits"),
        ("35%",  "Shift Time Lost to Navigation"),
        ("1.3M", "Medication Errors / Year (US)"),
        ("$361K","Est. Annual Savings / Dept."),
    ], CONTENT_W))
    story.append(sp(16))
    story.append(PageBreak())
    return story


# ── Section 1 — The Business Problem ─────────────────────────────────────────
def make_section1(S):
    story = []
    story.append(P("1.  The Business Problem", S["h1"]))
    story.append(hr())

    # 1.1
    story.append(sp(6))
    story.append(P("1.1  Emergency Departments Are in Crisis", S["h2"]))
    story.append(P(
        "Emergency Departments across the United States and globally are operating at or beyond "
        "capacity. According to the American College of Emergency Physicians (ACEP) and the Agency "
        "for Healthcare Research and Quality (AHRQ):",
        S["body"]))
    for item in [
        "<b>145 million</b> ED visits occur annually in the US alone",
        "<b>Average ED wait time</b> before seeing a physician: <b>2 hours 15 minutes</b>",
        "<b>1 in 5 patients</b> leaves without being seen due to wait times (LWBS)",
        "ED crowding is directly correlated with <b>increased patient mortality</b>",
        "<b>45%</b> of US hospitals reported their EDs operating at or over capacity",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "The core driver of this crisis is not a shortage of physical space — it is "
        "<b>information bottlenecks and cognitive overload</b> on clinical staff.",
        S["body"]))

    # 1.2
    story.append(sp(4))
    story.append(P("1.2  Clinicians Spend More Time Searching Than Treating", S["h2"]))
    story.append(P(
        "Studies from the Journal of the American Medical Informatics Association (JAMIA) show that "
        "emergency physicians and nurses spend:",
        S["body"]))
    for item in [
        "<b>Up to 35% of their shift</b> navigating Electronic Health Record (EHR) systems",
        "<b>6–10 minutes per patient</b> locating allergy records, medication lists, and prior visit history",
        "<b>Critical information is buried</b> across multiple screens, tabs, and legacy interfaces",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "In a 10-hour shift managing 20+ patients, a nurse may spend <b>2–3 hours</b> on "
        "information retrieval — time that should be spent on direct patient care.",
        S["body"]))

    # 1.3
    story.append(sp(4))
    story.append(P("1.3  Information Gaps Cause Preventable Harm", S["h2"]))
    story.append(P(
        "When clinicians cannot quickly access complete patient information, patients are harmed:",
        S["body"]))
    for item in [
        "<b>Medication errors</b> affect approximately <b>1.3 million</b> people annually in the US (FDA)",
        "<b>Missed allergy flags</b> account for thousands of preventable adverse drug reactions each year",
        "<b>Delayed ESI triage decisions</b> for ESI 1–2 patients — every 10-minute delay in sepsis care increases mortality risk by 7%",
        "<b>Hospital readmissions</b> spike when discharge staff lack a complete picture of the patient's recent history",
    ]:
        story.append(bullet(item, S))

    # 1.4
    story.append(sp(4))
    story.append(P("1.4  Staff Burnout Is at Breaking Point", S["h2"]))
    story.append(P(
        "Emergency medicine has the highest burnout rate of any medical specialty:",
        S["body"]))
    for item in [
        "<b>62% of emergency physicians</b> report symptoms of burnout (Medscape 2024)",
        "The primary driver is <b>administrative and cognitive burden</b>, not the clinical work itself",
        "Turnover cost for a single ED nurse: <b>$40,000–$60,000</b> in recruiting, onboarding, and lost productivity",
        "The US faces a projected shortage of <b>124,000 physicians</b> by 2034 (AAMC)",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "Reducing cognitive load through intelligent tooling is a proven lever for improving retention.",
        S["body"]))

    # 1.5
    story.append(sp(4))
    story.append(P("1.5  Healthcare Data Is Fragmented and Inaccessible", S["h2"]))
    story.append(P(
        "Hospitals operate with patient data siloed across EHR systems (Epic, Cerner, Meditech), "
        "pharmacy systems, lab information systems, radiology PACS, and legacy ADT platforms. "
        "Frontline staff must context-switch between 5–10 different systems per patient interaction. "
        "There is no unified, intelligent query layer. The result:",
        S["body"]))
    story.append(P(
        "<b>The right information exists — but cannot be reached fast enough.</b>",
        S["callout"]))
    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Section 2 — Solution and Value ───────────────────────────────────────────
def make_section2(S):
    story = []
    story.append(P("2.  The Solution and Its Value", S["h1"]))
    story.append(hr())

    # 2.1 capability table
    story.append(sp(6))
    story.append(P("2.1  What the ED AI Agent Does", S["h2"]))
    story.append(P(
        "The ED AI Agent provides a <b>conversational AI interface</b> over the hospital's patient "
        "database. Clinical staff ask questions in plain English and receive immediate, accurate, "
        "clinically formatted responses:",
        S["body"]))
    story.append(sp(6))

    cap_rows = [
        ('"Show me all critical patients right now"',
         "Queries ESI 1–2 triage records with vitals and known allergies"),
        ('"What medications is the patient on?"',
         "Fetches complete medication list with dosage, route, frequency"),
        ('"Who is allergic to penicillin today?"',
         "Cross-references allergy records against today's arrivals"),
        ('"What were the patient\'s vitals on arrival?"',
         "Pulls triage record and first vital sign set by MRN"),
        ('"How many arrived by ambulance this week?"',
         "Runs an aggregation query against triage records"),
        ('"Register a new patient — chest pain, ESI 2"',
         "Writes a new patient intake record to the database"),
    ]
    story.append(styled_table(
        ["Staff Natural-Language Query", "Agent Action"],
        cap_rows, S,
        col_widths=[CONTENT_W * 0.47, CONTENT_W * 0.53],
    ))
    story.append(sp(8))
    story.append(P(
        "The agent autonomously selects the right database tool, queries the data, and returns "
        "a clinical-grade formatted answer — <b>in under 10 seconds</b>.",
        S["body"]))

    # 2.2 value
    story.append(sp(6))
    story.append(P("2.2  Direct Business Value", S["h2"]))

    # patient safety
    story.append(P("Patient Safety", S["h3"]))
    for item in [
        "<b>Allergy warnings surface automatically</b> — the agent proactively flags contraindications every time a patient with known allergies is queried",
        "<b>Abnormal vital thresholds are hard-coded</b> (HR &gt; 100, SBP &lt; 90, SpO₂ &lt; 95%) and called out in every patient summary",
        "<b>ESI 1–2 patients are always highlighted as critical</b>, reducing the risk of a high-acuity patient being overlooked in a crowded department",
        "<b>Code status (Full Code vs. DNR)</b> is surfaced with every patient record, preventing inappropriate resuscitation",
    ]:
        story.append(bullet(item, S))

    # operational efficiency
    story.append(sp(4))
    story.append(P("Operational Efficiency", S["h3"]))
    for item in [
        "Reduces per-patient information retrieval from <b>6–10 minutes to under 30 seconds</b>",
        "A single natural-language query replaces navigation through 3–5 system screens",
        "Real-time census dashboard gives charge nurses a live operational picture without manual reporting",
        "Patient intake form integrates directly with the database — no double-entry into separate systems",
    ]:
        story.append(bullet(item, S))

    # financial
    story.append(sp(6))
    story.append(P("Financial Impact", S["h3"]))
    fin_rows = [
        ("Time saved per nurse per shift",    "1.5 hours"),
        ("Nurses in ED per shift",            "12"),
        ("Hourly nursing cost",               "$55"),
        ("Daily efficiency savings",          "~$990 / day"),
        ("Annual savings (one department)",   "~$361,000 / year"),
        ("Adverse drug event cost (avg)",     "$4,700 per event — reduced"),
        ("LWBS revenue recovery (avg visit)", "$1,500 per visit — captured"),
    ]
    story.append(styled_table(
        ["Metric", "Conservative Estimate"],
        fin_rows, S,
        col_widths=[CONTENT_W * 0.62, CONTENT_W * 0.38],
    ))
    story.append(sp(6))
    story.append(P(
        "These figures are conservative and exclude reduced malpractice exposure, improved CMS "
        "quality scores, and lower agency staffing costs driven by improved retention.",
        S["body"]))

    # staff experience
    story.append(sp(4))
    story.append(P("Staff Experience", S["h3"]))
    for item in [
        "Eliminates the frustration of navigating fragmented EHR screens under time pressure",
        "Gives junior nurses immediate access to the same information quality as experienced staff",
        "Reduces cognitive load during peak census hours, directly improving decision quality and staff retention",
    ]:
        story.append(bullet(item, S))

    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Section 3 — Critical Today ─────────────────────────────────────────────────
def make_section3(S):
    story = []
    story.append(P("3.  Why This Is Critical Today", S["h1"]))
    story.append(hr())

    story.append(sp(6))
    story.append(P("3.1  The AI Inflection Point in Healthcare", S["h2"]))
    story.append(P(
        "2024–2026 marks the <b>first practical window</b> in which large language models are "
        "sufficiently capable, reliable, and cost-effective to deploy in clinical environments. "
        "Three forces converge:",
        S["body"]))
    for item in [
        "<b>Model capability:</b> Claude Sonnet, GPT-4, and equivalent models now reason accurately over structured clinical data, follow safety constraints reliably, and produce clinically formatted output",
        "<b>Protocol standardization:</b> The Model Context Protocol (MCP), introduced in 2024, provides a standardized, secure interface between AI models and any database or data source — making integrations achievable in days instead of months",
        "<b>Cost:</b> AI inference costs have dropped by <b>100x</b> in three years — deploying an intelligent agent per query now costs cents, not dollars",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "Hospitals that build this capability <b>now</b> establish the data pipelines, staff "
        "workflows, and institutional knowledge to scale as AI improves. Those that wait face "
        "a steeper adoption curve and competitive disadvantage.",
        S["body"]))

    story.append(sp(6))
    story.append(P("3.2  Regulatory and Reimbursement Pressure", S["h2"]))
    story.append(P(
        "Healthcare reimbursement is shifting from volume-based to <b>value-based care</b> under CMS:",
        S["body"]))
    for item in [
        "Hospitals are measured on <b>readmission rates, patient safety indicators, and quality metrics</b> — all directly improved by AI decision support",
        "CMS star ratings and HCAHPS scores drive reimbursement — patient experience improvements (shorter waits, fewer errors) directly impact revenue",
        "The FDA's action plan for AI/ML in clinical decision support establishes a clear regulatory pathway for appropriately scoped systems",
    ]:
        story.append(bullet(item, S))

    story.append(sp(6))
    story.append(P("3.3  Competitive Differentiation", S["h2"]))
    story.append(P(
        "Health systems are competing for patients, physicians, and nurses. An ED offering "
        "faster triage decisions, fewer medication errors, lower staff burnout, and demonstrably "
        "better outcomes will attract better talent and stronger patient volumes. "
        "<b>AI-assisted care is rapidly becoming a marketing differentiator</b> for health systems "
        "targeting quality-conscious markets.",
        S["body"]))

    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Section 4 — Critical in the Future ────────────────────────────────────────
def make_section4(S):
    story = []
    story.append(P("4.  Why This Will Be Even More Critical in the Future", S["h1"]))
    story.append(hr())

    story.append(sp(6))
    story.append(P("4.1  The Physician Shortage Gets Worse", S["h2"]))
    story.append(P(
        "The US physician shortage, projected at <b>124,000 by 2034</b>, cannot be solved by "
        "training more doctors — the pipeline is too slow. AI clinical decision support is not a "
        "replacement for physicians; it is a <b>force multiplier</b> that allows existing clinical "
        "staff to manage larger patient panels without a proportional increase in cognitive load. "
        "Emergency medicine — where a single physician manages 2–4 simultaneous critical cases — "
        "will feel this shortage first and most acutely.",
        S["body"]))

    story.append(sp(6))
    story.append(P("4.2  Multimodal AI Will Transform Clinical Queries", S["h2"]))
    story.append(P(
        "The current system queries structured database records. Within 2–3 years the same "
        "conversational interface will surface:",
        S["body"]))
    for item in [
        "<b>Radiology images</b> (CT, X-ray, MRI) — interpretable by multimodal AI",
        "<b>Continuous vital sign streams</b> from bedside monitors feeding real-time AI risk scoring",
        "<b>Unstructured clinical notes</b> indexed and queryable alongside structured EHR data",
        "<b>Voice interfaces</b> enabling hands-free querying during active patient care",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "The architecture built today — a conversational layer over clinical data via MCP — is "
        "the foundation on which all of these capabilities will be layered. Organizations that "
        "establish this foundation early will extend it; those starting from scratch will be "
        "years behind.",
        S["body"]))

    story.append(sp(6))
    story.append(P("4.3  Interoperability Mandates Will Drive Data Accessibility", S["h2"]))
    story.append(P(
        "The <b>21st Century Cures Act</b> and <b>CMS Interoperability Rule</b> mandate that health "
        "systems make patient data accessible via FHIR APIs. As hospital data becomes more "
        "accessible, the bottleneck shifts entirely to <b>intelligent query and synthesis</b> — "
        "exactly what this system provides. The MCP-based architecture is inherently interoperable: "
        "today it connects to SQLite; tomorrow it connects to Epic's FHIR API, a cloud data "
        "warehouse, or a real-time lab results stream — with <b>zero changes to the AI agent layer</b>.",
        S["body"]))

    story.append(sp(6))
    story.append(P("4.4  Autonomous Agent Workflows Are Next", S["h2"]))
    story.append(P(
        "The current system responds to individual queries. The next generation will:",
        S["body"]))
    for item in [
        "<b>Proactively alert</b> nursing staff when a patient's vitals cross an abnormal threshold — without being asked",
        "<b>Autonomously draft</b> discharge instructions, transfer summaries, and care plans based on the complete patient record",
        "<b>Coordinate care handoffs</b> by synthesizing the incoming shift's critical patient list and pending orders",
        "<b>Identify deteriorating patients</b> (sepsis risk, stroke onset, cardiac event) using real-time pattern recognition across the census",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "Each of these capabilities is a direct extension of the current ReAct agent architecture. "
        "The agent loop (Reason → Tool Call → Observe → Reason) is already the "
        "correct abstraction for autonomous clinical workflows.",
        S["body"]))

    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Section 5 — Strategic Recommendations ─────────────────────────────────────
def make_section5(S):
    story = []
    story.append(P("5.  Strategic Recommendations", S["h1"]))
    story.append(hr())
    story.append(sp(6))

    phases = [
        ("Immediate  (0–6 months)", TEAL, [
            "<b>Integrate with production EHR</b> (Epic, Cerner, or Meditech) via FHIR API to replace the prototype with live patient data",
            "<b>Pilot with triage nurses</b> on a single ED shift, measuring time-to-information and adverse event rates",
            "<b>Add allergy conflict checking</b> as a proactive agent behavior — alert staff when a medication order conflicts with a known allergy",
            "<b>Obtain CISO sign-off</b> on data handling, audit logging, and HIPAA compliance posture",
        ]),
        ("Near-term  (6–18 months)", NAVY, [
            "<b>Extend to inpatient units</b> — the same architecture serves ICU, med-surg, and surgical floors",
            "<b>Add voice interface</b> — hands-free querying during active resuscitation",
            "<b>Implement real-time vital sign ingestion</b> — connect bedside monitor streams to the agent context",
            "<b>Train staff</b> through simulation exercises using the current system as a training environment",
        ]),
        ("Long-term  (18–36 months)", HexColor("#5A4FA0"), [
            "<b>Predictive risk scoring</b> — integrate ML models for sepsis, stroke, and ACS risk into the agent's tool set",
            "<b>Autonomous shift handoff synthesis</b> — agent-generated incoming shift briefings for charge nurses",
            "<b>Multi-hospital deployment</b> — federated architecture serving a health system across all sites",
            "<b>Revenue cycle integration</b> — AI-assisted coding and documentation accuracy to reduce claim denials",
        ]),
    ]

    for label, colour, items in phases:
        # Phase header pill
        class PhasePill(Flowable):
            def __init__(self, text, c, w=CONTENT_W):
                super().__init__()
                self.text = text
                self.c = c
                self.width = w
                self.height = 20

            def draw(self):
                self.canv.setFillColor(self.c)
                self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
                self.canv.setFont("Helvetica-Bold", 9)
                self.canv.setFillColor(WHITE)
                self.canv.drawString(10, 6, self.text)

        story.append(PhasePill(label, colour))
        story.append(sp(4))
        for item in items:
            story.append(bullet(item, S))
        story.append(sp(8))

    story.append(PageBreak())
    return story


# ── Section 6 — Summary ─────────────────────────────────────────────────────────
def make_section6(S):
    story = []
    story.append(P("6.  Summary: The Case in Three Sentences", S["h1"]))
    story.append(hr())
    story.append(sp(10))

    sentences = [
        ("The Problem",
         "Emergency Departments are drowning in fragmented data, under-resourced staff, and time "
         "pressure that turns information delays into patient harm."),
        ("The Solution",
         "The ED AI Agent directly attacks the root cause — not by adding more staff or replacing "
         "clinicians, but by eliminating the minutes of system navigation that stand between a "
         "clinician and the information they need to act."),
        ("The Imperative",
         "As AI capability, protocol standardization, and regulatory frameworks continue to mature, "
         "this conversational-AI-over-clinical-data architecture will become the standard interface "
         "layer for every hospital department — and the organizations that build it now will lead "
         "the ones that build it later."),
    ]

    colors_s = [RED, TEAL, NAVY]
    for (label, text), c in zip(sentences, colors_s):
        class SentenceBlock(Flowable):
            def __init__(self, lbl, txt, col, w=CONTENT_W):
                super().__init__()
                self.lbl = lbl
                self.txt = txt
                self.col = col
                self.width = w
                self.height = 62

            def draw(self):
                self.canv.setFillColor(LIGHT_BG)
                self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
                self.canv.setFillColor(self.col)
                self.canv.roundRect(0, 0, 5, self.height, 3, fill=1, stroke=0)
                self.canv.setFont("Helvetica-Bold", 9)
                self.canv.setFillColor(self.col)
                self.canv.drawString(14, self.height - 16, self.lbl)
                # body text (simple word-wrap)
                self.canv.setFont("Helvetica", 8.5)
                self.canv.setFillColor(MID_GREY)
                from reportlab.lib.utils import simpleSplit
                lines = simpleSplit(self.txt, "Helvetica", 8.5, self.width - 22)
                y = self.height - 30
                for line in lines[:4]:
                    self.canv.drawString(14, y, line)
                    y -= 13

        story.append(SentenceBlock(label, text, c))
        story.append(sp(10))

    story.append(sp(20))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "Document prepared for: <b>Adviava Regional Medical Center</b> — ED Operations and Digital Health Leadership",
        S["italic"]))
    story.append(P(
        "Technology: FastAPI · LangChain · Claude Sonnet 4.6 · Model Context Protocol (MCP) · SQLite / FHIR",
        S["italic"]))
    story.append(P(
        "Adviava Regional Medical Center  |  Confidential — For Internal Use Only  |  April 2026",
        S["footer"]))
    return story


# ── Document assembly ──────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    S = make_styles()

    cover_frame = Frame(
        MARGIN, 14 * mm, CONTENT_W, H - 28 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    inner_frame = Frame(
        MARGIN + 4 * mm, 16 * mm, CONTENT_W - 4 * mm, H - 32 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )

    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=16 * mm, bottomMargin=16 * mm,
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_background),
        PageTemplate(id="inner", frames=[inner_frame], onPage=inner_background),
    ])

    story = []
    story += make_cover(S)
    story += make_exec_summary(S)
    story += make_section1(S)
    story += make_section2(S)
    story += make_section3(S)
    story += make_section4(S)
    story += make_section5(S)
    story += make_section6(S)

    # switch to inner template after cover
    from reportlab.platypus import NextPageTemplate
    story.insert(1, NextPageTemplate("inner"))

    doc.build(story)
    print(f"PDF saved: {output_path}")


if __name__ == "__main__":
    out = Path("Adviava_ED_AI_Agent_Business_Case.pdf")
    build_pdf(str(out))
