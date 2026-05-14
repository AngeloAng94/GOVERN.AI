"""
GOVERN.AI — User Manual PDF Generator
Generates branded PDFs from the Markdown user manuals (IT + EN).
Updated: 14 May 2026 — MVP v3.0
"""
import io
import os
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)

C = {
    "bg": colors.HexColor("#020617"),
    "bg2": colors.HexColor("#0f172a"),
    "card": colors.HexColor("#1e293b"),
    "accent": colors.HexColor("#1e3a5f"),
    "white": colors.HexColor("#f8fafc"),
    "light": colors.HexColor("#e2e8f0"),
    "muted": colors.HexColor("#94a3b8"),
    "dim": colors.HexColor("#64748b"),
    "green": colors.HexColor("#22c55e"),
    "blue": colors.HexColor("#3b82f6"),
    "border": colors.HexColor("#334155"),
    "code_bg": colors.HexColor("#0b1224"),
}

PAGE_W, PAGE_H = A4
MARGIN = 22 * mm


def get_styles():
    return {
        "h1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=20, textColor=C["white"], leading=26, spaceBefore=18, spaceAfter=10, keepWithNext=True),
        "h2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14, textColor=C["blue"], leading=18, spaceBefore=14, spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, textColor=C["light"], leading=14, spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, alignment=TA_JUSTIFY, spaceAfter=4),
        "bullet": ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, leftIndent=14, bulletIndent=4, spaceAfter=2),
        "code": ParagraphStyle("Code", fontName="Courier", fontSize=8.5, textColor=C["green"], leading=12, leftIndent=10, backColor=C["code_bg"], borderPadding=4, spaceAfter=4),
        "small": ParagraphStyle("Small", fontName="Helvetica", fontSize=8, textColor=C["muted"], leading=11, spaceAfter=2),
        "quote": ParagraphStyle("Quote", fontName="Helvetica-Oblique", fontSize=9, textColor=C["muted"], leading=13, leftIndent=14, spaceAfter=4),
    }


def draw_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Header
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, PAGE_H - 18 * mm, PAGE_W, 18 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 13)
    canvas_obj.drawString(MARGIN, PAGE_H - 11 * mm, "GOVERN.AI")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawString(MARGIN, PAGE_H - 14.5 * mm, "Operational Manual")
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 9)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 11 * mm, "MVP v3.0")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 14.5 * mm, "14 May 2026")
    # Footer
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.setLineWidth(0.3)
    canvas_obj.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(MARGIN, 8 * mm, "GOVERN.AI by ANTHERA Systems")
    canvas_obj.drawCentredString(PAGE_W / 2, 8 * mm, f"Page {doc.page}")
    canvas_obj.drawRightString(PAGE_W - MARGIN, 8 * mm, "Confidential")
    canvas_obj.restoreState()


def draw_cover(canvas_obj, doc, subtitle, lang):
    canvas_obj.saveState()
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
    # Title
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 44)
    canvas_obj.drawString(MARGIN, PAGE_H - 80 * mm, "GOVERN.AI")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 14)
    canvas_obj.drawString(MARGIN, PAGE_H - 90 * mm, "Sovereign Control Plane for Enterprise AI")
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.line(MARGIN, PAGE_H - 96 * mm, PAGE_W - MARGIN, PAGE_H - 96 * mm)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.setFont("Helvetica-Bold", 14)
    canvas_obj.drawString(MARGIN, PAGE_H - 108 * mm, subtitle)
    # Meta
    meta_y = PAGE_H - 124 * mm
    canvas_obj.setFillColor(C["light"])
    canvas_obj.setFont("Helvetica", 10)
    label_ver = "Version" if lang == "en" else "Versione"
    label_date = "Date" if lang == "en" else "Data"
    label_author = "Author" if lang == "en" else "Autore"
    label_audience = "Audience" if lang == "en" else "Destinatari"
    canvas_obj.drawString(MARGIN, meta_y, f"{label_ver}: MVP 3.0")
    canvas_obj.drawString(MARGIN, meta_y - 16, f"{label_date}: 14 May 2026" if lang == "en" else f"{label_date}: 14 Maggio 2026")
    canvas_obj.drawString(MARGIN, meta_y - 32, f"{label_author}: ANTHERA Systems")
    canvas_obj.drawString(MARGIN, meta_y - 48, f"{label_audience}: Compliance, DPO, CISO, AI Engineer, DevOps")
    # Footer info
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(MARGIN, 30 * mm, "Angelo Anglani — Founder & Lead Engineer")
    canvas_obj.drawString(MARGIN, 25 * mm, "angelo.anglani94@gmail.com | +39 342 754 8655")
    canvas_obj.drawString(MARGIN, 20 * mm, "linkedin.com/in/angelo-anglani")
    canvas_obj.restoreState()


def make_table(headers, rows):
    cols = len(headers)
    avail = PAGE_W - 2 * MARGIN
    # Smart widths: first column narrower if 2-3 cols, else equal
    if cols == 2:
        col_widths = [avail * 0.35, avail * 0.65]
    elif cols == 3:
        col_widths = [avail * 0.25, avail * 0.30, avail * 0.45]
    elif cols == 4:
        col_widths = [avail * 0.20, avail * 0.25, avail * 0.30, avail * 0.25]
    elif cols == 5:
        col_widths = [avail * 0.16, avail * 0.21, avail * 0.21, avail * 0.21, avail * 0.21]
    elif cols == 6:
        col_widths = [avail / 6] * 6
    else:
        col_widths = [avail / cols] * cols
    S = get_styles()
    # Wrap cell content in Paragraphs to enable wrapping
    wrap_style = ParagraphStyle("cell", fontName="Helvetica", fontSize=8, textColor=C["light"], leading=11)
    head_style = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8, textColor=C["white"], leading=11)
    data = [[Paragraph(_md_inline(h), head_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(_md_inline(c), wrap_style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), C["accent"]),
        ("GRID", (0, 0), (-1, -1), 0.4, C["border"]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        bg = C["bg2"] if i % 2 == 0 else C["card"]
        style.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style))
    return t


def _md_inline(text):
    """Translate basic MD inline formatting to ReportLab tags."""
    if not isinstance(text, str):
        return str(text)
    # Escape & < > for ReportLab safety (we want bold to survive)
    text = text.replace("&", "&amp;")
    # Restore the entities for bold/italic processing
    # Bold **x**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Inline code `x`
    text = re.sub(r"`([^`]+?)`", r'<font name="Courier" color="#22c55e">\1</font>', text)
    # Escape standalone < > (after tag substitution they remain only in user content)
    # Keep <b> and <font> tags but escape angle brackets in other patterns:
    # Already done. Return as-is.
    return text


def parse_markdown_to_flowables(md_text):
    """Naive but effective parser for our specific Markdown style."""
    S = get_styles()
    elements = []
    lines = md_text.split("\n")
    i = 0
    in_code = False
    code_lines = []

    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer
        for b in bullet_buffer:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {_md_inline(b)}", S["bullet"]))
        bullet_buffer = []

    while i < len(lines):
        line = lines[i].rstrip()

        # Code block
        if line.strip().startswith("```"):
            flush_bullets()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                code_text = "\n".join(code_lines)
                # Escape HTML-like for code
                code_text = (code_text.replace("&", "&amp;")
                             .replace("<", "&lt;")
                             .replace(">", "&gt;"))
                elements.append(Paragraph(code_text.replace("\n", "<br/>"), S["code"]))
                code_lines = []
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Tables (start with | and next line has |---|)
        if line.startswith("|") and (i + 1) < len(lines) and re.match(r"^\|[\s\-:|]+\|\s*$", lines[i + 1]):
            flush_bullets()
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                # Pad/truncate to match headers length
                if len(row_cells) < len(headers):
                    row_cells += [""] * (len(headers) - len(row_cells))
                else:
                    row_cells = row_cells[:len(headers)]
                rows.append(row_cells)
                i += 1
            elements.append(make_table(headers, rows))
            elements.append(Spacer(1, 4))
            continue

        # Horizontal rule
        if line.strip() == "---":
            flush_bullets()
            elements.append(Spacer(1, 4))
            elements.append(HRFlowable(width="100%", thickness=0.6, color=C["border"]))
            elements.append(Spacer(1, 4))
            i += 1
            continue

        # Headings
        if line.startswith("# "):
            flush_bullets()
            elements.append(PageBreak())
            elements.append(Paragraph(_md_inline(line[2:].strip()), S["h1"]))
            i += 1
            continue
        if line.startswith("## "):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line[3:].strip()), S["h2"]))
            i += 1
            continue
        if line.startswith("### "):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line[4:].strip()), S["h3"]))
            i += 1
            continue

        # Bullets
        if line.startswith("- ") or line.startswith("* "):
            bullet_buffer.append(line[2:].strip())
            i += 1
            continue

        # Numbered list
        m_num = re.match(r"^\d+\.\s+(.*)$", line)
        if m_num:
            bullet_buffer.append(m_num.group(1))
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line.lstrip("> ").strip()), S["quote"]))
            i += 1
            continue

        # Empty line
        if line.strip() == "":
            flush_bullets()
            i += 1
            continue

        # Paragraph
        flush_bullets()
        # Collect multi-line paragraph
        para_lines = [line]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not lines[j].startswith(("#", "-", "*", "|", "```", ">")) and not re.match(r"^\d+\.\s+", lines[j]) and lines[j].strip() != "---":
            para_lines.append(lines[j].rstrip())
            j += 1
        para = " ".join(para_lines)
        elements.append(Paragraph(_md_inline(para), S["body"]))
        i = j

    flush_bullets()
    return elements


def build_manual_pdf(md_path, lang):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Strip top-level "# GOVERN.AI — ..." title (already on cover)
    md_text = re.sub(r"^# GOVERN\.AI[^\n]*\n", "", md_text)

    subtitle = "OPERATIONAL MANUAL" if lang == "en" else "MANUALE OPERATIVO"

    buf = io.BytesIO()
    elements = parse_markdown_to_flowables(md_text)

    def cover_handler(canvas_obj, doc):
        draw_cover(canvas_obj, doc, subtitle, lang)

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=22 * mm, bottomMargin=18 * mm,
    )
    doc.build(elements, onFirstPage=cover_handler, onLaterPages=draw_page)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    print("Generating User Manual IT...")
    pdf_it = build_manual_pdf("/app/GOVERN_AI_USER_MANUAL_IT.md", "it")
    out_it = "/app/GOVERN_AI_USER_MANUAL_IT.pdf"
    with open(out_it, "wb") as f:
        f.write(pdf_it)
    print(f"  -> {out_it} ({len(pdf_it)} bytes)")

    print("Generating User Manual EN...")
    pdf_en = build_manual_pdf("/app/GOVERN_AI_USER_MANUAL_EN.md", "en")
    out_en = "/app/GOVERN_AI_USER_MANUAL_EN.pdf"
    with open(out_en, "wb") as f:
        f.write(pdf_en)
    print(f"  -> {out_en} ({len(pdf_en)} bytes)")

    print("All manuals generated successfully!")
