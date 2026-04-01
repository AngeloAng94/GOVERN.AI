"""
GOVERN.AI Export Functions
Generates PDF and CSV exports for audit logs and compliance reports
"""

import io
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


# Color definitions matching GOVERN.AI design system
COLORS = {
    "bg_dark": colors.HexColor("#020617"),
    "bg_card": colors.HexColor("#0f172a"),
    "bg_row_even": colors.HexColor("#0f172a"),
    "bg_row_odd": colors.HexColor("#1a2744"),
    "header_bg": colors.HexColor("#1e3a5f"),
    "border": colors.HexColor("#1e293b"),
    "text_white": colors.HexColor("#ffffff"),
    "text_light": colors.HexColor("#e2e8f0"),
    "text_muted": colors.HexColor("#94a3b8"),
    "text_dim": colors.HexColor("#64748b"),
    "green": colors.HexColor("#22c55e"),
    "yellow": colors.HexColor("#eab308"),
    "orange": colors.HexColor("#f97316"),
    "red": colors.HexColor("#ef4444"),
    "blue": colors.HexColor("#3b82f6"),
}


def get_outcome_color(outcome: str) -> colors.HexColor:
    """Get color for audit outcome"""
    mapping = {
        "allowed": COLORS["green"],
        "blocked": COLORS["red"],
        "escalated": COLORS["orange"],
        "logged": COLORS["blue"],
    }
    return mapping.get(outcome.lower(), COLORS["text_muted"])


def get_risk_color(risk: str) -> colors.HexColor:
    """Get color for risk level"""
    mapping = {
        "critical": COLORS["red"],
        "high": COLORS["orange"],
        "medium": COLORS["yellow"],
        "low": COLORS["green"],
    }
    return mapping.get(risk.lower(), COLORS["text_muted"])


def get_progress_color(value: int) -> colors.HexColor:
    """Get color based on progress percentage"""
    if value >= 80:
        return COLORS["green"]
    elif value >= 50:
        return COLORS["yellow"]
    return COLORS["red"]


def format_timestamp(ts: str, format: str = "%d/%m/%Y %H:%M:%S") -> str:
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime(format)
    except:
        return ts


# ============================================================================
# CSV EXPORT
# ============================================================================

def generate_audit_csv(audit_logs: List[Dict[str, Any]]) -> bytes:
    """
    Generate CSV export of audit logs with UTF-8 BOM for Excel compatibility
    """
    output = io.StringIO()
    
    # Write UTF-8 BOM for Excel
    output.write('\ufeff')
    
    writer = csv.writer(output)
    
    # Header row
    writer.writerow([
        "Timestamp", "Agent", "Action", "Resource", "Outcome",
        "Risk Level", "Policy Applied", "User", "IP Address", "Details"
    ])
    
    # Data rows
    for log in audit_logs:
        writer.writerow([
            format_timestamp(log.get("timestamp", "")),
            log.get("agent_name", "—"),
            log.get("action", ""),
            log.get("resource", ""),
            log.get("outcome", "").upper(),
            log.get("risk_level", ""),
            log.get("policy_applied", "—"),
            log.get("user", ""),
            log.get("ip_address", ""),
            log.get("details", ""),
        ])
    
    return output.getvalue().encode("utf-8")


# ============================================================================
# PDF EXPORT - AUDIT TRAIL
# ============================================================================

class AuditPDFBuilder:
    """Builder for audit trail PDF reports"""
    
    def __init__(self, audit_logs: List[Dict], filters: Dict[str, Any]):
        self.audit_logs = audit_logs
        self.filters = filters
        self.buffer = io.BytesIO()
        self.page_width, self.page_height = landscape(A4)
        self.margin = 20
        
    def build(self) -> bytes:
        """Build the complete PDF"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=landscape(A4),
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=100,  # Space for header
            bottomMargin=50,
        )
        
        elements = []
        
        # Filter section
        elements.append(self._build_filter_section())
        elements.append(Spacer(1, 10))
        
        # Audit table
        if self.audit_logs:
            elements.append(self._build_audit_table())
        
        # Summary page
        elements.append(PageBreak())
        elements.extend(self._build_summary_section())
        
        # Build with custom canvas
        doc.build(elements, onFirstPage=self._draw_header_footer, onLaterPages=self._draw_header_footer)
        
        self.buffer.seek(0)
        return self.buffer.getvalue()
    
    def _draw_header_footer(self, canvas: canvas.Canvas, doc):
        """Draw header and footer on each page"""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(COLORS["bg_dark"])
        canvas.rect(0, self.page_height - 80, self.page_width, 80, fill=1, stroke=0)
        
        # Header text - left
        canvas.setFillColor(COLORS["text_white"])
        canvas.setFont("Helvetica-Bold", 24)
        canvas.drawString(self.margin, self.page_height - 40, "GOVERN.AI")
        
        canvas.setFillColor(COLORS["text_muted"])
        canvas.setFont("Helvetica", 10)
        canvas.drawString(self.margin, self.page_height - 55, "Sovereign Control Plane for Enterprise AI")
        
        # Header text - right
        canvas.setFillColor(COLORS["text_white"])
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 35, "AUDIT TRAIL REPORT")
        
        canvas.setFillColor(COLORS["text_muted"])
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 50, f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas.setFillColor(COLORS["red"])
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 65, "Confidential")
        
        # Footer
        canvas.setStrokeColor(COLORS["border"])
        canvas.setLineWidth(0.5)
        canvas.line(self.margin, 35, self.page_width - self.margin, 35)
        
        canvas.setFillColor(COLORS["text_dim"])
        canvas.setFont("Helvetica", 7)
        canvas.drawString(self.margin, 22, "GOVERN.AI — Confidential")
        canvas.drawCentredString(self.page_width / 2, 22, f"Page {doc.page}")
        canvas.drawRightString(self.page_width - self.margin, 22, f"Generated {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        canvas.restoreState()
    
    def _build_filter_section(self) -> Table:
        """Build the filters applied section"""
        filter_texts = []
        if self.filters.get("outcome"):
            filter_texts.append(f"Outcome: {self.filters['outcome']}")
        if self.filters.get("risk_level"):
            filter_texts.append(f"Risk Level: {self.filters['risk_level']}")
        if self.filters.get("search"):
            filter_texts.append(f"Search: \"{self.filters['search']}\"")
        
        if filter_texts:
            text = "Filters applied: " + " | ".join(filter_texts)
        else:
            text = "All records — no filters applied"
        
        data = [[text]]
        table = Table(data, colWidths=[self.page_width - 2 * self.margin])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLORS["bg_card"]),
            ("TEXTCOLOR", (0, 0), (-1, -1), COLORS["text_muted"]),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def _build_audit_table(self) -> Table:
        """Build the main audit data table"""
        # Column widths (total ~802pt for landscape A4 with margins)
        col_widths = [100, 130, 110, 70, 70, 130, 90, 102]
        
        # Header row
        headers = ["Timestamp", "Agent", "Action", "Outcome", "Risk Level", "Policy", "User", "IP"]
        data = [headers]
        
        # Data rows
        for log in self.audit_logs:
            data.append([
                format_timestamp(log.get("timestamp", "")),
                log.get("agent_name", "—")[:20],
                log.get("action", "")[:18],
                log.get("outcome", "").upper(),
                log.get("risk_level", ""),
                log.get("policy_applied", "—")[:20] if log.get("policy_applied") else "—",
                log.get("user", "")[:15],
                log.get("ip_address", ""),
            ])
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Base style
        style = [
            # Header
            ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["text_white"]),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (-1, 0), "LEFT"),
            
            # Data rows
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("TEXTCOLOR", (0, 1), (-1, -1), COLORS["text_light"]),
            
            # Grid
            ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
            
            # Padding
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
        
        # Alternating row colors and outcome/risk coloring
        for i, row in enumerate(data[1:], start=1):
            # Alternating background
            bg_color = COLORS["bg_row_even"] if i % 2 == 0 else COLORS["bg_row_odd"]
            style.append(("BACKGROUND", (0, i), (-1, i), bg_color))
            
            # Outcome color (column 3)
            outcome = row[3].lower() if row[3] else ""
            style.append(("TEXTCOLOR", (3, i), (3, i), get_outcome_color(outcome)))
            
            # Risk level color (column 4)
            risk = row[4].lower() if row[4] else ""
            style.append(("TEXTCOLOR", (4, i), (4, i), get_risk_color(risk)))
        
        table.setStyle(TableStyle(style))
        return table
    
    def _build_summary_section(self) -> List:
        """Build the executive summary page"""
        elements = []
        
        # Title
        style = ParagraphStyle(
            "SummaryTitle",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=COLORS["text_white"],
        )
        elements.append(Paragraph("Executive Summary", style))
        elements.append(Spacer(1, 20))
        
        # Calculate statistics
        total = len(self.audit_logs)
        allowed = sum(1 for l in self.audit_logs if l.get("outcome") == "allowed")
        blocked = sum(1 for l in self.audit_logs if l.get("outcome") == "blocked")
        escalated = sum(1 for l in self.audit_logs if l.get("outcome") == "escalated")
        
        allowed_pct = round(allowed / total * 100, 1) if total else 0
        blocked_pct = round(blocked / total * 100, 1) if total else 0
        escalated_pct = round(escalated / total * 100, 1) if total else 0
        
        agents = list(set(l.get("agent_name", "Unknown") for l in self.audit_logs))
        
        # Get date range
        if self.audit_logs:
            timestamps = [l.get("timestamp", "") for l in self.audit_logs if l.get("timestamp")]
            if timestamps:
                timestamps.sort()
                date_range = f"{format_timestamp(timestamps[0], '%d/%m/%Y')} — {format_timestamp(timestamps[-1], '%d/%m/%Y')}"
            else:
                date_range = "N/A"
        else:
            date_range = "N/A"
        
        # Statistics table
        stats_data = [
            ["Total Events", str(total)],
            ["Allowed", f"{allowed} ({allowed_pct}%)"],
            ["Blocked", f"{blocked} ({blocked_pct}%)"],
            ["Escalated", f"{escalated} ({escalated_pct}%)"],
            ["Date Range", date_range],
            ["Agents Involved", ", ".join(agents[:5]) + ("..." if len(agents) > 5 else "")],
        ]
        
        stats_table = Table(stats_data, colWidths=[150, 400])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLORS["bg_card"]),
            ("TEXTCOLOR", (0, 0), (0, -1), COLORS["text_muted"]),
            ("TEXTCOLOR", (1, 0), (1, -1), COLORS["text_white"]),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 1, COLORS["border"]),
            ("LINEBELOW", (0, 0), (-1, -2), 0.5, COLORS["border"]),
        ]))
        elements.append(stats_table)
        
        # Legal note
        elements.append(Spacer(1, 40))
        legal_style = ParagraphStyle(
            "Legal",
            fontName="Helvetica",
            fontSize=8,
            textColor=COLORS["text_dim"],
            leading=12,
        )
        legal_text = (
            "This report is generated automatically by GOVERN.AI. "
            "For compliance purposes, retain for 7 years per SOX Section 802, "
            "EU AI Act Art. 18 and GDPR Art. 30 requirements."
        )
        elements.append(Paragraph(legal_text, legal_style))
        
        return elements


def generate_audit_pdf(audit_logs: List[Dict], filters: Dict[str, Any] = None) -> bytes:
    """Generate PDF export of audit trail"""
    builder = AuditPDFBuilder(audit_logs, filters or {})
    return builder.build()


# ============================================================================
# PDF EXPORT - COMPLIANCE REPORT
# ============================================================================

class CompliancePDFBuilder:
    """Builder for compliance status PDF reports"""
    
    def __init__(self, standards: List[Dict]):
        self.standards = standards
        self.buffer = io.BytesIO()
        self.page_width, self.page_height = A4
        self.margin = 20
        
    def build(self) -> bytes:
        """Build the complete PDF"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=100,
            bottomMargin=50,
        )
        
        elements = []
        
        # Overall score section
        elements.extend(self._build_overall_score())
        elements.append(Spacer(1, 20))
        
        # Standards cards
        for standard in self.standards:
            elements.append(self._build_standard_card(standard))
            elements.append(Spacer(1, 10))
        
        # Legal note
        elements.append(Spacer(1, 30))
        elements.append(self._build_legal_note())
        
        doc.build(elements, onFirstPage=self._draw_header_footer, onLaterPages=self._draw_header_footer)
        
        self.buffer.seek(0)
        return self.buffer.getvalue()
    
    def _draw_header_footer(self, canvas: canvas.Canvas, doc):
        """Draw header and footer"""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(COLORS["bg_dark"])
        canvas.rect(0, self.page_height - 80, self.page_width, 80, fill=1, stroke=0)
        
        # Header text
        canvas.setFillColor(COLORS["text_white"])
        canvas.setFont("Helvetica-Bold", 24)
        canvas.drawString(self.margin, self.page_height - 40, "GOVERN.AI")
        
        canvas.setFillColor(COLORS["text_muted"])
        canvas.setFont("Helvetica", 10)
        canvas.drawString(self.margin, self.page_height - 55, "Sovereign Control Plane for Enterprise AI")
        
        canvas.setFillColor(COLORS["text_white"])
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 35, "COMPLIANCE STATUS REPORT")
        
        canvas.setFillColor(COLORS["text_muted"])
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 50, f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        canvas.setFillColor(COLORS["red"])
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 65, "Confidential")
        
        # Footer
        canvas.setStrokeColor(COLORS["border"])
        canvas.line(self.margin, 35, self.page_width - self.margin, 35)
        
        canvas.setFillColor(COLORS["text_dim"])
        canvas.setFont("Helvetica", 7)
        canvas.drawString(self.margin, 22, "GOVERN.AI — Confidential")
        canvas.drawCentredString(self.page_width / 2, 22, f"Page {doc.page}")
        canvas.drawRightString(self.page_width - self.margin, 22, f"Generated {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        canvas.restoreState()
    
    def _build_overall_score(self) -> List:
        """Build overall compliance score section"""
        elements = []
        
        # Calculate average
        if self.standards:
            avg_progress = round(sum(s.get("progress", 0) for s in self.standards) / len(self.standards))
        else:
            avg_progress = 0
        
        # Title
        title_style = ParagraphStyle(
            "ScoreTitle",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=COLORS["text_white"],
        )
        elements.append(Paragraph("Overall Compliance Score", title_style))
        elements.append(Spacer(1, 10))
        
        # Score display
        score_color = get_progress_color(avg_progress)
        score_data = [[f"{avg_progress}%"]]
        score_table = Table(score_data, colWidths=[120])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLORS["bg_card"]),
            ("TEXTCOLOR", (0, 0), (-1, -1), score_color),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 36),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 15),
            ("BOX", (0, 0), (-1, -1), 1, COLORS["border"]),
        ]))
        elements.append(score_table)
        
        return elements
    
    def _build_standard_card(self, standard: Dict) -> Table:
        """Build a single compliance standard card"""
        progress = standard.get("progress", 0)
        progress_color = get_progress_color(progress)
        
        # Status badge
        status = standard.get("status", "in_progress")
        status_text = {
            "compliant": "COMPLIANT",
            "in_progress": "IN PROGRESS",
            "non_compliant": "AT RISK",
        }.get(status, "UNKNOWN")
        
        # Build content
        name = standard.get("name", "Unknown")
        code = standard.get("code", "")
        req_met = standard.get("requirements_met", 0)
        req_total = standard.get("requirements_total", 0)
        last_assess = format_timestamp(standard.get("last_assessment", ""), "%d/%m/%Y")
        next_review = format_timestamp(standard.get("next_review", ""), "%d/%m/%Y")
        
        # Create a single-row table to simulate a card
        content = f"""
        <b>{name}</b> ({code})<br/>
        <font size="9" color="#94a3b8">Progress: {progress}% | Requirements: {req_met}/{req_total}</font><br/>
        <font size="8" color="#64748b">Status: {status_text} | Last Assessment: {last_assess} | Next Review: {next_review}</font>
        """
        
        style = ParagraphStyle(
            "CardContent",
            fontName="Helvetica",
            fontSize=10,
            textColor=COLORS["text_white"],
            leading=14,
        )
        
        para = Paragraph(content, style)
        
        # Progress bar simulation using nested table
        bar_width = 400
        filled_width = int((progress / 100) * bar_width)
        
        progress_data = [[
            para,
            f"{progress}%"
        ]]
        
        card_table = Table(progress_data, colWidths=[self.page_width - 2 * self.margin - 80, 60])
        card_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLORS["bg_card"]),
            ("TEXTCOLOR", (1, 0), (1, 0), progress_color),
            ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (1, 0), (1, 0), 14),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 12),
            ("BOX", (0, 0), (-1, -1), 1, COLORS["border"]),
        ]))
        
        return card_table
    
    def _build_legal_note(self) -> Paragraph:
        """Build legal disclaimer"""
        style = ParagraphStyle(
            "Legal",
            fontName="Helvetica",
            fontSize=8,
            textColor=COLORS["text_dim"],
            leading=10,
        )
        text = (
            "This compliance report is generated automatically by GOVERN.AI. "
            "It reflects the compliance status as of the generation timestamp. "
            "For regulatory submissions, verify data accuracy with your compliance officer."
        )
        return Paragraph(text, style)


def generate_compliance_pdf(standards: List[Dict]) -> bytes:
    """Generate PDF export of compliance status"""
    builder = CompliancePDFBuilder(standards)
    return builder.build()
