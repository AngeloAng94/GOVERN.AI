from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from datetime import datetime
import re
import io

from database import db
from routes.auth import require_role
from rate_limiter import limiter
from exporters import generate_audit_csv, generate_audit_pdf

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("")
@limiter.limit("60/minute")
async def list_audit_logs(request: Request, outcome: Optional[str] = None, risk_level: Optional[str] = None, action: Optional[str] = None, search: Optional[str] = None, limit: int = Query(default=50, le=200), skip: int = 0, user: dict = Depends(require_role("viewer"))):
    query = {}
    if outcome: query["outcome"] = outcome
    if risk_level: query["risk_level"] = risk_level
    if action: query["action"] = action
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"agent_name": {"$regex": safe_search, "$options": "i"}},
            {"details": {"$regex": safe_search, "$options": "i"}},
            {"user": {"$regex": safe_search, "$options": "i"}},
            {"resource": {"$regex": safe_search, "$options": "i"}},
        ]
    total = await db.audit_logs.count_documents(query)
    logs = await db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
    return {"total": total, "logs": logs}


@router.get("/export/csv")
@limiter.limit("10/minute")
async def export_audit_csv(
    request: Request,
    outcome: Optional[str] = None,
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=1000, le=1000),
    user: dict = Depends(require_role("auditor"))
):
    """Export audit logs as CSV file"""
    query = {}
    if outcome: query["outcome"] = outcome
    if risk_level: query["risk_level"] = risk_level
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"agent_name": {"$regex": safe_search, "$options": "i"}},
            {"details": {"$regex": safe_search, "$options": "i"}},
            {"user": {"$regex": safe_search, "$options": "i"}},
            {"resource": {"$regex": safe_search, "$options": "i"}},
        ]
    
    logs = await db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
    csv_bytes = generate_audit_csv(logs)
    
    filename = f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/pdf")
@limiter.limit("5/minute")
async def export_audit_pdf(
    request: Request,
    outcome: Optional[str] = None,
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=500, le=500),
    user: dict = Depends(require_role("auditor"))
):
    """Export audit logs as PDF report"""
    query = {}
    filters = {}
    
    if outcome:
        query["outcome"] = outcome
        filters["outcome"] = outcome
    if risk_level:
        query["risk_level"] = risk_level
        filters["risk_level"] = risk_level
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"agent_name": {"$regex": safe_search, "$options": "i"}},
            {"details": {"$regex": safe_search, "$options": "i"}},
            {"user": {"$regex": safe_search, "$options": "i"}},
            {"resource": {"$regex": safe_search, "$options": "i"}},
        ]
        filters["search"] = search
    
    logs = await db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
    pdf_bytes = generate_audit_pdf(logs, filters)
    
    filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
