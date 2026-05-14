"""
ANTHERA — Apertus Strategy PDF Generator
Reuses the user_manual PDF builder for the Apertus strategy markdown.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_user_manual_pdf import (
    parse_markdown_to_flowables, draw_page, get_styles,
    C, PAGE_W, PAGE_H, MARGIN
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate
import io
import re


def draw_apertus_cover(canvas_obj, doc, subtitle, lang):
    canvas_obj.saveState()
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Top stripe red (Swiss accent)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
    # Title
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 42)
    canvas_obj.drawString(MARGIN, PAGE_H - 78 * mm, "ANTHERA")
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.setFont("Helvetica-Bold", 30)
    canvas_obj.drawString(MARGIN, PAGE_H - 92 * mm, "x  APERTUS")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 12)
    canvas_obj.drawString(MARGIN, PAGE_H - 102 * mm, "Sovereign European AI as the Heart of the ANTHERA Ecosystem")
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.line(MARGIN, PAGE_H - 108 * mm, PAGE_W - MARGIN, PAGE_H - 108 * mm)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.setFont("Helvetica-Bold", 13)
    canvas_obj.drawString(MARGIN, PAGE_H - 120 * mm, subtitle)
    # Meta
    meta_y = PAGE_H - 136 * mm
    canvas_obj.setFillColor(C["light"])
    canvas_obj.setFont("Helvetica", 10)
    label_ver = "Version" if lang == "en" else "Versione"
    label_date = "Date" if lang == "en" else "Data"
    label_author = "Author" if lang == "en" else "Autore"
    label_clas = "Classification" if lang == "en" else "Classificazione"
    canvas_obj.drawString(MARGIN, meta_y, f"{label_ver}: 1.0")
    canvas_obj.drawString(MARGIN, meta_y - 16, f"{label_date}: 14 May 2026" if lang == "en" else f"{label_date}: 14 Maggio 2026")
    canvas_obj.drawString(MARGIN, meta_y - 32, f"{label_author}: ANTHERA Systems")
    canvas_obj.drawString(MARGIN, meta_y - 48, f"{label_clas}: Strategic / Confidential")
    # Tagline
    canvas_obj.setFillColor(C["green"])
    canvas_obj.setFont("Helvetica-BoldOblique", 11)
    canvas_obj.drawString(MARGIN, PAGE_H - 200 * mm, "\"European data deserves European AI.\"")
    # Footer info
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(MARGIN, 30 * mm, "Angelo Anglani  -  Founder, ANTHERA Systems")
    canvas_obj.drawString(MARGIN, 25 * mm, "angelo.anglani94@gmail.com  |  +39 342 754 8655")
    canvas_obj.drawString(MARGIN, 20 * mm, "linkedin.com/in/angelo-anglani")
    canvas_obj.restoreState()


def build_apertus_pdf(md_path, lang):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Strip first H1 (the document title) so it doesn't repeat after the cover
    md_text = re.sub(r"^# ANTHERA Systems[^\n]*\n", "", md_text)

    subtitle = "APERTUS STRATEGY" if lang == "en" else "STRATEGIA APERTUS"

    buf = io.BytesIO()
    elements = parse_markdown_to_flowables(md_text)

    def cover_handler(canvas_obj, doc):
        draw_apertus_cover(canvas_obj, doc, subtitle, lang)

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=22 * mm, bottomMargin=18 * mm,
    )
    doc.build(elements, onFirstPage=cover_handler, onLaterPages=draw_page)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    print("Generating ANTHERA Apertus Strategy IT...")
    pdf_it = build_apertus_pdf("/app/ANTHERA_APERTUS_STRATEGY_IT.md", "it")
    out_it = "/app/ANTHERA_APERTUS_STRATEGY_IT.pdf"
    with open(out_it, "wb") as f:
        f.write(pdf_it)
    print(f"  -> {out_it} ({len(pdf_it)} bytes)")

    print("Generating ANTHERA Apertus Strategy EN...")
    pdf_en = build_apertus_pdf("/app/ANTHERA_APERTUS_STRATEGY_EN.md", "en")
    out_en = "/app/ANTHERA_APERTUS_STRATEGY_EN.pdf"
    with open(out_en, "wb") as f:
        f.write(pdf_en)
    print(f"  -> {out_en} ({len(pdf_en)} bytes)")

    print("All Apertus Strategy PDFs generated successfully!")
