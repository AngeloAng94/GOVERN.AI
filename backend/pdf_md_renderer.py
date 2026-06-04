"""
Markdown -> Institutional PDF renderer (uses pdf_theme.py)

Used by:
- AUDIT_TECNICO_GOVERN.pdf
- GOVERN_AI_Technical_Overview.pdf
- GOVERN_AI_USER_MANUAL_{IT,EN}.pdf
- ANTHERA_APERTUS_STRATEGY_{IT,EN}.pdf
"""
import io
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable,
)

from pdf_theme import (
    PALETTE, MARGIN_LR, MARGIN_TOP, MARGIN_BOTTOM,
    get_styles, draw_cover, make_page_decorator, make_table,
    callout, divider,
)


# ── inline MD parsing ──────────────────────────────────────────────
def _md_inline(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.replace("&", "&amp;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(
        r"`([^`]+?)`",
        lambda m: f'<font face="Courier" color="#0B2540">{m.group(1)}</font>',
        text,
    )
    return text


def _strip_frontmatter_title(md_text):
    """Strip first H1 title to avoid duplicating the cover heading."""
    return re.sub(r"^# [^\n]*\n+", "", md_text, count=1)


def parse_md(md_text):
    """Naive but predictable Markdown -> ReportLab flowables."""
    S = get_styles()
    elements = []
    lines = md_text.split("\n")
    i = 0
    in_code = False
    code_lines = []
    bullet_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        for b in bullet_buf:
            elements.append(Paragraph(f"&bull;&nbsp;&nbsp;{_md_inline(b)}", S["bullet"]))
        bullet_buf = []

    while i < len(lines):
        line = lines[i].rstrip()

        # Code block fences
        if line.strip().startswith("```"):
            flush_bullets()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                code_text = "\n".join(code_lines)
                code_text = (code_text.replace("&", "&amp;")
                             .replace("<", "&lt;").replace(">", "&gt;"))
                elements.append(Paragraph(code_text.replace("\n", "<br/>"), S["code"]))
                code_lines = []
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Tables
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|\s*$", lines[i + 1]):
            flush_bullets()
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if len(cells) < len(headers):
                    cells += [""] * (len(headers) - len(cells))
                else:
                    cells = cells[:len(headers)]
                rows.append(cells)
                i += 1
            elements.append(make_table(headers, rows, first_col_emphasis=True))
            elements.append(Spacer(1, 6))
            continue

        # Horizontal rule
        if line.strip() == "---":
            flush_bullets()
            elements.append(divider())
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
            elements.append(Paragraph(_md_inline(line[3:].strip()), S["h1"]))
            i += 1
            continue
        if line.startswith("### "):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line[4:].strip()), S["h2"]))
            i += 1
            continue
        if line.startswith("#### "):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line[5:].strip()), S["h3"]))
            i += 1
            continue

        # Bullets
        if line.startswith("- ") or line.startswith("* "):
            bullet_buf.append(line[2:].strip())
            i += 1
            continue

        # Numbered list
        m_num = re.match(r"^\d+\.\s+(.*)$", line)
        if m_num:
            bullet_buf.append(m_num.group(1))
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            flush_bullets()
            elements.append(Paragraph(_md_inline(line.lstrip("> ").strip()), S["quote"]))
            i += 1
            continue

        if line.strip() == "":
            flush_bullets()
            i += 1
            continue

        # Paragraph (collect multi-line)
        flush_bullets()
        para = [line]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not lines[j].startswith(("#", "-", "*", "|", "```", ">")) \
                and not re.match(r"^\d+\.\s+", lines[j]) and lines[j].strip() != "---":
            para.append(lines[j].rstrip())
            j += 1
        elements.append(Paragraph(_md_inline(" ".join(para)), S["body"]))
        i = j

    flush_bullets()
    return elements


# ── public API ─────────────────────────────────────────────────────
def render_md_to_pdf(
    md_path: str,
    output_path: str,
    *,
    brand_top: str,
    brand_bottom: str = "ANTHERA Systems",
    doc_type: str,
    version: str,
    date_str: str,
    tagline: str = None,
    classification: str = "Confidential",
    intro_callout: str = None,
):
    """Convert a Markdown file to a branded institutional PDF."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    md_text = _strip_frontmatter_title(md_text)

    elements = []
    if intro_callout:
        elements.append(callout(intro_callout))
    elements.extend(parse_md(md_text))

    def cover_handler(canvas_obj, doc):
        draw_cover(
            canvas_obj,
            brand_top=brand_top,
            brand_bottom=brand_bottom,
            doc_type=doc_type,
            version=version,
            date_str=date_str,
            author="ANTHERA Systems",
            classification=classification,
            tagline=tagline,
            footer_lines=[
                "Angelo Anglani  -  Founder & Lead Engineer",
                "angelo.anglani94@gmail.com   |   +39 342 754 8655",
                "linkedin.com/in/angelo-anglani",
            ],
        )

    page_handler = make_page_decorator(
        brand=brand_top, doc_type=doc_type,
        version=version, date_str=date_str,
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN_LR, rightMargin=MARGIN_LR,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
    )
    doc.build([PageBreak()] + elements,
              onFirstPage=cover_handler,
              onLaterPages=page_handler)
    buf.seek(0)
    data = buf.getvalue()
    with open(output_path, "wb") as f:
        f.write(data)
    return len(data)
