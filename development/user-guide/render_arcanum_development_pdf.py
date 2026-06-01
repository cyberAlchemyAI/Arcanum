from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "ARCANUM-DEVELOPMENT-USAGE-GUIDE.print.pdf"

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - (2 * MARGIN)

INK = colors.HexColor("#17212b")
MUTED = colors.HexColor("#5c6875")
HAIRLINE = colors.HexColor("#d5dde5")
PANEL = colors.HexColor("#f5f8fb")
TEAL = colors.HexColor("#0f8f8c")
BLUE = colors.HexColor("#2e6bb8")
INDIGO = colors.HexColor("#5a5bc7")
AMBER = colors.HexColor("#c98214")
ROSE = colors.HexColor("#c84b64")
GREEN = colors.HexColor("#2f8b57")
SLATE = colors.HexColor("#334155")
LIGHT_TEAL = colors.HexColor("#dff4f2")
LIGHT_BLUE = colors.HexColor("#e8f0fb")
LIGHT_AMBER = colors.HexColor("#fff3dc")
LIGHT_ROSE = colors.HexColor("#fae8ed")
LIGHT_GREEN = colors.HexColor("#e6f4ea")
LIGHT_INDIGO = colors.HexColor("#eeeeff")


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style, bullet_color=TEAL):
    return ListFlowable(
        [
            ListItem(
                Paragraph(item, style),
                bulletColor=bullet_color,
                leftIndent=10,
            )
            for item in items
        ],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontSize=6,
    )


class Rule(Flowable):
    def __init__(self, width=CONTENT_W, color=HAIRLINE):
        super().__init__()
        self.width = width
        self.height = 6
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.7)
        self.canv.line(0, 3, self.width, 3)


class LabeledBoxChart(Flowable):
    def __init__(self, boxes, width=CONTENT_W, height=75 * mm):
        super().__init__()
        self.boxes = boxes
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        row_gap = 10
        box_h = 23
        cols = 3
        box_w = (self.width - (cols - 1) * 8) / cols
        for idx, box in enumerate(self.boxes):
            row = idx // cols
            col = idx % cols
            x = col * (box_w + 8)
            y = self.height - (row + 1) * box_h - row * row_gap
            c.setFillColor(box["fill"])
            c.setStrokeColor(box["stroke"])
            c.roundRect(x, y, box_w, box_h, 5, stroke=1, fill=1)
            c.setFillColor(box["stroke"])
            c.setFont("Helvetica-Bold", 7.4)
            c.drawString(x + 6, y + box_h - 9, box["title"])
            c.setFillColor(INK)
            c.setFont("Helvetica", 6.2)
            draw_wrapped(c, box["body"], x + 6, y + box_h - 17, box_w - 12, 7)
        c.restoreState()


class LifecycleChart(Flowable):
    def __init__(self, width=CONTENT_W, height=83 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.setStrokeColor(HAIRLINE)
        c.roundRect(0, 0, self.width, self.height, 6, stroke=1, fill=1)

        nodes = [
            ("Rich idea", "full prompt", TEAL, LIGHT_TEAL, 15, 50),
            ("Refine", "shape route", BLUE, LIGHT_BLUE, 30, 28),
            ("Invoke", "define/design/plan", INDIGO, LIGHT_INDIGO, 50, 50),
            ("Route gaps", "decide/research/x-ray", AMBER, LIGHT_AMBER, 70, 28),
            ("Task session", "one SWU", GREEN, LIGHT_GREEN, 85, 50),
            ("Evidence", "validate and learn", ROSE, LIGHT_ROSE, 50, 9),
        ]
        positions = {}
        for title, body, stroke, fill, px, py in nodes:
            x = self.width * px / 100 - 27
            y = self.height * py / 100 - 12
            positions[title] = (x, y)
            draw_node(c, x, y, 54, 24, title, body, stroke, fill)

        arrows = [
            ("Rich idea", "Refine"),
            ("Refine", "Invoke"),
            ("Invoke", "Route gaps"),
            ("Route gaps", "Task session"),
            ("Task session", "Evidence"),
            ("Evidence", "Route gaps"),
            ("Route gaps", "Refine"),
        ]
        for src, dst in arrows:
            sx, sy = positions[src]
            dx, dy = positions[dst]
            draw_arrow(
                c,
                sx + 27,
                sy + 12,
                dx + 27,
                dy + 12,
                color=SLATE,
            )

        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(self.width / 2, self.height - 10, "Use the loop every time ambition meets a gap.")
        c.restoreState()


class RefinementTimeline(Flowable):
    def __init__(self, width=CONTENT_W, height=59 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        steps = [
            ("Context", TEAL, "evidence"),
            ("Define", BLUE, "baseline"),
            ("Critique", ROSE, "holes"),
            ("Research", AMBER, "claims"),
            ("Distill", GREEN, "small unit"),
            ("Design", INDIGO, "views"),
            ("Review", ROSE, "risks"),
            ("Repair", AMBER, "scope"),
            ("Plan", BLUE, "work-pack"),
            ("Synthesis", TEAL, "route"),
        ]
        radius = 13
        gap = (self.width - 2 * radius) / (len(steps) - 1)
        y = 35
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(2)
        c.line(radius, y, self.width - radius, y)
        for idx, (label, color, note) in enumerate(steps):
            x = radius + idx * gap
            c.setFillColor(color)
            c.setStrokeColor(colors.white)
            c.circle(x, y, radius, stroke=1, fill=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(x, y - 2.5, str(idx + 1))
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 6.2)
            draw_centered_multiline(c, label, x, y - 22, 38, 6.8)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 5.5)
            c.drawCentredString(x, y - 33, note)
        c.restoreState()


class RouterChart(Flowable):
    def __init__(self, width=CONTENT_W, height=85 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PANEL)
        c.setStrokeColor(HAIRLINE)
        c.roundRect(0, 0, self.width, self.height, 6, stroke=1, fill=1)
        center_x = self.width / 2
        center_y = self.height / 2
        draw_node(c, center_x - 31, center_y - 14, 62, 28, "Plan reveals", "gap or blocker", SLATE, colors.white)
        lanes = [
            ("Human choice", "decision-gate", ROSE, LIGHT_ROSE, 13, 70),
            ("Fuzzy idea", "refine", BLUE, LIGHT_BLUE, 17, 25),
            ("Research lanes", "dispatch-spec", AMBER, LIGHT_AMBER, 50, 80),
            ("Hidden structure", "x-ray", INDIGO, LIGHT_INDIGO, 83, 25),
            ("Ready SWU", "task-session", GREEN, LIGHT_GREEN, 87, 70),
        ]
        for title, tool, stroke, fill, px, py in lanes:
            x = self.width * px / 100 - 31
            y = self.height * py / 100 - 14
            draw_arrow(c, center_x, center_y, x + 31, y + 14, stroke)
            draw_node(c, x, y, 62, 28, title, tool, stroke, fill)
        c.restoreState()


class EvidenceLadder(Flowable):
    def __init__(self, width=CONTENT_W, height=65 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        steps = [
            ("Idea", 22, TEAL, "rich prompt"),
            ("Definition", 35, BLUE, "scope and names"),
            ("Design", 48, INDIGO, "views and trade-offs"),
            ("Plan", 61, AMBER, "layers and SWUs"),
            ("Execution", 74, GREEN, "task-session"),
            ("Evidence", 87, ROSE, "receipts"),
        ]
        base = 11
        left = 8
        max_w = self.width - 16
        for idx, (label, pct, color, note) in enumerate(steps):
            y = base + idx * 9
            w = max_w * pct / 100
            c.setFillColor(colors.Color(color.red, color.green, color.blue, alpha=0.18))
            c.setStrokeColor(color)
            c.roundRect(left, y, w, 6, 2.5, stroke=1, fill=1)
            c.setFillColor(color)
            c.setFont("Helvetica-Bold", 6.4)
            c.drawString(left + 3, y + 1.5, label)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 6)
            c.drawRightString(left + max_w, y + 1.5, note)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left, self.height - 8, "Evidence should get heavier as mutation gets real.")
        c.restoreState()


class AmbitionWheel(Flowable):
    def __init__(self, width=CONTENT_W, height=88 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        cx = self.width / 2
        cy = self.height / 2
        spokes = [
            ("refine", "shape the ambition", TEAL, 90),
            ("invoke", "author artifacts", BLUE, 45),
            ("guide", "teach the route", GREEN, 0),
            ("x-ray", "make structure visible", INDIGO, -45),
            ("ux evidence", "test finished UI", ROSE, -90),
            ("whisper", "write with intent", AMBER, -135),
            ("dispatch", "research in lanes", SLATE, 180),
            ("task-session", "ship one unit", GREEN, 135),
        ]
        c.setFillColor(colors.white)
        c.setStrokeColor(HAIRLINE)
        c.circle(cx, cy, 25, stroke=1, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cx, cy + 3, "Ambitious")
        c.drawCentredString(cx, cy - 6, "tool idea")
        for title, note, color, angle in spokes:
            import math

            r = 63
            x = cx + math.cos(math.radians(angle)) * r
            y = cy + math.sin(math.radians(angle)) * r
            c.setStrokeColor(color)
            c.setLineWidth(1.1)
            c.line(cx, cy, x, y)
            draw_node(c, x - 32, y - 13, 64, 26, title, note, color, colors.white)
        c.restoreState()


def draw_node(c, x, y, w, h, title, body, stroke, fill):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.9)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
    c.setFillColor(stroke)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + w / 2, y + h - 9, title)
    c.setFillColor(INK)
    c.setFont("Helvetica", 5.8)
    draw_centered_multiline(c, body, x + w / 2, y + h - 17, w - 8, 6)


def draw_arrow(c, x1, y1, x2, y2, color=SLATE):
    import math

    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(0.8)
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length < 1:
        c.restoreState()
        return
    ux = dx / length
    uy = dy / length
    start_x = x1 + ux * 28
    start_y = y1 + uy * 13
    end_x = x2 - ux * 33
    end_y = y2 - uy * 15
    c.line(start_x, start_y, end_x, end_y)
    angle = math.atan2(dy, dx)
    size = 4
    left = angle + math.pi * 0.82
    right = angle - math.pi * 0.82
    p1 = (end_x, end_y)
    p2 = (end_x + math.cos(left) * size, end_y + math.sin(left) * size)
    p3 = (end_x + math.cos(right) * size, end_y + math.sin(right) * size)
    c.line(*p1, *p2)
    c.line(*p1, *p3)
    c.restoreState()


def draw_wrapped(c, text, x, y, max_w, leading):
    words = text.split()
    line = ""
    lines = []
    for word in words:
        candidate = f"{line} {word}".strip()
        if stringWidth(candidate, "Helvetica", 6.2) <= max_w:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for idx, line_text in enumerate(lines[:3]):
        c.drawString(x, y - idx * leading, line_text)


def draw_centered_multiline(c, text, cx, y, max_w, leading):
    words = text.split()
    line = ""
    lines = []
    font_name = c._fontname
    font_size = c._fontsize
    for word in words:
        candidate = f"{line} {word}".strip()
        if stringWidth(candidate, font_name, font_size) <= max_w:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for idx, line_text in enumerate(lines[:2]):
        c.drawCentredString(cx, y - idx * leading, line_text)


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=31,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14,
            textColor=SLATE,
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.2,
            textColor=INK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9.4,
            textColor=MUTED,
            spaceAfter=4,
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=12,
            textColor=INK,
            backColor=colors.HexColor("#f7fafc"),
            borderColor=HAIRLINE,
            borderWidth=0.6,
            borderPadding=7,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=6.6,
            leading=8.3,
            textColor=INK,
            backColor=colors.HexColor("#f3f6f9"),
            borderColor=HAIRLINE,
            borderWidth=0.4,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "table": ParagraphStyle(
            "table",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7,
            leading=8.7,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "table_head",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.7,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
    }


def table(data, widths, header_color=SLATE):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), header_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("GRID", (0, 0), (-1, -1), 0.35, HAIRLINE),
            ]
        )
    )
    return t


def cover_page(story, styles):
    story.append(Spacer(1, 22 * mm))
    story.append(p("Arcanum Development Usage Guide", styles["title"]))
    story.append(
        p(
            "A printable map for turning an ambitious idea into definition, design, plan, bounded execution, and evidence.",
            styles["subtitle"],
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(LifecycleChart(height=84 * mm))
    story.append(Spacer(1, 6 * mm))
    story.append(
        p(
            "Core promise: do not rush from idea to implementation. Make the idea inspectable, argued, evidenced, planned, and then executed in small verified steps.",
            styles["callout"],
        )
    )
    story.append(
        table(
            [
                [p("Start with", styles["table_head"]), p("End with", styles["table_head"]), p("Repeat when", styles["table_head"])],
                [
                    p("The richest prompt you can write: user, pain, promise, examples, constraints, risks, and unknowns.", styles["table"]),
                    p("One verified task or SWU, with receipts and a next route for remaining residue.", styles["table"]),
                    p("A blocker, research gap, design doubt, validation miss, or new ambition appears.", styles["table"]),
                ],
            ],
            [CONTENT_W * 0.34, CONTENT_W * 0.33, CONTENT_W * 0.33],
            TEAL,
        )
    )
    story.append(PageBreak())


def workflow_page(story, styles):
    story.append(p("1. The Whole Loop", styles["h1"]))
    story.append(
        p(
            "Arcanum development is a loop with explicit ownership. Refine shapes the idea, invoke authors durable artifacts, blocker tools route uncertainty, and task-session executes one ready unit.",
            styles["body"],
        )
    )
    story.append(LifecycleChart(height=80 * mm))
    story.append(Spacer(1, 4 * mm))
    story.append(p("The short version", styles["h2"]))
    story.append(
        p(
            "rich idea prompt -> refine -> invoke define/design/plan -> gaps and blockers -> decision-gate | dispatch-spec | x-ray | refine -> task-session -> validation evidence -> repeat",
            styles["code"],
        )
    )
    story.append(p("What changes as you move right", styles["h2"]))
    story.append(EvidenceLadder(height=61 * mm))
    story.append(PageBreak())


def first_prompt_page(story, styles):
    story.append(p("2. First Prompt Anatomy", styles["h1"]))
    story.append(
        p(
            "The first prompt should be rich, not polished. It gives refine enough material to preserve ambition while finding the next executable route.",
            styles["body"],
        )
    )
    story.append(
        LabeledBoxChart(
            [
                {"title": "User and Promise", "body": "Who it is for, what they should become able to do, and why it matters.", "stroke": TEAL, "fill": LIGHT_TEAL},
                {"title": "Current Reality", "body": "Existing tools, workflows, artifacts, constraints, and visible friction.", "stroke": BLUE, "fill": LIGHT_BLUE},
                {"title": "Ambition", "body": "What makes the idea exciting and what the larger version could become.", "stroke": INDIGO, "fill": LIGHT_INDIGO},
                {"title": "Boundaries", "body": "What should not happen, what should not be inferred, and decisions humans must make.", "stroke": ROSE, "fill": LIGHT_ROSE},
                {"title": "Evidence", "body": "References, examples, screenshots, prior artifacts, and market or research leads.", "stroke": AMBER, "fill": LIGHT_AMBER},
                {"title": "MVP Proof", "body": "What one small successful version would need to prove with evidence.", "stroke": GREEN, "fill": LIGHT_GREEN},
            ],
            height=61 * mm,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(p("Reusable prompt card", styles["h2"]))
    story.append(
        p(
            "[$refine] I want to develop this idea:<br/>"
            "&lt;Describe the idea in as much detail as possible: users, promise, current workflow, missing pieces, constraints, examples, risks, unresolved decisions, MVP proof, and ambitious future.&gt;<br/><br/>"
            "Please refine this into a development route. I want definition, design, plan, gaps, blockers, and the next executable task.",
            styles["code"],
        )
    )
    story.append(PageBreak())


def refine_invoke_page(story, styles):
    story.append(p("3. Refine To Invoke To Plan", styles["h1"]))
    story.append(
        p(
            "Refine is the front door for broad or under-shaped work. Invoke turns the refined direction into durable artifacts that later sessions can execute and inspect.",
            styles["body"],
        )
    )
    story.append(RefinementTimeline(height=58 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(
        table(
            [
                [p("Mode", styles["table_head"]), p("Produces", styles["table_head"]), p("Why it matters", styles["table_head"])],
                [p("invoke define", styles["table"]), p("Definition, glossary, scope, target baseline.", styles["table"]), p("Gives the idea a stable name and boundary.", styles["table"])],
                [p("invoke design", styles["table"]), p("Views, architecture, trade-offs, and consistency checks.", styles["table"]), p("Makes the system understandable before implementation.", styles["table"])],
                [p("invoke plan", styles["table"]), p("Layering, work-pack, SWUs, validation expectations.", styles["table"]), p("Turns design into executable bounded work.", styles["table"])],
                [p("invoke refresh", styles["table"]), p("Proposal-only updates from new evidence.", styles["table"]), p("Keeps artifacts current without silent mutation.", styles["table"])],
                [p("invoke handoff", styles["table"]), p("New session or thread handoff.", styles["table"]), p("Splits ownership without losing context.", styles["table"])],
            ],
            [CONTENT_W * 0.22, CONTENT_W * 0.39, CONTENT_W * 0.39],
            BLUE,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "A proposal-only result can be a useful route, but it is not implementation evidence. Treat runtime gaps, missing approvals, and unresolved decisions as first-class outputs.",
            styles["callout"],
        )
    )
    story.append(PageBreak())


def blocker_router_page(story, styles):
    story.append(p("4. Gap And Blocker Router", styles["h1"]))
    story.append(
        p(
            "A good plan reveals gaps. Do not smooth them over. Route each gap to the capability that can resolve it with the right kind of evidence.",
            styles["body"],
        )
    )
    story.append(RouterChart(height=83 * mm))
    story.append(Spacer(1, 3 * mm))
    rows = [
        [p("Situation", styles["table_head"]), p("Use", styles["table_head"]), p("Reason", styles["table_head"])],
        [p("Consequential choice with multiple viable options.", styles["table"]), p("decision-gate", styles["table"]), p("Records options, trade-offs, decision, and blocked state.", styles["table"])],
        [p("Idea, design, or plan still feels broad.", styles["table"]), p("refine", styles["table"]), p("Runs another refinement pass around the gap.", styles["table"])],
        [p("Multiple research streams or reusable route.", styles["table"]), p("dispatch-spec", styles["table"]), p("Creates lanes, gates, handoffs, and observability.", styles["table"])],
        [p("Architecture or workflow is hard to see.", styles["table"]), p("x-ray", styles["table"]), p("Explains parts, dependencies, flow, lifecycle, and risks.", styles["table"])],
        [p("One bounded task is ready.", styles["table"]), p("task-session", styles["table"]), p("Executes one unit with validation and synchronized evidence.", styles["table"])],
    ]
    story.append(table(rows, [CONTENT_W * 0.38, CONTENT_W * 0.22, CONTENT_W * 0.4], AMBER))
    story.append(PageBreak())


def task_session_page(story, styles):
    story.append(p("5. Task Session And Evidence", styles["h1"]))
    story.append(
        p(
            "Task-session is the execution route only after the unit is bounded enough to work safely. It should mutate declared scope, validate done criteria, and report follow-up residue.",
            styles["body"],
        )
    )
    story.append(
        table(
            [
                [p("Ready means", styles["table_head"]), p("Task-session should", styles["table_head"])],
                [
                    bullets(
                        [
                            "The task or SWU is bounded.",
                            "Inputs and source links are known.",
                            "Write scope is clear.",
                            "Blockers are resolved or recorded.",
                            "Validation surface exists.",
                            "Completion evidence is defined.",
                        ],
                        styles["table"],
                        GREEN,
                    ),
                    bullets(
                        [
                            "Build a context pack.",
                            "Evaluate gates.",
                            "Call decision-gate if a blocker-level choice appears.",
                            "Mutate only declared scope.",
                            "Validate done criteria.",
                            "Synchronize task evidence.",
                        ],
                        styles["table"],
                        BLUE,
                    ),
                ],
            ],
            [CONTENT_W * 0.5, CONTENT_W * 0.5],
            GREEN,
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(p("Evidence receipt model", styles["h2"]))
    story.append(EvidenceLadder(height=60 * mm))
    story.append(
        p(
            "A finished interface, sigil, spell, or workflow should leave enough evidence for another person to see what changed, why it changed, and what remains uncertain.",
            styles["callout"],
        )
    )
    story.append(PageBreak())


def designer_page(story, styles):
    story.append(p("6. Designer Ambition Surface", styles["h1"]))
    story.append(
        p(
            "Designers can use Arcanum as a creative amplifier, not just a ticket machine. The system can turn taste, intent, research, structure, and validation evidence into tools that teams can reuse.",
            styles["body"],
        )
    )
    story.append(AmbitionWheel(height=86 * mm))
    story.append(Spacer(1, 2 * mm))
    story.append(
        table(
            [
                [p("Capability", styles["table_head"]), p("How a designer can use it", styles["table_head"])],
                [p("whisper", styles["table"]), p("Shape the voice, constraints, review prompts, and writing residues of a tool or interface.", styles["table"])],
                [p("guide", styles["table"]), p("Create a teachable route so others can use the capability without knowing its internals.", styles["table"])],
                [p("x-ray", styles["table"]), p("Make hidden flows, dependencies, assumptions, and lifecycle states understandable.", styles["table"])],
                [p("ux evidence validator", styles["table"]), p("Turn finished frontend review into screenshots, measurements, accessibility signals, and human review prompts.", styles["table"])],
                [p("dispatch-spec", styles["table"]), p("Research academic, market, technical, and risk references in separate lanes.", styles["table"])],
                [p("task-session", styles["table"]), p("Build one concrete piece at a time while preserving proof and residue.", styles["table"])],
            ],
            [CONTENT_W * 0.28, CONTENT_W * 0.72],
            INDIGO,
        )
    )
    story.append(PageBreak())


def prompt_cards_page(story, styles):
    story.append(p("7. Printable Prompt Cards", styles["h1"]))
    cards = [
        (
            "Decision Gate",
            "[$decision-gate] Resolve the blocker for &lt;target&gt;.<br/>Context: current plan, consequential choice, visible options, affected artifacts, and what must not proceed until this is decided.",
            ROSE,
        ),
        (
            "Dispatch Spec",
            "[$dispatch-spec] Create a research route for &lt;topic&gt;.<br/>Streams: source truth, market practice, implementation, risks, validation or fixtures. Output: source ledger, claim map, implications, blockers.",
            AMBER,
        ),
        (
            "X-Ray",
            "[$x-ray] Explain &lt;target&gt; for &lt;audience&gt;.<br/>Focus: what it is, parts, responsibilities, flows, dependencies, lifecycle, assumptions, risks, open questions, next route.",
            INDIGO,
        ),
        (
            "Task Session",
            "[$task-session] Execute &lt;work-pack path&gt; --task &lt;TASK-ID&gt;<br/>Use only when the unit is bounded, scope is known, blockers are handled, and evidence expectations are clear.",
            GREEN,
        ),
    ]
    for title, body, color in cards:
        data = [[p(title, styles["table_head"])], [p(body, styles["code"])]]
        t = Table(data, colWidths=[CONTENT_W], hAlign="LEFT")
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("BOX", (0, 0), (-1, -1), 0.6, color),
                ]
            )
        )
        story.append(KeepTogether([t, Spacer(1, 4 * mm)]))
    story.append(PageBreak())


def closing_page(story, styles):
    story.append(p("8. What Good Looks Like", styles["h1"]))
    story.append(
        p(
            "Good Arcanum development leaves a trail: definition, design, plan, decisions, research, x-rays, task receipts, residues, and the next bounded step.",
            styles["body"],
        )
    )
    story.append(
        LabeledBoxChart(
            [
                {"title": "Clear Definition", "body": "A stable name, purpose, boundary, and vocabulary.", "stroke": BLUE, "fill": LIGHT_BLUE},
                {"title": "Visible Design", "body": "Multiple views, trade-offs, dependencies, and risks.", "stroke": INDIGO, "fill": LIGHT_INDIGO},
                {"title": "Executable Plan", "body": "Layers, SWUs, validators, and completion criteria.", "stroke": GREEN, "fill": LIGHT_GREEN},
                {"title": "Recorded Decisions", "body": "Consequential choices are explicit and durable.", "stroke": ROSE, "fill": LIGHT_ROSE},
                {"title": "Sourced Research", "body": "Claims stay linked to evidence and freshness rules.", "stroke": AMBER, "fill": LIGHT_AMBER},
                {"title": "Validation Receipts", "body": "Finished work has proof, limits, and remaining residue.", "stroke": TEAL, "fill": LIGHT_TEAL},
            ],
            height=61 * mm,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(p("Avoid", styles["h2"]))
    story.append(
        bullets(
            [
                "Jumping straight from idea to implementation.",
                "Running task-session before the task is bounded.",
                "Hiding human decisions inside implementation.",
                "Treating proposal-only refreshes as permission to mutate.",
                "Using research findings as canonical truth without review.",
                "Claiming MVP completion without validation evidence.",
            ],
            styles["body"],
            ROSE,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(Rule())
    story.append(
        p(
            "Source guide: development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md<br/>Generated artifact: development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.print.pdf",
            styles["small"],
        )
    )


def footer(c: canvas.Canvas, doc):
    c.saveState()
    c.setStrokeColor(HAIRLINE)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFont("Helvetica", 6.8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 7.5 * mm, "Arcanum Development Usage Guide")
    c.drawRightString(PAGE_W - MARGIN, 7.5 * mm, f"Page {doc.page}")
    c.restoreState()


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=14 * mm,
        bottomMargin=16 * mm,
        title="Arcanum Development Usage Guide",
        author="Arcanum",
    )
    story = []
    cover_page(story, styles)
    workflow_page(story, styles)
    first_prompt_page(story, styles)
    refine_invoke_page(story, styles)
    blocker_router_page(story, styles)
    task_session_page(story, styles)
    designer_page(story, styles)
    prompt_cards_page(story, styles)
    closing_page(story, styles)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUTPUT)
