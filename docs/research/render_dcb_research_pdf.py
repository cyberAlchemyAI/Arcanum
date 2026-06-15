from pathlib import Path
import re
import textwrap

from fpdf import FPDF


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "dcb-vs-multi-aggregate-append.md"
OUTPUT = ROOT / "dcb-vs-multi-aggregate-append.pdf"


class ResearchPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, "Dynamic Consistency Boundaries vs. Multi-Aggregate-Append Transactions", 0, 0, "L")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def clean_inline(text: str) -> str:
    text = text.replace("`", "")
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return text


def add_wrapped(pdf: FPDF, text: str, width_chars: int = 95, line_height: float = 5.2, indent: int = 0):
    text = clean_inline(text)
    wrapper = textwrap.TextWrapper(width=width_chars, subsequent_indent="", break_long_words=True)
    left = pdf.l_margin + indent
    usable_width = pdf.w - pdf.r_margin - left
    for line in wrapper.wrap(text) or [""]:
        pdf.set_x(left)
        pdf.multi_cell(usable_width, line_height, line)


def render_markdown():
    content = SOURCE.read_text(encoding="utf-8").splitlines()
    pdf = ResearchPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    in_code = False
    code_lines = []
    in_quote = False

    def flush_code():
        nonlocal code_lines
        if not code_lines:
            return
        pdf.set_fill_color(245, 247, 250)
        pdf.set_draw_color(215, 220, 228)
        pdf.set_text_color(35, 35, 35)
        pdf.set_font("Courier", "", 8.5)
        for code_line in code_lines:
            pdf.set_x(pdf.l_margin)
            width = pdf.w - pdf.l_margin - pdf.r_margin
            wrapped = textwrap.wrap(code_line, width=78, break_long_words=True) or [""]
            for part in wrapped:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(width, 4.6, part, border=0, fill=True)
        pdf.ln(2)
        code_lines = []

    for raw in content:
        line = raw.rstrip()

        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line:
            pdf.ln(2.5)
            continue

        if line.startswith("# "):
            title = line[2:]
            pdf.set_text_color(26, 38, 58)
            pdf.set_font("Helvetica", "B", 20)
            pdf.multi_cell(0, 9, title)
            pdf.ln(2)
            continue

        if line.startswith("## "):
            if pdf.get_y() > 245:
                pdf.add_page()
            pdf.ln(3)
            pdf.set_text_color(26, 38, 58)
            pdf.set_font("Helvetica", "B", 13)
            pdf.multi_cell(0, 7, line[3:])
            pdf.ln(1)
            continue

        if line.startswith("- "):
            pdf.set_text_color(45, 45, 45)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_x(pdf.l_margin + 5)
            pdf.cell(4, 5.2, "-")
            add_wrapped(pdf, line[2:], width_chars=88, line_height=5.2, indent=11)
            continue

        if line.startswith("> "):
            if not in_quote:
                pdf.ln(1)
            in_quote = True
            pdf.set_text_color(50, 65, 85)
            pdf.set_font("Helvetica", "I", 10)
            add_wrapped(pdf, line[2:], width_chars=86, line_height=5.4, indent=5)
            continue

        if in_quote:
            pdf.ln(1)
            in_quote = False

        if line.startswith("Prepared:"):
            pdf.set_text_color(90, 90, 90)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.multi_cell(0, 5, line)
            pdf.ln(4)
            continue

        pdf.set_text_color(35, 35, 35)
        pdf.set_font("Helvetica", "", 10)
        add_wrapped(pdf, line, width_chars=96, line_height=5.4)

    pdf.output(str(OUTPUT))


if __name__ == "__main__":
    render_markdown()
    print(OUTPUT)
