from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from datetime import datetime, timezone

from database import db
from models import Policy, PolicyCreate, AuditLog, AuditOutcome
from routes.auth import require_role
from rate_limiter import limiter

router = APIRouter(prefix="/api/policies", tags=["policies"])


@router.get("", response_model=List[Policy])
async def list_policies(regulation: Optional[str] = None, severity: Optional[str] = None, user: dict = Depends(require_role("viewer"))):
    query = {}
    if regulation: query["regulation"] = regulation
    if severity: query["severity"] = severity
    return await db.policies.find(query, {"_id": 0}).to_list(100)


@router.post("", response_model=Policy)
@limiter.limit("30/minute")
async def create_policy(request: Request, data: PolicyCreate, user: dict = Depends(require_role("dpo"))):
    policy = Policy(**data.model_dump())
    await db.policies.insert_one(policy.model_dump())
    log = AuditLog(policy_name=policy.name, action="policy_created", resource=f"/policies/{policy.id}", outcome=AuditOutcome.allowed, details=f"Policy '{policy.name}' created", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return await db.policies.find_one({"id": policy.id}, {"_id": 0})


@router.put("/{policy_id}", response_model=Policy)
async def update_policy(policy_id: str, data: PolicyCreate, user: dict = Depends(require_role("dpo"))):
    existing = await db.policies.find_one({"id": policy_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Policy not found")
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.policies.update_one({"id": policy_id}, {"$set": update_data})
    log = AuditLog(policy_name=data.name, action="policy_updated", resource=f"/policies/{policy_id}", outcome=AuditOutcome.allowed, details=f"Policy '{data.name}' updated", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return await db.policies.find_one({"id": policy_id}, {"_id": 0})


@router.delete("/{policy_id}")
@limiter.limit("10/minute")
async def delete_policy(request: Request, policy_id: str, user: dict = Depends(require_role("admin"))):
    existing = await db.policies.find_one({"id": policy_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Policy not found")
    await db.policies.delete_one({"id": policy_id})
    log = AuditLog(policy_name=existing.get("name", ""), action="policy_deleted", resource=f"/policies/{policy_id}", outcome=AuditOutcome.allowed, details=f"Policy '{existing.get('name', '')}' deleted", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return {"status": "deleted", "id": policy_id}
