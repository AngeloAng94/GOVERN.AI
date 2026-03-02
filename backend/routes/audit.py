from fastapi import APIRouter, HTTPException, Depends, Request, Query
from typing import Optional
import re

from database import db
from routes.auth import require_role
from rate_limiter import limiter

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
