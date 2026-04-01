"""
Generate all updated PDF documents for GOVERN.AI MVP v2.4
"""
import io
import os
import sys
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
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
    "red": colors.HexColor("#ef4444"),
}

PAGE_W, PAGE_H = A4
MARGIN = 25 * mm

def get_styles():
    return {
        "title": ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=26, textColor=C["white"], leading=32, spaceAfter=6),
        "h1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, textColor=C["white"], leading=24, spaceBefore=20, spaceAfter=8),
        "h2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14, textColor=C["blue"], leading=18, spaceBefore=14, spaceAfter=6),
        "h3": ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, textColor=C["light"], leading=14, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, alignment=TA_JUSTIFY, spaceAfter=4),
        "small": ParagraphStyle("Small", fontName="Helvetica", fontSize=8, textColor=C["muted"], leading=11, spaceAfter=2),
        "bullet": ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, leftIndent=16, bulletIndent=6, spaceAfter=2),
    }

def draw_page(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, PAGE_H - 22 * mm, PAGE_W, 22 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 16)
    canvas_obj.drawString(MARGIN, PAGE_H - 14 * mm, "GOVERN.AI")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawString(MARGIN, PAGE_H - 18 * mm, "Sovereign Control Plane for Enterprise AI")
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, "MVP v2.4")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 16 * mm, datetime.now().strftime('%B %Y'))
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.setLineWidth(0.4)
    canvas_obj.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(MARGIN, 8 * mm, "GOVERN.AI by ANTHERA Systems")
    canvas_obj.drawCentredString(PAGE_W / 2, 8 * mm, f"Page {doc.page}")
    canvas_obj.restoreState()

def draw_cover(canvas_obj, doc, title_text, subtitle_text):
    canvas_obj.saveState()
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 42)
    canvas_obj.drawString(MARGIN, PAGE_H - 80 * mm, "GOVERN.AI")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 14)
    canvas_obj.drawString(MARGIN, PAGE_H - 90 * mm, "The Sovereign Control Plane for Enterprise AI")
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.line(MARGIN, PAGE_H - 96 * mm, PAGE_W - MARGIN, PAGE_H - 96 * mm)
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(MARGIN, PAGE_H - 108 * mm, title_text)
    meta_y = PAGE_H - 120 * mm
    canvas_obj.setFillColor(C["light"])
    canvas_obj.setFont("Helvetica", 10)
    canvas_obj.drawString(MARGIN, meta_y, "Versione: MVP 2.4")
    canvas_obj.drawString(MARGIN, meta_y - 16, f"Data: {datetime.now().strftime('%B %Y')}")
    canvas_obj.drawString(MARGIN, meta_y - 32, "Autore: ANTHERA Systems")
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(MARGIN, 30 * mm, "Angelo Anglani — Founder & Lead Engineer")
    canvas_obj.drawString(MARGIN, 25 * mm, "angelo.anglani94@gmail.com | +39 342 754 8655")
    canvas_obj.restoreState()

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    w = col_widths or [((PAGE_W - 2 * MARGIN) / len(headers))] * len(headers)
    t = Table(data, colWidths=w, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), C["accent"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), C["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("TEXTCOLOR", (0, 1), (-1, -1), C["light"]),
        ("GRID", (0, 0), (-1, -1), 0.4, C["border"]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        bg = C["bg2"] if i % 2 == 0 else C["card"]
        style.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style))
    return t


def build_investor_pdf(lang="en"):
    buf = io.BytesIO()
    S = get_styles()
    elements = []

    cover_title = "EXECUTIVE INTRODUCTION" if lang == "en" else "PRESENTAZIONE PER INVESTITORI"
    
    elements.append(PageBreak())

    if lang == "en":
        elements.append(Paragraph("The Opportunity", S["h1"]))
        elements.append(Paragraph(
            "GOVERN.AI is the compliance-first AI control plane for enterprises operating in highly regulated industries. "
            "It provides a centralized governance layer for AI agents, workflows, and models.",
            S["body"]))
        
        elements.append(Paragraph("What We Do (MVP v2.4)", S["h1"]))
        capabilities = [
            "<b>Policy Engine + Conflict Detection:</b> Automated detection of action conflicts, gaps, overlaps, redundancies",
            "<b>SOX Section 404 Wizard:</b> Guided internal control assessment with Audit Readiness Score",
            "<b>Audit Trail:</b> Complete traceability with PDF/CSV export",
            "<b>Compliance Monitor:</b> Real-time tracking against 8 standards (EU AI Act, GDPR, ISO 27001/42001, DORA, NIS2, SOX, D.Lgs. 262)",
            "<b>Risk Classification:</b> Aligned with EU AI Act categories",
            "<b>AI Assistant (ARIA):</b> LLM-powered advisor with SSE streaming",
        ]
        for c in capabilities:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {c}", S["bullet"]))

        elements.append(Paragraph("Platform Highlights", S["h1"]))
        elements.append(make_table(
            ["Metric", "Value"],
            [
                ["Regulatory Standards", "8 (EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262)"],
                ["SOX Controls Tracked", "20 across 5 domains"],
                ["Policy Conflict Types", "4 (action conflict, gap, overlap, redundancy)"],
                ["Audit Logs (demo)", "150+ with 7 realistic incident clusters"],
                ["RBAC Roles", "4 (Admin, DPO, Auditor, Viewer)"],
                ["Backend Tests", "34/34 passing"],
                ["Languages", "2 (Italian, English)"],
            ],
            col_widths=[120, PAGE_W - 2 * MARGIN - 120]
        ))
        elements.append(PageBreak())

        elements.append(Paragraph("Use Case: Bank — AI Credit Scoring", S["h2"]))
        elements.append(Paragraph(
            "A major Italian bank deploys AI for automated credit scoring (high-risk under EU AI Act). "
            "GOVERN.AI provides: risk classification, GDPR policy enforcement, SOX 404 internal control assessment with "
            "Audit Readiness Score, policy conflict detection, and complete audit trail with PDF export.",
            S["body"]))
        
        elements.append(Paragraph("Use Case: Public Administration — AI Chatbot", S["h2"]))
        elements.append(Paragraph(
            "A regional government deploys an AI chatbot for citizen services. GOVERN.AI enforces transparency policies, "
            "restricts access to confidential data, monitors 8 compliance standards in real-time, and provides "
            "D.Lgs. 262/2005 controls for financial operations.",
            S["body"]))

        elements.append(Paragraph("Market Timing", S["h1"]))
        market_points = [
            "EU AI Act enforcement 2025-2026 — fines up to 35M EUR or 7% global revenue",
            "SOX compliance increasingly requires AI governance controls",
            "No incumbent solution addresses AI governance specifically",
            "Regulatory convergence: AI Act + DORA + NIS2 + SOX creates unique compliance matrix",
        ]
        for p in market_points:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {p}", S["bullet"]))

        elements.append(Paragraph("Business Model", S["h1"]))
        elements.append(make_table(
            ["Tier", "Target", "Pricing"],
            [
                ["Pro", "Up to 10 agents", "12,000 EUR/year"],
                ["Business", "Up to 50 agents", "48,000 EUR/year"],
                ["Enterprise", "Unlimited", "100,000+ EUR/year"],
            ],
            col_widths=[80, 130, PAGE_W - 2 * MARGIN - 210]
        ))

        elements.append(Paragraph("The Ask", S["h1"]))
        ask_items = [
            "Expand product — enterprise integrations, multi-tenancy, auto-fix engine",
            "Hire initial team — 2-3 engineers, 1 compliance domain expert",
            "Pilot with design partners — 3-5 enterprises in banking/PA",
            "Go-to-market Italy/EU — first-mover advantage on AI Act compliance",
        ]
        for a in ask_items:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {a}", S["bullet"]))

    else:  # Italian
        elements.append(Paragraph("L'Opportunita", S["h1"]))
        elements.append(Paragraph(
            "GOVERN.AI e il control plane compliance-first per l'AI, progettato per imprese in settori regolamentati. "
            "Fornisce un layer di governance centralizzato per agenti AI, workflow e modelli.",
            S["body"]))
        
        elements.append(Paragraph("Cosa Facciamo (MVP v2.4)", S["h1"]))
        capabilities = [
            "<b>Motore di Policy + Rilevamento Conflitti:</b> Detection automatica di action conflict, gap, overlap, ridondanza",
            "<b>SOX Section 404 Wizard:</b> Valutazione guidata controlli interni con Audit Readiness Score",
            "<b>Traccia di Audit:</b> Tracciabilita completa con export PDF/CSV",
            "<b>Monitor Compliance:</b> Monitoraggio real-time su 8 standard (EU AI Act, GDPR, ISO 27001/42001, DORA, NIS2, SOX, D.Lgs. 262)",
            "<b>Classificazione Rischio:</b> Allineata alle categorie EU AI Act",
            "<b>Assistente AI (ARIA):</b> Consulente LLM con streaming SSE",
        ]
        for c in capabilities:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {c}", S["bullet"]))

        elements.append(Paragraph("Highlights Piattaforma", S["h1"]))
        elements.append(make_table(
            ["Metrica", "Valore"],
            [
                ["Standard Normativi", "8 (EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262)"],
                ["Controlli SOX", "20 in 5 domini"],
                ["Tipi Conflitto Policy", "4 (action conflict, gap, overlap, ridondanza)"],
                ["Audit Log (demo)", "150+ con 7 cluster incidenti"],
                ["Ruoli RBAC", "4 (Admin, DPO, Auditor, Viewer)"],
                ["Test Backend", "34/34 passanti"],
                ["Lingue", "2 (Italiano, Inglese)"],
            ],
            col_widths=[120, PAGE_W - 2 * MARGIN - 120]
        ))
        elements.append(PageBreak())

        elements.append(Paragraph("Caso d'Uso: Banca — Credit Scoring AI", S["h2"]))
        elements.append(Paragraph(
            "Una grande banca italiana implementa AI per credit scoring (alto rischio per EU AI Act). "
            "GOVERN.AI fornisce: classificazione rischio, enforcement policy GDPR, valutazione controlli interni SOX 404 "
            "con Readiness Score, rilevamento conflitti policy, e audit trail completo con export PDF.",
            S["body"]))
        
        elements.append(Paragraph("Caso d'Uso: PA — Chatbot AI per Cittadini", S["h2"]))
        elements.append(Paragraph(
            "Un governo regionale usa chatbot AI per servizi ai cittadini. GOVERN.AI impone trasparenza, "
            "restringe accesso a dati confidenziali, monitora 8 standard in tempo reale, e applica controlli "
            "D.Lgs. 262/2005 per operazioni finanziarie.",
            S["body"]))

        elements.append(Paragraph("Timing di Mercato", S["h1"]))
        market_points = [
            "EU AI Act enforcement 2025-2026 — sanzioni fino a 35M EUR o 7% fatturato",
            "Compliance SOX richiede governance AI sempre piu stringente",
            "Nessuna soluzione incumbent per governance AI specifica",
            "Convergenza normativa: AI Act + DORA + NIS2 + SOX = matrice compliance unica",
        ]
        for p in market_points:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {p}", S["bullet"]))

        elements.append(Paragraph("Modello di Business", S["h1"]))
        elements.append(make_table(
            ["Tier", "Target", "Prezzo"],
            [
                ["Pro", "Fino a 10 agenti", "12.000 EUR/anno"],
                ["Business", "Fino a 50 agenti", "48.000 EUR/anno"],
                ["Enterprise", "Illimitati", "100.000+ EUR/anno"],
            ],
            col_widths=[80, 130, PAGE_W - 2 * MARGIN - 210]
        ))

        elements.append(Paragraph("La Richiesta", S["h1"]))
        ask_items = [
            "Espandere il prodotto — integrazioni enterprise, multi-tenancy, auto-fix engine",
            "Assumere team iniziale — 2-3 engineer, 1 esperto compliance",
            "Pilota con design partner — 3-5 imprese in banking/PA",
            "Go-to-market Italia/EU — first-mover advantage su AI Act",
        ]
        for a in ask_items:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {a}", S["bullet"]))

    # Founder section (same in both)
    elements.append(PageBreak())
    elements.append(Paragraph("About the Founder" if lang == "en" else "Il Founder", S["h1"]))
    elements.append(Paragraph("<b>Angelo Anglani</b> — Founder, GOVERN.AI", S["body"]))
    elements.append(make_table(
        ["Area", "Experience" if lang == "en" else "Esperienza"],
        [
            ["Cloud & Infrastructure", "18,000+ AWS VMs, 3M+ EUR savings, 99.9% SLA"],
            ["Enterprise Consulting", "BIP xTech, Deloitte Risk Advisory — 10M+ EUR programs"],
            ["IT Risk & Compliance", "IT Audit, cybersecurity advisory, zero violations"],
            ["Financial Comms", "Master Investor Relations (Euronext/Borsa Italiana)"],
        ],
        col_widths=[120, PAGE_W - 2 * MARGIN - 120]
    ))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("angelo.anglani94@gmail.com | +39 342 754 8655", S["body"]))
    elements.append(Paragraph("linkedin.com/in/angelo-anglani", S["body"]))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("GOVERN.AI — Sovereign Control Plane for Enterprise AI", S["small"]))
    elements.append(Paragraph("powered by ANTHERA Systems", S["small"]))

    def cover_handler(canvas_obj, doc):
        draw_cover(canvas_obj, doc, cover_title, "")

    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=26*mm, bottomMargin=18*mm)
    doc.build(elements, onFirstPage=cover_handler, onLaterPages=draw_page)
    buf.seek(0)
    return buf.getvalue()


def build_audit_pdf():
    buf = io.BytesIO()
    S = get_styles()
    elements = []

    elements.append(PageBreak())

    elements.append(Paragraph("AUDIT TECNICO — GOVERN.AI", S["h1"]))
    elements.append(Paragraph("Versione MVP v2.4 — Aprile 2026", S["small"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Stack Tecnologico", S["h2"]))
    elements.append(make_table(
        ["Componente", "Tecnologia", "Versione"],
        [
            ["Backend", "FastAPI", "0.110.1"],
            ["Frontend", "React + Tailwind", "19.0.0"],
            ["Database", "MongoDB (Motor async)", "7.0"],
            ["LLM", "litellm (configurable)", "1.80.0"],
            ["Auth", "JWT HS256 + bcrypt", "—"],
            ["Export", "ReportLab", "4.1.0"],
            ["Charts", "Recharts", "3.6.0"],
            ["CI/CD", "GitHub Actions", "4 jobs"],
        ],
        col_widths=[90, 130, PAGE_W - 2*MARGIN - 220]
    ))

    elements.append(Paragraph("2. Architettura", S["h2"]))
    arch_points = [
        "Backend modulare: server.py + 9 file route + models.py + database.py + seed.py + exporters.py",
        "Frontend SPA: 11 pagine, componente CRUD generico, 130+ chiavi i18n EN/IT",
        "Database: 7 collections, 15+ indici ottimizzati",
        "Autenticazione JWT con RBAC (4 ruoli: admin > dpo > auditor > viewer)",
        "Rate limiting su tutti gli endpoint (SlowAPI)",
        "Security headers middleware (5 header)",
    ]
    for p in arch_points:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {p}", S["bullet"]))

    elements.append(Paragraph("3. Collections MongoDB", S["h2"]))
    elements.append(make_table(
        ["Collection", "Documenti", "Indici"],
        [
            ["users", "1+", "id (unique), username (unique)"],
            ["agents", "14", "id (unique), status, risk_level"],
            ["policies", "20+", "id (unique), regulation, severity"],
            ["audit_logs", "150+", "id (unique), timestamp, agent_name, outcome, risk_level"],
            ["compliance_standards", "8", "id (unique), code (unique)"],
            ["chat_messages", "var", "session_id + timestamp (compound)"],
            ["sox_controls", "20", "id (unique), domain, status"],
        ],
        col_widths=[100, 60, PAGE_W - 2*MARGIN - 160]
    ))
    elements.append(PageBreak())

    elements.append(Paragraph("4. Sicurezza", S["h2"]))
    sec_items = [
        ["JWT Auth (HS256, 8h)", "IMPLEMENTATO"],
        ["RBAC 4 ruoli", "IMPLEMENTATO"],
        ["Rate Limiting (SlowAPI)", "IMPLEMENTATO"],
        ["CORS restrittivo", "IMPLEMENTATO"],
        ["Security Headers (5)", "IMPLEMENTATO"],
        ["Sanitizzazione regex", "IMPLEMENTATO"],
        ["Enum Pydantic (10)", "IMPLEMENTATO"],
        ["LLM error masking", "IMPLEMENTATO"],
    ]
    elements.append(make_table(["Meccanismo", "Stato"], sec_items, col_widths=[200, PAGE_W - 2*MARGIN - 200]))

    elements.append(Paragraph("5. Test & Qualita", S["h2"]))
    elements.append(Paragraph("<b>34/34 test backend passanti</b> (pytest) — Copertura: Auth, CRUD, Audit, Compliance, SOX Wizard, Policy Engine, Dashboard, Chat", S["body"]))
    elements.append(Paragraph("CI/CD: GitHub Actions con 4 job paralleli (backend-tests, frontend-build, security-scan, docker-build)", S["body"]))
    elements.append(Paragraph("7 iterazioni testing agent, tutte passate con 100% success rate", S["body"]))

    elements.append(Paragraph("6. Feature v2.4", S["h2"]))
    features = [
        "<b>SOX Foundation (v2.1):</b> Standard SOX, agente SOX Auditor, 3 policy SOX, cluster audit",
        "<b>SOX 404 Wizard (v2.2):</b> 20 controlli in 5 domini, progress tracking, export PDF, edit dialog",
        "<b>D.Lgs. 262 + Readiness Score (v2.3):</b> 8o standard, 2 policy, Dirigente Preposto, score pesato",
        "<b>Policy Conflict Engine (v2.4):</b> 4 regole detection, 3 endpoint, UI completa, resolve dialog",
    ]
    for f in features:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {f}", S["bullet"]))

    elements.append(Paragraph("7. Debito Tecnico Residuo", S["h2"]))
    elements.append(make_table(
        ["ID", "Area", "Problema", "Priorita"],
        [
            ["TD19", "Database", "Date come stringhe ISO", "P2"],
            ["TD-FE1", "Frontend", "Nessun test unitario frontend", "P2"],
            ["TD-BE1", "Backend", "Query dashboard non aggregate", "P2"],
            ["TD-BE2", "Backend", "Paginazione audit solo backend", "P2"],
        ],
        col_widths=[50, 70, 200, PAGE_W - 2*MARGIN - 320]
    ))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Documento generato: {datetime.now().strftime('%B %Y')} — MVP v2.4", S["small"]))

    def cover_handler(canvas_obj, doc):
        draw_cover(canvas_obj, doc, "AUDIT TECNICO", "")

    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=26*mm, bottomMargin=18*mm)
    doc.build(elements, onFirstPage=cover_handler, onLaterPages=draw_page)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    # Generate Investor PDFs
    print("Generating Investor Intro EN...")
    pdf_en = build_investor_pdf("en")
    with open("/app/GOVERN_AI_Investor_Intro_EN.pdf", "wb") as f:
        f.write(pdf_en)
    print(f"  -> {len(pdf_en)} bytes")

    print("Generating Investor Intro IT...")
    pdf_it = build_investor_pdf("it")
    with open("/app/GOVERN_AI_Investor_Intro_IT.pdf", "wb") as f:
        f.write(pdf_it)
    print(f"  -> {len(pdf_it)} bytes")

    print("Generating Audit Tecnico PDF...")
    pdf_audit = build_audit_pdf()
    with open("/app/AUDIT_TECNICO_GOVERN.pdf", "wb") as f:
        f.write(pdf_audit)
    print(f"  -> {len(pdf_audit)} bytes")

    print("All PDFs generated successfully!")
