from fastapi import APIRouter, Depends, Request

from database import db
from routes.auth import require_role
from rate_limiter import limiter

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
@limiter.limit("30/minute")
async def get_dashboard_stats(request: Request, user: dict = Depends(require_role("viewer"))):
    agents_total = await db.agents.count_documents({})
    agents_active = await db.agents.count_documents({"status": "active"})
    policies_total = await db.policies.count_documents({})
    policies_active = await db.policies.count_documents({"status": "active"})
    audit_total = await db.audit_logs.count_documents({})
    audit_blocked = await db.audit_logs.count_documents({"outcome": "blocked"})
    audit_escalated = await db.audit_logs.count_documents({"outcome": "escalated"})
    compliance_list = await db.compliance_standards.find({}, {"_id": 0, "progress": 1}).to_list(100)
    avg_compliance = sum(c["progress"] for c in compliance_list) / len(compliance_list) if compliance_list else 0
    recent_audit = await db.audit_logs.find({}, {"_id": 0}).sort("timestamp", -1).to_list(5)
    risk_dist = {}
    async for a in db.agents.find({}, {"_id": 0, "risk_level": 1}):
        rl = a.get("risk_level", "unknown")
        risk_dist[rl] = risk_dist.get(rl, 0) + 1
    return {
        "agents": {"total": agents_total, "active": agents_active},
        "policies": {"total": policies_total, "active": policies_active},
        "audit": {"total": audit_total, "blocked": audit_blocked, "escalated": audit_escalated},
        "compliance_avg": round(avg_compliance, 1),
        "recent_audit": recent_audit,
        "risk_distribution": risk_dist
    }
