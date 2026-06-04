"""
Investor Intro PDF generators — IT + EN — institutional design v3.1
Uses pdf_theme.py for boardroom-grade output.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether,
)

from pdf_theme import (
    PALETTE, MARGIN_LR, MARGIN_TOP, MARGIN_BOTTOM,
    get_styles, draw_cover, make_page_decorator, make_table,
    callout, divider,
)


# ─────────────────────────────────────────────────────────────────────
def build_investor_pdf(lang: str) -> bytes:
    S = get_styles()
    elements = []

    is_en = lang == "en"
    T = {
        "the_opportunity":  ("The Opportunity",          "L'Opportunita"),
        "what_we_do":       ("What We Do (MVP v3.1)",    "Cosa Facciamo (MVP v3.1)"),
        "whats_new":        ("What's New in v3.1",       "Le Novita di v3.1"),
        "use_cases":        ("Use Cases",                "Casi d'Uso"),
        "platform":         ("Platform Highlights",      "Highlights Piattaforma"),
        "timing":           ("Market Timing",            "Timing di Mercato"),
        "traction":         ("Traction & Status",        "Traction e Status"),
        "business":         ("Business Model",           "Modello di Business"),
        "competitive":      ("Competitive Landscape",    "Panorama Competitivo"),
        "ask":              ("The Ask",                  "La Richiesta"),
        "founder":          ("About the Founder",        "Il Founder"),
        "contact":          ("Contact",                  "Contatti"),
        "sovereign_h":      ("Sovereign AI — A Strategic Differentiator",
                             "Sovereign AI — Un Differenziatore Strategico"),
    }
    def tr(en, it): return en if is_en else it
    def L(key): return T[key][0] if is_en else T[key][1]

    # ── HERO STATEMENT (callout) ─────────────────────────────────────
    hero = tr(
        "GOVERN.AI is the compliance-first AI control plane for enterprises operating in "
        "highly regulated industries. Built in Europe, powered by Sovereign European AI.",
        "GOVERN.AI e il control plane compliance-first per le imprese che operano in settori "
        "altamente regolamentati. Costruito in Europa, alimentato da AI Sovrana Europea."
    )
    elements.append(callout(hero))

    # ── THE OPPORTUNITY ─────────────────────────────────────────────
    elements.append(Paragraph(L("the_opportunity"), S["h1"]))
    elements.append(Paragraph(tr(
        "As AI adoption accelerates across banking, insurance, healthcare, and public "
        "administration, organizations face a critical challenge: <b>deploy AI agents at scale "
        "while maintaining regulatory compliance, auditability, and control — and objectively "
        "measure compliance posture.</b>",
        "Con l'accelerazione dell'adozione dell'AI in banche, assicurazioni, sanita e pubblica "
        "amministrazione, le organizzazioni affrontano una sfida critica: <b>implementare agenti "
        "AI su larga scala mantenendo conformita normativa, auditabilita e controllo — e misurare "
        "oggettivamente la postura di compliance.</b>"
    ), S["body"]))
    elements.append(Paragraph(tr(
        "GOVERN.AI provides a centralized governance layer with a <b>deterministic, explainable "
        "scoring engine</b> that quantifies compliance posture in real time.",
        "GOVERN.AI fornisce un layer di governance centralizzato con un <b>motore di scoring "
        "deterministico e spiegabile</b> che quantifica la postura di compliance in tempo reale."
    ), S["body"]))

    # ── WHAT WE DO ──────────────────────────────────────────────────
    elements.append(Paragraph(L("what_we_do"), S["h1"]))
    capabilities = [
        ("Compliance Intelligence Engine",
         tr("Deterministic scoring for agents, standards and overall governance with native explainability.",
            "Scoring deterministico per agenti, standard e governance complessiva con explainability nativa.")),
        ("Intelligence Center",
         tr("Investor-ready dashboard: score ring, ranking, KPI breakdown, insights and remediations.",
            "Dashboard investor-ready: score ring, ranking, KPI breakdown, insights e remediation.")),
        ("Policy Engine + Conflict Detection",
         tr("Granular rules with automated detection (action conflicts, gaps, overlaps, redundancies).",
            "Regole granulari con rilevamento automatico (action conflict, gap, overlap, ridondanza).")),
        ("Policy Guidance Engine",
         tr("Operational guidance per conflict, documented resolution, full audit log.",
            "Guidance operativa per conflitto, risoluzione documentata, audit log completo.")),
        ("SOX Section 404 Wizard",
         tr("Guided internal control assessment with Audit Readiness Score.",
            "Valutazione guidata controlli interni con Audit Readiness Score.")),
        ("Compliance Monitor",
         tr("Real-time tracking against 8 standards (EU AI Act, GDPR, ISO 27001/42001, DORA, NIS2, SOX, D.Lgs. 262).",
            "Monitoraggio real-time su 8 standard (EU AI Act, GDPR, ISO 27001/42001, DORA, NIS2, SOX, D.Lgs. 262).")),
        ("AI Assistant (ARIA)",
         tr("LLM-powered advisor with SSE streaming, contextualized on score and open conflicts.",
            "Consulente LLM con streaming SSE, contestualizzato su score e conflitti aperti.")),
    ]
    elements.append(make_table(
        [tr("Capability", "Funzionalita"), tr("Description", "Descrizione")],
        capabilities,
        col_weights=[0.32, 0.68],
        first_col_emphasis=True,
    ))

    # ── SOVEREIGN AI — DIFFERENTIATOR ───────────────────────────────
    elements.append(Paragraph(L("sovereign_h"), S["h1"]))
    sovereign_body = tr(
        "<b>GOVERN.AI v3.1 integrates Apertus</b> (developed by ETH Zurich, EPFL and CSCS — Swiss "
        "National Supercomputing Centre) as its sovereign European AI provider. European data is "
        "processed by European AI, under Apache 2.0 license, outside US Cloud Act jurisdiction.",
        "<b>GOVERN.AI v3.1 integra Apertus</b> (sviluppato da ETH Zurich, EPFL e CSCS — Swiss "
        "National Supercomputing Centre) come provider AI sovrano europeo. I dati europei sono "
        "processati da AI europea, sotto licenza Apache 2.0, fuori dalla giurisdizione del US Cloud Act."
    )
    elements.append(Paragraph(sovereign_body, S["body"]))
    sovereign_rows = [
        ["Apache 2.0", tr("Open-source, no vendor lock-in, free for commercial use.",
                          "Open-source, no vendor lock-in, uso commerciale libero.")],
        ["EU/CH sovereign", tr("Trained on the Alps supercomputer (Lugano), hosted in EU/CH.",
                               "Addestrato sul supercomputer Alps (Lugano), hosted in EU/CH.")],
        ["EU AI Act ready", tr("Article 13/53 transparency requirements satisfied by design.",
                               "Requisiti di trasparenza Art. 13/53 soddisfatti by design.")],
        [tr("Automatic fallback", "Fallback automatico"),
         tr("Should sovereign provider fail, GPT-4o ensures business continuity.",
            "Se il provider sovrano fallisce, GPT-4o garantisce continuita operativa.")],
    ]
    elements.append(make_table([tr("Feature", "Caratteristica"), tr("Value", "Valore")],
                               sovereign_rows, col_weights=[0.30, 0.70], first_col_emphasis=True))

    elements.append(PageBreak())

    # ── PLATFORM HIGHLIGHTS ──────────────────────────────────────────
    elements.append(Paragraph(L("platform"), S["h1"]))
    highlights = [
        [tr("Regulatory Standards", "Standard Normativi"),
         "8 (EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262)"],
        [tr("SOX Controls Tracked", "Controlli SOX"), tr("20 across 5 domains", "20 su 5 domini")],
        [tr("Policy Conflict Types", "Tipi Conflitto Policy"),
         tr("4 (action conflict, gap, overlap, redundancy)", "4 (action conflict, gap, overlap, ridondanza)")],
        [tr("Audit Logs (demo)", "Audit Log (demo)"),
         tr("150+ across 7 realistic incident clusters", "150+ in 7 cluster di incidenti realistici")],
        ["RBAC", "4 roles (Admin, DPO, Auditor, Viewer)"],
        [tr("Backend Tests", "Test Backend"), "50 / 50"],
        [tr("REST + SSE Endpoints", "Endpoint REST + SSE"), "45+"],
        [tr("UI Pages", "Pagine UI"), "13 (incl. Settings v3.1)"],
        ["AI Provider", tr("Apertus 70B (sovereign) + GPT-4o (fallback)",
                           "Apertus 70B (sovrano) + GPT-4o (fallback)")],
        [tr("Languages", "Lingue"), "Italiano, English"],
    ]
    elements.append(make_table([tr("Metric", "Metrica"), tr("Value", "Valore")],
                               highlights, col_weights=[0.38, 0.62], first_col_emphasis=True))

    # ── MARKET TIMING ───────────────────────────────────────────────
    elements.append(Paragraph(L("timing"), S["h1"]))
    market = [
        tr("EU AI Act enforcement 2025-2026 — fines up to <b>35M EUR or 7% global revenue</b>.",
           "EU AI Act enforcement 2025-2026 — sanzioni fino a <b>35M EUR o 7% fatturato globale</b>."),
        tr("Enterprises deploying AI agents at unprecedented speed.",
           "Le imprese stanno implementando agenti AI a velocita senza precedenti."),
        tr("SOX compliance increasingly requires AI governance controls.",
           "Compliance SOX richiede sempre piu controlli sulla governance AI."),
        tr("No incumbent solution offers AI governance with deterministic scoring AND sovereign EU AI.",
           "Nessuna soluzione incumbent offre governance AI con scoring deterministico E AI sovrana EU."),
        tr("Investors and boards demand quantitative KPIs on AI compliance posture.",
           "Investitori e CdA chiedono KPI quantitativi sulla postura di AI compliance."),
    ]
    for m in market:
        elements.append(Paragraph(f"&bull;&nbsp;&nbsp;{m}", S["bullet"]))

    elements.append(Paragraph(tr("Target Market", "Mercato Target"), S["h2"]))
    elements.append(make_table(
        [tr("Segment", "Segmento"), tr("Regulatory Drivers", "Driver Normativi")],
        [
            [tr("Banks & Financial Services", "Banche e Servizi Finanziari"),
             "EU AI Act + DORA + SOX + D.Lgs. 262"],
            [tr("Public Administration", "Pubblica Amministrazione"),
             tr("EU AI Act + GDPR + transparency", "EU AI Act + GDPR + trasparenza")],
            [tr("Insurance", "Assicurazioni"), "EU AI Act + GDPR + DORA"],
            [tr("Healthcare", "Sanita"), tr("EU AI Act + GDPR + highest scrutiny",
                                            "EU AI Act + GDPR + massimo scrutinio")],
            [tr("Critical Infrastructure", "Infrastrutture Critiche"), "NIS2 + EU AI Act"],
        ],
        col_weights=[0.35, 0.65], first_col_emphasis=True,
    ))

    elements.append(PageBreak())

    # ── BUSINESS MODEL ───────────────────────────────────────────────
    elements.append(Paragraph(L("business"), S["h1"]))
    elements.append(Paragraph(tr(
        "<b>B2B SaaS</b> with tiered pricing aligned to AI agent volume and regulated industry usage.",
        "<b>B2B SaaS</b> con pricing a tier allineato al volume di agenti AI e all'uso in settori regolamentati."
    ), S["body"]))
    elements.append(make_table(
        [tr("Tier", "Tier"), tr("Target", "Target"), tr("Pricing / year", "Prezzo / anno")],
        [
            ["Pro", tr("Mid-market, up to 10 agents", "PMI, fino a 10 agenti"), "12,000 EUR"],
            ["Business", tr("Up to 50 agents", "Fino a 50 agenti"), "48,000 EUR"],
            ["Enterprise", tr("Unlimited agents", "Agenti illimitati"), "100,000+ EUR"],
        ],
        col_weights=[0.18, 0.52, 0.30], first_col_emphasis=True,
    ))

    # ── COMPETITIVE LANDSCAPE ────────────────────────────────────────
    elements.append(Paragraph(L("competitive"), S["h1"]))
    elements.append(make_table(
        [tr("Category", "Categoria"), tr("Players", "Player"), tr("Our Differentiation", "Nostra Differenziazione")],
        [
            [tr("Traditional GRC", "GRC Tradizionale"), "ServiceNow, Archer, OneTrust",
             tr("Not AI-native, retrofitting compliance.",
                "Non AI-native, retrofit della compliance.")],
            ["AI MLOps", "MLflow, Weights & Biases",
             tr("Technical focus, no governance layer.",
                "Focus tecnico, nessun layer di governance.")],
            ["AI Security", "Robust Intelligence, Protect AI",
             tr("Security-focused, not compliance-first.",
                "Focus sicurezza, non compliance-first.")],
            ["GOVERN.AI", "—",
             tr("<b>Purpose-built for AI governance + 8 standards + deterministic scoring + sovereign EU AI.</b>",
                "<b>Purpose-built per AI governance + 8 standard + scoring deterministico + AI sovrana EU.</b>")],
        ],
        col_weights=[0.22, 0.30, 0.48], first_col_emphasis=True,
    ))

    # ── ASK ──────────────────────────────────────────────────────────
    elements.append(Paragraph(L("ask"), S["h1"]))
    asks = [
        tr("Expand the product — enterprise connectors, multi-tenancy, auto-fix engine, real-time monitoring.",
           "Espandere il prodotto — connettori enterprise, multi-tenancy, auto-fix engine, real-time monitoring."),
        tr("Hire initial team — 2-3 engineers, 1 compliance domain expert.",
           "Assumere il team iniziale — 2-3 engineer, 1 esperto compliance."),
        tr("Pilot with design partners — 3-5 enterprises in banking and PA.",
           "Pilota con design partner — 3-5 imprese in banking e PA."),
        tr("Go-to-market in Italy and EU — first-mover on AI Act compliance.",
           "Go-to-market in Italia e EU — first-mover sulla compliance AI Act."),
    ]
    for a in asks:
        elements.append(Paragraph(f"&bull;&nbsp;&nbsp;{a}", S["bullet"]))

    elements.append(PageBreak())

    # ── FOUNDER ──────────────────────────────────────────────────────
    elements.append(Paragraph(L("founder"), S["h1"]))
    elements.append(Paragraph(tr(
        "<b>Angelo Anglani</b> is building GOVERN.AI with the vision of becoming the standard "
        "for AI governance in regulated industries.",
        "<b>Angelo Anglani</b> sta costruendo GOVERN.AI con la visione di diventare lo standard "
        "per la governance AI nei settori regolamentati."
    ), S["body"]))
    elements.append(make_table(
        [tr("Area", "Area"), tr("Experience", "Esperienza")],
        [
            [tr("Cloud & Infrastructure", "Cloud & Infrastruttura"),
             tr("Managed 18,000+ AWS VMs for Italy's largest PA, 3M+ EUR annual savings, 99.9% SLA.",
                "Gestiti 18.000+ VM AWS per la piu grande PA italiana, 3M+ EUR savings annuali, 99.9% SLA.")],
            [tr("Enterprise Consulting", "Consulenza Enterprise"),
             tr("BIP xTech, Deloitte Risk Advisory — led 10M+ EUR programs.",
                "BIP xTech, Deloitte Risk Advisory — guidati programmi da 10M+ EUR.")],
            [tr("IT Risk & Compliance", "IT Risk & Compliance"),
             tr("IT Audit, cybersecurity advisory, zero compliance violations.",
                "IT Audit, advisory cybersecurity, zero violazioni di compliance.")],
            [tr("Financial Communications", "Comunicazione Finanziaria"),
             tr("Master in Investor Relations (Euronext Academy / Borsa Italiana).",
                "Master in Investor Relations (Euronext Academy / Borsa Italiana).")],
        ],
        col_weights=[0.30, 0.70], first_col_emphasis=True,
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(tr("Education", "Formazione"), S["h2"]))
    edu = [
        tr("M.Sc. Data & Cloud Engineering — Politecnico di Milano (2023-2025)",
           "Master Data & Cloud Engineering — Politecnico di Milano (2023-2025)"),
        tr("Master in Investor Relations — Euronext Academy, Borsa Italiana (2025)",
           "Master in Investor Relations — Euronext Academy, Borsa Italiana (2025)"),
        tr("M.Sc. Industrial Management — LIUC Universita Cattaneo",
           "Laurea Magistrale Management Industriale — LIUC Universita Cattaneo"),
        "AWS Cloud Practitioner certified",
        "HPC & Quantum Computing — CINECA",
    ]
    for e in edu:
        elements.append(Paragraph(f"&bull;&nbsp;&nbsp;{e}", S["bullet"]))

    elements.append(divider())
    elements.append(Paragraph(L("contact"), S["h2"]))
    elements.append(Paragraph(
        "<b>Angelo Anglani</b> &nbsp;&nbsp;|&nbsp;&nbsp; angelo.anglani94@gmail.com "
        "&nbsp;&nbsp;|&nbsp;&nbsp; +39 342 754 8655 "
        "&nbsp;&nbsp;|&nbsp;&nbsp; linkedin.com/in/angelo-anglani",
        S["body"]
    ))

    # ── BUILD PDF ────────────────────────────────────────────────────
    doc_type = "Executive Introduction" if is_en else "Presentazione per Investitori"
    date_str = "14 May 2026" if is_en else "14 Maggio 2026"
    author = "ANTHERA Systems"

    def cover_handler(canvas_obj, doc):
        draw_cover(
            canvas_obj,
            brand_top="GOVERN.AI",
            brand_bottom="ANTHERA Systems",
            doc_type=doc_type,
            version="MVP v3.1",
            date_str=date_str,
            author=author,
            classification="Confidential",
            tagline=("European data deserves European AI."),
            footer_lines=[
                "Angelo Anglani  -  Founder & Lead Engineer",
                "angelo.anglani94@gmail.com   |   +39 342 754 8655",
                "linkedin.com/in/angelo-anglani",
            ],
        )

    page_handler = make_page_decorator(
        brand="GOVERN.AI",
        doc_type=doc_type,
        version="MVP v3.1",
        date_str=date_str,
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN_LR, rightMargin=MARGIN_LR,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
    )
    # First page = cover, content starts on page 2
    doc.build([PageBreak()] + elements,
              onFirstPage=cover_handler,
              onLaterPages=page_handler)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    print("Generating Investor Intro IT...")
    pdf_it = build_investor_pdf("it")
    with open("/app/GOVERN_AI_Investor_Intro_IT.pdf", "wb") as f:
        f.write(pdf_it)
    print(f"  -> /app/GOVERN_AI_Investor_Intro_IT.pdf ({len(pdf_it):,} bytes)")

    print("Generating Investor Intro EN...")
    pdf_en = build_investor_pdf("en")
    with open("/app/GOVERN_AI_Investor_Intro_EN.pdf", "wb") as f:
        f.write(pdf_en)
    print(f"  -> /app/GOVERN_AI_Investor_Intro_EN.pdf ({len(pdf_en):,} bytes)")
    print("Done.")
