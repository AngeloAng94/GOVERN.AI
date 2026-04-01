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


@router.get("/readiness-score")
async def readiness_score(user: dict = Depends(require_role("viewer"))):
    """Calculate audit readiness score weighted by risk level."""
    controls = await db.sox_controls.find({}, {"_id": 0}).to_list(200)
    if not controls:
        return {"overall_score": 0, "label": "NOT READY", "label_color": "red",
                "gap_to_ready": 80, "priority_controls": [], "domain_scores": {},
                "estimated_completion_days": 0}

    weight = {"critical": 10, "high": 7, "medium": 5, "low": 3}

    max_points = sum(weight.get(c.get("risk_level", "medium"), 5) for c in controls)
    earned = sum(
        weight.get(c.get("risk_level", "medium"), 5)
        for c in controls if c.get("status") == "completed"
    )
    score = round(earned / max_points * 100, 1) if max_points else 0

    if score >= 80:
        label, color = "READY FOR AUDIT", "green"
    elif score >= 50:
        label, color = "IN PROGRESS", "yellow"
    else:
        label, color = "NOT READY", "red"

    gap = round(max(0, 80 - score), 1)

    # Priority controls: non-completed sorted by impact
    incomplete = [c for c in controls if c.get("status") != "completed"]
    for c in incomplete:
        c["_impact"] = weight.get(c.get("risk_level", "medium"), 5)
    incomplete.sort(key=lambda c: c["_impact"], reverse=True)

    priority = []
    for c in incomplete[:5]:
        impact_pct = round(c["_impact"] / max_points * 100, 1) if max_points else 0
        priority.append({
            "control_id": c.get("control_id"),
            "title": c.get("title"),
            "domain": c.get("domain"),
            "risk_level": c.get("risk_level"),
            "impact_points": impact_pct,
            "current_status": c.get("status"),
        })

    # Domain scores
    domain_map = {}
    for c in controls:
        d = c.get("domain", "Unknown")
        domain_map.setdefault(d, []).append(c)

    domain_scores = {}
    for name, ctrls in domain_map.items():
        d_max = sum(weight.get(c.get("risk_level", "medium"), 5) for c in ctrls)
        d_earned = sum(weight.get(c.get("risk_level", "medium"), 5) for c in ctrls if c.get("status") == "completed")
        domain_scores[name] = round(d_earned / d_max * 100, 1) if d_max else 0

    # Estimated days: ~3 days per critical, 2 per high, 1 per medium/low
    day_weight = {"critical": 3, "high": 2, "medium": 1, "low": 1}
    est_days = sum(day_weight.get(c.get("risk_level", "medium"), 1) for c in incomplete[:5])

    return {
        "overall_score": score,
        "label": label,
        "label_color": color,
        "gap_to_ready": gap,
        "priority_controls": priority,
        "domain_scores": domain_scores,
        "estimated_completion_days": est_days,
    }


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
