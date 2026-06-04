"""
GOVERN.AI / ANTHERA — Investor-grade PDF Design System

Single source of truth for all PDF generators. Designed to look credible in
front of investors, board members, and procurement officers.

Design principles:
- White background (printable, projectable)
- Single institutional accent (deep navy)
- Restrained, predictable typography hierarchy
- Hairline borders, generous whitespace
- Minimal tables (no candy colors), structured numeric data
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    Table, TableStyle, Paragraph, Spacer, HRFlowable, PageBreak,
)

# ─────────────────────────────────────────────────────────────────────
# COLOR PALETTE — investor / boardroom grade
# ─────────────────────────────────────────────────────────────────────
PALETTE = {
    "ink":        colors.HexColor("#0F172A"),   # primary text / headings
    "graphite":   colors.HexColor("#334155"),   # body emphasis
    "slate":      colors.HexColor("#475569"),   # secondary text
    "mute":       colors.HexColor("#64748B"),   # captions, metadata
    "hairline":   colors.HexColor("#E2E8F0"),   # borders, dividers
    "soft_bg":    colors.HexColor("#F8FAFC"),   # alt row bg / callout bg
    "accent":     colors.HexColor("#1E3A5F"),   # primary brand navy
    "accent_dk":  colors.HexColor("#0B2540"),   # darker navy for emphasis
    "accent_lt":  colors.HexColor("#E6EEF7"),   # navy tint for header bg
    "success":    colors.HexColor("#15803D"),   # subtle green
    "warning":    colors.HexColor("#B45309"),   # subtle amber
    "danger":     colors.HexColor("#B91C1C"),   # subtle red
    "white":      colors.HexColor("#FFFFFF"),
}

# Page geometry
PAGE_W, PAGE_H = A4
MARGIN_LR = 22 * mm
MARGIN_TOP = 26 * mm
MARGIN_BOTTOM = 22 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_LR


# ─────────────────────────────────────────────────────────────────────
# TYPOGRAPHY — predictable hierarchy
# ─────────────────────────────────────────────────────────────────────
def get_styles():
    return {
        "h1": ParagraphStyle(
            "H1", fontName="Helvetica-Bold", fontSize=18, leading=24,
            textColor=PALETTE["ink"], spaceBefore=22, spaceAfter=10,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2", fontName="Helvetica-Bold", fontSize=13, leading=18,
            textColor=PALETTE["accent_dk"], spaceBefore=16, spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
            textColor=PALETTE["graphite"], spaceBefore=10, spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=9.5, leading=14,
            textColor=PALETTE["ink"], alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet", fontName="Helvetica", fontSize=9.5, leading=14,
            textColor=PALETTE["ink"], leftIndent=14, bulletIndent=4, spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "Quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
            textColor=PALETTE["slate"], leftIndent=14, rightIndent=10,
            spaceAfter=6, borderColor=PALETTE["hairline"],
            borderWidth=0, borderPadding=0,
            backColor=PALETTE["soft_bg"],
        ),
        "code": ParagraphStyle(
            "Code", fontName="Courier", fontSize=8.5, leading=12,
            textColor=PALETTE["accent_dk"], leftIndent=8, rightIndent=8,
            backColor=PALETTE["soft_bg"], borderPadding=6, spaceAfter=8,
            borderColor=PALETTE["hairline"], borderWidth=0.5,
        ),
        "small": ParagraphStyle(
            "Small", fontName="Helvetica", fontSize=8, leading=11,
            textColor=PALETTE["mute"], spaceAfter=2,
        ),
        "caption": ParagraphStyle(
            "Caption", fontName="Helvetica-Oblique", fontSize=8, leading=11,
            textColor=PALETTE["mute"], alignment=TA_CENTER, spaceAfter=8,
        ),
        "tag": ParagraphStyle(
            "Tag", fontName="Helvetica-Bold", fontSize=7.5, leading=10,
            textColor=PALETTE["accent_dk"], spaceAfter=0,
        ),
    }


# ─────────────────────────────────────────────────────────────────────
# COVER PAGE — restrained, lots of whitespace
# ─────────────────────────────────────────────────────────────────────
def draw_cover(canvas_obj, brand_top, brand_bottom, doc_type, version, date_str,
               author, classification=None, tagline=None, footer_lines=None):
    """Draw a single-color, premium cover page."""
    canvas_obj.saveState()
    # Background: solid white
    canvas_obj.setFillColor(PALETTE["white"])
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Top accent: full-width thin navy stripe
    canvas_obj.setFillColor(PALETTE["accent"])
    canvas_obj.rect(0, PAGE_H - 4, PAGE_W, 4, fill=1, stroke=0)

    # Side accent rule (thin vertical bar near left margin)
    canvas_obj.setFillColor(PALETTE["accent"])
    canvas_obj.rect(MARGIN_LR, PAGE_H - 80 * mm, 1.2, 32 * mm, fill=1, stroke=0)

    # Brand
    canvas_obj.setFillColor(PALETTE["ink"])
    canvas_obj.setFont("Helvetica-Bold", 32)
    canvas_obj.drawString(MARGIN_LR + 6 * mm, PAGE_H - 60 * mm, brand_top)
    if brand_bottom:
        canvas_obj.setFillColor(PALETTE["accent"])
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawString(MARGIN_LR + 6 * mm, PAGE_H - 72 * mm, brand_bottom)

    # Document type
    canvas_obj.setFillColor(PALETTE["slate"])
    canvas_obj.setFont("Helvetica", 11)
    canvas_obj.drawString(MARGIN_LR + 6 * mm, PAGE_H - 84 * mm, doc_type.upper())

    # Divider
    canvas_obj.setStrokeColor(PALETTE["hairline"])
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN_LR, PAGE_H - 96 * mm, PAGE_W - MARGIN_LR, PAGE_H - 96 * mm)

    # Meta block
    meta_y = PAGE_H - 108 * mm
    canvas_obj.setFillColor(PALETTE["mute"])
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.drawString(MARGIN_LR, meta_y, "VERSION")
    canvas_obj.drawString(MARGIN_LR + 55 * mm, meta_y, "DATE")
    canvas_obj.drawString(MARGIN_LR + 110 * mm, meta_y, "AUTHOR")
    canvas_obj.setFillColor(PALETTE["ink"])
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.drawString(MARGIN_LR, meta_y - 14, version)
    canvas_obj.drawString(MARGIN_LR + 55 * mm, meta_y - 14, date_str)
    canvas_obj.drawString(MARGIN_LR + 110 * mm, meta_y - 14, author)

    if classification:
        canvas_obj.setFillColor(PALETTE["mute"])
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.drawString(MARGIN_LR, meta_y - 36, "CLASSIFICATION")
        canvas_obj.setFillColor(PALETTE["ink"])
        canvas_obj.setFont("Helvetica-Bold", 10)
        canvas_obj.drawString(MARGIN_LR, meta_y - 50, classification)

    # Tagline (optional)
    if tagline:
        canvas_obj.setFillColor(PALETTE["accent"])
        canvas_obj.setFont("Helvetica-Oblique", 12)
        canvas_obj.drawString(MARGIN_LR, 70 * mm, tagline)

    # Footer block
    if footer_lines:
        canvas_obj.setStrokeColor(PALETTE["hairline"])
        canvas_obj.line(MARGIN_LR, 38 * mm, PAGE_W - MARGIN_LR, 38 * mm)
        canvas_obj.setFillColor(PALETTE["slate"])
        canvas_obj.setFont("Helvetica", 8.5)
        y = 30 * mm
        for line in footer_lines:
            canvas_obj.drawString(MARGIN_LR, y, line)
            y -= 11

    # Bottom stripe
    canvas_obj.setFillColor(PALETTE["accent"])
    canvas_obj.rect(0, 0, PAGE_W, 4, fill=1, stroke=0)

    canvas_obj.restoreState()


# ─────────────────────────────────────────────────────────────────────
# PAGE HEADER/FOOTER — same look across all docs
# ─────────────────────────────────────────────────────────────────────
def make_page_decorator(brand, doc_type, version, date_str, confidential=True):
    """Return a draw_page handler bound to this doc's metadata."""
    def draw_page(canvas_obj, doc):
        canvas_obj.saveState()
        # Top: brand on the left, doc info on the right
        canvas_obj.setFillColor(PALETTE["ink"])
        canvas_obj.setFont("Helvetica-Bold", 10)
        canvas_obj.drawString(MARGIN_LR, PAGE_H - 14 * mm, brand)
        canvas_obj.setFillColor(PALETTE["mute"])
        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.drawString(MARGIN_LR, PAGE_H - 18 * mm, doc_type)

        canvas_obj.setFillColor(PALETTE["slate"])
        canvas_obj.setFont("Helvetica-Bold", 8.5)
        canvas_obj.drawRightString(PAGE_W - MARGIN_LR, PAGE_H - 14 * mm, version)
        canvas_obj.setFillColor(PALETTE["mute"])
        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.drawRightString(PAGE_W - MARGIN_LR, PAGE_H - 18 * mm, date_str)

        # Thin hairline under header
        canvas_obj.setStrokeColor(PALETTE["hairline"])
        canvas_obj.setLineWidth(0.4)
        canvas_obj.line(MARGIN_LR, PAGE_H - 21 * mm, PAGE_W - MARGIN_LR, PAGE_H - 21 * mm)

        # Footer hairline + line
        canvas_obj.line(MARGIN_LR, 14 * mm, PAGE_W - MARGIN_LR, 14 * mm)
        canvas_obj.setFillColor(PALETTE["mute"])
        canvas_obj.setFont("Helvetica", 7.5)
        canvas_obj.drawString(MARGIN_LR, 9 * mm, f"{brand}  -  ANTHERA Systems")
        canvas_obj.drawCentredString(PAGE_W / 2, 9 * mm, f"Page {doc.page}")
        if confidential:
            canvas_obj.drawRightString(PAGE_W - MARGIN_LR, 9 * mm, "Confidential")
        canvas_obj.restoreState()

    return draw_page


# ─────────────────────────────────────────────────────────────────────
# TABLE — sober, minimal, navy header
# ─────────────────────────────────────────────────────────────────────
def make_table(headers, rows, col_weights=None, first_col_emphasis=False):
    """
    Build a clean institutional table.

    headers / rows: lists of strings (will be wrapped in Paragraph automatically).
    col_weights:    fractional widths summing to ~1.0; if None, smart defaults.
    """
    cols = len(headers)
    if col_weights is None:
        if cols == 2:   col_weights = [0.32, 0.68]
        elif cols == 3: col_weights = [0.22, 0.28, 0.50]
        elif cols == 4: col_weights = [0.18, 0.22, 0.28, 0.32]
        elif cols == 5: col_weights = [0.16] * 5
        else:           col_weights = [1.0 / cols] * cols
    col_widths = [w * CONTENT_W for w in col_weights]

    head_style = ParagraphStyle(
        "th", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=PALETTE["white"], alignment=TA_LEFT,
    )
    body_style = ParagraphStyle(
        "td", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=PALETTE["ink"], alignment=TA_LEFT,
    )
    body_first = ParagraphStyle(
        "tdf", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=PALETTE["accent_dk"], alignment=TA_LEFT,
    )

    data = [[Paragraph(str(h), head_style) for h in headers]]
    for row in rows:
        cells = []
        for i, c in enumerate(row):
            s = body_first if (first_col_emphasis and i == 0) else body_style
            cells.append(Paragraph(str(c), s))
        data.append(cells)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["accent"]),
        ("TEXTCOLOR",  (0, 0), (-1, 0), PALETTE["white"]),
        ("LINEBELOW",  (0, 0), (-1, 0), 0.6, PALETTE["accent_dk"]),
        ("LINEBELOW",  (0, -1), (-1, -1), 0.6, PALETTE["accent_dk"]),
        ("LINEABOVE",  (0, 0), (-1, 0), 0.6, PALETTE["accent_dk"]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), PALETTE["soft_bg"]))
        style.append(("LINEBELOW", (0, i), (-1, i), 0.25, PALETTE["hairline"]))
    t.setStyle(TableStyle(style))
    return t


# ─────────────────────────────────────────────────────────────────────
# CALLOUT BLOCK (key message in a soft box)
# ─────────────────────────────────────────────────────────────────────
def callout(text, style_key="body"):
    S = get_styles()
    style = ParagraphStyle(
        "callout", parent=S[style_key], fontSize=10, leading=14,
        textColor=PALETTE["accent_dk"], fontName="Helvetica-Bold",
        backColor=PALETTE["accent_lt"], borderColor=PALETTE["accent"],
        borderWidth=0, borderPadding=10, spaceBefore=6, spaceAfter=10,
        leftIndent=0, rightIndent=0, alignment=TA_LEFT,
    )
    return Paragraph(text, style)


# ─────────────────────────────────────────────────────────────────────
# Divider helper
# ─────────────────────────────────────────────────────────────────────
def divider():
    return HRFlowable(width="100%", thickness=0.4, color=PALETTE["hairline"],
                      spaceBefore=8, spaceAfter=8)
