"""
GOVERN.AI — Technical Overview PDF Generator
Generates a professional branded PDF document from the technical overview content.
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ─── Color Palette ───
C = {
    "bg":       colors.HexColor("#020617"),
    "bg2":      colors.HexColor("#0f172a"),
    "card":     colors.HexColor("#1e293b"),
    "accent":   colors.HexColor("#1e3a5f"),
    "white":    colors.HexColor("#f8fafc"),
    "light":    colors.HexColor("#e2e8f0"),
    "muted":    colors.HexColor("#94a3b8"),
    "dim":      colors.HexColor("#64748b"),
    "green":    colors.HexColor("#22c55e"),
    "yellow":   colors.HexColor("#eab308"),
    "orange":   colors.HexColor("#f97316"),
    "red":      colors.HexColor("#ef4444"),
    "blue":     colors.HexColor("#3b82f6"),
    "cyan":     colors.HexColor("#06b6d4"),
    "purple":   colors.HexColor("#a855f7"),
    "border":   colors.HexColor("#334155"),
}

PAGE_W, PAGE_H = A4
MARGIN = 25 * mm

# ─── Styles ───
def get_styles():
    return {
        "title": ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=26, textColor=C["white"], leading=32, spaceAfter=6),
        "h1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, textColor=C["white"], leading=24, spaceBefore=20, spaceAfter=8),
        "h2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14, textColor=C["blue"], leading=18, spaceBefore=14, spaceAfter=6),
        "h3": ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=11, textColor=C["light"], leading=14, spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, alignment=TA_JUSTIFY, spaceAfter=4),
        "small": ParagraphStyle("Small", fontName="Helvetica", fontSize=8, textColor=C["muted"], leading=11, spaceAfter=2),
        "caption": ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=8, textColor=C["dim"], leading=10, alignment=TA_CENTER),
        "bullet": ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5, textColor=C["light"], leading=14, leftIndent=16, bulletIndent=6, spaceAfter=2),
        "code": ParagraphStyle("Code", fontName="Courier", fontSize=8, textColor=C["cyan"], leading=11, leftIndent=10, spaceAfter=2),
    }


# ─── Header/Footer ───
def draw_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Header bar
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, PAGE_H - 22 * mm, PAGE_W, 22 * mm, fill=1, stroke=0)
    # Logo
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 16)
    canvas_obj.drawString(MARGIN, PAGE_H - 14 * mm, "GOVERN.AI")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawString(MARGIN, PAGE_H - 18 * mm, "Sovereign Control Plane for Enterprise AI")
    # Right header
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 10)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, "TECHNICAL OVERVIEW")
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 16 * mm, f"v2.4 — {datetime.now().strftime('%B %Y')}")
    canvas_obj.setFillColor(C["red"])
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 20 * mm, "Confidential")
    # Footer
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.setLineWidth(0.4)
    canvas_obj.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.drawString(MARGIN, 8 * mm, "GOVERN.AI by ANTHERA Systems — Confidential")
    canvas_obj.drawCentredString(PAGE_W / 2, 8 * mm, f"Page {doc.page}")
    canvas_obj.drawRightString(PAGE_W - MARGIN, 8 * mm, datetime.now().strftime("%d/%m/%Y %H:%M"))
    canvas_obj.restoreState()


def draw_first_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Full dark background
    canvas_obj.setFillColor(C["bg"])
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Accent stripe
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
    # Title
    canvas_obj.setFillColor(C["white"])
    canvas_obj.setFont("Helvetica-Bold", 42)
    canvas_obj.drawString(MARGIN, PAGE_H - 80 * mm, "GOVERN.AI")
    # Subtitle
    canvas_obj.setFillColor(C["muted"])
    canvas_obj.setFont("Helvetica", 14)
    canvas_obj.drawString(MARGIN, PAGE_H - 90 * mm, "The Sovereign Control Plane for Enterprise AI")
    # Divider
    canvas_obj.setStrokeColor(C["border"])
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN, PAGE_H - 96 * mm, PAGE_W - MARGIN, PAGE_H - 96 * mm)
    # Document type
    canvas_obj.setFillColor(C["blue"])
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(MARGIN, PAGE_H - 108 * mm, "TECHNICAL OVERVIEW")
    # Meta
    meta_y = PAGE_H - 120 * mm
    canvas_obj.setFillColor(C["light"])
    canvas_obj.setFont("Helvetica", 10)
    canvas_obj.drawString(MARGIN, meta_y, f"Versione: MVP 2.4")
    canvas_obj.drawString(MARGIN, meta_y - 16, f"Data: {datetime.now().strftime('%B %Y')}")
    canvas_obj.drawString(MARGIN, meta_y - 32, "Autore: ANTHERA Systems")
    canvas_obj.drawString(MARGIN, meta_y - 48, "Classificazione: Confidential")
    # Bottom info
    canvas_obj.setFillColor(C["dim"])
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(MARGIN, 30 * mm, "Angelo Anglani — Founder & Lead Engineer")
    canvas_obj.drawString(MARGIN, 25 * mm, "angelo.anglani94@gmail.com | +39 342 754 8655")
    canvas_obj.drawString(MARGIN, 20 * mm, "linkedin.com/in/angelo-anglani")
    canvas_obj.restoreState()


# ─── Table helper ───
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
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        bg = C["bg2"] if i % 2 == 0 else C["card"]
        style.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style))
    return t


def build_pdf() -> bytes:
    buf = io.BytesIO()
    S = get_styles()
    elements = []

    # ─── COVER (handled by draw_first_page, just add a page break) ───
    elements.append(PageBreak())

    # ─── TABLE OF CONTENTS ───
    elements.append(Paragraph("Indice", S["h1"]))
    elements.append(Spacer(1, 8))
    toc_items = [
        "1. Executive Summary",
        "2. Architettura del Sistema",
        "3. Modello Dati (7 Collections)",
        "4. Flussi Applicativi",
        "5. Sistema di Sicurezza",
        "6. Moduli Funzionali",
        "7. Compliance Framework",
        "8. Deployment & DevOps",
        "9. Roadmap Prodotto",
        "10. Target Audience & Value Proposition",
    ]
    for item in toc_items:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {item}", S["bullet"]))
    elements.append(PageBreak())

    # ─── 1. EXECUTIVE SUMMARY ───
    elements.append(Paragraph("1. Executive Summary", S["h1"]))
    elements.append(Paragraph(
        "GOVERN.AI e una piattaforma software (SaaS) progettata per <b>governare, monitorare e garantire la compliance</b> degli agenti AI nelle organizzazioni enterprise. "
        "Si posiziona come il <b>control plane</b> tra gli agenti AI aziendali e le normative europee, garantendo che ogni azione sia tracciata, conforme e auditabile.",
        S["body"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Il Problema", S["h2"]))
    problems = [
        "<b>Mancanza di visibilita:</b> Le organizzazioni non sanno cosa fanno i loro agenti AI",
        "<b>Rischio normativo:</b> EU AI Act, GDPR, DORA, NIS2 richiedono tracciabilita completa",
        "<b>Assenza di controllo:</b> Nessun meccanismo per definire policy di governance degli agenti",
        "<b>Audit impossibile:</b> Nessun log strutturato per dimostrare conformita ai regolatori",
    ]
    for p in problems:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {p}", S["bullet"]))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("La Soluzione", S["h2"]))
    solutions = [
        "<b>Registro centralizzato</b> di tutti gli agenti AI con profilo di rischio completo",
        "<b>Motore di policy</b> con rilevamento automatico conflitti per 8 normative",
        "<b>SOX Section 404 Wizard</b> con Audit Readiness Score per controlli interni",
        "<b>Audit trail completo</b> di ogni azione, con export PDF/CSV per i regolatori",
        "<b>Dashboard di compliance</b> con monitoraggio real-time di 8 standard",
        "<b>Assistente AI (ARIA)</b> esperto di regolamentazione, con SSE streaming",
    ]
    for s in solutions:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {s}", S["bullet"]))
    elements.append(PageBreak())

    # ─── 2. ARCHITETTURA ───
    elements.append(Paragraph("2. Architettura del Sistema", S["h1"]))
    elements.append(Paragraph(
        "L'architettura segue un pattern a due tier (Frontend SPA + Backend API) con database document-oriented e integrazione LLM esterna. "
        "L'intero stack e containerizzato con Docker Compose.",
        S["body"]
    ))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("2.1 Stack Frontend", S["h2"]))
    elements.append(make_table(
        ["Componente", "Tecnologia", "Scopo"],
        [
            ["Framework", "React 19", "UI reattiva e componentizzata"],
            ["Styling", "Tailwind CSS 3.4", "Design system utility-first"],
            ["Components", "Shadcn/UI + Radix", "Componenti accessibili e consistenti"],
            ["Charts", "Recharts", "Visualizzazioni dati interattive"],
            ["Routing", "React Router 6", "Navigazione SPA client-side"],
            ["HTTP Client", "Axios", "Chiamate API con interceptor JWT automatico"],
            ["i18n", "Custom Context", "Interfaccia bilingue IT/EN"],
        ],
        col_widths=[90, 100, PAGE_W - 2 * MARGIN - 190]
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2.2 Stack Backend", S["h2"]))
    elements.append(make_table(
        ["Componente", "Tecnologia", "Scopo"],
        [
            ["Framework", "FastAPI 0.110", "API REST async ad alte prestazioni"],
            ["Runtime", "Uvicorn (ASGI)", "Server asincrono production-grade"],
            ["Validation", "Pydantic V2", "Type safety e validazione automatica"],
            ["Database Driver", "Motor (async)", "Operazioni MongoDB non bloccanti"],
            ["Auth", "python-jose + bcrypt", "JWT HS256 + password hashing sicuro"],
            ["Rate Limiting", "SlowAPI", "Protezione endpoint da abusi"],
            ["PDF Export", "ReportLab 4.1", "Generazione report professionali"],
            ["LLM", "Emergent Integrations", "Accesso a OpenAI GPT-5.2"],
        ],
        col_widths=[90, 110, PAGE_W - 2 * MARGIN - 200]
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2.3 Infrastruttura", S["h2"]))
    elements.append(make_table(
        ["Componente", "Tecnologia", "Scopo"],
        [
            ["Database", "MongoDB 7.0", "Document store flessibile con 15 indici"],
            ["Container", "Docker + Compose", "Orchestrazione 3 container (FE, BE, DB)"],
            ["Proxy", "Nginx", "Reverse proxy per SPA routing + API forwarding"],
        ],
        col_widths=[90, 110, PAGE_W - 2 * MARGIN - 200]
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2.4 Struttura del Progetto", S["h2"]))
    code_lines = [
        "backend/",
        "  server.py          # Entry point, middleware, lifespan",
        "  models.py           # Pydantic models + Enum",
        "  database.py         # Motor connection + indexes",
        "  seed.py             # Enterprise demo data (14 agents, 20+ policies, 150+ logs, 20 SOX controls)",
        "  exporters.py        # PDF/CSV generation (ReportLab)",
        "  routes/             # 9 modular routers (auth, agents, policies, audit, sox_wizard, policy_engine, ...)",
        "frontend/src/",
        "  pages/              # DashboardLayout, OverviewPage, AgentsPage, ...",
        "  components/         # CrudPage (generic), Logo, UI components",
        "  locales/            # Traduzioni IT/EN",
    ]
    for line in code_lines:
        elements.append(Paragraph(line, S["code"]))
    elements.append(PageBreak())

    # ─── 3. MODELLO DATI ───
    elements.append(Paragraph("3. Modello Dati", S["h1"]))
    elements.append(Paragraph(
        "Il database MongoDB ospita 7 collections con 15+ indici ottimizzati per performance su query con filtri, ordinamento e ricerca full-text.",
        S["body"]
    ))

    collections = [
        ("users", "Utenti della piattaforma", [
            ["id", "UUID", "Identificativo univoco"],
            ["username", "String (unique)", "Nome utente per login"],
            ["email", "String", "Email aziendale"],
            ["password_hash", "String", "Hash bcrypt della password"],
            ["role", "Enum", "admin | dpo | auditor | viewer"],
        ]),
        ("agents", "Registro agenti AI", [
            ["id", "UUID", "Identificativo univoco"],
            ["name", "String", "Nome descrittivo dell'agente"],
            ["model_type", "String", "GPT-5.2 | Claude-3.5 | Custom-ML"],
            ["risk_level", "Enum", "low | medium | high | critical"],
            ["status", "Enum", "active | suspended | inactive"],
            ["allowed_actions", "Array", "Whitelist azioni consentite"],
            ["restricted_domains", "Array", "Blacklist domini ristretti"],
            ["data_classification", "String", "public | internal | confidential | restricted"],
        ]),
        ("policies", "Regole di governance", [
            ["id", "UUID", "Identificativo univoco"],
            ["name", "String", "Nome della policy"],
            ["rule_type", "Enum", "restriction | logging | rate_limit | approval | retention"],
            ["regulation", "Enum", "GDPR | EU-AI-ACT | ISO-27001 | ISO-42001 | DORA | NIS2"],
            ["severity", "Enum", "low | medium | high | critical"],
            ["enforcement", "Enum", "block | log | throttle | auto"],
        ]),
        ("audit_logs", "Traccia immutabile azioni AI", [
            ["id", "UUID", "Identificativo univoco"],
            ["timestamp", "ISO DateTime", "Momento esatto dell'evento"],
            ["agent_name", "String", "Agente coinvolto"],
            ["action", "String", "Tipo di azione eseguita"],
            ["outcome", "Enum", "allowed | blocked | escalated | logged"],
            ["risk_level", "Enum", "low | medium | high | critical"],
            ["policy_applied", "String", "Policy che ha determinato l'esito"],
        ]),
        ("compliance_standards", "Standard normativi monitorati", [
            ["code", "String", "Codice standard (es. GDPR)"],
            ["progress", "Integer", "Percentuale completamento (0-100)"],
            ["requirements_total", "Integer", "Requisiti totali"],
            ["requirements_met", "Integer", "Requisiti soddisfatti"],
            ["status", "Enum", "compliant | in_progress | non_compliant"],
        ]),
        ("chat_messages", "Storico conversazioni ARIA", [
            ["session_id", "String", "ID sessione conversazionale"],
            ["role", "Enum", "user | assistant"],
            ["content", "String", "Contenuto messaggio (markdown)"],
            ["timestamp", "ISO DateTime", "Momento del messaggio"],
        ]),
        ("sox_controls", "Controlli interni SOX Section 404", [
            ["domain", "String", "Access Control | Change Mgmt | IT Ops | Data Integrity | Security"],
            ["control_id", "String", "Codice controllo (es. AC-01)"],
            ["status", "Enum", "not_started | in_progress | completed | failed"],
            ["evidence", "String", "Evidenze documentali"],
            ["risk_level", "Enum", "low | medium | high | critical"],
        ]),
    ]

    for coll_name, coll_desc, fields in collections:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"3.x Collection: <font color='#3b82f6'>{coll_name}</font>", S["h3"]))
        elements.append(Paragraph(coll_desc, S["small"]))
        elements.append(make_table(
            ["Campo", "Tipo", "Descrizione"],
            fields,
            col_widths=[100, 90, PAGE_W - 2 * MARGIN - 190]
        ))

    elements.append(PageBreak())

    # ─── 4. FLUSSI APPLICATIVI ───
    elements.append(Paragraph("4. Flussi Applicativi", S["h1"]))

    elements.append(Paragraph("4.1 Flusso di Autenticazione", S["h2"]))
    auth_steps = [
        "<b>1. Login Request:</b> Il client invia POST /api/auth/login con username e password.",
        "<b>2. Verifica Credenziali:</b> Il backend cerca l'utente nel DB e verifica l'hash bcrypt.",
        "<b>3. Generazione JWT:</b> Se valido, genera un token JWT (HS256) con payload {sub, role, exp} e scadenza 8 ore.",
        "<b>4. Audit Log:</b> Registra automaticamente un evento 'login' nell'audit trail.",
        "<b>5. Client Storage:</b> Il frontend salva il token in localStorage. L'interceptor Axios aggiunge automaticamente l'header 'Authorization: Bearer {token}' a tutte le richieste.",
    ]
    for step in auth_steps:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {step}", S["bullet"]))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("4.2 Flusso CRUD con Audit Automatico", S["h2"]))
    crud_steps = [
        "<b>1. Richiesta API:</b> Il client invia una richiesta (es. POST /api/agents) con il JWT nell'header.",
        "<b>2. Validazione JWT:</b> Il middleware verifica il token e controlla che il ruolo abbia i permessi necessari (RBAC).",
        "<b>3. Validazione Dati:</b> Pydantic V2 valida automaticamente il body della richiesta contro il modello definito.",
        "<b>4. Operazione Database:</b> Motor esegue l'operazione su MongoDB in modo asincrono.",
        "<b>5. Audit Automatico:</b> Ogni operazione CRUD genera un audit_log con dettagli completi (agente, azione, utente, esito).",
    ]
    for step in crud_steps:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {step}", S["bullet"]))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("4.3 Flusso ARIA AI Assistant", S["h2"]))
    aria_steps = [
        "<b>1. Query Utente:</b> POST /api/chat con messaggio e session_id. Validazione lunghezza (5-2000 chars).",
        "<b>2. Rate Limiting:</b> SlowAPI verifica il limite di 10 query/minuto per utente.",
        "<b>3. Context Loading:</b> Carica lo storico della conversazione da chat_messages per mantenere il contesto.",
        "<b>4. System Prompt:</b> Prepara il prompt di sistema che definisce ARIA come esperta di compliance EU.",
        "<b>5. LLM Call:</b> Invia la richiesta a GPT-5.2 tramite Emergent Integrations con tutto il contesto.",
        "<b>6. Persistenza:</b> Salva sia il messaggio utente che la risposta in chat_messages. Log audit 'chat_query'.",
    ]
    for step in aria_steps:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {step}", S["bullet"]))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("4.4 Flusso Export PDF", S["h2"]))
    export_steps = [
        "<b>1. Richiesta:</b> GET /api/audit/export/pdf con query params per filtri (outcome, risk_level, search).",
        "<b>2. Verifica RBAC:</b> Solo ruoli admin, dpo e auditor possono esportare.",
        "<b>3. Query Filtrata:</b> MongoDB restituisce i dati filtrati secondo i parametri.",
        "<b>4. Generazione PDF:</b> ReportLab costruisce il documento con header GOVERN.AI, tabella colorata e executive summary.",
        "<b>5. Streaming Response:</b> Il PDF viene inviato come StreamingResponse con Content-Disposition: attachment.",
    ]
    for step in export_steps:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {step}", S["bullet"]))
    elements.append(PageBreak())

    # ─── 5. SICUREZZA ───
    elements.append(Paragraph("5. Sistema di Sicurezza", S["h1"]))

    elements.append(Paragraph("5.1 Autenticazione JWT", S["h2"]))
    elements.append(Paragraph(
        "L'autenticazione utilizza JSON Web Token (JWT) con algoritmo HS256. I token hanno una durata di 8 ore e contengono "
        "il nome utente (sub), il ruolo (role) e la scadenza (exp). La chiave segreta e configurata tramite variabile d'ambiente.",
        S["body"]
    ))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("5.2 RBAC — Role-Based Access Control", S["h2"]))
    elements.append(Paragraph(
        "Il sistema implementa 4 ruoli gerarchici. Ogni endpoint verifica che il ruolo dell'utente abbia un livello sufficiente. "
        "La gerarchia e: Admin (4) > DPO (3) > Auditor (2) > Viewer (1).",
        S["body"]
    ))
    elements.append(make_table(
        ["Ruolo", "Livello", "Read", "Write", "Delete", "Export", "Admin"],
        [
            ["Admin", "4", "Si", "Si", "Si", "Si", "Si"],
            ["DPO", "3", "Si", "Si", "No", "Si", "No"],
            ["Auditor", "2", "Si", "No", "No", "Si", "No"],
            ["Viewer", "1", "Si", "No", "No", "No", "No"],
        ],
        col_widths=[60, 45, 45, 45, 45, 45, 45]
    ))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("5.3 Rate Limiting", S["h2"]))
    elements.append(make_table(
        ["Endpoint", "Limite", "Motivazione"],
        [
            ["/api/auth/login", "5 richieste/min", "Prevenzione attacchi brute-force"],
            ["/api/chat", "10 richieste/min", "Controllo costi LLM (GPT-5.2)"],
            ["/api/*/export/pdf", "5 richieste/min", "Generazione PDF CPU-intensive"],
            ["/api/*/export/csv", "10 richieste/min", "File CSV piu leggeri"],
            ["Altri endpoint", "30-60 richieste/min", "Uso applicativo normale"],
        ],
        col_widths=[120, 100, PAGE_W - 2 * MARGIN - 220]
    ))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("5.4 Security Headers", S["h2"]))
    headers_list = [
        "<b>X-Content-Type-Options: nosniff</b> — Previene MIME type sniffing",
        "<b>X-Frame-Options: DENY</b> — Previene clickjacking (iframe)",
        "<b>X-XSS-Protection: 1; mode=block</b> — Filtro XSS del browser",
        "<b>Referrer-Policy: strict-origin-when-cross-origin</b> — Controlla info referer",
        "<b>Permissions-Policy: camera=(), microphone=()</b> — Disabilita API sensibili",
    ]
    for h in headers_list:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {h}", S["bullet"]))
    elements.append(PageBreak())

    # ─── 6. MODULI FUNZIONALI ───
    elements.append(Paragraph("6. Moduli Funzionali", S["h1"]))

    modules = [
        ("6.1 Agent Registry", "Censimento di tutti gli agenti AI dell'organizzazione",
         "Traccia nome, descrizione, tipo di modello (GPT-5.2, Claude, Custom ML), livello di rischio (low/medium/high/critical), "
         "stato operativo (active/suspended/inactive), azioni consentite (whitelist), domini ristretti (blacklist), classificazione "
         "dei dati e responsabile.",
         "Il DPO deve sapere quanti agenti AI ad alto rischio sono in produzione e chi ne e responsabile per la reportistica EU AI Act."),
        ("6.2 Policy Engine", "Definizione di regole di governance per gli agenti",
         "Supporta 5 tipi di regole: restriction (blocca azioni), logging (forza log dettagliato), rate_limit (limita frequenza), "
         "approval (richiede approvazione umana), retention (gestisce conservazione dati). Ogni policy e mappata su una normativa "
         "europea specifica con 4 livelli di enforcement.",
         "Creare una policy 'High-Risk AI Oversight' che blocchi decisioni automatiche di credito senza approvazione umana (EU AI Act Art. 14)."),
        ("6.3 Audit Trail", "Tracciabilita completa di ogni azione AI",
         "Registra timestamp, agente, azione, risorsa acceduta, esito (allowed/blocked/escalated/logged), livello di rischio, "
         "policy applicata, utente e IP. Supporta ricerca full-text, filtri multipli e export in PDF (report branded con Executive "
         "Summary) e CSV (UTF-8 BOM per Excel).",
         "Durante un'ispezione Garante Privacy, esportare tutti gli eventi 'blocked' dell'ultimo trimestre con dettagli delle policy GDPR violate."),
        ("6.4 Compliance Dashboard", "Monitoraggio real-time dello stato di conformita",
         "Monitora 6 standard europei: EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2. Per ogni standard traccia: percentuale "
         "di avanzamento, requisiti soddisfatti/totali, stato (compliant/in_progress/non_compliant), data ultimo assessment e prossima revisione.",
         "Verificare lo stato di avanzamento GDPR prima dell'audit annuale e identificare i gap da colmare."),
        ("6.5 ARIA AI Assistant", "Consulente AI esperto di compliance EU",
         "Assistente basato su GPT-5.2 con system prompt specializzato in normative europee (AI Act, GDPR, DORA, NIS2, ISO). "
         "Mantiene il contesto conversazionale tramite session_id, risponde in italiano e inglese, formatta in Markdown.",
         "Chiedere ad ARIA come classificare un agente di credit scoring secondo l'EU AI Act e quali requisiti documentali soddisfare."),
        ("6.6 Export & Reporting", "Generazione report professionali",
         "PDF: Report branded con header GOVERN.AI, tabelle colorate per rischio/esito, Executive Summary con statistiche aggregate. "
         "CSV: Export con UTF-8 BOM per compatibilita Excel, supporto filtri. Entrambi protetti da RBAC (solo admin, dpo, auditor).",
         "Generare un report audit PDF completo per il consiglio di amministrazione di un istituto bancario prima di un'ispezione."),
    ]

    for title, purpose, desc, use_case in modules:
        elements.append(Paragraph(title, S["h2"]))
        elements.append(Paragraph(f"<b>Scopo:</b> {purpose}", S["body"]))
        elements.append(Paragraph(desc, S["body"]))
        elements.append(Paragraph(f"<i>Use case: {use_case}</i>", S["small"]))
        elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # ─── 7. COMPLIANCE FRAMEWORK ───
    elements.append(Paragraph("7. Compliance Framework", S["h1"]))
    elements.append(Paragraph(
        "GOVERN.AI monitora 8 standard normativi europei e internazionali, coprendo l'intero spettro di requisiti per le organizzazioni "
        "che utilizzano agenti AI in settori regolamentati (finance, healthcare, PA, energy).",
        S["body"]
    ))
    elements.append(make_table(
        ["Standard", "Tipo", "Focus", "Sanzioni", "Progress Demo"],
        [
            ["EU AI Act", "Regolamento", "Classificazione rischio AI", "Fino a 35M / 7%", "45%"],
            ["GDPR", "Regolamento", "Protezione dati personali", "Fino a 20M / 4%", "78%"],
            ["ISO 27001", "Standard", "Sicurezza delle informazioni", "Perdita certificazione", "92%"],
            ["ISO 42001", "Standard", "Gestione sistemi AI", "Perdita certificazione", "35%"],
            ["DORA", "Regolamento", "Resilienza digitale finanza", "Sanzioni settoriali", "61%"],
            ["NIS2", "Direttiva", "Cybersecurity infrastrutture", "Fino a 10M / 2%", "83%"],
            ["SOX", "Regolamento", "Controlli interni finanziari", "Sanzioni penali/civili", "56%"],
            ["D.Lgs. 262", "Legge IT", "Controlli contabili quotate", "Sanzioni CONSOB", "48%"],
        ],
        col_widths=[65, 65, 120, 95, 65]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "<i>I valori di progress si riferiscono allo scenario demo enterprise (Banca Enterprise S.p.A.) e rappresentano "
        "un esempio realistico di stato di conformita per un istituto bancario italiano.</i>",
        S["small"]
    ))
    elements.append(PageBreak())

    # ─── 8. DEPLOYMENT ───
    elements.append(Paragraph("8. Deployment & DevOps", S["h1"]))
    elements.append(Paragraph(
        "L'intero stack applicativo e containerizzato con Docker e orchestrato tramite Docker Compose. "
        "Il setup completo richiede 3 comandi.",
        S["body"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("8.1 Architettura Container", S["h2"]))
    elements.append(make_table(
        ["Container", "Immagine Base", "Porta", "Funzione"],
        [
            ["MongoDB", "mongo:7", "27017", "Database con volume persistente"],
            ["Backend", "python:3.11-slim", "8001", "FastAPI + Uvicorn + auto-seed"],
            ["Frontend", "node:18 + nginx:alpine", "3000", "React build + Nginx reverse proxy"],
        ],
        col_widths=[70, 100, 50, PAGE_W - 2 * MARGIN - 220]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("8.2 Setup Rapido", S["h2"]))
    setup_cmds = [
        "git clone https://github.com/.../GOVERN.AI && cd GOVERN.AI",
        "cp .env.example backend/.env   # Configurare JWT_SECRET_KEY e LLM key",
        "docker-compose up --build      # Avvia tutti i servizi",
        "# Accessibile su http://localhost:3000",
        "# Credenziali demo: admin / AdminGovern2026!",
    ]
    for cmd in setup_cmds:
        elements.append(Paragraph(cmd, S["code"]))
    elements.append(PageBreak())

    # ─── 9. ROADMAP ───
    elements.append(Paragraph("9. Roadmap Prodotto", S["h1"]))

    elements.append(Paragraph("Completato (MVP v2.4)", S["h2"]))
    completed = [
        "Core platform completa (Agent Registry, Policy Engine, Audit Trail, Compliance Monitor)",
        "Autenticazione JWT con RBAC a 4 livelli",
        "ARIA AI Assistant con SSE streaming",
        "Export report in PDF e CSV (Audit, Compliance, SOX)",
        "Dashboard con 3 grafici interattivi (Recharts)",
        "8 standard normativi (EU AI Act, GDPR, ISO 27001/42001, DORA, NIS2, SOX, D.Lgs. 262)",
        "SOX Section 404 Wizard con 20 controlli e Audit Readiness Score",
        "Policy Conflict Detection Engine (4 tipi di conflitto)",
        "CI/CD GitHub Actions (4 job)",
        "Docker deployment (Compose) + Interfaccia mobile responsive",
    ]
    for item in completed:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {item}", S["bullet"]))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Prossimi Sviluppi", S["h2"]))
    next_items = [
        "<b>D.Lgs. 262 Wizard:</b> Workflow dedicato per attestazione dirigente preposto",
        "<b>Auto-Fix Engine:</b> Risoluzione automatica dei conflitti tra policy",
        "<b>Test Frontend:</b> Test unitari con Jest e Testing Library",
    ]
    for item in next_items:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {item}", S["bullet"]))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Vision Enterprise (P2)", S["h2"]))
    future_items = [
        "<b>Multi-tenancy:</b> Supporto clienti multipli con isolamento dati",
        "<b>Connettori Enterprise:</b> Integrazione con SIEM (Splunk, ELK), IAM (Okta, Azure AD), ServiceNow",
        "<b>WebSocket Real-time:</b> Monitoraggio live con aggiornamenti push",
        "<b>API Key Management:</b> Registrazione agenti via API esterna",
        "<b>Sistema Notifiche:</b> Email alerts su violazioni policy critiche",
    ]
    for item in future_items:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {item}", S["bullet"]))
    elements.append(PageBreak())

    # ─── 10. VALUE PROPOSITION ───
    elements.append(Paragraph("10. Target Audience & Value Proposition", S["h1"]))

    personas = [
        ("DPO / Compliance Manager", [
            "Visibilita totale sugli agenti AI in produzione",
            "Tracciabilita di ogni azione per audit e ispezioni",
            "Mapping normativo automatico (GDPR, AI Act, DORA)",
            "Report pronti per regolatori in formato PDF",
        ]),
        ("CISO", [
            "Classificazione rischio allineata a EU AI Act",
            "Policy enforcement automatico con 4 livelli",
            "Security headers e rate limiting integrati",
            "RBAC granulare con 4 livelli di permessi",
        ]),
        ("CTO / Engineering", [
            "API REST documentata (Swagger/ReDoc automatico)",
            "Architettura modulare e manutenibile",
            "Stack moderno (FastAPI, React, MongoDB)",
            "Docker ready per deployment rapido",
        ]),
        ("CEO / Board", [
            "Riduzione rischio sanzioni (AI Act: fino a 35M)",
            "Due diligence documentabile per investitori",
            "Competitive advantage sulla compliance",
            "Dashboard executive con KPI real-time",
        ]),
    ]

    for persona_name, points in personas:
        elements.append(Paragraph(persona_name, S["h2"]))
        for pt in points:
            elements.append(Paragraph(f"<bullet>&bull;</bullet> {pt}", S["bullet"]))
        elements.append(Spacer(1, 4))

    # ─── CLOSING ───
    elements.append(PageBreak())
    elements.append(Spacer(1, 60))
    elements.append(Paragraph("GOVERN.AI", S["title"]))
    elements.append(Paragraph("Sovereign Control Plane for Enterprise AI", S["body"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("powered by ANTHERA Systems", S["small"]))
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="30%", thickness=0.5, color=C["border"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Angelo Anglani</b> — Founder & Lead Engineer", S["body"]))
    elements.append(Paragraph("angelo.anglani94@gmail.com | +39 342 754 8655", S["body"]))
    elements.append(Paragraph("linkedin.com/in/angelo-anglani", S["body"]))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Documento generato: {datetime.now().strftime('%B %Y')} — Versione 2.4", S["caption"]))

    # ─── BUILD ───
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=26 * mm, bottomMargin=18 * mm,
    )
    doc.build(elements, onFirstPage=draw_first_page, onLaterPages=draw_page)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    pdf_bytes = build_pdf()
    output_path = "/app/GOVERN_AI_Technical_Overview.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF generated: {output_path} ({len(pdf_bytes)} bytes)")
