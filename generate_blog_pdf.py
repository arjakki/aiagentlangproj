"""
Generate Blog Post PDF — "Building an ED AI Agent with Claude Code"
"""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor

# ── Palette ────────────────────────────────────────────────────────────────────
NAVY      = HexColor("#0D2B4E")
TEAL      = HexColor("#007C91")
TEAL_LITE = HexColor("#E0F4F7")
MID_GREY  = HexColor("#4A5568")
LIGHT_BG  = HexColor("#F7FAFC")
CODE_BG   = HexColor("#1E2D3D")
CODE_FG   = HexColor("#A8D8EA")
RED       = HexColor("#C8341F")
GOLD      = HexColor("#D4A017")
GREEN     = HexColor("#276749")
PURPLE    = HexColor("#553C9A")
WHITE     = colors.white

W, H      = A4
MARGIN    = 18 * mm
CONTENT_W = W - 2 * MARGIN


# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    def S(name, **kw):
        return ParagraphStyle(name, **kw)
    return {
        "cover_kicker": S("cover_kicker",
            fontName="Helvetica-Bold", fontSize=10, textColor=GOLD,
            leading=14, alignment=TA_LEFT, spaceAfter=6),
        "cover_title": S("cover_title",
            fontName="Helvetica-Bold", fontSize=30, textColor=WHITE,
            leading=38, alignment=TA_LEFT, spaceAfter=10),
        "cover_sub": S("cover_sub",
            fontName="Helvetica", fontSize=13, textColor=HexColor("#B0C8D8"),
            leading=19, alignment=TA_LEFT, spaceAfter=8),
        "cover_author": S("cover_author",
            fontName="Helvetica-Bold", fontSize=10, textColor=GOLD,
            leading=15, alignment=TA_LEFT),
        "cover_date": S("cover_date",
            fontName="Helvetica", fontSize=9, textColor=HexColor("#90A8B8"),
            alignment=TA_LEFT),
        "h1": S("h1",
            fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
            spaceBefore=18, spaceAfter=6, leading=22),
        "h2": S("h2",
            fontName="Helvetica-Bold", fontSize=12, textColor=TEAL,
            spaceBefore=13, spaceAfter=4, leading=16),
        "h3": S("h3",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            spaceBefore=9, spaceAfter=3, leading=14),
        "body": S("body",
            fontName="Helvetica", fontSize=10, textColor=MID_GREY,
            leading=16, alignment=TA_JUSTIFY, spaceAfter=6),
        "body_left": S("body_left",
            fontName="Helvetica", fontSize=10, textColor=MID_GREY,
            leading=16, alignment=TA_LEFT, spaceAfter=6),
        "bullet": S("bullet",
            fontName="Helvetica", fontSize=10, textColor=MID_GREY,
            leading=16, leftIndent=16, bulletIndent=4, spaceAfter=3),
        "bold_bullet": S("bold_bullet",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=16, leftIndent=16, bulletIndent=4, spaceAfter=3),
        "code_inline": S("code_inline",
            fontName="Courier", fontSize=8.5, textColor=TEAL,
            leading=13),
        "pullquote": S("pullquote",
            fontName="Helvetica-BoldOblique", fontSize=13, textColor=NAVY,
            leading=20, alignment=TA_CENTER, spaceAfter=6),
        "th": S("th",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE,
            alignment=TA_CENTER, leading=12),
        "td": S("td",
            fontName="Helvetica", fontSize=8.5, textColor=MID_GREY,
            alignment=TA_LEFT, leading=13),
        "td_bold": S("td_bold",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=NAVY,
            alignment=TA_LEFT, leading=13),
        "td_num": S("td_num",
            fontName="Helvetica-Bold", fontSize=9, textColor=TEAL,
            alignment=TA_CENTER, leading=13),
        "caption": S("caption",
            fontName="Helvetica-Oblique", fontSize=8.5, textColor=HexColor("#718096"),
            leading=12, alignment=TA_CENTER, spaceAfter=4),
        "italic": S("italic",
            fontName="Helvetica-Oblique", fontSize=9, textColor=MID_GREY,
            leading=13, alignment=TA_CENTER),
        "footer": S("footer",
            fontName="Helvetica", fontSize=7.5, textColor=HexColor("#8090A0"),
            alignment=TA_CENTER),
        "tag": S("tag",
            fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
            alignment=TA_CENTER),
    }


# ── Page templates ─────────────────────────────────────────────────────────────
def cover_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # gradient-effect dark stripe right
    canvas.setFillColor(HexColor("#0A2240"))
    canvas.rect(W - 58 * mm, 0, 58 * mm, H, fill=1, stroke=0)
    # teal bottom bar
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, W, 16 * mm, fill=1, stroke=0)
    # gold top bar
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 5 * mm, W, 5 * mm, fill=1, stroke=0)
    # decorative diagonal lines
    canvas.setStrokeColor(HexColor("#1A3D60"))
    canvas.setLineWidth(0.5)
    for i in range(0, int(H) + 200, 38):
        canvas.line(W - 58 * mm, i, W, i - 58 * mm)
    # left teal accent bar
    canvas.setFillColor(TEAL)
    canvas.rect(0, 16 * mm, 5 * mm, H - 21 * mm, fill=1, stroke=0)
    canvas.restoreState()


def inner_background(canvas, doc):
    canvas.saveState()
    # header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 14 * mm, W, 14 * mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(HexColor("#90A8C8"))
    canvas.drawString(MARGIN, H - 9 * mm, "DEVELOPER BLOG")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#607080"))
    canvas.drawRightString(W - MARGIN, H - 9 * mm,
                           "Building an ED AI Agent with Claude Code")
    # left teal bar
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 3 * mm, H - 14 * mm, fill=1, stroke=0)
    # footer rule
    canvas.setStrokeColor(HexColor("#CBD5E0"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, W - MARGIN, 12 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#8090A0"))
    canvas.drawString(MARGIN, 7 * mm, "Adviava Regional Medical Center  |  April 2026")
    canvas.drawRightString(W - MARGIN, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


# ── Helpers ────────────────────────────────────────────────────────────────────
def sp(n=6):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=0.5,
                                color=HexColor("#CBD5E0"), spaceAfter=4, spaceBefore=4)
def P(t, s):  return Paragraph(t, s)
def bullet(t, S, bold=False):
    return Paragraph(f"• {t}", S["bold_bullet" if bold else "bullet"])


def styled_table(headers, rows, S, col_widths=None, num_cols=None):
    data = [[Paragraph(h, S["th"]) for h in headers]]
    for row in rows:
        styled = []
        for j, cell in enumerate(row):
            if num_cols and j in num_cols:
                styled.append(Paragraph(str(cell), S["td_num"]))
            elif j == 0:
                styled.append(Paragraph(str(cell), S["td_bold"]))
            else:
                styled.append(Paragraph(str(cell), S["td"]))
        data.append(styled)
    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)
    ts = TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("GRID",           (0, 0), (-1, -1), 0.4, HexColor("#CBD5E0")),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
        ("LEFTPADDING",    (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 7),
        ("LINEBELOW",      (0, 0), (-1, 0),  1.2, TEAL),
    ])
    return Table(data, colWidths=col_widths, style=ts, hAlign="LEFT")


class PullQuote(Flowable):
    def __init__(self, text, accent=TEAL, width=None, padding=14):
        super().__init__()
        self.text = text
        self.accent = accent
        self.width = width or CONTENT_W
        self.padding = padding
        self.height = 68

    def draw(self):
        from reportlab.lib.utils import simpleSplit
        self.canv.setFillColor(TEAL_LITE)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        self.canv.setFillColor(self.accent)
        self.canv.roundRect(0, 0, 6, self.height, 4, fill=1, stroke=0)
        # quote mark
        self.canv.setFont("Helvetica-Bold", 36)
        self.canv.setFillColor(HexColor("#B2D8E0"))
        self.canv.drawString(14, self.height - 34, "“")
        # text
        self.canv.setFont("Helvetica-BoldOblique", 10)
        self.canv.setFillColor(NAVY)
        lines = simpleSplit(self.text, "Helvetica-BoldOblique", 10, self.width - 52)
        y = self.height - 20
        for line in lines[:4]:
            self.canv.drawString(46, y, line)
            y -= 15


class StatBar(Flowable):
    def __init__(self, stats, width=None, height=54, bg=NAVY):
        super().__init__()
        self.stats = stats
        self.width = width or CONTENT_W
        self.height = height
        self.bg = bg

    def draw(self):
        n = len(self.stats)
        cw = self.width / n
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        for i, (val, lbl) in enumerate(self.stats):
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


class TimelineItem(Flowable):
    def __init__(self, time, title, detail, colour=TEAL, width=None):
        super().__init__()
        self.time   = time
        self.title  = title
        self.detail = detail
        self.colour = colour
        self.width  = width or CONTENT_W
        self.height = 52

    def draw(self):
        from reportlab.lib.utils import simpleSplit
        # connector line
        self.canv.setStrokeColor(HexColor("#CBD5E0"))
        self.canv.setLineWidth(1)
        self.canv.line(20, 0, 20, self.height)
        # dot
        self.canv.setFillColor(self.colour)
        self.canv.circle(20, self.height - 14, 6, fill=1, stroke=0)
        # time label
        self.canv.setFont("Helvetica-Bold", 7.5)
        self.canv.setFillColor(self.colour)
        self.canv.drawString(34, self.height - 17, self.time)
        # title
        self.canv.setFont("Helvetica-Bold", 9.5)
        self.canv.setFillColor(NAVY)
        self.canv.drawString(34, self.height - 30, self.title)
        # detail
        self.canv.setFont("Helvetica", 8.5)
        self.canv.setFillColor(MID_GREY)
        lines = simpleSplit(self.detail, "Helvetica", 8.5, self.width - 42)
        y = self.height - 42
        for line in lines[:2]:
            self.canv.drawString(34, y, line)
            y -= 12


class TagRow(Flowable):
    def __init__(self, tags, width=None):
        super().__init__()
        self.tags = tags
        self.width = width or CONTENT_W
        self.height = 22

    def draw(self):
        x = 0
        colours = [TEAL, NAVY, GREEN, PURPLE, RED, GOLD]
        for i, (tag, colour) in enumerate(zip(self.tags, colours)):
            tw = len(tag) * 6 + 16
            self.canv.setFillColor(colour)
            self.canv.roundRect(x, 3, tw, 16, 4, fill=1, stroke=0)
            self.canv.setFont("Helvetica-Bold", 7.5)
            self.canv.setFillColor(WHITE)
            self.canv.drawCentredString(x + tw / 2, 7, tag)
            x += tw + 8


# ── Cover ──────────────────────────────────────────────────────────────────────
def make_cover(S):
    story = []
    story.append(Spacer(1, 52 * mm))
    story.append(P("DEVELOPER BLOG  —  APRIL 2026", S["cover_kicker"]))
    story.append(sp(6))
    story.append(P("Building a Production", S["cover_title"]))
    story.append(P("ED AI Agent with Claude Code", S["cover_title"]))
    story.append(sp(10))
    story.append(P(
        "From blank repository to a live, AWS-deployed clinical decision support "
        "system — in a single development session.",
        S["cover_sub"]))
    story.append(sp(16))

    story.append(StatBar([
        ("3,583",  "Lines — first commit"),
        ("17",     "Files bootstrapped"),
        ("9",      "MCP tools built"),
        ("8",      "Git commits"),
        ("~24 hrs","Zero to production"),
    ]))
    story.append(sp(22))
    story.append(P("Adviava Regional Medical Center  ·  Digital Health", S["cover_author"]))
    story.append(P("April 2026", S["cover_date"]))
    story.append(PageBreak())
    return story


# ── Introduction ───────────────────────────────────────────────────────────────
def make_intro(S):
    story = []
    story.append(P("The Idea: A Conversational AI for the Emergency Department", S["h1"]))
    story.append(hr())
    story.append(sp(4))

    story.append(P(
        "Emergency Departments are among the most information-dense environments in healthcare. "
        "Nurses and physicians context-switch between multiple screens, EHR systems, and paper "
        "charts to find what they need — every minute of delay has consequences. The idea was "
        "simple: what if a clinician could just <i>ask</i> for what they need in plain English, "
        "and get an immediate, clinically formatted answer directly from the patient database?",
        S["body"]))
    story.append(sp(4))
    story.append(P(
        "That idea became the <b>Adviava ED AI Agent</b> — a full-stack web application combining "
        "FastAPI, LangGraph, Anthropic's Claude Sonnet 4.6, and the Model Context Protocol (MCP). "
        "And the entire thing was built with <b>Claude Code</b> as the primary development tool.",
        S["body"]))
    story.append(sp(8))

    story.append(PullQuote(
        "Claude Code didn't assist with the build — it was the build. "
        "Every file, every commit, every PDF carries its co-authorship tag.",
        accent=TEAL))
    story.append(sp(10))

    story.append(P(
        "This post walks through exactly what Claude Code did across every phase of the project: "
        "architecture, code generation, documentation, rebranding, PDF creation, deployment "
        "documentation, and prompt engineering. It's an honest account — including what worked "
        "exceptionally well and where human judgment was still essential.",
        S["body"]))
    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── What We Built ──────────────────────────────────────────────────────────────
def make_what_we_built(S):
    story = []
    story.append(P("What We Built", S["h1"]))
    story.append(hr())
    story.append(sp(4))
    story.append(P(
        "Before getting into how Claude Code helped, here's a quick picture of the finished system:",
        S["body"]))
    story.append(sp(6))

    arch_rows = [
        ("Frontend",     "Vanilla HTML5 / CSS3 / JavaScript",
         "4 pages: Dashboard, AI Chat, Patient Intake, Business Case"),
        ("Backend",      "Python 3.11 + FastAPI + Uvicorn",
         "REST API serving frontend pages and /api/chat, /api/intake endpoints"),
        ("AI Agent",     "LangGraph ReAct + Claude Sonnet 4.6",
         "Stateless per-request agent with tool-use reasoning loop"),
        ("Tool Protocol","Model Context Protocol (MCP) via stdio",
         "9 tools exposing the SQLite database to the agent"),
        ("Database",     "SQLite",
         "7 tables: patients, triage, vitals, allergies, meds, history, contacts"),
        ("Deployment",   "AWS EC2 (t2.micro, us-east-2)",
         "Systemd service, public IP http://18.224.64.93:8000"),
    ]
    story.append(styled_table(
        ["Layer", "Technology", "Detail"],
        arch_rows, S,
        col_widths=[CONTENT_W * 0.18, CONTENT_W * 0.30, CONTENT_W * 0.52],
    ))

    story.append(sp(10))
    story.append(P(
        "The agent can answer questions like <i>\"Show me all critical patients right now\"</i>, "
        "<i>\"What medications is patient A10003 on?\"</i>, or <i>\"Who arrived by ambulance "
        "today?\"</i> — and it autonomously selects the right database tool, queries the data, "
        "and returns a clinically formatted response in under ten seconds.",
        S["body"]))
    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── The Build Timeline ─────────────────────────────────────────────────────────
def make_timeline(S):
    story = []
    story.append(P("The Build: A Commit-by-Commit Walkthrough", S["h1"]))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "Every commit in the repository carries the co-authorship tag "
        "<font face='Courier'>Co-Authored-By: Claude Sonnet 4.6</font>. "
        "Here's what happened, in order:",
        S["body"]))
    story.append(sp(8))

    timeline = [
        (TEAL,   "Commit 1 — Initial Application",
         "Apr 29, 14:46",
         "3,583 lines across 17 files: FastAPI backend, LangGraph ReAct agent, MCP server with 9 tools, "
         "SQLite database initializer with 10 patients and full sample data, 4 frontend pages, "
         "ReportLab PDF generator, startup scripts for Windows and Unix."),
        (NAVY,   "Commit 2 — Comprehensive README",
         "Apr 29, 14:51",
         "745-line README with ASCII architecture diagrams, step-by-step installation guide, full API "
         "reference, MCP tools table, database schema, and troubleshooting section. Written in one pass."),
        (GREEN,  "Commit 3 — Business Case PDF",
         "Apr 29, 19:34",
         "818-line ReportLab PDF generator producing a professional 9-section business case document "
         "with branded cover page, metric stat blocks, styled tables, phase roadmap pills, and "
         "3-sentence summary callout cards."),
        (PURPLE, "Commit 4 — Business Case Web Page",
         "Apr 29, 19:39",
         "555-line HTML business case page added to the web app, with problem cards, capability query "
         "table, financial impact table, 3-phase roadmap, and summary section. Navigation updated "
         "across all 4 existing pages simultaneously."),
        (GOLD,   "Commit 5 — Rebrand: Mercy → Adviava",
         "Apr 29, 19:53",
         "Precision find-and-replace across 6 files and 8 occurrences: agent system prompt, 2 frontend "
         "pages, PDF generator, and both startup scripts. Zero regressions, zero missed instances."),
        (TEAL,   "Commit 6 — README & Deployment Update",
         "Apr 29, 20:04",
         "README updated with Adviava branding, new business case page, and EC2 deployment details "
         "including the live public IP address."),
        (RED,    "Commit 7 — AWS Deployment Architecture PDF",
         "Apr 29, 20:09",
         "1,033-line ReportLab generator for a 9-page AWS deployment architecture document covering "
         "EC2 instance specs, VPC config, security group, request flow diagram, CI/CD pipeline, "
         "operations reference, and future architecture roadmap."),
        (NAVY,   "Commit 8 — Prompt Templates + This PDF",
         "Apr 30, 10:08",
         "CLAUDE.md project context prompt, restructured 4-section SYSTEM_PROMPT with clinical "
         "reference tables and safety rules, 7-page prompt template PDF, and this blog post PDF."),
    ]

    for colour, title, time, detail in timeline:
        story.append(KeepTogether([
            TimelineItem(time, title, detail, colour=colour),
            sp(6),
        ]))

    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Deep Dives ─────────────────────────────────────────────────────────────────
def make_deep_dives(S):
    story = []
    story.append(P("Five Things Claude Code Did Exceptionally Well", S["h1"]))
    story.append(hr())
    story.append(sp(4))

    # ── 1. Full-stack bootstrap ──
    story.append(P("1. Bootstrapping a Full-Stack Application in One Shot", S["h2"]))
    story.append(P(
        "The first commit was not a skeleton or a starter template — it was a working application. "
        "3,583 lines across 17 files, including:",
        S["body"]))
    for item in [
        "A FastAPI server with lifespan management, static file mounting, and 4 routes",
        "A LangGraph ReAct agent using <font face='Courier'>create_react_agent</font> with a "
        "custom system prompt and MCP tool integration",
        "An MCP server with 9 fully implemented tools — each with correct SQL, error handling, "
        "and JSON serialization",
        "240 lines of database initialization code seeding 10 realistic patients with vitals, "
        "allergies, medications, medical history, and emergency contacts",
        "A 698-line patient intake HTML form with auto-generated MRN and pre-filled timestamps",
        "A 1,213-line branded PDF generator with cover page, architecture diagrams, and styled tables",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "It compiled and ran on the first attempt. The mental model Claude Code brought to the "
        "project — understanding how FastAPI, LangChain, MCP, and ReportLab fit together — was "
        "complete from the start.",
        S["body"]))
    story.append(sp(8))

    # ── 2. PDF generation ──
    story.append(P("2. Professional PDF Generation with ReportLab", S["h2"]))
    story.append(P(
        "Three separate PDF documents were generated across the project, each with distinct "
        "content and identical visual brand consistency:",
        S["body"]))
    story.append(sp(6))
    pdf_rows = [
        ("Architecture PDF",       "1,213 lines", "System design, component breakdown, API reference"),
        ("Business Case PDF",      "818 lines",   "Cover, exec summary, problem analysis, ROI, roadmap"),
        ("AWS Deployment PDF",     "1,033 lines", "EC2 specs, VPC, security, request flow, CI/CD"),
        ("Prompt Template PDF",    "540 lines",   "CLAUDE.md docs, SYSTEM_PROMPT reference, format spec"),
        ("Blog Post PDF",          "this file",   "Full developer blog post with timeline and analysis"),
    ]
    story.append(styled_table(
        ["Document", "Generator Size", "Contents"],
        pdf_rows, S,
        col_widths=[CONTENT_W * 0.30, CONTENT_W * 0.20, CONTENT_W * 0.50],
    ))
    story.append(sp(6))
    story.append(P(
        "ReportLab is notoriously verbose. Claude Code held the entire visual system — navy/teal/gold "
        "palette, custom Flowable subclasses, page background functions, frame geometry — consistently "
        "across all five generators without a style reference document.",
        S["body"]))
    story.append(sp(8))

    story.append(PageBreak())

    # ── 3. Precision rebranding ──
    story.append(P("3. Precision Codebase Refactoring", S["h2"]))
    story.append(P(
        "When the hospital name changed from Mercy to Adviava, Claude Code found every occurrence "
        "across the codebase — not just in obvious places like the homepage header, but in the "
        "agent system prompt, PDF footer metadata, startup script banners, and intake form "
        "organisation header. Eight occurrences across six files. Zero missed. Zero broken.",
        S["body"]))
    story.append(sp(4))
    story.append(PullQuote(
        "Refactoring that would take a developer 20 minutes of grep-and-verify "
        "took Claude Code one tool call.",
        accent=NAVY))
    story.append(sp(8))

    # ── 4. Prompt engineering ──
    story.append(P("4. Structured Prompt Engineering", S["h2"]))
    story.append(P(
        "The original SYSTEM_PROMPT was 15 lines — functional but flat. Claude Code rewrote it "
        "into a structured 4-section template that the agent can use as an operational reference:",
        S["body"]))
    for item in [
        "<b>Role statement</b> — identity, audience, and the hard boundary (no autonomous clinical decisions)",
        "<b>Tool routing guide</b> — which MCP tool to call for each query type, reducing unnecessary tool invocations",
        "<b>Clinical reference tables</b> — ESI triage levels and abnormal vital sign thresholds baked in",
        "<b>Safety rules</b> — five non-negotiable guardrails encoded as prompt constraints",
    ]:
        story.append(bullet(item, S))
    story.append(P(
        "The prompt went from a style guide to an operational specification. The agent now has "
        "enough context to handle edge cases — patient not found, write SQL attempt, allergy "
        "conflict — without needing additional instructions.",
        S["body"]))
    story.append(sp(8))

    # ── 5. Documentation ──
    story.append(P("5. Documentation That Developers Actually Use", S["h2"]))
    story.append(P(
        "Documentation is often the first thing dropped under time pressure. Claude Code produced "
        "three distinct documentation artefacts that are genuinely useful:",
        S["body"]))
    for item in [
        "<b>README.md</b> (745 lines) — ASCII architecture diagrams, installation walkthrough, "
        "API reference, MCP tools table, DB schema, troubleshooting. Written in 5 minutes.",
        "<b>CLAUDE.md</b> — Project context prompt that loads into every future Claude Code "
        "session automatically. Architecture, key files, conventions, and constraints "
        "captured before they could be forgotten.",
        "<b>Prompt Template PDF</b> — A 7-page reference document that non-technical clinical "
        "governance stakeholders can read to understand exactly how the AI is instructed to behave.",
    ]:
        story.append(bullet(item, S))
    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Honest Assessment ──────────────────────────────────────────────────────────
def make_assessment(S):
    story = []
    story.append(P("An Honest Assessment", S["h1"]))
    story.append(hr())
    story.append(sp(4))
    story.append(P(
        "Claude Code is a powerful tool. But the goal of this post is accuracy, not advocacy. "
        "Here's a balanced look at where it excelled and where human input was still essential.",
        S["body"]))
    story.append(sp(8))

    story.append(P("Where Claude Code Excelled", S["h2"]))
    wins = [
        ("Speed",           "Tasks that would take hours took minutes. The first commit alone "
                            "would have been a full day's work for a solo developer."),
        ("Consistency",     "Brand palette, code style, and architectural patterns stayed "
                            "consistent across every file and every session without a style guide."),
        ("Breadth",         "Switching from Python backend to HTML frontend to ReportLab PDF "
                            "generation to Markdown documentation in the same session with no "
                            "context loss."),
        ("Error handling",  "Pydantic models, FastAPI lifespan management, MCP subprocess "
                            "teardown, SQLite connection handling — all done correctly without "
                            "prompting."),
        ("Refactoring",     "Codebase-wide changes (rebrand, prompt restructure) executed with "
                            "precision — no regressions, no half-finished edits."),
    ]
    story.append(styled_table(
        ["Area", "Observation"],
        wins, S,
        col_widths=[CONTENT_W * 0.22, CONTENT_W * 0.78],
    ))

    story.append(sp(10))
    story.append(P("Where Human Judgment Was Essential", S["h2"]))
    story.append(P(
        "Claude Code executes. It does not decide what to build, who to build it for, or "
        "what the safety constraints should be. These decisions required human input:",
        S["body"]))
    for item in [
        "<b>Clinical domain knowledge</b> — the specific ESI triage level definitions, vital sign thresholds, and allergy warning protocols came from the human, not the model",
        "<b>Architectural choices</b> — the decision to use MCP over a direct function call approach, and the stateless per-request agent design, were human-made",
        "<b>Scope and restraint</b> — knowing when <i>not</i> to add a feature (no session memory, no autonomous writes) required judgment the model deferred to",
        "<b>Product direction</b> — the business case framing, the rebranding, and the decision to generate PDFs as artefacts were human-driven",
    ]:
        story.append(bullet(item, S))

    story.append(sp(8))
    story.append(PullQuote(
        "The developer's job shifted from writing code to making decisions. "
        "Claude Code handled the execution; the human handled the judgement.",
        accent=GREEN))
    story.append(sp(10))
    story.append(PageBreak())
    return story


# ── Key Takeaways ──────────────────────────────────────────────────────────────
def make_takeaways(S):
    story = []
    story.append(P("Key Takeaways for Development Teams", S["h1"]))
    story.append(hr())
    story.append(sp(6))

    takeaways = [
        (TEAL,   "1",  "Start with CLAUDE.md",
         "Write a project context file at the start of every project. It takes 10 minutes and "
         "saves hours of repeated context-setting across sessions. Every architectural decision, "
         "key file, and convention captured there pays dividends on every future task."),
        (NAVY,   "2",  "Give it the whole problem, not a slice",
         "Claude Code performs best when given a complete task with clear requirements. "
         "\"Build a FastAPI backend with these endpoints and this data model\" produces better "
         "results than iterating through each component separately."),
        (GREEN,  "3",  "Prompt engineering is real engineering",
         "The SYSTEM_PROMPT for the AI agent is as important as the application code. Structure "
         "it like a specification — role, tools, reference data, format rules, safety constraints. "
         "A flat prompt produces flat behaviour."),
        (PURPLE, "4",  "Use it for documentation too",
         "The instinct is to use AI tools for code and write docs yourself. Reverse it. Claude "
         "Code produces better documentation faster than most developers write it, and CLAUDE.md "
         "ensures those docs stay in sync with the project automatically."),
        (RED,    "5",  "Keep humans in the safety loop",
         "In any safety-critical domain — healthcare, finance, legal — the human defines the "
         "guardrails and the AI enforces them. The five safety rules in this project's SYSTEM_PROMPT "
         "came from human clinical judgment, not from the model."),
        (GOLD,   "6",  "Commit frequently with descriptive messages",
         "Claude Code co-authors commits. Treating each logical change as a discrete commit "
         "with a meaningful message (not just 'update') creates a readable history that explains "
         "not just what changed, but why."),
    ]

    for colour, num, title, body in takeaways:
        class TakeawayCard(Flowable):
            def __init__(self, c, n, t, b, w=CONTENT_W):
                super().__init__()
                self.c = c; self.n = n; self.t = t; self.b = b
                self.width = w; self.height = 64

            def draw(self):
                from reportlab.lib.utils import simpleSplit
                self.canv.setFillColor(LIGHT_BG)
                self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
                self.canv.setFillColor(self.c)
                self.canv.roundRect(0, 0, 6, self.height, 3, fill=1, stroke=0)
                # number circle
                self.canv.setFillColor(self.c)
                self.canv.circle(24, self.height - 18, 9, fill=1, stroke=0)
                self.canv.setFont("Helvetica-Bold", 9)
                self.canv.setFillColor(WHITE)
                self.canv.drawCentredString(24, self.height - 21, self.n)
                # title
                self.canv.setFont("Helvetica-Bold", 10)
                self.canv.setFillColor(self.c)
                self.canv.drawString(40, self.height - 21, self.t)
                # body
                self.canv.setFont("Helvetica", 8.5)
                self.canv.setFillColor(MID_GREY)
                lines = simpleSplit(self.b, "Helvetica", 8.5, self.width - 48)
                y = self.height - 35
                for line in lines[:4]:
                    self.canv.drawString(40, y, line)
                    y -= 12

        story.append(TakeawayCard(colour, num, title, body))
        story.append(sp(6))

    story.append(sp(8))
    story.append(PageBreak())
    return story


# ── Closing ────────────────────────────────────────────────────────────────────
def make_closing(S):
    story = []
    story.append(P("Closing Thoughts", S["h1"]))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "The Adviava ED AI Agent is a genuinely useful piece of healthcare technology. "
        "It runs in production on AWS, it handles real clinical queries, and it surfaces "
        "patient information faster than navigating an EHR. It was built in roughly 24 hours "
        "by one person with Claude Code as their primary tool.",
        S["body"]))
    story.append(sp(6))
    story.append(P(
        "That timeline would have been impossible without AI-assisted development. Not because "
        "any single piece of the stack is beyond a skilled developer — it isn't — but because "
        "the combination of full-stack breadth, documentation quality, visual design consistency, "
        "and clinical domain precision would have taken weeks to achieve at this quality level "
        "working alone.",
        S["body"]))
    story.append(sp(6))
    story.append(P(
        "The more interesting shift is not in speed. It's in what the developer actually does. "
        "When execution is fast and reliable, the bottleneck moves to decisions: what to build, "
        "who it's for, what it must never do, and how it should behave at the edges. "
        "Those are the right questions for a developer to be spending their time on.",
        S["body"]))
    story.append(sp(10))

    story.append(PullQuote(
        "Claude Code compresses the distance between an idea and a running system. "
        "What you do with that compression is still entirely up to you.",
        accent=TEAL))

    story.append(sp(12))
    story.append(P("Technology Stack", S["h2"]))
    story.append(TagRow([
        "FastAPI", "LangGraph", "Claude Sonnet 4.6", "MCP", "SQLite",
        "ReportLab",
    ]))
    story.append(sp(6))
    story.append(TagRow([
        "AWS EC2", "Python 3.11", "HTML5 / CSS3", "Claude Code", "GitHub",
    ]))
    story.append(sp(16))
    story.append(hr())
    story.append(sp(6))
    story.append(P(
        "<b>Repository:</b> github.com/arjakki/pntdigappproj  ·  "
        "<b>Live:</b> http://18.224.64.93:8000",
        S["italic"]))
    story.append(P(
        "Adviava Regional Medical Center  |  Digital Health  |  April 2026  |  For Internal Use",
        S["footer"]))
    return story


# ── Assembly ───────────────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    S = make_styles()

    cover_frame = Frame(
        MARGIN + 8 * mm, 14 * mm, CONTENT_W - 8 * mm, H - 28 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    inner_frame = Frame(
        MARGIN + 4 * mm, 16 * mm, CONTENT_W - 4 * mm, H - 32 * mm,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )

    doc = BaseDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=16 * mm, bottomMargin=16 * mm,
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_background),
        PageTemplate(id="inner", frames=[inner_frame], onPage=inner_background),
    ])

    story = []
    story += make_cover(S)
    story.insert(1, NextPageTemplate("inner"))
    story += make_intro(S)
    story += make_what_we_built(S)
    story += make_timeline(S)
    story += make_deep_dives(S)
    story += make_assessment(S)
    story += make_takeaways(S)
    story += make_closing(S)

    doc.build(story)
    print(f"PDF saved: {output_path}")


if __name__ == "__main__":
    out = Path("Adviava_ED_AI_Agent_Blog_Post.pdf")
    build_pdf(str(out))
