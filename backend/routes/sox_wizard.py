from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from datetime import datetime, timezone
import io

from database import db
from models import AuditLog, AuditOutcome, RiskLevel
from routes.auth import require_role
from rate_limiter import limiter
from exporters import generate_sox_report_pdf

router = APIRouter(prefix="/api/sox", tags=["sox-wizard"])


@router.get("/controls")
async def list_sox_controls(user: dict = Depends(require_role("viewer"))):
    """Return all SOX controls grouped by domain."""
    controls = await db.sox_controls.find({}, {"_id": 0}).to_list(200)

    domain_map = {}
    for c in controls:
        d = c.get("domain", "Unknown")
        if d not in domain_map:
            domain_map[d] = []
        domain_map[d].append(c)

    domains = []
    total = 0
    completed = 0
    for name, ctrls in domain_map.items():
        done = sum(1 for c in ctrls if c.get("status") == "completed")
        pct = round(done / len(ctrls) * 100) if ctrls else 0
        domains.append({
            "name": name,
            "controls": ctrls,
            "completion_pct": pct,
        })
        total += len(ctrls)
        completed += done

    overall_pct = round(completed / total * 100) if total else 0
    return {
        "domains": domains,
        "overall_pct": overall_pct,
        "total": total,
        "completed": completed,
    }


@router.patch("/controls/{control_id}")
async def update_sox_control(
    control_id: str,
    data: dict,
    user: dict = Depends(require_role("auditor")),
):
    """Update a single SOX control and create an audit log."""
    existing = await db.sox_controls.find_one({"id": control_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Control not found")

    allowed = {"status", "evidence", "assignee", "due_date"}
    update = {k: v for k, v in data.items() if k in allowed}
    update["updated_at"] = datetime.now(timezone.utc).isoformat()

    if update.get("status") == "completed" and existing.get("status") != "completed":
        update["completed_date"] = datetime.now(timezone.utc).isoformat()

    await db.sox_controls.update_one({"id": control_id}, {"$set": update})

    # Audit log
    new_status = update.get("status", existing.get("status"))
    log = AuditLog(
        action="sox_control_updated",
        resource=f"/sox/controls/{control_id}",
        outcome=AuditOutcome.allowed,
        details=f"Control {existing['control_id']} '{existing['title']}' updated to {new_status}",
        risk_level=RiskLevel.medium,
        user=user["username"],
        agent_name="SOX Internal Control Auditor",
    )
    await db.audit_logs.insert_one(log.model_dump())

    return await db.sox_controls.find_one({"id": control_id}, {"_id": 0})


@router.get("/report")
async def sox_report_json(user: dict = Depends(require_role("viewer"))):
    """Generate SOX Section 404 report as structured JSON."""
    controls = await db.sox_controls.find({}, {"_id": 0}).to_list(200)

    domain_map = {}
    for c in controls:
        d = c.get("domain", "Unknown")
        if d not in domain_map:
            domain_map[d] = []
        domain_map[d].append(c)

    total = len(controls)
    completed = sum(1 for c in controls if c.get("status") == "completed")
    failed = sum(1 for c in controls if c.get("status") == "failed")
    in_progress = sum(1 for c in controls if c.get("status") == "in_progress")
    not_started = sum(1 for c in controls if c.get("status") == "not_started")

    overall_pct = round(completed / total * 100) if total else 0

    if overall_pct >= 80:
        overall_status = "READY FOR AUDIT"
    elif overall_pct >= 50:
        overall_status = "IN PROGRESS"
    else:
        overall_status = "NOT READY"

    domains = []
    for name, ctrls in domain_map.items():
        done = sum(1 for c in ctrls if c.get("status") == "completed")
        pct = round(done / len(ctrls) * 100) if ctrls else 0
        domains.append({"name": name, "controls": ctrls, "completion_pct": pct})

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fiscal_year": str(datetime.now().year),
        "organization": "GOVERN.AI Enterprise",
        "overall_status": overall_status,
        "overall_pct": overall_pct,
        "domains": domains,
        "controls_summary": {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "failed": failed,
        },
        "auditor_notes": "This report has been generated automatically by GOVERN.AI SOX Section 404 Wizard. All control assessments should be reviewed and validated by the internal audit team before submission.",
    }


@router.get("/report/pdf")
@limiter.limit("5/minute")
async def sox_report_pdf(
    request: Request,
    user: dict = Depends(require_role("dpo")),
):
    """Generate SOX Section 404 PDF report."""
    controls = await db.sox_controls.find({}, {"_id": 0}).to_list(200)
    pdf_bytes = generate_sox_report_pdf(controls)
    filename = f"SOX_404_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
